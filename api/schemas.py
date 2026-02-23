from pydantic import BaseModel
from typing import List, Tuple


class ChatRequest(BaseModel):
    question: str
    chat_history: List[Tuple[str, str]] = []  # list of (human, ai) tuples


class SourceDocument(BaseModel):
    source: str
    page: int | str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]