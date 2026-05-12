"""FastAPI backend for AI Content Generator."""

import os
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal
from dotenv import load_dotenv
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ai_client import AIClient

load_dotenv()

app = FastAPI(
    title="AI Content Generator",
    description="Generate e-commerce content with AI — text + video + audio",
    version="2.1.0"
)

# Import and include skill routes
try:
    from routes_skills import router as skills_router
    app.include_router(skills_router)
    logger.info("✓ Skill routes loaded")
except Exception as e:
    logger.warning(f"⚠ Skill routes not loaded: {e}")


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"status": "ok", "service": "ai-content-generator-api", "version": "2.0.0"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Request Models ───────────────────────────────────────

class ProductDescriptionRequest(BaseModel):
    product_name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    features: str = Field(..., description="Key features (comma-separated)")
    target_audience: str = Field(default="general", description="Target audience")
    language: str = Field(default="English", description="Output language")
    tone: str = Field(default="professional", description="Tone of voice")


class CaptionSEORequest(BaseModel):
    product_name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    features: str = Field(..., description="Key features (comma-separated)")
    platform: str = Field(default="shopee", description="Platform (shopee, lazada, amazon, etc.)")
    language: str = Field(default="English", description="Output language")


class AdCopyRequest(BaseModel):
    product_name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    selling_points: str = Field(..., description="Key selling points (comma-separated)")
    target_audience: str = Field(default="general", description="Target audience")
    platform: str = Field(default="facebook", description="Ad platform")
    language: str = Field(default="English", description="Output language")
    tone: str = Field(default="persuasive", description="Tone of voice")


class VideoScriptRequest(BaseModel):
    """Request model for video script generation."""
    product_name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    features: str = Field(..., description="Key features (comma-separated)")
    target_audience: str = Field(default="general", description="Target audience")
    platform: str = Field(default="tiktok", description="Platform (tiktok, reels, shorts)")
    language: str = Field(default="Vietnamese", description="Output language")
    tone: str = Field(default="engaging", description="Tone of voice")
    duration: int = Field(default=30, ge=15, le=120, description="Video duration in seconds (15-120)")
    n_scenes: int = Field(default=4, ge=2, le=10, description="Number of scenes (2-10)")
    
    # TTS options
    generate_audio: bool = Field(default=True, description="Generate TTS audio for the script")
    voice_language: str = Field(default="vi", description="TTS voice language (vi, en, zh, ja, ko)")
    voice_gender: str = Field(default="female", description="TTS voice gender (female, male)")
    tts_speed: float = Field(default=1.0, ge=0.5, le=2.0, description="TTS speed (0.5-2.0)")


# ─── Endpoints ─────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "app": "AI Content Generator",
        "version": "2.0.0",
        "endpoints": [
            "/api/generate/product-description",
            "/api/generate/caption-seo",
            "/api/generate/ad-copy",
            "/api/generate/video-script",
            "/api/audio/{filename}",
            "/api/health"
        ]
    }


@app.get("/api/health")
async def health():
    client = AIClient()
    result = await client.health_check()
    return result


# ─── Auth Helper ─────────────────────────────────────────────

async def get_user_api_key(authorization: str = Header(None)) -> tuple:
    """Extract user API key from JWT token. Returns (api_key, user_email, error)."""
    if not authorization or not authorization.startswith("Bearer "):
        return None, None, None  # No auth = use env key

    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        return None, None, "Invalid or expired token"

    user = get_user_by_id(payload["sub"])
    if not user:
        return None, None, "User not found"

    # Get user's API key from their profile (per-user keys)
    email = user.get("email", "")
    user_keys = get_user_api_keys(email)
    api_key = user_keys.get("OPENROUTER_API_KEY", "")

    return api_key, email, None


# ─── Generate Endpoints ──────────────────────────────────────

@app.post("/api/generate/product-description")
async def generate_product_description(
    request: ProductDescriptionRequest,
    authorization: str = Header(None)
):
    """Generate product description. Uses user's API key if authenticated."""
    api_key, email, err = await get_user_api_key(authorization)
    if err:
        raise HTTPException(status_code=401, detail=err)

    client = AIClient(user_api_key=api_key)
    logger.info(f"Product description request: {request.product_name} (user={email or 'anonymous'})")

    result = await client.generate(
        content_type="product_description",
        product_name=request.product_name,
        category=request.category,
        features=request.features,
        target_audience=request.target_audience,
        language=request.language,
        tone=request.tone
    )

    if not result["success"]:
        logger.error(f"Generation failed: {result['error']}")
        raise HTTPException(status_code=500, detail=result["error"])

    # Track generation for logged-in users
    if email:
        increment_generation(email)

    logger.info(f"Success: model={result.get('model')}")
    return result


