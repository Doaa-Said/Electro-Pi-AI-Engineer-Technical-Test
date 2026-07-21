# Section 1 – LiveKit Voice Agent with Tool Calling

---

# Overview

This section implements a complete voice-enabled AI customer support agent using the LiveKit Agents SDK.

The assistant acts as a Food Delivery Support Agent capable of understanding spoken requests, reasoning with a Large Language Model (LLM), invoking backend tools when required, and responding with synthesized speech.

The complete voice pipeline consists of:

- Speech-to-Text (STT)
- Large Language Model (LLM)
- Tool Calling
- Text-to-Speech (TTS)
- Voice Activity Detection (VAD)

The implementation follows a modular architecture where each provider is abstracted through a provider factory, making it easy to replace any provider without changing the application logic.

---

# Project Structure

```text
section1/
│
├── agent.py
├── config.py
├── provider_factory.py
├── main.py
├── prompts.py
├── tools.py
├── test.py
├── requirements.txt
├── .env
├── Write-up.md
├── README.md
└── Food Support Voice Agent – Tool Calling Demonstration.mp4
```

---

# Project Files

## main.py

The main entry point of the application.

Responsibilities include:

- Starting the LiveKit worker
- Waiting for participants
- Creating the AgentSession
- Loading the STT, LLM and TTS providers
- Initializing Voice Activity Detection (VAD)
- Starting the Food Support Agent
- Handling the live voice conversation

---

## provider_factory.py

Implements the provider abstraction layer.

This factory creates the required pipeline components according to the selected providers inside the `.env` file.

Supported providers include:

- Deepgram Speech-to-Text
- Groq Speech-to-Text
- Groq Large Language Model
- Cartesia Text-to-Speech

Using this design, providers can be swapped without modifying the rest of the application.

---

## config.py

Loads all configuration values from the `.env` file.

Includes:

- LiveKit configuration
- API Keys
- Room configuration
- Provider selection
- Model configuration

---

## agent.py

Defines the Food Support Agent.

Registers:

- System prompt
- Agent instructions
- Backend tools

---

## prompts.py

Contains the system prompt that defines the assistant's behavior as a food delivery support representative.

---

## tools.py

Implements the backend tools used by the language model.

Registered tools:

- get_order_status()
- cancel_order()
- estimate_delivery_time()

Whenever the LLM determines that external information or an action is required, it automatically invokes one of these functions.

---

## requirements.txt

Lists all required Python packages.

Install everything using:

```bash
pip install -r requirements.txt
```

---

## .env

Stores all runtime configuration.

Includes:

- LiveKit URL
- LiveKit API Key
- LiveKit API Secret
- Groq API Key
- Cartesia API Key
- Room Name
- Provider selection
- Model names

---

## Write-up.md

Contains the required design write-ups including:

- Barge-in / interruption handling
- Safe tool execution
- Provider swapping
- Design decisions
- Error handling

---


## Food Support Voice Agent – Tool Calling Demonstration.mp4

The video demonstrates the complete voice interaction between the user and the LiveKit voice agent.

The conversation proceeds as follows:

1. The user asks:
   "Where is my order? My order number is 1001."

2. The speech is transcribed by the STT component.

3. The LLM recognizes that the request requires checking an order status instead of answering from its own knowledge.

4. The agent automatically invokes the `get_order_status(order_id)` tool.

5. The tool returns the mock order information:

   - Order ID: 1001
   - Status: Preparing
   - Estimated delivery time: 15 minutes

6. The LLM converts the structured tool output into a natural language response:

   "Your order number one thousand one is currently being prepared and is expected to arrive within 15 minutes."

7. The agent then asks:

   "Would you like to know anything else about your order?"

8. The user replies:

   "I want to cancel this order."

9. The LLM determines that this request requires a different backend action and invokes the `cancel_order(order_id)` tool.

10. The cancellation tool successfully updates the mock order state and returns a confirmation.

