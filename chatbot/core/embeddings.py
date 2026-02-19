from langchain_openai import OpenAIEmbeddings
from chatbot.config import OPENAI_API_KEY

def get_embeddings():
    return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
