import logging
import warnings

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

import os
from config import DOCS_PATH, INDEX_PATH
from core.loader import load_documents
from core.splitter import split_documents
from core.vector_store import create_vector_store, load_vector_store
from core.rag_chain import ask


def main():
    if not os.path.exists(INDEX_PATH):
        docs = load_documents(DOCS_PATH)
        chunks = split_documents(docs)
        vector_store = create_vector_store(chunks, INDEX_PATH)
    else:
        vector_store = load_vector_store(INDEX_PATH)

    print("\n🤖 RAG Pipeline ready! Type 'exit' to quit.\n")
    chat_history = []
    while True:
        question = input("Ask a question: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if question:
            result = ask(vector_store, question, chat_history)
            # Update history for next turn
            chat_history.append([question, result["answer"]])


if __name__ == "__main__":
    main()