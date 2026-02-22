from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE, TOP_K


def build_rag_chain(vector_store):
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        openai_api_key=OPENAI_API_KEY
    )

    prompt_template = """
    You are a helpful assistant. Use the context below to answer the question.
    If you don't know the answer from the context, say "I don't have enough information to answer that."

    Context:
    {context}

    Question: {question}

    Answer:
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return rag_chain


def ask(chain, question: str):
    print(f"\n🔍 Question: {question}")
    result = chain.invoke({"query": question})

    print(f"\n💬 Answer:\n{result['result']}")

    print("\n📄 Sources:")
    for i, doc in enumerate(result["source_documents"]):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        print(f"  [{i+1}] {source} — page {page}")

    return result