"""
Chunker
Splits documents into smaller, manageable chunks
This is important because:
1. LLMs have token limits
2. Smaller chunks = more precise retrieval
3. Each chunk focuses on a specific topic
"""

from typing import List, Dict
import config


class Chunker:
    """
    Splits documents into overlapping chunks
    """

    def __init__(self, chunk_size: int = config.CHUNK_SIZE,
                 chunk_overlap: int = config.CHUNK_OVERLAP):
        """
        Initialize chunker with size and overlap settings

        Args:
            chunk_size (int): Maximum characters per chunk
            chunk_overlap (int): Number of characters that overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Split documents into chunks

        Args:
            documents: List of documents with 'content' and 'source'

        Returns:
            List of chunks with metadata
            Example: [
                {
                    'content': 'Chunk text...',
                    'source': 'file1.txt',
                    'chunk_id': 0
                }
            ]
        """
        all_chunks = []

        for doc in documents:
            content = doc['content']
            source = doc['source']

            # Split into chunks
            chunks = self._split_text(content)

            # Add metadata to each chunk
            for i, chunk_text in enumerate(chunks):
                all_chunks.append({
                    'content': chunk_text,
                    'source': source,
                    'chunk_id': i
                })

        print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks

    def _split_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks

        Args:
            text: The text to split

        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:

            end = start + self.chunk_size

            chunk = text[start:end]

            if chunk.strip():
                chunks.append(chunk)

            start += self.chunk_size - self.chunk_overlap

        return chunks

