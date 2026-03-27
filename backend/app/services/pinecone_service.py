from pinecone import Pinecone, ServerlessSpec
from app.config import settings
from typing import List, Dict, Any, Optional
import time


class PineconeService:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = settings.pinecone_index_name
        self._ensure_index_exists()

    def _ensure_index_exists(self):
        existing_indexes = [idx.name for idx in self.pc.list_indexes()]
        
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            time.sleep(5)

    def get_index(self):
        return self.pc.Index(self.index_name)

    def upsert_vectors(
        self,
        vectors: List[Dict[str, Any]]
    ):
        index = self.get_index()
        index.upsert(vectors=vectors)

    def query(
        self,
        vector: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        index = self.get_index()
        
        query_response = index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict
        )
        
        results = []
        for match in query_response.matches:
            results.append({
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            })
        
        return results

    def delete_all(self):
        index = self.get_index()
        index.delete(delete_all=True)

    def get_stats(self):
        index = self.get_index()
        return index.describe_index_stats()


pinecone_service = PineconeService()
