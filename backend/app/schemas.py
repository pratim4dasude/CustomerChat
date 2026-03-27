from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SessionCreate(BaseModel):
    user_id: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    user_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str
    user_id: Optional[str] = None


class SourceItem(BaseModel):
    ki_id: str
    title: str
    category: Optional[str]
    snippet: Optional[str] = None


class MessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    sentiment: Optional[str] = None
    frustration_score: Optional[float] = None
    sources: Optional[List[SourceItem]] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    reply: str
    sentiment: str
    frustration_score: float
    sources: List[SourceItem]


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]
