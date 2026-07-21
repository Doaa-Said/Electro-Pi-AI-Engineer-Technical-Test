from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = os.getenv(
    "MODEL_DIR",
    str(BASE_DIR / "onnx_model"),
)

MAX_TOKENS = int(
    os.getenv("MAX_TOKENS", 256)
)

TEMPERATURE = float(
    os.getenv("TEMPERATURE", 0.7)
)

TOP_P = float(
    os.getenv("TOP_P", 0.9)
)

DO_SAMPLE = os.getenv(
    "DO_SAMPLE",
    "true"
).lower() == "true"