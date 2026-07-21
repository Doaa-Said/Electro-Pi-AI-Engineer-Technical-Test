from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

print("Downloading tokenizer...")

AutoTokenizer.from_pretrained(
    MODEL,
    cache_dir="models/fp"
)

print("Downloading model...")

AutoModelForCausalLM.from_pretrained(
    MODEL,
    cache_dir="models/fp"
)

print("Done!")