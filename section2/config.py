from __future__ import annotations
from langchain_groq import ChatGroq

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent

DOCS_DIR = BASE_DIR / os.getenv("DOCS_DIR", "documents")
CHROMA_DIR = BASE_DIR / os.getenv("CHROMA_DIR", "chroma_db")

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "docs")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 900))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 180))

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
}

LLM_MODEL = os.getenv("LLM_MODEL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_llm():
    return ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0,
    )