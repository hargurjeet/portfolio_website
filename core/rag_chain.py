from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_community.vectorstores import FAISS
from config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE, TOP_K


def build_llm(streaming: bool = False, callbacks: list = []):
    return ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        openai_api_key=OPENAI_API_KEY,
        streaming=streaming,
        callbacks=callbacks
    )


def retrieve_docs(vector_store, question: str):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )
    return retriever.invoke(question)


def build_prompt(question: str, context: str, chat_history: list) -> list:
    """
    Build messages list with system prompt, history, and current question.
    chat_history: list of [human, ai] pairs
    """
    system = """You are a helpful assistant for Hargurjeet Singh Ganger's portfolio chatbot.
Use the context below to answer questions about his experience, skills, and background.
For conversational questions (like "what did I just ask?" or "can you elaborate?"),
use the chat history to respond naturally.
If you cannot answer from either the context or conversation history,
say "I don't have enough information to answer that."

Context from documents:
{context}"""

    messages = [{"role": "system", "content": system.format(context=context)}]

    # Inject prior turns
    for human, ai in chat_history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})

    # Add current question
    messages.append({"role": "user", "content": question})
    return messages


def ask(vector_store, question: str, chat_history: list = []):
    """For terminal use via main.py"""
    docs = retrieve_docs(vector_store, question)
    context = "\n\n".join(doc.page_content for doc in docs)
    messages = build_prompt(question, context, chat_history)

    llm = build_llm()
    response = llm.invoke(messages)

    print(f"\n💬 Answer:\n{response.content}")
    print("\n📄 Sources:")
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        print(f"  [{i+1}] {source} — page {page}")

    return {"answer": response.content, "source_documents": docs}