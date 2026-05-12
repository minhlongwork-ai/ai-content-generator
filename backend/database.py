"""Database connection and session management.

Handles PostgreSQL connection using SQLAlchemy.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from typing import Generator
from dotenv import load_dotenv

from models import Base

load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/ai_content_generator"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Disable connection pooling for serverless
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database - create all tables."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def get_db() -> Generator[Session, None, None]:
    """Get database session (for FastAPI dependency injection).
    
    Usage:
        @app.get("/api/skills")
        async def list_skills(db: Session = Depends(get_db)):
            skills = db.query(Skill).all()
            return skills
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get database session (for standalone use).
    
    Usage:
        with get_db_session() as db:
            skills = db.query(Skill).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_default_skills():
    """Seed database with default skills."""
    from models import Skill
    
    default_skills = [
        {
            'name': 'product-description',
            'description': 'Generate compelling e-commerce product descriptions',
            'category': 'e-commerce',
            'version': '1.0.0',
            'is_premium': False,
            'price': 0.00,
            'author': 'AI Content Generator',
            'tags': ['product', 'description', 'seo', 'e-commerce']
        },
        {
            'name': 'caption-seo',
            'description': 'Generate SEO-optimized titles, captions, and hashtags',
            'category': 'e-commerce',
            'version': '1.0.0',
            'is_premium': False,
            'price': 0.00,
            'author': 'AI Content Generator',
            'tags': ['seo', 'caption', 'title', 'hashtags', 'social-media']
        },
        {
            'name': 'ad-copy',
            'description': 'Generate high-converting ad copy using proven formulas',
            'category': 'marketing',
            'version': '1.0.0',
            'is_premium': False,
            'price': 0.00,
            'author': 'AI Content Generator',
            'tags': ['ad-copy', 'marketing', 'copywriting', 'conversion']
        },
        {
            'name': 'video-script',
            'description': 'Generate engaging video scripts for short-form content',
            'category': 'video-marketing',
            'version': '1.0.0',
            'is_premium': False,
            'price': 0.00,
            'author': 'AI Content Generator',
            'tags': ['video', 'script', 'tiktok', 'reels', 'youtube-shorts']
        }
    ]
    
    with get_db_session() as db:
        for skill_data in default_skills:
            # Check if skill already exists
            existing = db.query(Skill).filter(Skill.name == skill_data['name']).first()
            if not existing:
                skill = Skill(**skill_data)
                db.add(skill)
                print(f"✓ Added skill: {skill_data['name']}")
            else:
                print(f"  Skill already exists: {skill_data['name']}")
        
        db.commit()
    
    print("✓ Default skills seeded")


if __name__ == '__main__':
    """Run this script to initialize database."""
    print("Initializing database...")
    init_db()
    seed_default_skills()
    print("✓ Database initialization complete!")
