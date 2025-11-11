"""
Retriever
Orchestrates the entire retrieval pipeline
"""

from typing import List, Dict
from .embedder import Embedder
from database.vector_store import VectorStore
import config


class Retriever:
    """
    High-level interface for retrieving relevant documents
    """

    def __init__(self):
        """
        Initialize retriever with embedder and vector store
        """
        self.embedder = Embedder()
        self.vector_store = VectorStore()

    def index_documents(self, chunks: List[Dict[str, str]]):
        """
        Create embeddings and add to vector store

        Args:
            chunks: List of document chunks with metadata
        """
        print("\n" + "=" * 50)
        print("INDEXING DOCUMENTS")
        print("=" * 50)

        # Extract text content
        texts = [chunk['content'] for chunk in chunks]

        # Create embeddings
        embeddings = self.embedder.embed_texts(texts)

        # Add to vector store
        self.vector_store.add_embeddings(embeddings, chunks)

        print("=" * 50 + "\n")

    def retrieve(self, query: str, top_k: int = config.TOP_K) -> List[Dict]:
        """
        Retrieve relevant documents for a query

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of relevant chunks with metadata and scores
        """
        print(f"Searching for: '{query}'")
        print("-" * 50)

        # Create query embedding
        query_embedding = self.embedder.embed_query(query)

        # Search vector store
        results = self.vector_store.search(query_embedding, top_k)

        # Display results
        print(f"Found {len(results)} relevant chunks:\n")
        for result in results:
            print(f"  Rank {result['rank']} | Distance: {result['distance']:.4f}")
            print(f"  Source: {result['source']} (Chunk {result['chunk_id']})")
            print(f"  Preview: {result['content'][:150]}...")
            print()

        return results

    def save(self):
        """Save vector store to disk"""
        self.vector_store.save()

    def load(self):
        """Load vector store from disk"""
        return self.vector_store.load()