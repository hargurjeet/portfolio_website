from fastapi import APIRouter, HTTPException
from api.schemas import ChatRequest, ChatResponse, SourceDocument
from core.vector_store import load_vector_store
from core.rag_chain import build_rag_chain
from config import INDEX_PATH

router = APIRouter()

# Load vector store and chain once at startup
try:
    _vector_store = load_vector_store(INDEX_PATH)
    _chain = build_rag_chain(_vector_store)
except Exception as e:
    _chain = None
    print(f"⚠️  Could not load vector store: {e}")


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if _chain is None:
        raise HTTPException(
            status_code=503,
            detail="Vector store not loaded. Run main.py first to build the index."
        )

    result = _chain.invoke({
        "question": request.question,
        "chat_history": request.chat_history  # list of (human, ai) tuples
    })

    sources = [
        SourceDocument(
            source=doc.metadata.get("source", "Unknown"),
            page=doc.metadata.get("page", "?")
        )
        for doc in result["source_documents"]
    ]

    return ChatResponse(answer=result["answer"], sources=sources)