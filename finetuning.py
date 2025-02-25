# -*- coding: utf-8 -*-
"""finetuning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MRg5BDrSf3rk1Vsxm6RJA9qak8Xxgqk7
"""

!pip install -q torch peft bitsandbytes transformers trl accelerate einops tqdm scipy



import os
from dataclasses import dataclass, field
from typing import Optional

import torch
from datasets import load_dataset, load_from_disk
from peft import LoraConfig, prepare_model_for_kbit_training
from transformers import (
AutoModelForCausalLM,
AutoTokenizer,
BitsAndBytesConfig,
HfArgumentParser,

TrainingArguments,
)

from tqdm.notebook import tqdm

from trl import SFTTrainer

from huggingface_hub import interpreter_login

interpreter_login()

dataset= load_dataset("Amod/mental_health_counseling_conversations", split="train")

dataset

import pandas as pd
df = pd.DataFrame(dataset)

df.head(5)

df.info()

def format_row(row):
  question = row['Context']
  answer = row['Response']
  formatted_string = f"[INST] {question} [/INST] {answer} "
  return formatted_string

df['Formatted']= df.apply(format_row, axis=1)

df['Formatted']

new_df = df.rename(columns={'Formatted':'text'})

new_df

new_df = new_df['text']

new_df.head(3)

new_df.to_csv("formatted_dataset.csv",index=False)



training_dataset = load_dataset("csv",data_files="formatted_dataset.csv",split="train")

training_dataset

"""### Fine Tuning Code"""

base_model = "microsoft/phi-2"
new_model = "phi2_mental_health"

tokenizer = AutoTokenizer.from_pretrained(base_model,use_fast=True)

tokenizer.pad_token = tokenizer.eos_token

from transformers import AutoModelForCausalLM, TrainingArguments, BitsAndBytesConfig
from peft import LoraConfig, prepare_model_for_kbit_training
import torch

# Fix padding side
tokenizer.padding_side = "right"

# Configure 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=False,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# Load model with quantization
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=bnb_config,
    device_map="auto",  # Auto-distribute across available GPUs
    trust_remote_code=True,
)

# Model configuration
model.config.use_cache = False
model.config.pretraining_tp = 1

# Prepare for LoRA training with gradient checkpointing
model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)

# Training arguments
training_arguments = TrainingArguments(
    output_dir="mdGPT",
    num_train_epochs=1,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=32,
    eval_steps=100,
    save_steps=1500,
    logging_steps=15,
    optim="paged_adamw_8bit",
    lr_scheduler_type="cosine",  # Fixed typo
    learning_rate=2e-4,
    weight_decay=0.01,
    warmup_ratio=0.05,
)

# LoRA configuration
peft_config = LoraConfig(
    lora_alpha=64,
    lora_dropout=0.05,
    r=32,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["Wqkv", "fc1", "fc2"]
)

training_dataset

tokenized_dataset

print(tokenized_dataset)

print(training_dataset['text'])

trainer = SFTTrainer(
    model=model,
    train_dataset=training_dataset,
    peft_config=peft_config,
    tokenizer=tokenizer,
    args=training_arguments

)

training_dataset

# Set padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  # Use EOS as padding if available
    if tokenizer.pad_token is None:  # If eos_token is also None, add a new PAD token
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# Resize model embedding size
model.resize_token_embeddings(len(tokenizer))

# Now train
trainer.train()



