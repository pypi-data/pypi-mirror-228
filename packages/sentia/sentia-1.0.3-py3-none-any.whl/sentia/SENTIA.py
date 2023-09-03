import torch
import torch.nn as nn
import math
import sacrebleu
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import DataLoader, Dataset
import torch.nn.functional as F
from transformers import AutoTokenizer, GPT2Model
from torch.cuda.amp import autocast
from datasets import load_dataset
from torch.optim.adamw import AdamW
from tqdm import tqdm
from positional_encodings.torch_encodings import PositionalEncoding1D
import os
import wandb
from sentia.utils import SENTIAFF, SENTIAMHA
from rotary_embedding_torch import RotaryEmbedding
from sklearn.metrics import f1_score
data = load_dataset("Skylion007/openwebtext", split="train[650000:700000]", cache_dir="E:/Datasets")
val_data = load_dataset("lighteval/mmlu", "all", split="validation")
def init_weights(module):
    if isinstance(module, nn.Linear):
        nn.init.xavier_uniform_(module.weight.data)
        if module.bias is not None:
            module.bias.data.zero_()
class MEPA(nn.Module):
    """
    Mutation Enhanced Plasticity Architecture (MEPA) Module with multiple layers.

    This module implements a fully connected layer, also known as a Multi-Layer Perceptron (MLP),
    with an affine transformation. It takes an input tensor and applies a linear transformation
    followed by bias addition. The weights and biases of the module are learned during training.

    Args:
        hidden_dim (int): The size of the input and output features.
        layers (int): The number of layers in the network.
        activation (callable, optional): The activation function to be applied after forwarding
            through all layers. Default is F.sigmoid

    Shape:
        - Input: `(batch_size, hidden_dim)` or `(batch_size, *, hidden_dim)` where `*` represents
          any number of additional dimensions.
        - Output: `(batch_size, hidden_dim)` or `(batch_size, *, hidden_dim)` depending on the
          input shape.

    Example:
        >>> hidden_dim = 10
        >>> batch_size = 32
        >>> input_tensor = torch.randn(batch_size, hidden_dim)
        >>> layers = 3
        >>> mepa = MEPA(hidden_dim, layers)
        >>> output_tensor = mepa(input_tensor)
        >>> print(output_tensor.shape)
        torch.Size([32, 10])
    """

    class MEPALayer(nn.Module):
        """
        A single layer of the Mutation Enhanced Plasticity Architecture (MEPA) module.

        Args:
            hidden_dim (int): The size of the input and output features for this layer.

        Shape:
            - Input: `(batch_size, hidden_dim)`
            - Output: `(batch_size, hidden_dim)`
        """
        def __init__(self, hidden_dim):
            super(MEPA.MEPALayer, self).__init__()
            self.weight = nn.Linear(hidden_dim, hidden_dim)
            self.bias = nn.Parameter(torch.Tensor(hidden_dim))
            self.scaling_matrix = nn.Parameter(torch.Tensor(hidden_dim, hidden_dim))
            self.layer_norm = nn.LayerNorm(hidden_dim)
            self.ffn = SENTIAFF(hidden_dim, hidden_dim, 0, True)
            self.reset_parameters()

        def reset_parameters(self):
            """
            Initialize the layer's parameters.

            This function initializes the weight, bias, and scaling matrix parameters of the layer
            using Kaiming normal initialization for the weight, and uniform initialization for
            bias and scaling matrix.

            Note:
                Kaiming normal initialization is used for weight initialization, which is suitable
                for activations like sigmoid and tanh.

            Shape:
                - weight: `(hidden_dim, hidden_dim)`
                - bias: `(hidden_dim)`
                - scaling_matrix: `(hidden_dim, hidden_dim)`
            """
            nn.init.kaiming_normal_(self.weight.weight, mode='fan_out', nonlinearity='sigmoid')
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight.weight)
            bound = 1 / math.sqrt(fan_in)
            nn.init.uniform_(self.bias, -bound, bound)
            nn.init.uniform_(self.scaling_matrix, 0, 1)

        def forward(self, x):
            """
            Forward pass of the MEPALayer.

            Args:
                x (torch.Tensor): The input tensor of shape `(batch_size, hidden_dim)`.

            Returns:
                torch.Tensor: The output tensor of shape `(batch_size, hidden_dim)`.
            """
            # Calculate the linear transformation
            linear_output = self.weight(x)
            # Apply the affine transformation (scaling) to the linear output
            scaled_output = self.layer_norm(torch.matmul(linear_output, self.scaling_matrix.t()))
            scaled_output = self.ffn(scaled_output + self.bias)
            # Add biases to the scaled output
            return scaled_output

    def __init__(self, hidden_dim, layers, activation=None):
        """
        Initialize the Mutation Enhanced Plasticity Architecture (MEPA) module.

        Args:
            hidden_dim (int): The size of the input and output features for each layer.
            layers (int): The number of layers in the network.
            activation (callable, optional): The activation function to be applied after forwarding
                through all layers. Default is F.relu.
        """
        super(MEPA, self).__init__()
        self.activation = None
        self.hidden_dim = hidden_dim
        self.layers = layers
        if activation is not None:
            self.activation = activation()
        self.layer_modules = nn.ModuleList([self.MEPALayer(hidden_dim) for _ in range(layers)])

    def forward(self, x):
        """
        Forward pass of the MEPA module.

        Args:
            x (torch.Tensor): The input tensor of shape `(batch_size, hidden_dim)` or
                `(batch_size, *, hidden_dim)`.

        Returns:
            torch.Tensor: The output tensor of shape `(batch_size, hidden_dim)` or
                `(batch_size, *, hidden_dim)` depending on the input shape.
        """
        if x.dim() > 2:
            x = x.reshape(x.size(0), x.size(1), -1)

        for layer_module in self.layer_modules:
            # Apply the current layer's transformation
            x = layer_module(x)

        # Apply the activation function after forwarding through all layers
        if self.activation is not None:
            x = self.activation(x)

        return x
