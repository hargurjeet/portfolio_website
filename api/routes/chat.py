import json
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from core.vector_store import load_vector_store
from core.rag_chain import build_llm, retrieve_docs, build_prompt
from api.schemas import ChatRequest
from config import INDEX_PATH

router = APIRouter()

try:
    _vector_store = load_vector_store(INDEX_PATH)
except Exception as e:
    _vector_store = None
    print(f"⚠️  Could not load vector store: {e}")


@router.post("/chat")
async def chat(request: ChatRequest):
    if _vector_store is None:
        raise HTTPException(
            status_code=503,
            detail="Vector store not loaded. Run main.py first to build the index."
        )

    async def stream():
        # 1. Retrieve relevant docs (fast, non-streaming)
        docs = retrieve_docs(_vector_store, request.question)
        context = "\n\n".join(doc.page_content for doc in docs)

        # 2. Build messages with full history
        messages = build_prompt(request.question, context, request.chat_history)

        # 3. Stream LLM response token by token
        callback = AsyncIteratorCallbackHandler()
        llm = build_llm(streaming=True, callbacks=[callback])

        task = asyncio.create_task(llm.ainvoke(messages))

        async for token in callback.aiter():
            yield f"data: {json.dumps({'token': token})}\n\n"

        await task  # ensure completion before sending sources

        # 4. Send sources at the end
        sources = [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "?")
            }
            for doc in docs
        ]
        yield f"data: {json.dumps({'sources': sources})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")