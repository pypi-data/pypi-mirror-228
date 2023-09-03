from torch.optim import AdamW
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader
from transformers import SENTIAConfig, SENTIALMHeadModel, SENTIATokenizerFast
from sentia import SENTIADataset, SENTIATokenizerFast, ConversationDataset
import sentia
import wandb
from datasets import load_dataset
import torch


if __name__ == "__main__":
    data = load_dataset("Skylion007/openwebtext", split="train[:500000]", cache_dir="E:/Datasets")
    val_data = load_dataset("lighteval/mmlu", "all", split="validation")
    tokenizer = SENTIATokenizerFast.from_pretrained("Locutusque/gpt2-large-conversational")
    embedding_dim = 512 # Set the embedding dimension
    num_heads = 16 # Set the number of attention heads
    num_layers = 12 # Set the number of transformer and MEPA layers
    hidden_dim = 512
    batch_size = 16
    config = SENTIAConfig(len(tokenizer), hidden_dim, n_embed=embedding_dim, n_layer=num_layers, n_head=num_heads)
    model = SENTIALMHeadModel._from_config(config)
    #model.load('D:\\Projects\\chatTulu\\')
    model.summary()
    val_dataset = ConversationDataset(tokenizer=tokenizer, data=val_data, type="val")
    val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True, pin_memory=True)
    dataset1 = SENTIADataset(tokenizer=tokenizer, data=data, batch_size=batch_size)
    dataloader = DataLoader(dataset1, batch_size=batch_size, shuffle=True, pin_memory=True)
    optimizer = AdamW
    scheduler = LambdaLR
    wandb.init("SENTIA-session-2", 'D:\\Projects\\chatTulu\\', project="SENTIA")
    try:
        SENTIALMHeadModel.fit(model, 5, dataloader, tokenizer, optimizer, val_dataloader, scheduler, torch.device("cuda"))
    except KeyboardInterrupt:
        print("Cleaning up and saving model...")
        print("DO NOT KILL THE TERMINAL IT WILL CORRUPT THE MODEL FILES")
        model.save_pretrained('D:\\Projects\\sentia\\')
        print("Finished saving the model!")
        quit(1)