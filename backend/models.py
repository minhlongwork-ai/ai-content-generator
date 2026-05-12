"""Database models for AI Content Generator.

SQLAlchemy models for skill system tables and marketplace.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, JSON, UniqueConstraint, Index, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Skill(Base):
    """Skills table - stores available content generation skills."""
    
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50), index=True)
    version = Column(String(20), default='1.0.0')
    is_premium = Column(Boolean, default=False, index=True)
    price = Column(DECIMAL(10, 2), default=0.00)
    author = Column(String(100))
    tags = Column(JSON)
    skill_metadata = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'version': self.version,
            'is_premium': self.is_premium,
            'price': float(self.price) if self.price else 0.00,
            'author': self.author,
            'tags': self.tags or [],
            'metadata': self.skill_metadata or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class SkillListing(Base):
    """Marketplace listings for skills."""
    
    __tablename__ = 'skill_listings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String(100), ForeignKey('skills.name'), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    short_desc = Column(Text)
    long_desc = Column(Text)
    cover_image_url = Column(Text)
    cover_emoji = Column(String(20))
    price = Column(DECIMAL(10, 2), default=0.00)
    currency = Column(String(10), default='USD')
    category = Column(String(50), index=True)
    tags = Column(JSON)
    author_id = Column(Integer)
    author_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False, index=True)
    total_sales = Column(Integer, default=0)
    avg_rating = Column(DECIMAL(3, 2), default=0.00)
    rating_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class SkillReview(Base):
    """User reviews for marketplace skills."""
    
    __tablename__ = 'skill_reviews'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String(100), ForeignKey('skills.name'), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    rating = Column(Integer, nullable=False) # 1-5
    title = Column(String(200))
    body = Column(Text)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint('skill_name', 'user_id', name='uq_skill_user_review'),
    )


class SkillInstall(Base):
    """Tracks which skills a user has installed."""
    
    __tablename__ = 'skill_installs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    skill_name = Column(String(100), ForeignKey('skills.name'), nullable=False)
    purchase_id = Column(Integer)
    installed_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'skill_name', name='uq_user_skill_install'),
    )


class UserSkillConfig(Base):
    """User skill configs - stores per-user customizations."""
    
    __tablename__ = 'user_skill_configs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    config = Column(JSON, nullable=False, default={})
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint('user_id', 'skill_name', name='uq_user_skill'),
    )


class Generation(Base):
    """Generations - stores generation history with quality scores."""
    
    __tablename__ = 'generations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    input_params = Column(JSON, nullable=False)
    output_content = Column(JSON, nullable=False)
    quality_score = Column(JSON)
    model_used = Column(String(100))
    backend = Column(String(50))
    tokens_used = Column(Integer)
    duration_ms = Column(Integer)
    created_at = Column(DateTime, default=func.now(), index=True)


class SkillPurchase(Base):
    """Skill purchases - stores marketplace transactions."""
    
    __tablename__ = 'skill_purchases'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50))
    transaction_id = Column(String(100))
    status = Column(String(20), default='completed')
    purchased_at = Column(DateTime, default=func.now(), index=True)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'skill_name', name='uq_user_skill_purchase'),
    )


class SkillAnalytics(Base):
    """Skill analytics - tracks usage events."""
    
    __tablename__ = 'skill_analytics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String(100), nullable=False, index=True)
    user_id = Column(Integer)
    event_type = Column(String(50), nullable=False, index=True)
    analytics_metadata = Column(JSON)
    created_at = Column(DateTime, default=func.now(), index=True)
