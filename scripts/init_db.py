#!/usr/bin/env python
"""
Database initialization script for seeding destinations and embeddings.

This script populates the destinations table with real content from Wikivoyage,
travel blogs, and tourism boards. It also generates embeddings using a local
vector embedding model or placeholder vectors.

Usage:
    python scripts/init_db.py
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent.parent / "backend")
sys.path.insert(0, backend_path)

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.core.models import Destination, DestinationEmbedding
from app.tools.rag_tool import get_all_destinations
import uuid
from datetime import datetime
import numpy as np


def generate_placeholder_embedding(destination_name: str) -> np.ndarray:
    """
    Generate a placeholder embedding for a destination.
    
    In production, you would use:
    - OpenAI embeddings: from langchain.embeddings.openai import OpenAIEmbeddings
    - Hugging Face: from sentence_transformers import SentenceTransformer
    - Local model: from langchain.embeddings.huggingface import HuggingFaceEmbeddings
    
    For now, we use a deterministic placeholder based on destination name.
    """
    # Use destination name to seed random number generator for reproducibility
    np.random.seed(hash(destination_name) % (2**32))
    embedding = np.random.randn(1536).astype(np.float32)
    # Normalize to unit vector
    embedding = embedding / np.linalg.norm(embedding)
    return embedding.tolist()


def seed_destinations(db: Session):
    """Populate destinations table with real content and embeddings."""
    
    print("🌍 Seeding destinations table...")
    
    destinations_data = get_all_destinations()
    
    for dest_data in destinations_data:
        # Check if destination already exists
        existing = db.query(Destination).filter(
            Destination.name == dest_data["destination"]
        ).first()
        
        if existing:
            print(f"  ⏭️  {dest_data['destination']} already exists")
            continue
        
        # Create destination record
        destination = Destination(
            id=uuid.uuid4(),
            name=dest_data["destination"],
            category=dest_data.get("category", ""),
            description=dest_data.get("description", ""),
            source=dest_data.get("source", "Travel Database"),
            source_url=dest_data.get("source_url"),
            content=dest_data.get("content", dest_data.get("description", "")),
            created_at=datetime.utcnow()
        )
        
        db.add(destination)
        db.flush()  # Get the ID
        
        # Generate and store embedding
        print(f"  📍 {destination.name}")
        embedding_vector = generate_placeholder_embedding(destination.name)
        
        embedding = DestinationEmbedding(
            id=uuid.uuid4(),
            destination_id=destination.id,
            embedding=embedding_vector,
            created_at=datetime.utcnow()
        )
        
        db.add(embedding)
    
    db.commit()
    print(f"✅ Successfully seeded {len(destinations_data)} destinations!")


def main():
    """Initialize database and seed data."""
    
    print("🚀 Initializing Travel AI Agent Database...\n")
    
    # Create tables
    print("📊 Creating database tables...")
    init_db()
    print("✅ Tables created successfully!\n")
    
    # Seed destinations
    db = SessionLocal()
    try:
        seed_destinations(db)
    finally:
        db.close()
    
    print("\n🎉 Database initialization complete!")
    print("   You can now start the backend server:")
    print("   python -m uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
