import os
import datetime
import torch
import torch.distributed as dist
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling 
)
from datasets import load_dataset

# Force NCCL stability on cloud instances
os.environ["NCCL_P2P_DISABLE"] = "1"
os.environ["NCCL_IB_DISABLE"] = "1"

def main():
    if not dist.is_initialized():
        dist.init_process_group(backend="nccl", timeout=datetime.timedelta(minutes=10))

    model_id = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token

    # 1. Load tiny dataset
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train[:1%]")
    
    # 2. Tokenize function with padding and truncation
    def tokenize_function(examples):
        return tokenizer(
            examples["text"], 
            truncation=True, 
            max_length=128, # Keep small for fast test
            padding="max_length"
        )

    # 3. Prepare data (Filter out empty rows to avoid errors)
    dataset = dataset.filter(lambda x: len(x["text"]) > 5)
    tokenized_ds = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)

    # 4. Data Collator 
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir="./checkpoints",
        per_device_train_batch_size=2,
        num_train_epochs=1,
        deepspeed="ds_config_zero3.json", 
        fp16=True,
        logging_steps=1,
        report_to="none"
    )

    # 5. Load Model
    model = AutoModelForCausalLM.from_pretrained(model_id)
    model.config.use_cache = False 

    # 6. Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_ds,
        data_collator=data_collator # ADDED THIS
    )

    print("🚀 Launching Final Verified ZeRO-3 Engine...")
    trainer.train()

if __name__ == "__main__":
    main()