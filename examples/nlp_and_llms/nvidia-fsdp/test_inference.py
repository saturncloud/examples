import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def run_inference(checkpoint_path, prompt="The history of WikiText is"):
    print(f"Loading checkpoint: {checkpoint_path}")
    
    # 1. Initialize Model and Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    
    # 2. Load trained weights
    # Use map_location='cpu' if testing on a machine without GPU
    state_dict = torch.load(checkpoint_path, map_location='cpu')
    model.load_state_dict(state_dict)
    
    # 3. Generate Text
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=200, do_sample=True, top_p=0.95)
    
    print("\n--- GENERATED TEXT ---")
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

if __name__ == "__main__":
    # Point this to your latest .bin file in the checkpoints folder
    run_inference("checkpoints/gpt2_step_200.bin")