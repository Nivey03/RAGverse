"""
Embedder
Converts text into numerical vectors (embeddings)

What are embeddings?
- Text → Numbers that capture meaning
- Similar text → Similar numbers
- Enables mathematical similarity search

Example:
"dog" → [0.2, 0.8, 0.1, ...]
"puppy" → [0.3, 0.7, 0.15, ...] ← Similar to "dog"
"car" → [0.9, 0.1, 0.05, ...] ← Different from "dog"
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import config


class Embedder:
    """
    Creates embeddings using a pre-trained model
    """

    def __init__(self, model_name: str = config.EMBEDDING_MODEL):
        """
        Initialize the embedding model

        Args:
            model_name (str): Name of the sentence-transformer model
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("------------- Model loaded successfully -------------")

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Convert a list of texts into embeddings

        Args:
            texts: List of text strings

        Returns:
            numpy array of shape (n_texts, embedding_dimension)
            Example: 10 texts → (10, 384) array
        """
        print(f"Creating embeddings for {len(texts)} texts...")

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        print(f"✓ Created embeddings with shape: {embeddings.shape}")
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """
        Convert a single query into an embedding

        Args:
            query: Query text

        Returns:
            numpy array of shape (embedding_dimension,)
        """
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding