# app/models.py
import hashlib
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict


class DocumentModel(BaseModel):
    page_content: str
    metadata: Optional[dict] = {}

    def generate_digest(self):
        hash_obj = hashlib.md5(self.page_content.encode())
        return hash_obj.hexdigest()


class StoreDocument(BaseModel):
    filepath: str
    filename: str
    file_content_type: str
    file_id: str


class QueryRequestBody(BaseModel):
    query: str
    file_id: str
    k: int = 4
    entity_id: Optional[str] = None


class CleanupMethod(str, Enum):
    incremental = "incremental"
    full = "full"


class QueryMultipleBody(BaseModel):
    query: str
    file_ids: List[str]
    k: int = 4


class ChatRequest(BaseModel):
    query: str
    file_id: str
    model: str = "azure-gpt4o-mini"
    k: int = 4
    temperature: float = 0.7
    entity_id: Optional[str] = None


class SourceDocument(BaseModel):
    content: str
    score: float
    metadata: Optional[dict] = {}


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    model_used: str


class SimpleChatResponse(BaseModel):
    """Simplified response with only the answer text - no sources or metadata"""
    answer: str