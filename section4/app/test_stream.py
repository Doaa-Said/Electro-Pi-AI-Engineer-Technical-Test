import requests
import time

start = time.perf_counter()

r = requests.post(
    "http://localhost:8000/stream",
    json={"prompt": "Tell me a joke"},
    stream=True,
)

first_token = None

text = ""

for chunk in r.iter_content(chunk_size=None):

    if chunk:

        if first_token is None:
            first_token = time.perf_counter()

        text += chunk.decode()

end = time.perf_counter()

print("Response:")
print(text)

print()
print(f"TTFT          : {first_token-start:.2f} sec")
print(f"Total latency : {end-start:.2f} sec")