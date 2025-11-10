"""
Vector Store
Stores embeddings and performs similarity search using FAISS

FAISS (Facebook AI Similarity Search):
- Ultra-fast similarity search library
- Can handle millions of vectors
- Perfect for RAG systems
"""

import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Tuple
import config


class VectorStore:
    """
    Vector database using FAISS for similarity search
    """

    def __init__(self, dimension: int = config.EMBEDDING_DIMENSION):
        """
        Initialize vector store

        Args:
            dimension (int): Dimension of embedding vectors
        """
        self.dimension = dimension

        self.index = faiss.IndexFlatL2(dimension)

        # Store metadata for each vector
        self.metadata = []

        print(f"\nVector store initialized (dimension={dimension})")

    def add_embeddings(self, embeddings: np.ndarray, metadata: List[Dict]):
        """
        Add embeddings and their metadata to the store

        Args:
            embeddings: numpy array of shape (n, dimension)
            metadata: List of metadata dicts (one per embedding)
        """
        # Ensure correct shape
        if len(embeddings.shape) == 1:
            embeddings = embeddings.reshape(1, -1)

        # Ensure float32 (FAISS requirement)
        embeddings = embeddings.astype('float32')

        self.index.add(embeddings)

        self.metadata.extend(metadata)

        print(f"✓ Added {len(embeddings)} embeddings to vector store")
        print(f"  Total vectors in store: {self.index.ntotal}")

    def search(self, query_embedding: np.ndarray, top_k: int = config.TOP_K) -> List[Dict]:
        """
        Search for similar vectors

        Args:
            query_embedding: Query vector
            top_k: Number of results to return

        Returns:
            List of metadata dicts for top_k most similar vectors
        """
        # Ensure correct shape and type
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        query_embedding = query_embedding.astype('float32')

        # Search
        distances, indices = self.index.search(query_embedding, top_k)

        # Get metadata for results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):  # Valid index
                result = self.metadata[idx].copy()
                result['distance'] = float(distance)
                result['rank'] = i + 1
                results.append(result)

        return results

    def save(self, path: str = config.VECTOR_DB_PATH):
        """
        Save vector store to disk

        Args:
            path: Base path for saving (will create .index and .metadata files)
        """
        # Save FAISS index
        faiss.write_index(self.index, f"{path}.index")

        # Save metadata
        with open(f"{path}.metadata", 'wb') as f:
            pickle.dump(self.metadata, f)

        print(f"Vector store saved to {path}")

    def load(self, path: str = config.VECTOR_DB_PATH):
        """
        Load vector store from disk

        Args:
            path: Base path for loading (will load .index and .metadata files)
        """
        # Check if files exist
        if not os.path.exists(f"{path}.index"):
            print(f"No saved vector store found at {path}")
            return False

        # Load FAISS index
        self.index = faiss.read_index(f"{path}.index")

        # Load metadata
        with open(f"{path}.metadata", 'rb') as f:
            self.metadata = pickle.load(f)

        print(f"Vector store loaded from {path}")
        print(f"  Total vectors: {self.index.ntotal}")
        return True

    def clear(self):
        """
        Clear all data from vector store
        """
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        print("Vector store cleared")
