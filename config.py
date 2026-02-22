import os
from dotenv import load_dotenv

load_dotenv()

# Paths
DOCS_PATH = "data/Hargurjeet_Lead_GenAI_Specialist.pdf"
INDEX_PATH = "faiss_index"

# Embedding model
EMBEDDING_MODEL = "all-mpnet-base-v2"
EMBEDDING_DEVICE = "cpu"
NORMALIZE_EMBEDDINGS = True

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval
TOP_K = 4

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.3