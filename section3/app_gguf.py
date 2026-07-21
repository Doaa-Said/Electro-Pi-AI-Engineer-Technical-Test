import time
import psutil

from llama_cpp import Llama

process = psutil.Process()

print("Loading GGUF model...")

llm = Llama(
    model_path="models/gguf/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,
)

ram = process.memory_info().rss / 1024**2

print(f"RAM after loading model: {ram:.2f} MB")

while True:

    prompt = input("\nPrompt: ")

    if prompt.lower() == "exit":
        break

    start = time.perf_counter()

    output = llm.create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    elapsed = time.perf_counter() - start

    answer = output["choices"][0]["message"]["content"]

    usage = output.get("usage", {})

    completion_tokens = usage.get("completion_tokens", 0)

    tokens_per_second = (
        completion_tokens / elapsed
        if elapsed > 0
        else 0
    )

    ram = process.memory_info().rss / 1024**2

    print("\nAnswer:\n")
    print(answer)

    print("\n------ Statistics ------")
    print(f"RAM Usage      : {ram:.2f} MB")
    print(f"Output Tokens  : {completion_tokens}")
    print(f"Time           : {elapsed:.2f} sec")
    print(f"Tokens / sec   : {tokens_per_second:.2f}")