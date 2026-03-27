import csv
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from app.database import engine, SessionLocal, Base
from app.models import KBItem
from app.services import openai_service, pinecone_service


def extract_category(title: str) -> str:
    title_lower = title.lower()
    
    categories = {
        "vpn": ["vpn", "virtual private network", "remote access"],
        "email": ["email", "outlook", "mail", "smtp", "imap"],
        "password": ["password", "credentials", "login", "authentication"],
        "network": ["network", "wifi", "wi-fi", "internet", "connection"],
        "hardware": ["laptop", "computer", "printer", "monitor", "keyboard", "mouse", "hardware"],
        "software": ["software", "installation", "install", "update", "app", "application"],
        "account": ["account", "access", "permissions", "user rights", "admin"],
        "security": ["security", "virus", "malware", "antivirus", "firewall"],
        "mobile": ["mobile", "phone", "tablet", "ios", "android"],
        "teams": ["teams", "slack", "zoom", "meeting", "video call"],
    }
    
    for category, keywords in categories.items():
        if any(keyword in title_lower for keyword in keywords):
            return category
    
    return "General"


def ingest_knowledge_base(csv_path: str):
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        existing_count = db.query(KBItem).count()
        print(f"Existing KB items in database: {existing_count}")
        
        if existing_count > 0:
            response = input("Database already has items. Do you want to skip ingestion? (y/n): ")
            if response.lower() == 'y':
                print("Skipping database insertion.")
                kb_items = db.query(KBItem).all()
            else:
                print("Clearing existing data and re-ingesting...")
                db.query(KBItem).delete()
                db.commit()
                kb_items = read_csv(csv_path)
        else:
            kb_items = read_csv(csv_path)
        
        if existing_count == 0 or (existing_count > 0 and response.lower() != 'y'):
            print(f"Inserting {len(kb_items)} items into database...")
            for item_data in kb_items:
                db_item = KBItem(**item_data)
                db.add(db_item)
            
            db.commit()
            print(f"Inserted {len(kb_items)} items into database.")
        
        print("\nGenerating embeddings and indexing to Pinecone...")
        all_items = db.query(KBItem).all()
        
        vectors = []
        for idx, item in enumerate(all_items):
            if idx % 100 == 0:
                print(f"Processing item {idx + 1}/{len(all_items)}...")
            
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
            
            if len(vectors) >= 100:
                pinecone_service.upsert_vectors(vectors)
                vectors = []
        
        if vectors:
            pinecone_service.upsert_vectors(vectors)
        
        print(f"\nSuccessfully indexed {len(all_items)} items to Pinecone!")
        print("Ingestion complete!")
        
    except Exception as e:
        print(f"Error during ingestion: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def read_csv(csv_path: str):
    kb_items = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for idx, row in enumerate(reader):
            title = row.get('ki_topic', '').strip()
            content = row.get('ki_text', '').strip()
            
            if not title or not content:
                continue
            
            category = extract_category(title)
            
            kb_items.append({
                "ki_id": str(idx + 1),
                "title": title,
                "content": content,
                "category": category,
                "tags": ""
            })
    
    return kb_items


if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "Dataset", "synthetic_knowledge_items.csv")
    csv_path = os.path.abspath(csv_path)
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found at: {csv_path}")
        print("Please provide the correct path to the synthetic_knowledge_items.csv file.")
        sys.exit(1)
    
    print(f"Reading from: {csv_path}")
    ingest_knowledge_base(csv_path)
