# Fine-Tuned Mental Health Chatbot (Phi-2)

## 🚀 Project Overview
This project focuses on fine-tuning the different models to build an AI-powered **mental health chatbot**. The chatbot is designed to provide supportive and empathetic responses to users seeking guidance. 

By leveraging **LoRA (Low-Rank Adaptation)** and **4-bit quantization**, the model is optimized for efficient training and deployment while maintaining high-quality responses.

---

## 🔥 Features
✅ Fine-tuned different models for mental health conversations  
✅ **LoRA fine-tuning** for efficient adaptation  
✅ **4-bit quantization** for faster inference and low memory usage  
✅ Uses **Gradient Checkpointing** for improved training efficiency  
✅ Built using **Hugging Face Transformers, PEFT, and TRL**  

---

## 📂 Tech Stack
- **Deep Learning Frameworks**: PyTorch, Transformers  
- **Fine-Tuning Methods**: LoRA, BitsAndBytes  
- **Optimization Techniques**: Quantization, Gradient Checkpointing  
- **Dataset**: Mental Health Counseling Conversations  
- **Deployment Possibilities**: API, Chatbot UI, Edge Devices  

---

## 🔧 Setup & Installation
1️⃣ Clone the repository:
```sh
git clone https://github.com/yourusername/fine-tuned-mental-health-chatbot.git
cd fine-tuned-mental-health-chatbot
```
2️⃣ Install dependencies:

```sh
pip install torch peft bitsandbytes transformers trl accelerate einops tqdm scipy pandas datasets
```
3️⃣ Login to Hugging Face:

```sh
from huggingface_hub import interpreter_login
interpreter_login()
```
4️⃣ Train or load the model for inference.
