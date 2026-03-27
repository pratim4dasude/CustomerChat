from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import sessions_router, admin_router
from app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CustomerChat API",
    description="IT Support Chatbot powered by RAG, Pinecone, and ChatGPT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router, tags=["sessions"])
app.include_router(admin_router, tags=["admin"])


@app.get("/")
def root():
    return {
        "name": "CustomerChat API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CustomerChat API",
        "version": "1.0.0",
        "message": "Backend is running and ready to accept requests"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
