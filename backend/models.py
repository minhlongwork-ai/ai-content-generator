"""Database models for AI Content Generator.

SQLAlchemy models for skill system tables.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, TIMESTAMP, JSON, ARRAY, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
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
    tags = Column(ARRAY(Text))
    metadata = Column(JSON)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        """Convert to dictionary."""
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
            'metadata': self.metadata or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserSkillConfig(Base):
    """User skill configs - stores per-user customizations."""
    
    __tablename__ = 'user_skill_configs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    config = Column(JSON, nullable=False, default={})
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint('user_id', 'skill_name', name='uq_user_skill'),
        Index('idx_user_skill_configs_user_id', 'user_id'),
        Index('idx_user_skill_configs_skill_name', 'skill_name'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_name': self.skill_name,
            'config': self.config or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


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
    created_at = Column(TIMESTAMP, default=func.now(), index=True)
    
    __table_args__ = (
        Index('idx_generations_user_id', 'user_id'),
        Index('idx_generations_skill_name', 'skill_name'),
        Index('idx_generations_created_at', 'created_at'),
        Index('idx_generations_user_skill', 'user_id', 'skill_name'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_name': self.skill_name,
            'input_params': self.input_params or {},
            'output_content': self.output_content or {},
            'quality_score': self.quality_score or {},
            'model_used': self.model_used,
            'backend': self.backend,
            'tokens_used': self.tokens_used,
            'duration_ms': self.duration_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


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
    purchased_at = Column(TIMESTAMP, default=func.now(), index=True)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'skill_name', name='uq_user_skill_purchase'),
        Index('idx_skill_purchases_user_id', 'user_id'),
        Index('idx_skill_purchases_skill_name', 'skill_name'),
        Index('idx_skill_purchases_purchased_at', 'purchased_at'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_name': self.skill_name,
            'price': float(self.price) if self.price else 0.00,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'purchased_at': self.purchased_at.isoformat() if self.purchased_at else None
        }


class SkillAnalytics(Base):
    """Skill analytics - tracks usage events."""
    
    __tablename__ = 'skill_analytics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String(100), nullable=False, index=True)
    user_id = Column(Integer)
    event_type = Column(String(50), nullable=False, index=True)  # 'view', 'generate', 'purchase', 'config_update'
    metadata = Column(JSON)
    created_at = Column(TIMESTAMP, default=func.now(), index=True)
    
    __table_args__ = (
        Index('idx_skill_analytics_skill_name', 'skill_name'),
        Index('idx_skill_analytics_event_type', 'event_type'),
        Index('idx_skill_analytics_created_at', 'created_at'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'metadata': self.metadata or {},
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
