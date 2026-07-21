from optimum.onnxruntime import ORTModelForCausalLM
from transformers import AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

print("Downloading model...")

model = ORTModelForCausalLM.from_pretrained(
    MODEL_NAME,
    export=True,
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model.save_pretrained("onnx_model")
tokenizer.save_pretrained("onnx_model")

print("Finished.")