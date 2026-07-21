from __future__ import annotations

from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

from config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    get_llm,
)
from prompts import SYSTEM_PROMPT


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""

    TOP_K = 5

    # Keep documents whose similarity score is close to the best one.
    # Lower score = more similar.
    MAX_SCORE_DIFF = 0.15

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        self.vectorstore = Chroma(
            persist_directory=str(CHROMA_DIR),
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
        )

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    """Context:
{context}

Question:
{question}
""",
                ),
            ]
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def retrieve(self, question: str) -> List[Document]:
        """Retrieve only the most relevant chunks."""

        results = self.vectorstore.similarity_search_with_score(
            question,
            k=self.TOP_K,
        )

        if not results:
            return []

        best_score = results[0][1]

        docs = []

        for doc, score in results:
            if score <= best_score + self.MAX_SCORE_DIFF:
                docs.append(doc)

        return docs

    @staticmethod
    def format_context(docs: List[Document]) -> str:
        """Merge retrieved chunks into one context."""

        return "\n\n".join(
            doc.page_content for doc in docs
        )

    @staticmethod
    def format_sources(docs: List[Document]) -> str:
        """Create unique citations."""

        seen = set()
        citations = []

        for doc in docs:

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page")

            if page is not None:
                citation = f"{source} (page {page + 1})"
            else:
                citation = source

            if citation not in seen:
                seen.add(citation)
                citations.append(citation)

        return "\n".join(citations)

    def answer(self, question: str) -> str:
        """Generate answer with citations."""

        docs = self.retrieve(question)

        if not docs:
            return (
                "I couldn't find relevant information "
                "in the provided documents."
            )

        context = self.format_context(docs)

        response = self.chain.invoke(
            {
                "context": context,
                "question": question,
            }
        ).strip()

        if (
            "I couldn't find relevant information "
            "in the provided documents."
            in response
        ):
            return response

        citations = self.format_sources(docs)

        return (
            f"{response}\n\n"
            f"Sources:\n{citations}"
        )