# Results

## Experimental Setup

- Model: Qwen2.5-0.5B-Instruct
- Hardware: CPU-only
- Full Precision Runtime: Hugging Face Transformers (FP)
- Quantized Runtime: llama.cpp (GGUF Q4_K_M)
- Evaluation Prompts: 5 identical prompts
- Metrics: RAM usage, response time, output tokens, throughput (tokens/sec), and qualitative response quality.

---

## Full Precision (Transformers)

| Prompt                            | Response Quality                       | Time (s) | Output Tokens | Throughput (tokens/s) | RAM Usage (MB) |
| :-------------------------------- | :------------------------------------- | -------: | ------------: | --------------------: | -------------: |
| Explain recursion in simple terms | Detailed explanation with examples     |    35.34 |           200 |                  5.66 |        1276.89 |
| Write a Python factorial function | Correct recursive implementation       |    33.40 |           200 |                  5.99 |        1276.62 |
| Summarize machine learning        | Accurate concise summary               |    20.54 |           104 |                  5.06 |        1030.62 |
| Translate to French               | Correct translation                    |     4.07 |             9 |                  2.21 |        1029.38 |
| Professional annual leave email   | Professional and well-structured email |    31.11 |           200 |                  6.43 |        1033.40 |

### Full Precision Summary

| Metric                |            Value |
| :-------------------- | ---------------: |
| Average RAM Usage     |       1129.38 MB |
| Average Response Time |         24.89 s |
| Average Throughput    |    5.72 tokens/s |
| Average Output Tokens |            143 |
| Overall Quality       |    Very Good |

---

## Quantized Model (GGUF - llama.cpp)

| Prompt                            | Response Quality                                             | Time (s) | Output Tokens | Throughput (tokens/s) | RAM Usage (MB) |
| :-------------------------------- | :----------------------------------------------------------- | -------: | ------------: | --------------------: | -------------: |
| Explain recursion in simple terms | Clear explanation, slightly shorter                          |     6.30 |           125 |                 19.85 |         550.08 |
| Write a Python factorial function | Correct implementation with explanation                     |    18.35 |           455 |                 24.80 |         552.41 |
| Summarize machine learning        | Accurate concise summary                                     |     5.88 |           118 |                 20.08 |         554.32 |
| Translate to French               | Correct translation                                          |     0.94 |            19 |                 20.14 |         556.11 |
| Professional annual leave email   | Severe repetition loop (hallucination) – repeated the same sentence endlessly |   229.47 |          4059 |                 17.69 |         561.09 |

### Quantized Summary

| Metric                |                                      Value |
| :-------------------- | -----------------------------------------: |
| Average RAM Usage     |                                554.80 MB |
| Average Response Time |                                 52.19 s |
| Average Throughput    |                        18.30 tokens/s |
| Average Output Tokens |                                    955 |
| Overall Quality       |   Mixed (4 good, 1 severe failure) |

> Overall throughput calculated as total tokens (4776) divided by total time (260.94 s).

---

## Overall Comparison

| Metric                | Full Precision (FP) | GGUF Quantized |                Improvement / Change |
| :-------------------- | ------------------: | -------------: | ---------------------------------: |
| Average RAM Usage     |          1129.38 MB |       554.80 MB |                   51 percent lower |
| Average Response Time |            24.89 s |        52.19 s |                  2.1 times slower |
| Average Throughput    |          5.72 t/s  |       18.30 t/s |                3.2 times higher |
| Average Output Tokens |               143  |           955  |                   Not comparable |
| Response Quality      |           Very Good |      Mixed (one severe failure) |    FP was more reliable |
| Hardware Requirement  |              Higher |     Much Lower |  Better for CPU deployment |

> The average response time for GGUF is skewed by the 229.47-second email failure. Excluding that single outlier, the GGUF average time drops to 7.87 s, which is 3.2 times faster than FP.

---

## Observations

- The GGUF quantized model reduced average memory consumption from approximately 1.13 GB to 555 MB, representing a 51 percent reduction.

- Total token throughput improved from 5.72 tokens/s to 18.30 tokens/s, a 3.2 times increase overall.

- Per-prompt performance (excluding the failed email) was dramatically better:
  - Recursion: 35.34 s → 6.30 s (5.6 times faster)
  - Factorial: 33.40 s → 18.35 s (1.8 times faster)
  - Machine Learning: 20.54 s → 5.88 s (3.5 times faster)
  - Translation: 4.07 s → 0.94 s (4.3 times faster)

- Quality was not uniformly better. While the quantized model handled recursion, factorial, machine learning, and translation correctly, it failed catastrophically on the annual leave email prompt by entering a severe repetition loop, generating 4,059 tokens (most of them duplicates) and taking nearly 4 minutes to finish. The full-precision model handled this prompt correctly in 31 seconds with only 200 tokens.

- For CPU-only environments, GGUF offers excellent memory and speed benefits for most tasks, but careful attention must be paid to decoding parameters, such as repetition penalties, stop tokens, or maximum new tokens, to prevent infinite loops on certain prompt types.

---

## Write-up

For a production deployment, the choice of quantization method depends primarily on the deployment environment rather than on model quality alone.

Bitsandbytes is recommended when using NVIDIA GPUs during development or research. It integrates easily with the Hugging Face Transformers ecosystem, requires only a few lines of code, and allows switching between full precision and 4-bit or 8-bit quantization without converting the model. This makes it ideal for rapid experimentation, debugging, and evaluation. However, because it depends on CUDA, it is less suitable for CPU-only deployments.

For a production GPU service, GPTQ or AWQ are preferred over bitsandbytes. Both methods produce an offline-quantized model that is optimized before deployment, resulting in lower memory usage and faster inference. Between the two, AWQ is generally selected when maintaining response quality is important because it preserves important activation information during quantization. GPTQ is chosen when inference speed and memory efficiency are the highest priorities and a small reduction in quality is acceptable.

For CPU deployment, edge devices, or systems without a dedicated GPU, GGUF is the preferred choice. During this project, a full-precision Transformers model was compared with a GGUF version running through llama.cpp on CPU. The GGUF model required much less memory and generated responses significantly faster on the majority of prompts while maintaining similar answer quality. It was also straightforward to deploy because it did not require CUDA or PyTorch acceleration. However, the repetition loop observed on the email prompt highlights that GGUF with llama.cpp may need stricter generation controls, such as repetition penalty, max tokens, or custom stopping criteria, to match the stability of the full-precision pipeline.

Overall, the recommended deployment strategy is:

- Bitsandbytes for fast experimentation and development on NVIDIA GPUs.
- GPTQ or AWQ for high-performance GPU production inference, with AWQ preferred when preserving model quality is more important.
- GGUF for CPU-only deployment, edge devices, and lightweight local applications where memory usage and inference speed are critical, with robust generation safeguards in place.