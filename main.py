"""
Main Script - Simple RAG System
Run this file to see everything in action!

Usage:
    python main.py
"""

from core import DocumentLoader, Chunker, Retriever
import config


def main():

    # LOAD DOCUMENTS
    print("Loading documents...")

    loader = DocumentLoader(config.DATA_DIR)
    documents = loader.load_documents()

    if not documents:
        print("\n  No documents found!")
        print(f"Please add .txt files to: {config.DATA_DIR}")
        return

    # CHUNK DOCUMENTS
    print("-" * 60)
    print("Chunking documents...")

    chunker = Chunker()
    chunks = chunker.chunk_documents(documents)

    # INDEX DOCUMENTS
    print("-" * 60)
    print("Creating embeddings and indexing...")

    retriever = Retriever()

    # Try to load existing index
    if retriever.load():
        print("\nLoaded existing vector store")
        user_input = input("\nRe-index documents? (y/n): ")
        if user_input.lower() == 'y':
            retriever.vector_store.clear()
            retriever.index_documents(chunks)
            retriever.save()
    else:
        # Index for first time
        retriever.index_documents(chunks)
        retriever.save()


    # QUERY LOOP
    print("\nQuery your documents!")
    print("=" * 60)
    print("Type your questions ('q', 'exit' or 'quit' to exit)")
    print("-" * 60)

    while True:
        query = input("\nYour question: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye! *Program Ended*")
            break

        if not query:
            continue

        # Retrieve relevant chunks
        results = retriever.retrieve(query, top_k=3)

        print("\n" + "=" * 60)
        print("RETRIEVED CONTEXT:")
        print("=" * 60)
        for i, result in enumerate(results, 1):
            print(f"\n[Result {i}]")
            print(f"Source: {result['source']} | Chunk: {result['chunk_id']}")
            print(f"Relevance Score: {1 / (1 + result['distance']):.4f}")  # Convert distance to similarity
            # print(f"\nContent:\n{result['content']}")
            print("-" * 60)


if __name__ == "__main__":
    main()