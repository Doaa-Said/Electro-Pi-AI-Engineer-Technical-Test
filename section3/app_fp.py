import time
import psutil
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

process = psutil.Process()

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL,
    cache_dir="models/fp",
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    cache_dir="models/fp",
)

model.eval()

ram = process.memory_info().rss / 1024**2

print(f"RAM after loading model: {ram:.2f} MB")

while True:

    prompt = input("\nPrompt: ")

    if prompt.lower() == "exit":
        break

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        text,
        return_tensors="pt",
    )

    start = time.perf_counter()

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
        )

    elapsed = time.perf_counter() - start

    answer_ids = outputs[0][inputs["input_ids"].shape[1]:]

    answer = tokenizer.decode(
        answer_ids,
        skip_special_tokens=True,
    )

    num_tokens = len(answer_ids)

    tokens_per_second = (
        num_tokens / elapsed
        if elapsed > 0
        else 0
    )

    ram = process.memory_info().rss / 1024**2

    print("\nAnswer:\n")
    print(answer)

    print("\n------ Statistics ------")
    print(f"RAM Usage      : {ram:.2f} MB")
    print(f"Output Tokens  : {num_tokens}")
    print(f"Time           : {elapsed:.2f} sec")
    print(f"Tokens / sec   : {tokens_per_second:.2f}")