11. The agent responds:

    "Your order number one thousand one has been cancelled."

12. The user later asks about another order (1002).

13. The agent again calls `get_order_status(order_id)` and returns the corresponding delivery estimate from the tool.

14. Finally, the user asks about order 1004.

15. Since this order does not exist in the mock database, the tool returns an error indicating that no matching order was found.

16. Instead of generating incorrect information, the LLM safely reports the tool result:

    "I'm sorry, but I couldn't find any information on order number one thousand four. Could you please check if the order number is correct or provide more details?"

This demonstration verifies that the LLM is not memorizing responses. Instead, it decides when a tool is required, invokes the appropriate function, waits for the returned result, and generates its final spoken response using that tool output. The last interaction also demonstrates safe error handling when the requested order does not exist.

The video clearly demonstrates the complete processing pipeline:

```
User Speech
      ↓
Speech-to-Text
      ↓
Large Language Model
      ↓
Tool Invocation
      ↓
Tool Response
      ↓
LLM Response Generation
      ↓
Text-to-Speech
      ↓
Voice Response
```



---

# Setup Instructions

## 1. Clone the repository

```bash
git clone <repository-url>
cd section1
```

---

## 2. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate it

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file.

Example:

```env
LIVEKIT_URL=...

LIVEKIT_API_KEY=...

LIVEKIT_API_SECRET=...

ROOM_NAME=test-room-debug-001

GROQ_API_KEY=...

CARTESIA_API_KEY=...

STT_PROVIDER=deepgram

LLM_PROVIDER=groq

TTS_PROVIDER=cartesia
```

---

## 5. Start the worker

```bash
python main.py start
```

The worker connects to LiveKit Cloud and waits for participants.

---

## 6. Open LiveKit Playground

Open the LiveKit Playground.

Connect using the same room specified in the `.env` file.

After joining the room, the worker automatically starts the voice session.

No additional client application is required.

---

## 7. Test the Agent

Example:

```
Where is my order 1001?
```

The LLM automatically calls:

```python
get_order_status()
```

Example:

```
Cancel my order 1001.
```

The LLM automatically calls:

```python
cancel_order()
```

Example:

```
When will order 1002 arrive?
```

The LLM automatically calls:

```python
estimate_delivery_time()
```

---

# Features Demonstrated

- Live speech recognition
- Live voice conversation
- Tool Calling
- Voice Activity Detection
- LiveKit integration
- Modular provider architecture
- Backend function execution
- Natural language responses
- Speech synthesis

---

# Bonus Task Completed

The bonus requirement, "Swap a Pipeline Component," has been successfully implemented.

The project uses a provider factory that separates the application logic from the selected providers.

Original configuration:

```env
STT_PROVIDER=deepgram
LLM_PROVIDER=groq
TTS_PROVIDER=cartesia
```

Alternative configuration:

```env
STT_PROVIDER=groq
LLM_PROVIDER=groq
TTS_PROVIDER=cartesia
```

Only the configuration changes.

No modifications to the application code are required.

This demonstrates that the architecture is fully decoupled from any specific STT or TTS vendor.

---

# Assumptions

- Valid API keys are provided.
- Internet access is available.
- LiveKit Cloud is accessible.
- Provider services are operational.

---

# Known Limitations

- Order data is mocked and not connected to a production database.
- Conversation history is not persisted.
- User authentication is limited to LiveKit room access.
- Tool failures return simple error messages.
- External provider availability depends on their APIs.

---

# Deliverables Included

✔ Complete LiveKit Voice Agent

✔ Tool Calling

✔ LiveKit Playground Demonstration

✔ Demonstration Video

✔ Source Code

✔ Setup Instructions


✔ Write-up

✔ Provider Abstraction

✔ Bonus Provider Swapping Implementation

---

# Section 2 – Retrieval-Augmented Generation (RAG) Assistant

---

# Overview

