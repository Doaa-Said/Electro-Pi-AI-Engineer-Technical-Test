from rag_chain import RAGPipeline


def main():
    pipeline = RAGPipeline()

    print("RAG assistant ready. Type 'exit' to quit.\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        answer = pipeline.answer(question)
        print("\n" + answer + "\n")


if __name__ == "__main__":
    main()