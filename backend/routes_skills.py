"""API routes for skill system.

Endpoints for managing skills, configs, and generations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from database import get_db
from models import Skill, UserSkillConfig, Generation, SkillPurchase, SkillAnalytics
from skills.skill_loader import list_skills as load_available_skills, load_skill

router = APIRouter(prefix="/api/skills", tags=["Skills"])


# ============================================================================
# Request/Response Models
# ============================================================================

class SkillResponse(BaseModel):
    """Skill response model."""
    id: int
    name: str
    description: str
    category: str
    version: str
    is_premium: bool
    price: float
    author: Optional[str]
    tags: List[str]
    created_at: str
    updated_at: str


class SkillConfigRequest(BaseModel):
    """Skill config update request."""
    config: dict = Field(..., description="Skill configuration overrides")


class SkillConfigResponse(BaseModel):
    """Skill config response."""
    id: int
    user_id: int
    skill_name: str
    config: dict
    created_at: str
    updated_at: str


class GenerateWithSkillRequest(BaseModel):
    """Generate content with skill request."""
    skill_name: str = Field(..., description="Skill name")
    params: dict = Field(..., description="Input parameters")
    user_config: Optional[dict] = Field(None, description="Optional config overrides")


class GenerationResponse(BaseModel):
    """Generation response."""
    id: int
    user_id: int
    skill_name: str
    input_params: dict
    output_content: dict
    quality_score: dict
    model_used: Optional[str]
    backend: Optional[str]
    created_at: str


# ============================================================================
# Skill Endpoints
# ============================================================================

@router.get("/", response_model=List[SkillResponse])
async def list_skills(
    category: Optional[str] = Query(None, description="Filter by category"),
    is_premium: Optional[bool] = Query(None, description="Filter by premium status"),
    db: Session = Depends(get_db)
):
    """List all available skills.
    
    Returns skills from database with optional filters.
    """
    query = db.query(Skill)
    
    if category:
        query = query.filter(Skill.category == category)
    
    if is_premium is not None:
        query = query.filter(Skill.is_premium == is_premium)
    
    skills = query.all()
    
    # Track analytics
    for skill in skills:
        analytics = SkillAnalytics(
            skill_name=skill.name,
            event_type='view',
            metadata={'source': 'list_endpoint'}
        )
        db.add(analytics)
    
    db.commit()
    
    return [
        SkillResponse(
            id=s.id,
            name=s.name,
            description=s.description or '',
            category=s.category or '',
            version=s.version or '1.0.0',
            is_premium=s.is_premium or False,
            price=float(s.price) if s.price else 0.00,
            author=s.author,
            tags=s.tags or [],
            created_at=s.created_at.isoformat() if s.created_at else '',
            updated_at=s.updated_at.isoformat() if s.updated_at else ''
        )
        for s in skills
    ]


@router.get("/{skill_name}")
async def get_skill_details(
    skill_name: str,
    db: Session = Depends(get_db)
):
    """Get detailed information about a skill.
    
    Returns skill metadata from database + runtime metadata from skill loader.
    """
    # Get from database
    skill_db = db.query(Skill).filter(Skill.name == skill_name).first()
    if not skill_db:
        raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")
    
    # Get runtime metadata
    skill_instance = load_skill(skill_name)
    if not skill_instance:
        raise HTTPException(status_code=404, detail=f"Skill implementation not found: {skill_name}")
    
    skill_metadata = skill_instance.get_skill_metadata()
    default_config = skill_instance.get_default_config()
    
    # Track analytics
    analytics = SkillAnalytics(
        skill_name=skill_name,
        event_type='view',
        metadata={'source': 'detail_endpoint'}
    )
    db.add(analytics)
    db.commit()
    
    return {
        'id': skill_db.id,
        'name': skill_db.name,
        'description': skill_db.description,
        'category': skill_db.category,
        'version': skill_db.version,
        'is_premium': skill_db.is_premium,
        'price': float(skill_db.price) if skill_db.price else 0.00,
        'author': skill_db.author,
        'tags': skill_db.tags or [],
        'metadata': skill_metadata,
        'default_config': default_config,
        'created_at': skill_db.created_at.isoformat() if skill_db.created_at else None,
        'updated_at': skill_db.updated_at.isoformat() if skill_db.updated_at else None
    }


# ============================================================================
# Skill Config Endpoints
# ============================================================================

@router.get("/{skill_name}/config")
async def get_skill_config(
    skill_name: str,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get user's config for a skill.
    
    Returns user's custom config or default config if not customized.
    """
    # Check if skill exists
    skill_db = db.query(Skill).filter(Skill.name == skill_name).first()
    if not skill_db:
        raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")
    
    # Get user config
    user_config = db.query(UserSkillConfig).filter(
        UserSkillConfig.user_id == user_id,
        UserSkillConfig.skill_name == skill_name
    ).first()
    
    if user_config:
        return {
            'skill_name': skill_name,
            'config': user_config.config,
            'is_customized': True,
            'updated_at': user_config.updated_at.isoformat() if user_config.updated_at else None
        }
    else:
        # Return default config
        skill_instance = load_skill(skill_name)
        if not skill_instance:
            raise HTTPException(status_code=404, detail=f"Skill implementation not found: {skill_name}")
        
        return {
            'skill_name': skill_name,
            'config': skill_instance.get_default_config(),
            'is_customized': False,
            'updated_at': None
        }


