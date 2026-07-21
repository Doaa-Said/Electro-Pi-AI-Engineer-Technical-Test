from typing import Generator

import torch
from transformers import AutoTokenizer, TextIteratorStreamer
from optimum.onnxruntime import ORTModelForCausalLM

from threading import Thread

from app.config import (
    MODEL_DIR,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_P,
    DO_SAMPLE,
)

print("=" * 60)
print("Loading ONNX model...")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

model = ORTModelForCausalLM.from_pretrained(
    MODEL_DIR,
    provider="CPUExecutionProvider",
)

print("=" * 60)
print("Model loaded successfully!")
print("=" * 60)


def generate(prompt: str) -> str:

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        do_sample=DO_SAMPLE,
        pad_token_id=tokenizer.eos_token_id,
    )

    text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    )

    if text.startswith(prompt):
        text = text[len(prompt):]

    return text.strip()


def stream_generate(prompt: str) -> Generator[str, None, None]:

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    thread = Thread(
        target=model.generate,
        kwargs=dict(
            **inputs,
            streamer=streamer,
            max_new_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=DO_SAMPLE,
            pad_token_id=tokenizer.eos_token_id,
        ),
    )

    thread.start()

    for token in streamer:
        yield token