from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from chatbot.config import OPENAI_API_KEY

def create_rag_chain(vector_store):
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    return qa_chain

def get_answer(qa_chain, question):
    result = qa_chain.invoke({"query": question})
    return result['result']
