import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def test_generation():
    
    model_path = "./checkpoints/checkpoint-65"
    
    print(f"📦 Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained(model_path)

    # Move to GPU if available
    device = 0 if torch.cuda.is_available() else -1
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

    # Test prompt from the WikiText domain
    prompt = "The phenomenon of distributed computing allows"
    
    print("🔮 Generating...")
    output = generator(prompt, max_length=50, num_return_sequences=1, truncation=True)
    
    print("\n--- GENERATED TEXT ---")
    print(output[0]['generated_text'])
    print("----------------------")

if __name__ == "__main__":
    test_generation()