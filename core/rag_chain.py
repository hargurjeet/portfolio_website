from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE, TOP_K


def build_rag_chain(vector_store):
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        openai_api_key=OPENAI_API_KEY
    )

    # This prompt explicitly includes chat history so the LLM can answer
    # both document-based AND conversational follow-up questions
    system_template = """
You are a helpful assistant for Hargurjeet Singh Ganger's portfolio chatbot.
You have access to his resume/documents as context below.

Use the context to answer questions about Hargurjeet's experience, skills, and background.
For conversational questions (like "what did I just ask?" or "can you elaborate?"), 
use the chat history to respond naturally.
If you truly cannot answer from either the context or conversation history, 
say "I don't have enough information to answer that."

Chat History:
{chat_history}

Context from documents:
{context}
"""

    human_template = "Question: {question}"

    combine_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ])

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )

    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": combine_prompt}
    )

    return rag_chain


def ask(chain, question: str, chat_history: list = []):
    """
    chat_history: list of (human_message, ai_message) tuples
    """
    print(f"\n🔍 Question: {question}")
    result = chain.invoke({
        "question": question,
        "chat_history": chat_history
    })

    print(f"\n💬 Answer:\n{result['answer']}")

    print("\n📄 Sources:")
    for i, doc in enumerate(result["source_documents"]):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        print(f"  [{i+1}] {source} — page {page}")

    return result