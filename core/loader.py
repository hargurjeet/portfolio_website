import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader


def load_documents(path: str):
    """
    Load documents from a file path or a folder.
    Supports .pdf and .txt files.
    """
    if os.path.isdir(path):
        loader = DirectoryLoader(path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    elif path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    elif path.endswith(".txt"):
        loader = TextLoader(path)
    else:
        raise ValueError("Unsupported file type. Use .pdf or .txt")

    documents = loader.load()
    print(f"✅ Loaded {len(documents)} document(s)")
    return documents