This section implements a complete Retrieval-Augmented Generation (RAG) question-answering assistant using LangChain, ChromaDB, Hugging Face embeddings, and an open-weight Large Language Model.

Instead of relying only on the language model's internal knowledge, the assistant retrieves relevant information from a collection of company documents before generating an answer.

The implemented RAG pipeline consists of:

- Document Loading
- Text Chunking
- Embedding Generation
- Chroma Vector Database
- Semantic Retrieval
- Prompt Construction
- Large Language Model (LLM)
- Source Citation

The implementation follows a modular architecture where document ingestion, retrieval, prompting, and generation are separated into different files, making the system easy to extend or replace.

---

# Project Structure

```text
section2/
│
├── app.py
├── config.py
├── ingest.py
├── prompts.py
├── rag_chain.py
├── requirements.txt
├── .env
├── write_up.md
├── README.md
│
├── documents/
│   ├── Employee_Handbook.pdf
│   ├── Leave_Policy.pdf
│   └── IT_FAQ.pdf
│
├── chroma_db/
│
├── log1.png
├── log2.png
├── log3.png
└── log4.png
```

---

# Project Files

## app.py

The main entry point of the application.

Responsibilities include:

- Loading the RAG pipeline
- Accepting user questions
- Retrieving relevant document chunks
- Sending context to the language model
- Displaying the generated answer
- Showing document citations

Run using:

```bash
python app.py
```

---

## ingest.py

Builds the vector database.

Responsibilities include:

- Loading PDF documents
- Splitting documents into chunks
- Generating embeddings
- Creating the Chroma vector database
- Persisting embeddings for future retrieval

This file only needs to be executed once (or whenever documents change).

Run using:

```bash
python ingest.py
```

---

## rag_chain.py

Implements the complete Retrieval-Augmented Generation pipeline.

Responsibilities include:

- Loading the Chroma database
- Performing semantic retrieval
- Formatting retrieved context
- Building prompts
- Calling the language model
- Returning answers with citations

Current retrieval strategy:

- Maximum Marginal Relevance (MMR)
- Top-K retrieval
- Context merging
- Source citation generation

---

## prompts.py

Contains the system prompt used by the language model.

The prompt instructs the assistant to:

- Answer only using retrieved document context
- Avoid hallucinating information
- Clearly state when information is unavailable
- Produce concise and accurate responses

---

## config.py

Loads all configuration values.

Includes:

- Embedding model
- LLM configuration
- Chroma database directory
- Collection name
- Environment variables

---

## requirements.txt

Lists all required Python packages.

Install using:

```bash
pip install -r requirements.txt
```

---

## .env

Stores runtime configuration.

Typical variables include:

```env
MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHROMA_DIR=./chroma_db
```

---

## documents/

Contains the knowledge base used by the assistant.

The provided documents are:

- Employee_Handbook.pdf
- Leave_Policy.pdf
- IT_FAQ.pdf

These files are indexed into ChromaDB during ingestion.

---

## chroma_db/

Stores the persistent vector database generated during ingestion.

This directory contains:

- embeddings
- metadata
- vector index

The assistant loads this database during inference without rebuilding embeddings.

---

## Execution Logs

The project includes execution screenshots demonstrating the RAG assistant during inference.

Included screenshots:

- `log1.png`
- `log2.png`
- `log3.png`
- `log4.png`

These logs show example interactions with the assistant, including generated answers, retrieved document citations, and the application's runtime behavior.

---

## write_up.md

Contains the required design discussion including:

- Chunking strategy
- Retrieval improvements
- Hybrid search
- Re-ranking
- Design decisions
- Known limitations

---

# System Architecture

The complete RAG pipeline follows the workflow below:

```

User Question
↓
Embedding Generation
↓
Semantic Search (ChromaDB)
↓
Relevant Document Chunks
↓
Prompt Construction
↓
Large Language Model
↓
Answer Generation
↓
Source Citations

```

---

# Setup Instructions

## 1. Clone the repository

