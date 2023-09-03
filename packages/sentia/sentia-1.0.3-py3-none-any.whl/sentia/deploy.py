import torch
from transformers import SENTIATokenizerFast
from transformers import SENTIALMHeadModel
from sentia.config_sentia import SENTIAConfig
from transformers import GenerationConfig, GPT2Model
import os
start_token = "<|ASSISTANT|>"
end_token = "<|"
embedding_dim = 512 # Set the embedding dimension
num_heads = 16 # Set the number of attention heads
num_layers = 12 # Set the number of transformer layers
hidden_dim = 512
tokenizer = SENTIATokenizerFast.from_pretrained("Locutusque/gpt2-large-conversational")
config = SENTIAConfig(len(tokenizer), hidden_dim=hidden_dim, n_embed=embedding_dim, n_layer=12, n_head=num_heads)
model = SENTIALMHeadModel._from_config(config)
model.load(r'D:\Projects\chatTulu')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device, dtype=torch.float16)
def generate_text(model: SENTIALMHeadModel, tokenizer, prompt, max_length=256):
    #prompt = f'<|USER|> {prompt} <|ASSISTANT|> ' this is for conversational
    input_ids = tokenizer.encode(prompt, add_special_tokens=True, max_length=max_length, truncation=True, return_tensors="pt").to(device)
    generation_config = GenerationConfig(temperature=0.33, top_p=0.67, top_k=300, repetition_penalty=1.5, pad_token_id=tokenizer.pad_token_id, eos_token_id=tokenizer.eos_token_id, bos_token_id=tokenizer.eos_token_id, num_beams=5, max_length=max_length)
    output = model.generate_text(input_ids, generation_config=generation_config)
    output_ids = tokenizer.decode(output[0], skip_special_tokens=False)
    return output_ids
# Loop to interact with the model
while True:
    prompt = input("Enter a prompt (or 'q' to quit): ")
    if prompt == "q":
        break
    output_text = generate_text(model, tokenizer, prompt)
    print(output_text)

