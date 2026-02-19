import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
VECTOR_STORE_PATH = 'data/processed/vector_store'
RESUME_PATH = 'data/resume.pdf'
