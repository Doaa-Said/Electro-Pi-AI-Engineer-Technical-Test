from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from config import (
    BASE_DIR,
    DOCS_DIR,
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SUPPORTED_EXTENSIONS,
)


def load_documents() -> List[Document]:
    """Load all supported documents."""

    if not DOCS_DIR.exists():
        raise FileNotFoundError(
            f"Documents folder not found: {DOCS_DIR}"
        )

    documents: List[Document] = []

    files = [
        p
        for p in DOCS_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        raise FileNotFoundError(
            f"No supported documents found in {DOCS_DIR}"
        )

    for file_path in files:

        print(f"[ingest] Loading {file_path.name}")

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
        else:
            loader = TextLoader(
                str(file_path),
                encoding="utf-8",
            )

        docs = loader.load()

        for doc in docs:

            try:
                source = str(file_path.relative_to(BASE_DIR))
            except ValueError:
                source = str(file_path)

            doc.metadata.update(
                {
                    "source": source,
                    "file_name": file_path.name,
                    "file_type": suffix,
                }
            )

        documents.extend(docs)

    print(f"[ingest] Loaded {len(documents)} pages.")

    return documents


def split_documents(documents: List[Document]) -> List[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = idx

    print(f"[ingest] Created {len(chunks)} chunks.")

    return chunks


def build_vectorstore(chunks: List[Document]) -> Chroma:

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    try:
        db = Chroma(
            persist_directory=str(CHROMA_DIR),
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
        )

        db.delete_collection()

        print("[ingest] Old collection deleted.")

    except Exception:
        pass

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )

    print(f"[ingest] Chroma DB saved to {CHROMA_DIR}")

    return vectorstore


def main():

    docs = load_documents()

    chunks = split_documents(docs)

    build_vectorstore(chunks)

    print("[ingest] Finished successfully.")


if __name__ == "__main__":
    main()