@router.post("/{skill_name}/config")
async def update_skill_config(
    skill_name: str,
    user_id: int = Query(..., description="User ID"),
    request: SkillConfigRequest = None,
    db: Session = Depends(get_db)
):
    """Update user's config for a skill.
    
    Creates or updates user's custom configuration.
    """
    # Check if skill exists
    skill_db = db.query(Skill).filter(Skill.name == skill_name).first()
    if not skill_db:
        raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")
    
    # Get or create user config
    user_config = db.query(UserSkillConfig).filter(
        UserSkillConfig.user_id == user_id,
        UserSkillConfig.skill_name == skill_name
    ).first()
    
    if user_config:
        # Update existing
        user_config.config = request.config
        user_config.updated_at = datetime.utcnow()
    else:
        # Create new
        user_config = UserSkillConfig(
            user_id=user_id,
            skill_name=skill_name,
            config=request.config
        )
        db.add(user_config)
    
    # Track analytics
    analytics = SkillAnalytics(
        skill_name=skill_name,
        user_id=user_id,
        event_type='config_update',
        metadata={'config': request.config}
    )
    db.add(analytics)
    
    db.commit()
    db.refresh(user_config)
    
    return {
        'success': True,
        'skill_name': skill_name,
        'config': user_config.config,
        'updated_at': user_config.updated_at.isoformat() if user_config.updated_at else None
    }


# ============================================================================
# Generation Endpoints
# ============================================================================

@router.post("/{skill_name}/generate")
async def generate_with_skill(
    skill_name: str,
    user_id: int = Query(..., description="User ID"),
    request: dict = None,
    db: Session = Depends(get_db)
):
    """Generate content using a skill.
    
    This is the main generation endpoint that uses the skill system.
    """
    from ai_client import AIClient
    import time
    
    # Check if skill exists
    skill_db = db.query(Skill).filter(Skill.name == skill_name).first()
    if not skill_db:
        raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")
    
    # Get user config if exists
    user_config_db = db.query(UserSkillConfig).filter(
        UserSkillConfig.user_id == user_id,
        UserSkillConfig.skill_name == skill_name
    ).first()
    
    user_config = user_config_db.config if user_config_db else None
    
    # Extract params from request
    params = request.get('params', {})
    user_config_override = request.get('user_config', user_config)
    
    # Generate content
    client = AIClient()
    start_time = time.time()
    
    result = await client.generate_with_skill(
        skill_name=skill_name,
        params=params,
        user_config=user_config_override
    )
    
    duration_ms = int((time.time() - start_time) * 1000)
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result.get('error', 'Generation failed'))
    
    # Save to database
    generation = Generation(
        user_id=user_id,
        skill_name=skill_name,
        input_params=params,
        output_content=result['content'],
        quality_score=result.get('quality_report', {}),
        model_used=result.get('model'),
        backend=result.get('backend'),
        duration_ms=duration_ms
    )
    db.add(generation)
    
    # Track analytics
    analytics = SkillAnalytics(
        skill_name=skill_name,
        user_id=user_id,
        event_type='generate',
        metadata={
            'quality_score': result.get('quality_report', {}).get('score'),
            'duration_ms': duration_ms
        }
    )
    db.add(analytics)
    
    db.commit()
    db.refresh(generation)
    
    return {
        'success': True,
        'generation_id': generation.id,
        'content': result['content'],
        'quality_report': result.get('quality_report'),
        'model': result.get('model'),
        'backend': result.get('backend'),
        'duration_ms': duration_ms
    }


@router.get("/generations/history")
async def get_generation_history(
    user_id: int = Query(..., description="User ID"),
    skill_name: Optional[str] = Query(None, description="Filter by skill"),
    limit: int = Query(10, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """Get user's generation history.
    
    Returns paginated list of past generations.
    """
    query = db.query(Generation).filter(Generation.user_id == user_id)
    
    if skill_name:
        query = query.filter(Generation.skill_name == skill_name)
    
    total = query.count()
    generations = query.order_by(Generation.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        'total': total,
        'limit': limit,
        'offset': offset,
        'generations': [
            {
                'id': g.id,
                'skill_name': g.skill_name,
                'quality_score': g.quality_score.get('score') if g.quality_score else None,
                'model_used': g.model_used,
                'created_at': g.created_at.isoformat() if g.created_at else None
            }
            for g in generations
        ]
    }


@router.get("/generations/{generation_id}")
async def get_generation_details(
    generation_id: int,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific generation."""
    generation = db.query(Generation).filter(
        Generation.id == generation_id,
        Generation.user_id == user_id
    ).first()
    
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    
    return generation.to_dict()
