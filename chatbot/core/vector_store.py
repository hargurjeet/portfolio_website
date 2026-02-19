from langchain_community.vectorstores import FAISS
from chatbot.core.embeddings import get_embeddings

def create_vector_store(chunks):
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def load_vector_store(path):
    embeddings = get_embeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