@app.post("/api/generate/caption-seo")
async def generate_caption_seo(request: CaptionSEORequest, authorization: str = Header(None)):
    """Generate SEO caption and title. Uses user's API key if authenticated."""
    api_key, email, err = await get_user_api_key(authorization)
    if err:
        raise HTTPException(status_code=401, detail=err)

    client = AIClient(user_api_key=api_key)
    result = await client.generate(
        content_type="caption_seo",
        product_name=request.product_name,
        category=request.category,
        features=request.features,
        platform=request.platform,
        language=request.language
    )

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])

    if email:
        increment_generation(email)
    return result


@app.post("/api/generate/ad-copy")
async def generate_ad_copy(request: AdCopyRequest, authorization: str = Header(None)):
    """Generate ad copy variations. Uses user's API key if authenticated."""
    api_key, email, err = await get_user_api_key(authorization)
    if err:
        raise HTTPException(status_code=401, detail=err)

    client = AIClient(user_api_key=api_key)
    result = await client.generate(
        content_type="ad_copy",
        product_name=request.product_name,
        category=request.category,
        selling_points=request.selling_points,
        target_audience=request.target_audience,
        platform=request.platform,
        language=request.language,
        tone=request.tone
    )

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])

    if email:
        increment_generation(email)
    return result


@app.post("/api/generate/video-script")
async def generate_video_script(request: VideoScriptRequest, authorization: str = Header(None)):
    """Generate video script with optional TTS audio. Uses user's API key if authenticated."""
    api_key, email, err = await get_user_api_key(authorization)
    if err:
        raise HTTPException(status_code=401, detail=err)

    client = AIClient(user_api_key=api_key)
    logger.info(f"Video script request: {request.product_name} ({request.duration}s, {request.platform}) user={email or 'anonymous'}")

    # Step 1: Generate video script via LLM
    result = await client.generate(
        content_type="video_script",
        product_name=request.product_name,
        category=request.category,
        features=request.features,
        target_audience=request.target_audience,
        platform=request.platform,
        language=request.language,
        tone=request.tone,
        duration=request.duration,
        n_scenes=request.n_scenes,
    )
    
    if not result["success"]:
        logger.error(f"Video script generation failed: {result['error']}")
        raise HTTPException(status_code=500, detail=result["error"])
    
    script = result["content"]
    
    # Step 2: Generate TTS audio if requested
    audio_result = None
    if request.generate_audio:
        try:
            from tts_service import generate_audio_from_script
            
            audio_result = await generate_audio_from_script(
                script=script,
                language=request.voice_language,
                gender=request.voice_gender,
                speed=request.tts_speed,
            )
            
            # Convert audio paths to URLs
            base_url = "http://localhost:8000"  # Will be overridden by request in production
            if audio_result.get("full_narration"):
                audio_result["full_narration_url"] = f"{base_url}/api/audio/{Path(audio_result['full_narration']).name}"
            if audio_result.get("hook"):
                audio_result["hook_url"] = f"{base_url}/api/audio/{Path(audio_result['hook']).name}"
            if audio_result.get("cta"):
                audio_result["cta_url"] = f"{base_url}/api/audio/{Path(audio_result['cta']).name}"
            
            for scene in audio_result.get("scenes", []):
                if scene.get("audio"):
                    scene["audio_url"] = f"{base_url}/api/audio/{Path(scene['audio']).name}"
            
            logger.info(f"TTS audio generated: {audio_result['total_duration']}s total")
            
        except ImportError as e:
            logger.warning(f"TTS not available: {e}")
            audio_result = {"error": str(e), "available": False}
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            audio_result = {"error": str(e), "available": False}
    
    if email:
        increment_generation(email)

    return {
        "success": True,
        "model": result.get("model"),
        "backend": result.get("backend"),
        "content_type": "video_script",
        "script": script,
        "audio": audio_result,
    }


@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    """Serve generated audio files."""
    audio_dir = Path("output/audio")
    file_path = audio_dir / filename
    
    # Security: prevent path traversal
    try:
        file_path.resolve().relative_to(audio_dir.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        path=str(file_path),
        media_type="audio/mpeg",
        headers={"Content-Disposition": f'inline; filename="{filename}"'}
    )


