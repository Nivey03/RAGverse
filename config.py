
import os
from dotenv import load_dotenv

load_dotenv()

# CHUNKING SETTINGS
CHUNK_SIZE = 500        # Maximum characters per chunk
CHUNK_OVERLAP = 50      # Characters that overlap between chunks (for context continuity)


# EMBEDDING MODEL SETTINGS
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384  # This model produces 384-dimensional vectors


# RETRIEVAL SETTINGS
TOP_K = 3


# LLM SETTINGS
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GENERATION_MODEL = "gemini-2.0-flash"
# Where documents are stored
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "documents")

# Where vector database is saved
VECTOR_DB_PATH = os.path.join(os.path.dirname(__file__), "database", "vector_db")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(VECTOR_DB_PATH), exist_ok=True)