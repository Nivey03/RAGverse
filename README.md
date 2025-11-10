# RAGverse

An LLM that uses a basic Retrieval-Augmented Generation (RAG) method to retrieve information from user-provided PDFs (custom knowledge base).

## Installation
1. CLone the repository:
```bash
  git clone https://github.com/Nivey03/RAGverse.git
  cd RAGverse
```
2. Install dependencies
```bash
  pip install -r requirements.txt
```
3. Add your documents
    
    Place your `.pdf` or `.txt` files inside the `data/documents/` folder.

## Usage
Run the main script:
```bash
  python main.py
```

## How It Works

1. **Document Loading**: Reads all .txt files from `data/documents/`
2. **Chunking**: Splits documents into 500-character chunks with 50-character overlap
3. **Embedding**: Converts chunks to 384-dimensional vectors using `all-MiniLM-L6-v2`
4. **Indexing**: Stores vectors in FAISS for fast similarity search
5. **Retrieval**: Finds top-3 most relevant chunks for your query

## Features
- Load and chunk documents 
- Generate embeddings 
- Store them in a simple vector database 
- Retrieve and use relevant chunks to answer queries

## Configuration
Edit `config.py` to customize:
- `CHUNK_SIZE`: Size of each chunk (default: 500 characters)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50 characters)
- `TOP_K`: Number of results to retrieve (default: 3)
- `EMBEDDING_MODEL`: Embedding model to use