@app.get("/api/voices")
async def get_voices():
    """Get available TTS voices."""
    from tts_service import get_available_voices
    return {"voices": get_available_voices()}


# ─── Settings Endpoints ─────────────────────────────────────

from settings_manager import load_settings


class SettingsRequest(BaseModel):
    """Request to update settings."""
    settings: dict = Field(..., description="Key-value pairs to update")


@app.get("/api/settings")
async def get_settings(authorization: str = Header(None)):
    """Get current user's settings (with masked API keys)."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")

    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email = user.get("email", "")
    user_keys = get_user_api_keys(email)

    # Mask sensitive keys
    masked = {}
    for key, value in user_keys.items():
        if "API_KEY" in key and value:
            masked[key] = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
        else:
            masked[key] = value

    return {
        "settings": masked,
        "api_keys_configured": {k: bool(v) for k, v in user_keys.items() if "API_KEY" in k},
    }


@app.post("/api/settings")
async def update_settings(request: SettingsRequest, authorization: str = Header(None)):
    """Update user's settings (API keys, model selection, etc.)."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")

    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email = user.get("email", "")
    try:
        set_user_api_keys(email, request.settings)
        user_keys = get_user_api_keys(email)
        return {
            "success": True,
            "message": "Settings saved successfully",
            "api_keys_configured": {k: bool(v) for k, v in user_keys.items() if "API_KEY" in k},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save settings: {e}")


@app.get("/api/settings/check")
async def check_settings(authorization: str = Header(None)):
    """Check which API keys are configured for current user."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")

    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email = user.get("email", "")
    user_keys = get_user_api_keys(email)
    return {k: bool(v) for k, v in user_keys.items() if "API_KEY" in k}


# ─── Auth Endpoints ──────────────────────────────────────────

from auth import (
    create_user, authenticate_user, create_token, verify_token,
    get_user_by_id, get_user_by_email, get_generation_stats, increment_generation,
    upgrade_user_plan, get_user_api_keys, set_user_api_keys, get_user_setting,
)
from payment import (
    create_checkout_session, handle_webhook, get_subscription,
    is_stripe_configured, PLANS,
)


class RegisterRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")
    name: str = Field(default="", description="Display name")


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    """Register a new user account."""
    try:
        user = create_user(req.email, req.password, req.name)
        token = create_token(user)
        return {
            "success": True,
            "token": token,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "plan": user.get("plan", "free"),
                "role": user.get("role", "user"),
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/auth/login")
async def login(req: LoginRequest):
    """Login and get JWT token."""
    user = authenticate_user(req.email, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token(user)
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "plan": user.get("plan", "free"),
            "role": user.get("role", "user"),
        },
    }


@app.get("/api/auth/me")
async def get_current_user(authorization: str = Header(None)):
    """Get current user info from JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    stats = get_generation_stats(user["email"])
    return {
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "plan": user.get("plan", "free"),
            "role": user.get("role", "user"),
        },
        "stats": stats,
    }


@app.get("/api/auth/stats")
async def get_stats(authorization: str = Header(None)):
    """Get generation stats for current user."""
    if not authorization or not authorization.startswith("Bearer "):
        # Return default free stats
        return {"today": 0, "total": 0, "remaining": 5, "plan": "free"}
    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        return {"today": 0, "total": 0, "remaining": 5, "plan": "free"}
    stats = get_generation_stats(payload["email"])
    return stats


# ─── Payment Endpoints ───────────────────────────────────────

class CheckoutRequest(BaseModel):
    plan: str = Field(..., description="Plan ID: pro or business")


@app.post("/api/payment/checkout")
async def create_subscription_checkout(req: CheckoutRequest, authorization: str = Header(None)):
    """Create a Stripe checkout session for subscription."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload["email"]
    success_url = "http://localhost:5173/pricing?success=true"
    cancel_url = "http://localhost:5173/pricing?canceled=true"

    result = create_checkout_session(req.plan, email, success_url, cancel_url)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/api/payment/plans")
async def get_plans():
    """Get available subscription plans."""
    return {
        "plans": [
            {
                "id": pid,
                "name": p["name"],
                "price_vnd": p["price_vnd"],
                "price_usd": p["price_usd"],
                "features": p["features"],
            }
            for pid, p in PLANS.items()
        ],
        "stripe_configured": is_stripe_configured(),
    }


@app.get("/api/payment/subscription")
async def get_my_subscription(authorization: str = Header(None)):
    """Get current user's subscription status."""
    if not authorization or not authorization.startswith("Bearer "):
        return {"plan": "free", "status": "active"}
    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        return {"plan": "free", "status": "active"}
    sub = get_subscription(payload["email"])
    if sub:
        return sub
    return {"plan": "free", "status": "active"}