class SENTIARotaryEmbedding(nn.Module):
    def __init__(self, dim):
        super(SENTIARotaryEmbedding, self).__init__()
        self.emb = RotaryEmbedding(dim)
    def forward(self, x):
        x = self.emb.rotate_queries_or_keys(x)
        return x
class SENTIATransformer(nn.Module):
    """
    Decoder part of the Transformer with multiple SENTIATransformerBlocks.

    Args:
        hidden_dim (int): The size of the input and output features for each layer.
        num_heads (int): The number of attention heads in each SENTIATransformerBlock.
        num_layers (int): The number of Transformer decoder layers.

    Shape:
        - Input: `(batch_size, seq_length, hidden_dim)`
        - Output: `(batch_size, seq_length, hidden_dim)`
    """

    def __init__(self, hidden_dim, num_heads, num_layers):
        super(SENTIATransformer, self).__init__()
        self.blocks = nn.ModuleList([
            SENTIATransformerBlock(hidden_dim, num_heads)
            for _ in range(num_layers)
        ])

    def forward(self, x, mask):
        """
        Forward pass of the SENTIATransformer.

        Args:
            x (torch.Tensor): The input tensor of shape `(batch_size, seq_length, hidden_dim)`.
            mask (torch.Tensor): The attention mask of shape `(batch_size, seq_length, seq_length)`.

        Returns:
            torch.Tensor: The output tensor of shape `(batch_size, seq_length, hidden_dim)`.
        """
        for block in self.blocks:
            x = block(x, mask)
        return x
class SENTIAMLP(nn.Module):

    def __init__(self, hidden_dim, activation=nn.GELU):
        super().__init__()
        
        self.dense_1 = nn.Linear(hidden_dim, hidden_dim * 4)
        if activation == nn.Softmax:
            self.activation = activation(dim=1)
        else:
            self.activation = activation()
        self.dense_2 = nn.Linear(hidden_dim * 4, hidden_dim)
        self.a_D = nn.Dropout(0.05)
        self.l_D = nn.Dropout(0.01)
        
    def forward(self, x):
        
        x = self.dense_1(x)
        x = self.activation(x)
        x = self.a_D(x)
        x = self.dense_2(x)
        x = self.l_D(x)
        
        return x
