# test_setup.py
import torch
import transformers
from peft import PeftModel
import gradio as gr

def test_setup():
    # Check CUDA availability
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    
    # Check transformers version
    print(f"Transformers version: {transformers.__version__}")
    
    # Test basic model loading (small model for test)
    try:
        model_name = "microsoft/phi-2"
        tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
        print("✓ Tokenizer loading successful")
    except Exception as e:
        print(f"× Tokenizer loading failed: {str(e)}")

if __name__ == "__main__":
    test_setup()