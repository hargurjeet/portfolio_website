from fastapi import FastAPI
from api.routes.chat import router as chat_router

app = FastAPI(
    title="RAG Chatbot API",
    description="Ask questions against your documents",
    version="1.0.0"
)

app.include_router(chat_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}