import logging
import warnings

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

import os
from config import DOCS_PATH, INDEX_PATH
from core.loader import load_documents
from core.splitter import split_documents
from core.vector_store import create_vector_store, load_vector_store
from core.rag_chain import build_rag_chain, ask


def main():
    # Build index if it doesn't exist, otherwise load from disk
    if not os.path.exists(INDEX_PATH):
        docs = load_documents(DOCS_PATH)
        chunks = split_documents(docs)
        vector_store = create_vector_store(chunks, INDEX_PATH)
    else:
        vector_store = load_vector_store(INDEX_PATH)

    chain = build_rag_chain(vector_store)

    print("\n🤖 RAG Pipeline ready! Type 'exit' to quit.\n")
    while True:
        question = input("Ask a question: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if question:
            ask(chain, question)


if __name__ == "__main__":
    main()