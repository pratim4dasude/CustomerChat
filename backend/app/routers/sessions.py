import uuid
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Session as SessionModel, Message as MessageModel, KBItem
from app.schemas import (
    SessionCreate, SessionResponse, MessageCreate, MessageResponse,
    ChatResponse, MessageListResponse, SourceItem
)
from app.services import openai_service, pinecone_service, detect_sentiment

router = APIRouter()


@router.post("/sessions", response_model=SessionResponse)
def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    
    db_session = SessionModel(
        session_id=session_id,
        user_id=session_data.user_id
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return db_session


@router.get("/sessions/{session_id}/messages", response_model=MessageListResponse)
def get_messages(session_id: str, db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = db.query(MessageModel).filter(
        MessageModel.session_id == db_session.id
    ).order_by(MessageModel.timestamp).all()
    
    message_responses = []
    for msg in messages:
        sources = None
        if msg.sources:
            try:
                sources = json.loads(msg.sources)
            except json.JSONDecodeError:
                sources = None
        
        message_responses.append(MessageResponse(
            id=msg.id,
            session_id=msg.session_id,
            role=msg.role,
            content=msg.content,
            sentiment=msg.sentiment,
            frustration_score=msg.frustration_score,
            sources=sources,
            timestamp=msg.timestamp
        ))
    
    return MessageListResponse(messages=message_responses)


@router.post("/sessions/{session_id}/messages", response_model=ChatResponse)
def create_message(session_id: str, message_data: MessageCreate, db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    sentiment, frustration_score = detect_sentiment(message_data.content)
    
    db_message = MessageModel(
        session_id=db_session.id,
        role="user",
        content=message_data.content,
        sentiment=sentiment,
        frustration_score=frustration_score
    )
    db.add(db_message)
    db.commit()
    
    conversation_history = []
    all_messages = db.query(MessageModel).filter(
        MessageModel.session_id == db_session.id
    ).order_by(MessageModel.timestamp).all()
    
    for msg in all_messages[:-1]:
        conversation_history.append({
            "role": msg.role,
            "content": msg.content
        })
    
    user_embedding = openai_service.get_embedding(message_data.content)
    
    pinecone_results = pinecone_service.query(vector=user_embedding, top_k=5)
    
    context_items = []
    sources_list = []
    
    for result in pinecone_results:
        metadata = result.get("metadata", {})
        ki_id = metadata.get("ki_id", result["id"])
        
        db_item = db.query(KBItem).filter(KBItem.ki_id == ki_id).first()
        
        item_content = db_item.content if db_item else metadata.get("content", "")
        item_title = db_item.title if db_item else metadata.get("title", "Untitled")
        item_category = db_item.category if db_item else metadata.get("category", "General")
        
        context_items.append({
            "ki_id": ki_id,
            "title": item_title,
            "content": item_content,
            "category": item_category
        })
        
        snippet = item_content[:200] + "..." if len(item_content) > 200 else item_content
        sources_list.append(SourceItem(
            ki_id=ki_id,
            title=item_title,
            category=item_category,
            snippet=snippet
        ))
    
    assistant_reply = openai_service.generate_chat_response(
        user_message=message_data.content,
        context_items=context_items,
        conversation_history=conversation_history
    )
    
    db_assistant_message = MessageModel(
        session_id=db_session.id,
        role="assistant",
        content=assistant_reply,
        sentiment=sentiment,
        frustration_score=frustration_score,
        sources=json.dumps([s.model_dump() for s in sources_list])
    )
    db.add(db_assistant_message)
    db.commit()
    
    return ChatResponse(
        reply=assistant_reply,
        sentiment=sentiment,
        frustration_score=frustration_score,
        sources=sources_list
    )
