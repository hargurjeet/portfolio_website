from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    question: str


class SourceDocument(BaseModel):
    source: str
    page: int | str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]