from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import KBItem
from app.services import openai_service, pinecone_service

router = APIRouter()


@router.post("/admin/kb/reindex")
def reindex_knowledge_base(db: Session = Depends(get_db)):
    try:
        pinecone_service.delete_all()
    except Exception:
        pass
    
    kb_items = db.query(KBItem).all()
    
    if not kb_items:
        return {"message": "No knowledge items found in database", "indexed_count": 0}
    
    vectors = []
    for item in kb_items:
        text_to_embed = f"{item.title}\n\n{item.content}"
        
        embedding = openai_service.get_embedding(text_to_embed)
        
        vectors.append({
            "id": f"kb_{item.ki_id}",
            "values": embedding,
            "metadata": {
                "ki_id": item.ki_id,
                "title": item.title,
                "content": item.content,
                "category": item.category or "General",
                "tags": item.tags or ""
            }
        })
    
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        pinecone_service.upsert_vectors(batch)
    
    return {
        "message": "Knowledge base reindexed successfully",
        "indexed_count": len(vectors)
    }


@router.get("/admin/kb/stats")
def get_kb_stats(db: Session = Depends(get_db)):
    kb_count = db.query(KBItem).count()
    
    try:
        pinecone_stats = pinecone_service.get_stats()
        pinecone_count = pinecone_stats.total_vector_count
    except Exception:
        pinecone_count = "Unable to fetch"
    
    return {
        "database_items": kb_count,
        "pinecone_vectors": pinecone_count
    }