class SENTIATransformerBlock(nn.Module):
    """
    Single Transformer Block with masked multi-head self-attention and feed-forward layers.

    Args:
        hidden_dim (int): The size of the input and output features for each layer.
        num_heads (int): The number of attention heads in the Transformer block.

    Shape:
        - Input: `(batch_size, seq_length, hidden_dim)`
        - Output: `(batch_size, seq_length, hidden_dim)`
    """

    def __init__(self, hidden_dim, num_heads):
        super(SENTIATransformerBlock, self).__init__()
        self.masked_multihead_attention = SENTIAMHA(num_heads, hidden_dim, hidden_dim // 8, 0.1)
        self.feed_forward = SENTIAFF(hidden_dim, hidden_dim, 0)
        self.norm1 = nn.LayerNorm(hidden_dim)
        self.norm2 = nn.LayerNorm(hidden_dim)
        
    def forward(self, x, mask=None):
        """
        Forward pass of the SENTIATransformerBlock.

        Args:
            x (torch.Tensor): The input tensor of shape `(batch_size, seq_length, hidden_dim)`.
            mask (torch.Tensor): The attention mask of shape `(batch_size, seq_length, seq_length)`.

        Returns:
            torch.Tensor: The output tensor of shape `(batch_size, seq_length, hidden_dim)`.
        """
        if mask is None:
            mask = SENTIA.generate_causal_mask(x)
        attention_output = self.masked_multihead_attention(x)
        attention_output = self.norm1(attention_output)
        attention_output = attention_output
        # Apply feed-forward layer
        feed_forward_output = self.feed_forward(attention_output)
        norm2 = self.norm2(feed_forward_output + x)
        return norm2

class SENTIA(nn.Module):
    """
    SENTIA (Self-Enhanced Neural Transformer with Integration and Attention) Model Class.

    This model incorporates Transformer layers, Head layers, MHAs, and MEPA layers for text generation tasks.

    Args:
        vocab_size (int): The size of the vocabulary.
        embedding_dim (int): The dimensionality of the embedding space.
        num_heads (int): The number of attention heads in the Transformer.
        num_layers (int): The number of Transformer decoder layers.
        hidden_dim (int): The dimensionality of the hidden layers.

    Attributes:
        embedding (nn.Embedding): Embedding layer for the input sequence.
        lstm (nn.LSTM): LSTM layer for sequential processing.
        mepa (MEPA): MEPA (Mutation Enhanced Plasticity Architecture) layer for dynamic neural connections.
        transformer_layers (nn.ModuleList): List of Transformer decoder layers.
        mha (nn.MultiheadAttention): Multi-Head Attention (MHA) layer.
        head_layers (nn.Sequential): Fully connected head layers for text generation.
    """

    def __init__(self, vocab_size, embedding_dim, num_heads, num_layers, hidden_dim):
        super(SENTIA, self).__init__()
        self.embedding_dim = embedding_dim
        self.vocab_size = vocab_size
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.hidden_dim = hidden_dim
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.posenc = SENTIARotaryEmbedding(embedding_dim)
        self.mepa = MEPA(hidden_dim, num_layers // 4)
        self.transformer_decoder = SENTIATransformer(hidden_dim, num_heads, num_layers)
        self.head_layers = nn.Linear(hidden_dim, vocab_size)
        self.init_weights()
    def init_weights(self):
            # Initialize all the model parameters
            for module in self.modules():
                init_weights(module)
    @DeprecationWarning
    def positional_encoding(self, x):
        # Create positional encodings with sine and cosine functions
        pos_encoding = torch.arange(0, x.size(1), device=x.device).unsqueeze(0)
        div_term = torch.exp(torch.arange(0, self.embedding_dim, 2, device=x.device) * -(math.log(10000.0) / self.embedding_dim))
        pe = torch.zeros(x.size(1), self.embedding_dim, device=x.device)
        pe[:, 0::2] = torch.sin(pos_encoding * div_term)
        pe[:, 1::2] = torch.cos(pos_encoding * div_term)
        pe = pe.unsqueeze(0)  # Add batch dimension
        return pe

    def forward(self, x, labels=None, attention_mask=None):
        loss = float('nan')
        embedded = self.embedding(x)
        pos_encoding = self.posenc(embedded)
        mepa_output = self.mepa(pos_encoding)
        transformer_output = self.transformer_decoder(pos_encoding, attention_mask)
        logits = self.head_layers(transformer_output + mepa_output)
        probabilities = F.softmax(logits, dim=1)
        
        if labels is not None:
            loss = nn.CrossEntropyLoss().forward(logits.view(-1, logits.size(-1)), labels.view(-1))
        return probabilities, loss
    @staticmethod
    def generate_causal_mask(x):
        """
        Generate a causal mask for autoregressive self-attention.

        Args:
            x (torch.Tensor): The input tensor of shape `(seq_length, hidden_dim)`.

        Returns:
            torch.Tensor: The causal mask of shape `(seq_length, seq_length)`.
        """
        seq_length = x.size(1)
        batch_size = x.size(0)
        mask = torch.triu(torch.ones(batch_size, seq_length), diagonal=1).cuda()
        return mask.bool()
    def backward(self, loss, threshold=1e-6):
        """
        Backward pass of the SENTIA model with optional gradient pruning.

        Args:
            loss (torch.Tensor): Loss tensor.
            threshold (float, optional): Threshold value for gradient pruning. Defaults to 1e-6.
        """
        for p in self.parameters():
            if p.grad is not None and torch.max(torch.abs(p.grad)) < threshold:
                p.grad = None
        loss.backward()
    def save(self, directory):
        """
        Save the SENTIA model to a given directory.

        Args:
            model (nn.Module): The SENTIA model instance to save.
            directory (str): The directory path to save the model.

        Returns:
            None
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the model's state dictionary
        model_path = os.path.join(directory, 'sentia_model.bin')
        torch.save(model.state_dict(), model_path)

        print(f"Model saved at {model_path}")
    def load(self, directory):
        """
        Load the SENTIA model from a given directory.

        Args:
            model_class (nn.Module): The class of the SENTIA model to instantiate.
            directory (str): The directory path where the model is saved.

        Returns:
            model (nn.Module): The loaded SENTIA model.
        """
        # Instantiate the model
        model = self

        # Load the saved model's state dictionary
        model_path = os.path.join(directory, 'sentia_model.bin')
        model.load_state_dict(torch.load(model_path))

        print(f"Model loaded from {model_path}")

        return model
    def generate(
        self,
        input_ids,
        temperature=0.44,
        top_k=4,
        top_p=0.91,
        max_length=10,
        device="cuda" if torch.cuda.is_available() else "cpu"
    ):
        model = self
        model.eval()
        input_ids = input_ids.to(device)
        
        generated_text = input_ids.clone()  # Initialize with the provided input_ids

        for step in range(max_length):
            logits, _ = model(generated_text)  # Generate logits for the current input
            
            # Keep only the last token predictions of the first batch item (batch size 1), apply a temperature coefficient and filter
            logits = logits[0, -1, :] / temperature
            filtered_logits = self.top_k_top_p_filtering(logits, top_k=top_k, top_p=top_p)
            
            # Sample from the filtered distribution
            probabilities = F.softmax(filtered_logits, dim=-1)
            next_token = torch.multinomial(probabilities, 1)
            
            # Append the next token to the generated text
            generated_text = torch.cat((generated_text, next_token.unsqueeze(0)), dim=1)
            
            # Stop generating if the generated text reaches the desired max_length
            if generated_text.size(1) >= max_length:
                break

        return generated_text

    def _reorder_past(self, past, next_tokens):
        """
        Reorders the past state based on the selected next tokens.

        Args:
            past (tuple): Tuple containing the past states.
            next_tokens (torch.Tensor): Tensor containing the selected next tokens of shape (batch_size * num_beams).

        Returns:
            tuple: Reordered past state.
        """
        next_tokens = next_tokens.unsqueeze(-1).unsqueeze(-1)
        past = tuple([p.index_select(1, next_tokens[i].view(-1)) for i, p in enumerate(past)])
        return past
    @staticmethod
    def calculate_accuracy(predictions, targets):
        """
        Calculate the accuracy.

        Args:
            predictions (Tensor): Model predictions (e.g., logits).
            targets (Tensor): Ground truth labels.

        Returns:
            float: Accuracy.
        """
        predicted_classes = predictions
        correct_predictions = torch.sum(predicted_classes == targets).item()
        total_predictions = targets.size(0)  # Number of samples

        accuracy = correct_predictions / total_predictions
        return accuracy

    @staticmethod
    def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
        """ Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
            Args:
                logits: logits distribution shape (vocabulary size)
                top_k >0: keep only top k tokens with highest probability (top-k filtering).
                top_p >0.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
                    Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
        """
        logits = logits.squeeze(0)
        assert logits.dim() == 1  # batch size 1 for now - could be updated for more but the code would be less clear
        top_k = min(top_k, logits.size(-1))  # Safety check
        if top_k > 0:
            # Remove all tokens with a probability less than the last token of the top-k
            indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
            logits[indices_to_remove] = filter_value

        if top_p > 0.0:
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

            # Remove tokens with cumulative probability above the threshold
            sorted_indices_to_remove = cumulative_probs > top_p
            # Shift the indices to the right to keep also the first token above the threshold
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0

            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            logits[indices_to_remove] = filter_value
        return logits
    def fit(self, num_epochs, dataloader, tokenizer, optimizer, val_dataloader, scheduler, device: torch.device, lr=1e-5):
        """
        Train the SENTIA model.

        Args:
            num_epochs (int): Number of training epochs.
            dataloader (DataLoader): Training data loader.
            model: The SENTIA model instance.
            tokenizer: Tokenizer for decoding predictions.
            optimizer: Optimizer for model parameter updates.
            val_dataloader (DataLoader): Validation data loader.
            scheduler: Learning rate scheduler.
        """
        model = self
        model.to(device, dtype=torch.float32)
        optimizer = optimizer(model.parameters(), lr, fused=True)
        scheduler = scheduler(optimizer, step_size=1, gamma=0.7)
        torch.cuda.empty_cache()
        for epoch in range(num_epochs):
            model.train()
            print(f"Epoch {epoch+1}/{num_epochs}")
            total_loss = 0
            total_reward = 0
            total_bleu = 0
            total_perplexity = 0
            num_batches = 0
            accumulation_steps = 12  # Accumulate gradients over 12 batches
            predictions_list: list = []
            bleu_scores: list = []
            for i, batch in tqdm(enumerate(dataloader)):
                input_ids = batch["input_ids"].to(device)
                target_ids = batch["labels"].to(device)
                target_text = batch["target_text"]
                # Generate the output and calculate the loss
                with autocast():
                    outputs = model(input_ids, labels=target_ids)
                    logits, loss = outputs[:2]
                # Calculate the BLEU score
                predictions = torch.argmax(logits, dim=-1)
                predictions_str = [tokenizer.decode(pred, skip_special_tokens=True) for pred in predictions.tolist()]
                target_ids_str = [tokenizer.decode(tgt, skip_special_tokens=True) for tgt in target_ids.tolist()]
                print(predictions_str[0])
                bleu_scores = []
                accuracy_scores = []
                for pred_str, target_str in zip(predictions_str, target_ids_str):
                    bleu = sacrebleu.sentence_bleu(pred_str, [target_str])
                    bleu_scores.append(bleu.score)
                for pred_id, target_id in zip(predictions, target_ids):
                    accuracy = self.calculate_accuracy(pred_id, target_id)
                    accuracy_scores.append(accuracy)
                accuracy = sum(accuracy_scores) / len(accuracy_scores)
                bleu = sum(bleu_scores) / len(bleu_scores)
                # Calculate the reward
                #reward, penalty = self.get_reward(predictions.tolist()[0], target_ids.tolist()[0])

                # Backpropagate the loss and update the parameters with the reward
                #if penalty > 0 and penalty < reward:
                    #loss = (loss * (penalty * 5))
                #if reward > penalty:
                    #loss = (loss / (reward * 5))
                #loss = loss.mean()
                loss.backward()
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                # Update the metrics
                total_loss += loss.item()
                #total_reward += reward
                total_bleu += bleu
                total_perplexity += torch.exp(loss).item()
                num_batches += 1
                wandb.log({"loss": loss.item(), "bleu": bleu, "perplexity": torch.exp(loss).item(), "accuracy": accuracy})
                print(f"Epoch {epoch+1}/{num_epochs}, Batch {i+1}/{len(dataloader)}: Loss - {loss.item():.4f}, Reward - {0:.4f}, Penalty - {0:.4f}, BLEU - {bleu:.4f}, Perplexity - {torch.exp(loss).item()}, Accuracy - {accuracy} (reinforcement learning disabled for pretraining)")
                torch.cuda.empty_cache()
            # Display the metrics for the epoch
            model.save('D:\\Projects\\chatTulu\\')
            tokenizer.save_pretrained('D:\\Projects\\chatTulu\\')
            val_loss, val_reward, val_penalty, val_bleu, val_perplexity, val_accuracy = self.evaluate(model, val_dataloader, tokenizer, device)
            wandb.log({"val_loss": val_loss.item(), "val_bleu": val_bleu, "val_perplexity": val_perplexity, "val_accuracy": val_accuracy,})
            print(f"Validation metrics: Loss={val_loss:.4f}, Reward={val_reward:.4f}, Penalty={val_penalty}, BLEU={val_bleu:.4f}, Perplexity={val_perplexity:.4f}")
    @staticmethod
    def get_reward(predictions, target_ids):
        """
        Calculate the reward and penalty for the generated predictions.

        Args:
            predictions (list): List of predicted output tokens.
            target_ids (list): List of target output tokens.

        Returns:
            reward (int): Reward score.
            penalty (int): Penalty score.
        """
        reward = 0
        penalty = 0
        for i in range(len(predictions)):
            # Penalize for repeating words consecutively
            if i > 0 and predictions[i] == predictions[i-1]:
                penalty += 1
            # Reward for using words correctly
            if predictions[i] in target_ids:
                reward += 1
        return reward, penalty
    @staticmethod
    def evaluate(model, dataloader, tokenizer, device: torch.device):
        """
        Evaluate the model on the validation set and calculate metrics.

        Args:
            model (nn.Module): Model to evaluate.
            dataloader (DataLoader): Validation data loader.
            tokenizer: Tokenizer for decoding predictions.

        Returns:
            avg_loss (float): Average loss.
            avg_reward (float): Average reward.
            avg_penalty (float): Average penalty.
            avg_bleu (float): Average BLEU score.
            avg_perplexity (float): Average perplexity.
        """
        model.eval()
        total_loss = 0
        total_reward = 0
        total_bleu = 0
        total_perplexity = 0
        num_batches = 0
        total_penalty = 0
        total_accuracy = 0

        with torch.no_grad():
            for batch in dataloader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                target_ids = batch["labels"].to(device)
                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)
                target_ids = target_ids.to(device)
                target_text = batch["target_text"]
                # Generate the output and calculate the loss
                with autocast():
                    outputs = model(input_ids, labels=target_ids)
                    logits, loss = outputs[:2]
                # Calculate the BLEU score
                predictions = torch.argmax(logits, dim=-1)
                predictions_str = [tokenizer.decode(pred, skip_special_tokens=True) for pred in predictions.tolist()]
                target_str = [tokenizer.decode(tgt, skip_special_tokens=True) for tgt in target_ids.tolist()]
                reward, penalty = SENTIA.get_reward(predictions_str[0], target_str[0])
                bleu = sacrebleu.corpus_bleu(predictions_str, [target_str])
                accuracy_scores = []
                for pred_id, target_id in zip(predictions, target_ids):
                    accuracy = SENTIA.calculate_accuracy(pred_id, target_id)
                    accuracy_scores.append(accuracy)
                accuracy = sum(accuracy_scores) / len(accuracy_scores)
                # Update the metrics
                total_loss += loss
                total_reward += reward
                total_penalty += penalty
                total_bleu += bleu.score
                total_accuracy += accuracy
                total_perplexity += torch.exp(torch.tensor(loss)).item()
                num_batches += 1

        # Calculate the average metrics
        avg_loss = total_loss / num_batches
        avg_reward = total_reward / num_batches
        avg_bleu = total_bleu / num_batches
        avg_perplexity = total_perplexity / num_batches
        avg_penalty = total_penalty / num_batches
        avg_accuracy = total_accuracy / num_batches
        return avg_loss, avg_reward, avg_penalty, avg_bleu, avg_perplexity, avg_accuracy

    def summary(self):
        """
        Print a summary of the model architecture and the number of parameters.
        """
        model = self
        num_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

        print("Model Summary:")
        print(f"{'='*40}")
        print(model)
        print(f"{'='*40}")
        print(f"Total params: {num_params}")
        print(f"Trainable params: {trainable_params}")
class SENTIADataset(Dataset):
    def __init__(self, tokenizer, data, batch_size, max_length=1024):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.batch_size = batch_size

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if len(self.data[idx]["text"]) > self.max_length:
            self.data[idx]["text"] = self.data[idx]["text"][:self.max_length]
        text = self.data[idx]["text"].strip("\n")
        index = len(text) // 2
        input_text = text[:index]
        target_text = text[index:]
        input_ids = self.tokenizer.encode(input_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        target_ids = self.tokenizer.encode(target_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        input_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(input_ids))
        target_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(target_ids))
        attention_mask = [True] * len(input_ids)
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.int64),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.int64),
            "labels": torch.tensor(target_ids, dtype=torch.int64),
            "target_text": target_text
        }
class ConversationDataset(Dataset):
    def __init__(self, tokenizer, type, max_length=256, data=data):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.type = type
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        try:
            user = self.data[idx]["Input"].strip('\n')
            assistant = self.data[idx]["Output"].strip('\n')
        except KeyError:
            user = self.data[idx]["question"].strip("\n")
            ans_index = self.data[idx]["answer"]
            assistant = self.data[idx]["choices"][ans_index].strip('\n')
        input_text = f"<|USER|> {user} <|ASSISTANT|> "
        target_text = f"<|USER|> {user} <|ASSISTANT|> {assistant}"
        input_ids = self.tokenizer.encode(input_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        target_ids = self.tokenizer.encode(target_text, add_special_tokens=True, max_length=self.max_length, truncation=True)
        input_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(input_ids))
        target_ids += [self.tokenizer.pad_token_id] * (self.max_length - len(target_ids))
        attention_mask = [1] * len(input_ids)
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.int64),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.int64),
            "labels": torch.tensor(target_ids, dtype=torch.int64),
            "target_text": target_text
        }

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("Locutusque/gpt2-large-conversational")
    embedding_dim = 1024 # Set the embedding dimension
    num_heads = 16 # Set the number of attention heads
    num_layers = 12 # Set the number of transformer and MEPA layers
    hidden_dim = 1024
    batch_size = 6
    model = SENTIA(len(tokenizer), embedding_dim, num_heads, num_layers, hidden_dim)
    model.load('D:\\Projects\\chatTulu\\')
    model.summary()
    val_dataset = ConversationDataset(tokenizer=tokenizer, data=val_data, type="val")
    val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True, pin_memory=True)
    dataset1 = SENTIADataset(data=data, tokenizer=tokenizer, batch_size=batch_size)
    dataloader = DataLoader(dataset1, batch_size=batch_size, shuffle=True, pin_memory=True)
    optimizer = AdamW
    scheduler = StepLR
    wandb.init("SENTIA-session-2", 'D:\\Projects\\chatTulu\\', project="SENTIA")
    try:
        model.fit(5, dataloader, tokenizer, optimizer, val_dataloader, scheduler, torch.device("cuda"))
    except KeyboardInterrupt:
        print("Cleaning up and saving model...")
        print("DO NOT KILL THE TERMINAL IT WILL CORRUPT THE MODEL FILES")
        model.save("D:\\Projects\\chatTulu\\")
        print("Finished saving the model!")
        quit(1)