```bash
git clone <repository-url>

cd section2
```

---

## 2. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate it

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file.

Example:

```env
MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHROMA_DIR=./chroma_db
```

---

## 5. Build the Vector Database

Run the ingestion script:

```bash
python ingest.py
```

This process:

- Loads PDF documents
- Splits them into chunks
- Computes embeddings
- Creates the Chroma database

This only needs to be repeated if the document collection changes.

---

## 6. Start the Assistant

Run:

```bash
python app.py
```

You should see:

```
RAG assistant ready.
Type 'exit' to quit.
```

---

## 7. Test the Assistant

Example questions:

```
How many annual leave days do employees receive?
```

```
What are the company's working hours?
```

```
Can employees work remotely?
```

```
How do I reset my company password?
```

```
Summarize the leave policy.
```

Questions outside the document collection:

```
Who is the CEO of the company?
```

```
Where is the company headquarters?
```

For these questions, the assistant correctly reports that the information is not available in the indexed documents.

---

# Features Demonstrated

- Retrieval-Augmented Generation (RAG)
- PDF document ingestion
- Semantic vector search
- Hugging Face embeddings
- Chroma vector database
- Maximum Marginal Relevance (MMR) retrieval
- Prompt engineering
- Source citation generation
- Hallucination reduction
- Persistent vector storage

---

# Retrieval Strategy

The project currently uses:

- Semantic embeddings
- Chroma vector database
- Maximum Marginal Relevance (MMR)
- Top-K retrieval
- Context aggregation
- Source citation generation

This approach improves answer diversity while reducing duplicate retrieved chunks.

---

# Assumptions

- Documents are written in English.
- Documents are available before running the ingestion script.
- The embedding model can be downloaded successfully.
- Internet access is available during the first model download.
- ChromaDB persists correctly between runs.

---

# Known Limitations

- Retrieval is based only on dense semantic search.
- No keyword (BM25) retrieval is implemented.
- No cross-encoder re-ranking is used.
- Very long documents may require improved chunking strategies.
- Image-based PDFs are not supported without OCR.
- Answers are limited to the indexed document collection.

---

# Future Improvements

Potential improvements include:

- Hybrid retrieval (BM25 + semantic search)
- Cross-encoder re-ranking
- Adaptive chunk sizes
- Metadata-aware retrieval
- Multi-query retrieval
- Parent-document retrieval
- OCR support for scanned PDFs
- Streaming responses
- Web interface

---

# Deliverables Included

✔ Complete Retrieval-Augmented Generation (RAG) Assistant

✔ PDF Document Ingestion Pipeline

✔ Chroma Vector Database

✔ Semantic Retrieval

✔ Hugging Face Embeddings

✔ Source Citation

✔ Interactive Question-Answer Interface

✔ Demonstration Screenshots

✔ Setup Instructions

✔ Design Write-up

✔ Modular Architecture

---

# Section 3 – LLM Quantization and Performance Evaluation

---

# Overview

This section evaluates the performance of an open-weight Large Language Model (LLM) running locally on a CPU in both full precision and quantized formats.

The project compares two inference approaches:

- Full Precision model using Hugging Face Transformers
- Quantized GGUF model using llama.cpp

Both implementations are evaluated using the same prompts to compare:

- Memory usage (RAM)
- Response time
- Throughput (tokens/second)
- Output quality

The objective is to demonstrate the practical trade-offs between full precision and quantized inference for local deployment.

---

# Project Structure

```text
section3/
│
├── .venv/
├── models/
│   ├── fp/
│   └── gguf/
│
├── app_fp.py
├── app_gguf.py
├── download_model.py
├── prompts.txt
├── log.txt
├── requirements.txt
├── results and write_up.md
└── README.md
```

---

# Project Files

## app_fp.py

Runs the original Hugging Face model using the Transformers library.

Responsibilities include:

- Loading the full precision model
- Loading the tokenizer
- Generating responses
- Measuring RAM usage
- Measuring response time
- Counting output tokens
- Calculating throughput (tokens/second)

---

## app_gguf.py

Runs the quantized GGUF model using llama.cpp.

Responsibilities include:

- Loading the GGUF model
- Running inference
- Measuring RAM usage
- Measuring response time
- Counting generated tokens
- Calculating throughput
- Comparing performance with the full precision implementation

---

## download_model.py

Downloads the Hugging Face model and stores it locally.

Running this script avoids downloading the model every time the application starts.

---

## prompts.txt

Contains the five fixed evaluation prompts used for benchmarking both implementations.

Using identical prompts ensures a fair comparison.

---

## log.txt

Contains the execution logs generated during benchmarking, including model responses and performance statistics.

---

## results and write_up.md

Contains:

- Experimental setup
- Benchmark tables
- Performance comparison
- Memory analysis
- Throughput comparison
- Output quality evaluation
- Production deployment discussion
- Quantization trade-off analysis

---

## requirements.txt

Lists all required Python packages.

Install them using:

```bash
pip install -r requirements.txt
```

---

## models/

Stores the downloaded models.

### fp/

Contains the original Hugging Face model.

### gguf/

Contains the quantized GGUF model used by llama.cpp.

---

# Experimental Pipeline

```
User Prompt
      ↓
Load Model
      ↓
Generate Response
      ↓
Measure RAM Usage
      ↓
Measure Response Time
      ↓
Count Output Tokens
      ↓
Calculate Tokens/Second
      ↓
Compare Performance
```

---

# Setup Instructions

## 1. Clone the repository

```bash
git clone <repository-url>

cd section3
```

---

## 2. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate it

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Download the models

Run:

```bash
python download_model.py
```

This downloads the Hugging Face model into the `models/fp` directory.

Download the GGUF version from:

[https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/blob/main/qwen2.5-0.5b-instruct-q4_k_m.gguf)

Place it inside:

```text
models/
└── gguf/
    └── qwen2.5-0.5b-instruct-q4_k_m.gguf
```

---

## 5. Run the Full Precision Model

```bash
python app_fp.py
```

The application reports:

- Generated response
- RAM usage
- Output tokens
- Response time
- Tokens per second

---

## 6. Run the Quantized Model

```bash
python app_gguf.py
```

The application reports the same metrics for the GGUF model.

---

## 7. Review the Results

Open:

```text
results and write_up.md
```

The report contains:

- Full precision benchmark
- Quantized benchmark
- Performance comparison
- Output quality comparison
- Production deployment discussion

---

# Evaluation Prompts

Both implementations are evaluated using the same prompts:

- Explain recursion in simple terms.
- Write a Python function to compute factorial.
- Summarize machine learning in 100 words.
- Translate "Good morning, how are you?" into French.
- Write a professional email requesting annual leave.

Using identical prompts ensures a fair and consistent comparison.

---

# Metrics Measured

The evaluation measures:

- RAM usage
- Response time
- Output tokens
- Throughput (tokens/second)
- Qualitative response quality

---

# Features Demonstrated

- Full precision inference
- Quantized inference
- CPU-only execution
- Hugging Face Transformers
- llama.cpp integration
- GGUF model loading
- Runtime benchmarking
- Memory measurement
- Throughput measurement
- Quality comparison

---

# Experimental Results

Detailed benchmark results are available in:

```
results and write_up.md
```

The report includes:

- Full precision benchmark
- GGUF benchmark
- Performance tables
- Overall comparison
- Quantization discussion

---

# Assumptions

- The required model files have been downloaded before execution.
- The evaluation is performed on a CPU-only environment.
- Internet access is available for the initial model download.
- The system has sufficient RAM to load the selected model.

---

# Known Limitations

- CPU inference is slower than GPU inference.
- The benchmark uses only five evaluation prompts.
- Only one quantization format (GGUF) is evaluated.
- Performance varies depending on processor and available memory.
- Output quality is evaluated qualitatively rather than with standardized benchmarks.