@app.post("/api/payment/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    result = handle_webhook(payload, sig_header)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# ─── Video Generation Endpoints ─────────────────────────────

from video_engine import (
    VideoEngine, VideoConfig, TTSConfig,
    VideoModel, TTSProvider, VideoProvider,
    estimate_video_cost, compare_video_prices, get_max_duration,
    VIDEO_PRICING, AUDIO_SUPPORTED_MODELS,
)

# Initialize video engine (lazy, uses env vars as fallback)
video_engine: VideoEngine = None


def get_video_engine(
    user_fal_key: str = None,
    user_replicate_key: str = None,
    user_elevenlabs_key: str = None,
    user_openai_key: str = None,
) -> VideoEngine:
    """Create VideoEngine with user's API keys, falling back to env vars."""
    global video_engine
    video_engine = VideoEngine(
        fal_api_key=user_fal_key or None,
        replicate_api_key=user_replicate_key or None,
        elevenlabs_api_key=user_elevenlabs_key or None,
        openai_api_key=user_openai_key or None,
    )
    return video_engine


async def get_user_video_keys(authorization: str = Header(None)) -> tuple:
    """Extract user's video-related API keys from JWT. Returns (keys_dict, email, error)."""
    if not authorization or not authorization.startswith("Bearer "):
        return {}, None, None

    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        return {}, None, "Invalid or expired token"

    user = get_user_by_id(payload["sub"])
    if not user:
        return {}, None, "User not found"

    email = user.get("email", "")
    user_keys = get_user_api_keys(email)

    return {
        "fal_api_key": user_keys.get("FAL_API_KEY", ""),
        "replicate_api_key": user_keys.get("REPLICATE_API_KEY", ""),
        "elevenlabs_api_key": user_keys.get("ELEVENLABS_API_KEY", ""),
        "openai_api_key": user_keys.get("OPENAI_API_KEY", ""),
    }, email, None


class VideoGenerateRequest(BaseModel):
    """Request for AI video generation."""
    prompt: str = Field(..., description="Video generation prompt")
    model: str = Field(default="SEEDANCE_2_FAST", description="Video model to use")
    duration: int = Field(default=5, ge=3, le=20, description="Duration in seconds")
    width: int = Field(default=1080, description="Video width")
    height: int = Field(default=1920, description="Video height (1920=portrait, 1080=landscape)")
    negative_prompt: str = Field(default="blurry, low quality, distorted, watermark")
    seed: Optional[int] = None
    image_path: Optional[str] = Field(default=None, description="Image for image-to-video")
    style_prompt: Optional[str] = Field(default=None, description="Style: cinematic, anime, cartoon")
    include_audio: bool = Field(default=False, description="Include native audio (if model supports)")
    
    # TTS overlay
    add_tts: bool = Field(default=False, description="Add TTS narration overlay")
    tts_text: Optional[str] = Field(default=None, description="TTS text (defaults to prompt)")
    tts_provider: str = Field(default="edge", description="TTS provider: edge, elevenlabs, openai_tts")
    tts_voice_id: Optional[str] = Field(default=None)
    tts_language: str = Field(default="vi")
    tts_gender: str = Field(default="female")
    tts_speed: float = Field(default=1.0, ge=0.5, le=2.0)
    
    # BGM
    bgm_path: Optional[str] = Field(default=None, description="Background music file path")
    bgm_volume: float = Field(default=0.2, ge=0.0, le=1.0)


class VideoScriptToVideoRequest(BaseModel):
    """Request to convert a video script to actual video."""
    script: dict = Field(..., description="Video script from /api/generate/video-script")
    model: str = Field(default="SEEDANCE_2_FAST")
    duration_per_scene: int = Field(default=5, ge=3, le=10)
    tts_provider: str = Field(default="edge")
    tts_language: str = Field(default="vi")
    tts_gender: str = Field(default="female")
    tts_speed: float = Field(default=1.0)
    add_bgm: bool = Field(default=False)
    bgm_path: Optional[str] = None
    bgm_volume: float = Field(default=0.2)


@app.get("/api/video/providers")
async def get_video_providers(authorization: str = Header(None)):
    """Get available video generation providers for current user."""
    user_keys, email, err = await get_user_video_keys(authorization)
    engine = get_video_engine(
        user_fal_key=user_keys.get("fal_api_key"),
        user_replicate_key=user_keys.get("replicate_api_key"),
        user_elevenlabs_key=user_keys.get("elevenlabs_api_key"),
        user_openai_key=user_keys.get("openai_api_key"),
    )
    return {
        "providers": engine.available_providers,
        "models": [
            {
                "id": m.value,
                "price_per_sec": VIDEO_PRICING.get(m, 0),
                "max_duration": get_max_duration(m),
                "native_audio": m in AUDIO_SUPPORTED_MODELS,
            }
            for m in VideoModel
        ],
    }


@app.get("/api/video/prices")
async def get_video_prices(duration: int = 5):
    """Compare video generation prices across all models."""
    return {"duration": duration, "prices": compare_video_prices(duration)}


@app.post("/api/video/generate")
async def generate_video(request: VideoGenerateRequest, authorization: str = Header(None)):
    """Generate AI video from prompt.
    
    Supports multiple models via fal.ai and Replicate.
    Optionally adds TTS narration and BGM.
    Uses user's API keys from their profile.
    """
    # Get user's API keys
    user_keys, email, err = await get_user_video_keys(authorization)
    if err:
        raise HTTPException(status_code=401, detail=err)

    engine = get_video_engine(
        user_fal_key=user_keys.get("fal_api_key"),
        user_replicate_key=user_keys.get("replicate_api_key"),
        user_elevenlabs_key=user_keys.get("elevenlabs_api_key"),
        user_openai_key=user_keys.get("openai_api_key"),
    )
    
    # Check providers
    available = engine.available_providers
    if not available.get("fal.ai") and not available.get("replicate"):
        raise HTTPException(
            status_code=503,
            detail="No video generation provider configured. Please add FAL_API_KEY or REPLICATE_API_KEY in Settings."
        )
    
    # Parse model
    try:
        model = VideoModel[request.model]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown model: {request.model}")
    
    # Build config
    video_config = VideoConfig(
        model=model,
        duration=request.duration,
        width=request.width,
        height=request.height,
        negative_prompt=request.negative_prompt,
        seed=request.seed,
        prompt=request.prompt,
        image_path=request.image_path,
        style_prompt=request.style_prompt,
        include_audio=request.include_audio,
    )
    
    try:
        # Generate video
        result = await engine.generate_video(video_config)
        
        # Add TTS if requested
        if request.add_tts:
            tts_text = request.tts_text or request.prompt
            tts_config = TTSConfig(
                provider=TTSProvider(request.tts_provider),
                voice_id=request.tts_voice_id,
                language=request.tts_language,
                gender=request.tts_gender,
                speed=request.tts_speed,
            )
            
            audio_path = await engine.generate_tts(tts_text, tts_config)
            result.audio_path = audio_path
            
            # Merge
            combined_path = str(VIDEO_DIR / f"combined_{uuid.uuid4().hex}.mp4")
            engine.composer.merge_audio_video(result.video_path, audio_path, combined_path)
            result.combined_path = combined_path
            result.video_path = combined_path
        
        # Add BGM if requested
        if request.bgm_path and result.video_path:
            final_path = str(VIDEO_DIR / f"final_{uuid.uuid4().hex}.mp4")
            engine.composer.add_bgm(result.video_path, request.bgm_path, final_path, request.bgm_volume)
            result.video_path = final_path
            result.combined_path = final_path
        
        # Build response
        video_filename = Path(result.video_path).name
        audio_filename = Path(result.audio_path).name if result.audio_path else None
        
        return {
            "success": True,
            "video_url": f"/api/video/file/{video_filename}",
            "audio_url": f"/api/audio/{audio_filename}" if audio_filename else None,
            "duration": result.duration,
            "cost_usd": result.cost,
            "model": result.model,
            "provider": result.provider,
            "metadata": result.metadata,
        }
        
    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/video/script-to-video")
async def script_to_video(request: VideoScriptToVideoRequest, authorization: str = Header(None)):
    """Convert a video script to actual video with TTS.
    
    Takes a script from /api/generate/video-script and generates:
    1. TTS audio for narration
    2. AI video from visual descriptions
    3. Merges audio + video
    Uses user's API keys from their profile.
    """
    user_keys, email, err = await get_user_video_keys(authorization)
    if err:
        raise HTTPException(status_code=401, detail=err)

    engine = get_video_engine(
        user_fal_key=user_keys.get("fal_api_key"),
        user_replicate_key=user_keys.get("replicate_api_key"),
        user_elevenlabs_key=user_keys.get("elevenlabs_api_key"),
        user_openai_key=user_keys.get("openai_api_key"),
    )
    
    available = engine.available_providers
    if not available.get("fal.ai") and not available.get("replicate"):
        raise HTTPException(
            status_code=503,
            detail="No video generation provider configured. Please add FAL_API_KEY or REPLICATE_API_KEY in Settings."
        )
    
    try:
        model = VideoModel[request.model]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown model: {request.model}")
    
    # Build video config
    video_config = VideoConfig(
        model=model,
        duration=request.duration_per_scene,
    )
    
    # Build TTS config
    tts_config = TTSConfig(
        provider=TTSProvider(request.tts_provider),
        language=request.tts_language,
        gender=request.tts_gender,
        speed=request.tts_speed,
    )
    
    try:
        result = await engine.generate_full_video(
            script=request.script,
            video_config=video_config,
            tts_config=tts_config,
            merge=True,
            add_bgm_path=request.bgm_path if request.add_bgm else None,
            bgm_volume=request.bgm_volume,
        )
        
        video_filename = Path(result.video_path).name
        audio_filename = Path(result.audio_path).name if result.audio_path else None
        
        return {
            "success": True,
            "video_url": f"/api/video/file/{video_filename}",
            "audio_url": f"/api/audio/{audio_filename}" if audio_filename else None,
            "duration": result.duration,
            "cost_usd": result.cost,
            "model": result.model,
            "metadata": result.metadata,
        }
        
    except Exception as e:
        logger.error(f"Script-to-video failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/video/file/{filename}")
async def get_video_file(filename: str):
    """Serve generated video files."""
    video_dir = Path("output/video")
    file_path = video_dir / filename
    
    # Security: prevent path traversal
    try:
        file_path.resolve().relative_to(video_dir.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        path=str(file_path),
        media_type="video/mp4",
        headers={"Content-Disposition": f'inline; filename="{filename}"'}
    )


@app.get("/api/video/estimate")
async def estimate_video_cost_endpoint(
    model: str = "SEEDANCE_2_FAST",
    duration: int = 5,
    tts_provider: str = "edge",
    text_length: int = 500,
):
    """Estimate video generation cost."""
    try:
        video_model = VideoModel[model]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown model: {model}")
    
    tts_config = TTSConfig(provider=TTSProvider(tts_provider))
    video_config = VideoConfig(model=video_model, duration=duration)
    
    engine = get_video_engine()
    return engine.estimate_cost(video_config, tts_config, text_length)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


# ─── Admin Endpoints ──────────────────────────────────────────

from admin import (
    require_admin, get_all_users, get_admin_stats,
    set_user_role, set_user_plan, delete_user,
)


class AdminUserUpdateRequest(BaseModel):
    role: Optional[str] = Field(default=None, description="user or admin")
    plan: Optional[str] = Field(default=None, description="free, pro, or business")


@app.get("/api/admin/stats")
async def admin_stats(authorization: str = Header(None)):
    """Get platform-wide stats (admin only)."""
    await require_admin(authorization)
    return get_admin_stats()


@app.get("/api/admin/users")
async def admin_users(authorization: str = Header(None)):
    """Get all users (admin only)."""
    await require_admin(authorization)
    return {"users": get_all_users()}


@app.put("/api/admin/users/{email}")
async def admin_update_user(email: str, req: AdminUserUpdateRequest, authorization: str = Header(None)):
    """Update user role/plan (admin only)."""
    await require_admin(authorization)
    
    if req.role:
        if not set_user_role(email, req.role):
            raise HTTPException(status_code=400, detail="Invalid role or user not found")
    
    if req.plan:
        if not set_user_plan(email, req.plan):
            raise HTTPException(status_code=400, detail="Invalid plan or user not found")
    
    return {"success": True, "message": f"User {email} updated"}


@app.delete("/api/admin/users/{email}")
async def admin_delete_user(email: str, authorization: str = Header(None)):
    """Delete a user (admin only)."""
    await require_admin(authorization)
    if not delete_user(email):
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": f"User {email} deleted"}
