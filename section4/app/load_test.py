import concurrent.futures
import requests
import time

URL = "http://localhost:8000/generate"

payload = {
    "prompt": "Tell me a joke."
}

def send_request(i):
    start = time.perf_counter()

    response = requests.post(URL, json=payload)

    end = time.perf_counter()

    return {
        "id": i,
        "status": response.status_code,
        "latency": end - start,
    }

overall_start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(send_request, i) for i in range(10)]
    results = [f.result() for f in futures]

overall_end = time.perf_counter()

print("\nResults")
print("-" * 40)

for r in results:
    print(
        f"Request {r['id']:2d}: "
        f"{r['status']}   "
        f"{r['latency']:.2f} sec"
    )

latencies = [r["latency"] for r in results]

print("\nSummary")
print("-" * 40)
print(f"Average latency : {sum(latencies)/len(latencies):.2f} sec")
print(f"Minimum latency : {min(latencies):.2f} sec")
print(f"Maximum latency : {max(latencies):.2f} sec")
print(f"Total wall time : {overall_end-overall_start:.2f} sec")