# Results and Write-up

## Environment

- Model: Qwen2.5-0.5B-Instruct (ONNX Runtime)
- Runtime: ONNX Runtime CPU
- API Framework: FastAPI
- Server: Uvicorn
- Hardware: CPU-only

---

# Streaming Test

Prompt:

```text
Tell me a joke
```

The `/stream` endpoint was used to measure the Time To First Token (TTFT) and the total response latency.

| Metric | Result |
|--------|--------|
| Time To First Token (TTFT) | 3.46 sec |
| Total Latency | 54.26 sec |

### Observation

The API started returning generated tokens after approximately 3.46 seconds, allowing the client to display partial output immediately while generation continued. The complete response finished in 54.26 seconds.

Streaming improves the user experience because users begin seeing the response before generation is complete.

---

# Concurrent Load Test

A simple Python script sent 10 concurrent POST requests to the `/generate` endpoint.

## Results

| Request | Status | Latency (sec) |
|---------|--------|---------------|
| 0 | 200 | 580.34 |
| 1 | 200 | 571.23 |
| 2 | 200 | 568.58 |
| 3 | 200 | 584.35 |
| 4 | 200 | 567.83 |
| 5 | 200 | 583.45 |
| 6 | 200 | 578.89 |
| 7 | 200 | 571.60 |
| 8 | 200 | 581.53 |
| 9 | 200 | 593.08 |

## Summary

| Metric | Value |
|--------|-------|
| Concurrent Requests | 10 |
| Successful Requests | 10 / 10 |
| Average Latency | 578.09 sec |
| Minimum Latency | 567.83 sec |
| Maximum Latency | 593.08 sec |
| Total Wall Time | 593.14 sec |

### Discussion

The ONNX Runtime implementation successfully processed all concurrent requests without failures. However, because inference was executed on CPU without batching or request scheduling, latency increased significantly under concurrent load.

The streaming endpoint provided a much better user experience, with a Time To First Token of only 3.46 seconds, even though the complete response required approximately 54 seconds.

---

# Write-up

The current implementation is designed as a simple ONNX Runtime inference server and is suitable for demonstrating model serving. However, it is not optimized for production workloads with many simultaneous users.

If the service needed to support approximately 50 concurrent users, several architectural improvements would be required.

Dynamic batching would combine multiple requests arriving within a short time window into a single inference batch. This improves CPU or GPU utilization and increases throughput while reducing the average inference cost per request.

Autoscaling would deploy multiple API replicas behind a load balancer. As traffic increases, additional containers would automatically start, and when traffic decreases, unused replicas could be removed to reduce infrastructure costs. This can be implemented using Kubernetes Horizontal Pod Autoscaler or Docker Swarm.

A request queue, such as Redis Queue, RabbitMQ, or Kafka, should be placed between the API and the inference workers. Instead of rejecting requests when all workers are busy, new requests would wait until a worker becomes available, improving system stability during traffic spikes.

Response caching using Redis would eliminate repeated inference for identical prompts. Frequently requested responses could be returned immediately, reducing latency and CPU utilization.

GPU inference would significantly improve performance. Deploying the ONNX model with CUDA, TensorRT, or NVIDIA Triton Inference Server would reduce both Time To First Token and total response latency while supporting a much higher number of concurrent users.

A production deployment should also include monitoring. Metrics such as request latency, throughput, CPU utilization, memory usage, queue length, and error rate should be collected using tools like Prometheus and Grafana. These metrics help identify bottlenecks and enable automatic scaling decisions.

Overall, the current ONNX Runtime implementation successfully demonstrates CPU-based model serving and streaming inference. To efficiently support around 50 concurrent users, the system should incorporate batching, autoscaling, request queueing, response caching, monitoring, and GPU-accelerated inference to achieve higher throughput and lower latency.