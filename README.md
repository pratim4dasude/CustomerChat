<h1 align="center">CustomerChat</h1>

<div align="center">



![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=next.js&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-00B5B9?style=flat-square&logo=pinecone&logoColor=white)
![GPT-4](https://img.shields.io/badge/GPT--4-OpenAI-412991?style=flat-square&logo=openai&logoColor=white)

**Contextual IT Support Chatbot powered by RAG, Pinecone, and ChatGPT**

*Get instant, accurate IT support answers from your knowledge base*

[Features](#features) • [Architecture](#architecture) • [Quick Start](#quick-start) • [API Reference](#api-reference) • [Tech Stack](#tech-stack)

</div>

---

## 🎯 Overview

CustomerChat is a full-stack IT support chatbot that provides contextual answers to user queries using **Retrieval-Augmented Generation (RAG)**. It leverages semantic search with **Pinecone** vector database and generates human-like responses using **OpenAI's GPT-4o-mini** model. The system indexes your knowledge base articles into Pinecone vectors, allowing it to find the most relevant content based on semantic similarity rather than just keyword matching. When a user asks a question, the system retrieves the top matching articles and uses them as context for GPT-4 to generate accurate, domain-specific answers. Every response includes sentiment analysis to detect user frustration levels and tracks which knowledge base articles were used, giving transparency into how answers are generated. The modern chat interface built with Next.js provides a seamless experience where users can get instant IT support without waiting for human agents.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Semantic Search** | Pinecone-powered vector similarity search for finding relevant KB articles |
| 🤖 **RAG Pipeline** | Combines retrieval + generation for accurate, context-rich answers |
| 💬 **Session Management** | Persistent chat sessions with conversation history |
| 😊 **Sentiment Analysis** | Real-time detection of user frustration levels (0-1 score) |
| 📚 **Source Tracking** | Shows which KB articles were used for each answer |
| 📝 **Markdown Support** | Beautiful formatted responses with lists, code blocks, and bold text |
| 🔄 **Knowledge Base Indexing** | Admin endpoint to re-index the entire knowledge base |
| 🛡️ **Clean UI** | Modern, responsive chat interface built with Next.js & Tailwind |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                      │
│                                                                 │
│   Landing Page ─────► Chat Interface ─────► Side Panels         │
│   (Hero Section)      (Real-time Chat)     (Sentiment + Sources)│
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend (FastAPI)                       │
│                                                                 │
│   ┌─────────────┐     ┌─────────────┐    ┌─────────────────┐    │
│   │  Sessions   │     │   Messages  │    │      Admin      │    │
│   │   Router    │     │   Router    │    │     Router      │    │
│   └──────┬──────┘     └──────┬──────┘    └────────┬────────     │
│          │                   │                    │             │
│          └───────────────────┼────────────────────┘             │
│                              │                                  │
│   ┌──────────────────────────┼────────────────────────────────┐ │
│   │                     Services Layer                        │ │
│   │                                                           │ │
│   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │ │
│   │   │   OpenAI    │  │   Pinecone  │  │    Sentiment    │   │ │
│   │   │   Service   │  │   Service   │  │     Service     │   │ │
│   │   │  (GPT-4 +   │  │  (Vector    │  │  (Keyword-based │   │ │
│   │   │ Embeddings) │  │   Search)   │  │  Detection)     │   │ │
│   │   └─────────────┘  └─────────────┘  └─────────────────┘   │ │
│   └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
└──────────────────────────────┼──────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │   SQLite    │      │  Pinecone   │      │   OpenAI    │
   │  Database   │      │  Vector DB  │      │    API      │
   └─────────────┘      └─────────────┘      └─────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key
- Pinecone API key

### 1. Clone & Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI and Pinecone API keys
```

### 2. Ingest Knowledge Base

```bash
# Run the ingestion script to index KB articles
python scripts/ingest_kb.py
```

### 3. Start Backend

```bash
# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API docs available at: http://localhost:8000/docs
```

### 4. Setup Frontend

```bash
# New terminal - navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local

# Start development server
npm run dev
```

### 5. Open in Browser

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## 📡 API Reference

### Sessions

#### Create Session
```http
POST /sessions
```
Creates a new chat session.

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": null,
  "created_at": "2024-01-15T10:30:00"
}
```

#### Get Messages
```http
GET /sessions/{session_id}/messages
```
Retrieves all messages for a session.

#### Send Message
```http
POST /sessions/{session_id}/messages
```
**Body:**
```json
{
  "content": "How do I reset my VPN password?"
}
```

**Response:**
```json
{
  "reply": "To reset your VPN password, follow these steps...",
  "sentiment": "neutral",
  "frustration_score": 0.5,
  "sources": [
    {
      "ki_id": "123",
      "title": "VPN Password Reset Guide",
      "category": "vpn",
      "snippet": "To reset your VPN password..."
    }
  ]
}
```

### Admin

#### Reindex Knowledge Base
```http
POST /admin/kb/reindex
```
Re-ingests all KB articles into Pinecone.

#### Get KB Stats
```http
GET /admin/kb/stats
```
Returns database and Pinecone vector counts.

### Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "CustomerChat API",
  "version": "1.0.0"
}
```

---

## 🗄️ Database Schema

### Sessions
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| session_id | String | Unique UUID |
| user_id | String | Optional user identifier |
| created_at | DateTime | Creation timestamp |

### Messages
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| session_id | Integer | FK to sessions |
| role | String | "user" or "assistant" |
| content | Text | Message content |
| sentiment | String | positive/neutral/negative |
| frustration_score | Float | 0-1 scale |
| sources | Text | JSON of used KB articles |
| timestamp | DateTime | Message timestamp |

### KB Items
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| ki_id | String | Unique KB identifier |
| title | String | Article title |
| content | Text | Full article text |
| category | String | Topic category |
| tags | String | Optional tags |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|-------------|---------|
| **FastAPI** | REST API framework |
| **SQLAlchemy** | ORM for SQLite |
| **Pinecone** | Vector database for embeddings |
| **OpenAI** | GPT-4o-mini + text-embeddings-3-small |
| **Uvicorn** | ASGI server |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Next.js 14** | React framework with App Router |
| **TypeScript** | Type safety |
| **Tailwind CSS** | Styling |
| **React Markdown** | Markdown rendering |
| **Lucide Icons** | Icon library |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| **Pinecone** | Vector similarity search |
| **OpenAI API** | LLM + embeddings |
| **SQLite** | Local database |

---

## 📁 Project Structure

```
CustomerChat/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # Environment config
│   │   ├── database.py       # SQLite setup
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── routers/          # API endpoints
│   │   │   ├── sessions.py   # Chat sessions
│   │   │   └── admin.py      # Admin operations
│   │   └── services/         # Business logic
│   │       ├── openai_service.py
│   │       ├── pinecone_service.py
│   │       └── sentiment_service.py
│   ├── scripts/
│   │   └── ingest_kb.py     # KB ingestion script
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx     # Landing page
│   │   │   ├── chat/page.tsx # Chat interface
│   │   │   └── layout.tsx
│   │   ├── components/       # UI components
│   │   ├── lib/             # API client
│   │   └── types/           # TypeScript types
│   ├── package.json
│   └── tailwind.config.ts
└── Dataset/
    └── synthetic_knowledge_items.csv
```

---

## 🔮 How RAG Works

1. **Ingestion**: KB articles are embedded using `text-embedding-3-small` and stored in Pinecone
2. **Query**: User message is embedded with the same model
3. **Retrieval**: Pinecone finds top-5 similar articles using cosine similarity
4. **Generation**: GPT-4o-mini generates answer using:
   - System prompt (role: IT support assistant)
   - Retrieved context (KB articles)
   - Conversation history
   - User message
5. **Response**: Formatted answer returned with sentiment + sources

---

<div align="center">

**Built with ❤️ using FastAPI, Next.js, Pinecone & OpenAI**

</div>