---

# Future Improvements

Possible future enhancements include:

- GPU benchmarking
- GPTQ evaluation
- AWQ evaluation
- bitsandbytes comparison
- Larger language models
- Automated benchmarking scripts
- Additional benchmark datasets
- Batch inference evaluation
- Streaming text generation

---

# Deliverables Included

✔ Full Precision Model Implementation

✔ GGUF Quantized Model Implementation

✔ CPU Performance Benchmark

✔ Memory Usage Measurement

✔ Throughput Measurement

✔ Experimental Results

✔ Quantization Trade-off Analysis

✔ Setup Instructions

✔ Design Write-up

✔ Source Code

---

# Section 4 – LLM Deployment as a REST API

---

# Overview

This section deploys an open-weight Large Language Model (LLM) as a production-style inference service using FastAPI, ONNX Runtime, and Docker.

The model is exported to ONNX format and served through a REST API that supports both standard and streaming text generation.

The implementation demonstrates a complete deployment pipeline including:

- ONNX Runtime inference
- FastAPI REST API
- Docker containerization
- Streaming responses
- Concurrent request handling
- Load and latency evaluation

The objective is to demonstrate how an LLM can be packaged as a reusable service suitable for local deployment.

---

# Deployment Choice

This project uses FastAPI with ONNX Runtime to deploy the language model as a REST API.

FastAPI was selected because it is a lightweight, high-performance web framework that is easy to develop, deploy, and maintain. It provides automatic API documentation through Swagger UI, supports asynchronous request handling, and offers native support for streaming responses, making it well suited for serving Large Language Models (LLMs).

ONNX Runtime was chosen as the inference engine because it is optimized for efficient execution on CPU and GPU across multiple platforms. By exporting the model to ONNX format, the model becomes portable and independent of the original PyTorch implementation. ONNX Runtime applies graph optimizations that improve inference efficiency while reducing deployment complexity.

Compared with inference servers such as vLLM or Hugging Face Text Generation Inference (TGI), this implementation is simpler to set up, requires fewer resources, and is sufficient for deploying a lightweight CPU-based language model. It also satisfies the project requirements by providing a containerized REST API with streaming inference and load testing.

---

# Project Structure

```text
section4/
│
├── .venv/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── model.py
│   ├── schemas.py
│   ├── load_test.py
│   └── test_stream.py
│
├── onnx_model/
│   ├── config.json
│   ├── generation_config.json
│   ├── model.onnx
│   ├── model.onnx_data
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   ├── vocab.json
│   ├── merges.txt
│   └── ...
│
├── Dockerfile
├── export_model.py
├── requirements.txt
├── results_and_write_up.md
├── docker_run.PNG
├── load_test_results.PNG
├── stream.PNG
├── streaming_test_results.PNG
├── ttft.PNG
└── README.md
```

---

# Project Files

## main.py

Creates the FastAPI application and exposes the REST API endpoints.

Responsibilities include:

- Initializing the FastAPI application
- Defining the health endpoint
- Handling text generation requests
- Returning streaming responses

---

## model.py

Loads the ONNX model and performs text generation.

Responsibilities include:

- Loading the tokenizer
- Loading the ONNX Runtime model
- Encoding user prompts
- Running inference
- Decoding generated text
- Streaming generated output

---

## config.py

Stores configurable runtime parameters.

Includes:

- ONNX model path
- Maximum generated tokens
- Temperature
- Generation configuration

---

## schemas.py

Defines the request and response schemas using Pydantic.

---

## export_model.py

Downloads the Hugging Face model and exports it to ONNX format.

Running this script prepares the model for deployment without requiring export each time the API starts.

---

## load_test.py

Runs a basic concurrent load test against the deployed API.

The script reports:

- Individual request latency
- Average latency
- Minimum latency
- Maximum latency
- Total wall time

