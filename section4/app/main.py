from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.schemas import PromptRequest, PromptResponse
from app.model import generate, stream_generate

app = FastAPI(
    title="ONNX Runtime LLM API",
    description="FastAPI + ONNX Runtime + Qwen2.5",
    version="2.0.0",
)


@app.get("/")
def home():
    return {
        "message": "ONNX Runtime API is running."
    }


@app.post("/generate", response_model=PromptResponse)
def generate_text(request: PromptRequest):

    answer = generate(request.prompt)

    return PromptResponse(response=answer)


@app.post("/stream")
def stream(request: PromptRequest):

    return StreamingResponse(
        stream_generate(request.prompt),
        media_type="text/plain",
    )