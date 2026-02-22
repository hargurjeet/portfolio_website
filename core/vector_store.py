from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL, EMBEDDING_DEVICE, NORMALIZE_EMBEDDINGS


def _get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": EMBEDDING_DEVICE},
        encode_kwargs={"normalize_embeddings": NORMALIZE_EMBEDDINGS}
    )


def create_vector_store(chunks, save_path: str):
    embeddings = _get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(save_path)
    print(f"✅ Vector store saved to '{save_path}'")
    return vector_store


def load_vector_store(save_path: str):
    embeddings = _get_embeddings()
    vector_store = FAISS.load_local(
        save_path, embeddings, allow_dangerous_deserialization=True
    )
    print(f"✅ Vector store loaded from '{save_path}'")
    return vector_store