---

## test_stream.py

Evaluates streaming performance.

The script measures:

- Time-to-First-Token (TTFT)
- Total response latency

---

## Dockerfile

Builds the complete deployment container.

The image contains:

- Python runtime
- ONNX Runtime
- FastAPI
- Exported ONNX model
- API source code

---

## requirements.txt

Lists all required Python packages.

Install them using:

```bash
pip install -r requirements.txt
```

---

## onnx_model/

Contains the exported ONNX model and tokenizer files used during inference.

---

## results_and_write_up.md

Contains:

- Load testing results
- Streaming benchmark
- TTFT measurements
- Production deployment discussion
- Scalability recommendations

---

# Deployment Pipeline

```
User Request
      │
      ▼
FastAPI REST API
      │
      ▼
Tokenizer
      │
      ▼
ONNX Runtime
      │
      ▼
ONNX Model
      │
      ▼
Generated Response
```

---

# Setup Instructions

## 1. Clone the repository

```bash
git clone <repository-url>

cd section4
```

---

## 2. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate it

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Export the model

Run:

```bash
python export_model.py
```

The exported model will be stored inside:

```text
onnx_model/
```

---

## 5. Build the Docker image

```bash
docker build -t onnx-api .
```

---

## 6. Run the Docker container

```bash
docker run -p 8000:8000 onnx-api
```

The API will be available at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

# API Endpoints

## Health Check

```http
GET /
```

Returns

```json
{
  "message": "ONNX LLM API is running successfully."
}
```

---

## Generate Text

```http
POST /generate
```

Example request

```json
{
  "prompt": "Explain recursion."
}
```

Example response

```json
{
  "response": "..."
}
```

---

## Streaming Generation

```http
POST /stream
```

Returns generated text incrementally as it is produced by the model.

---

# Load Testing

Run

```bash
python app/load_test.py
```

Measures:

- Concurrent request latency
- Average latency
- Minimum latency
- Maximum latency
- Total wall time

---

# Streaming Evaluation

Run

```bash
python app/test_stream.py
```

Measures:

- Time-to-First-Token (TTFT)
- Total response latency

---

# Performance Metrics

The deployment evaluates:

- API latency
- Streaming latency
- Time-to-First-Token
- Concurrent request latency
- End-to-end response time

Detailed benchmark results are available in:

```text
results_and_write_up.md
```

---

# Features Demonstrated

- ONNX Runtime inference
- FastAPI REST API
- Docker containerization
- REST endpoints
- Streaming responses
- Concurrent request handling
- Load testing
- TTFT measurement
- Local CPU inference
- Production-style deployment

---

# Experimental Results

Detailed benchmark results are available in:

```text
results_and_write_up.md
```

The report includes:

- Concurrent load testing
- Streaming benchmark
- TTFT measurements
- Production deployment discussion
- Scalability recommendations

---

# Assumptions

- The ONNX model has been exported before running the API.
- Docker is installed and running.
- The system has sufficient memory to load the model.
- CPU inference is used throughout the evaluation.

---

# Known Limitations

- CPU inference is slower than GPU inference.
- Large language models require significant memory.
- Dynamic batching is not implemented.
- Performance depends on available CPU resources.
- Concurrent requests increase overall latency on CPU-only systems.

---

# Future Improvements

Possible future enhancements include:

- GPU inference with ONNX Runtime CUDA
- Dynamic batching
- Request queueing
- Response caching
- Autoscaling with Kubernetes
- Multi-worker deployment
- Authentication and rate limiting
- Monitoring with Prometheus and Grafana

---

# Deliverables Included

✔ ONNX Runtime Deployment

✔ FastAPI REST API

✔ Dockerized Service

✔ Streaming Endpoint

✔ Load Testing Scripts

✔ TTFT Evaluation

✔ Concurrent Request Benchmark

✔ Production Deployment Discussion

✔ Setup Instructions

✔ Source Code

---
