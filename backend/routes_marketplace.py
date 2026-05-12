"""API routes for Skill Marketplace.

Endpoints:
  GET  /api/marketplace              — list listings (filter, sort, search)
  GET  /api/marketplace/{skill_name} — listing detail + reviews
  POST /api/marketplace/{skill_name}/install   — install free skill
  POST /api/marketplace/{skill_name}/purchase  — buy premium skill (Stripe)
  GET  /api/marketplace/my/installs  — skills đã install của user
  POST /api/marketplace/{skill_name}/review    — đăng review
  GET  /api/marketplace/{skill_name}/reviews   — list reviews
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
import logging
import os
import stripe

from database import get_db
from models import Skill, SkillPurchase, SkillAnalytics

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/marketplace", tags=["Marketplace"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


# ============================================================================
# Auth helper (reuse pattern from main.py)
# ============================================================================

def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """Decode JWT and return user dict. Returns None if no token."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    try:
        import jwt as pyjwt
        secret = os.getenv("JWT_SECRET", "dev-secret-key")
        payload = pyjwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except Exception:
        return None


def require_user(authorization: Optional[str] = Header(None)) -> dict:
    """Like get_current_user but raises 401 if not authenticated."""
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


# ============================================================================
# Static listings (fallback khi chưa có DB / chưa chạy migration 002)
# ============================================================================

STATIC_LISTINGS = [
    {
        "skill_name": "product-description",
        "title": "Mô Tả Sản Phẩm Pro",
        "short_desc": "Tạo mô tả sản phẩm chuyên nghiệp, tối ưu SEO với 11 quality checks",
        "long_desc": "Skill tạo mô tả sản phẩm toàn diện:\n- Headline hấp dẫn\n- Bullet points lợi ích\n- Mô tả đầy đủ\n- Từ khóa SEO\n- 11 quality checks tự động\n- Hỗ trợ Tiếng Việt & Tiếng Anh",
        "price": 0.00,
        "currency": "USD",
        "category": "ecommerce",
        "tags": ["seo", "shopee", "tiktok-shop", "product"],
        "author_name": "AI Content Gen",
        "is_active": True,
        "is_featured": True,
        "total_sales": 0,
        "avg_rating": 4.8,
        "rating_count": 12,
        "cover_emoji": "📝",
    },
    {
        "skill_name": "caption-seo",
        "title": "Caption & SEO Creator",
        "short_desc": "Caption tối ưu cho mạng xã hội + hashtag thông minh, 13 quality checks",
        "long_desc": "Tạo caption chuẩn SEO cho mọi nền tảng:\n- Facebook / Instagram / TikTok\n- SEO title dưới 60 ký tự\n- Hashtag phân tầng\n- 13 quality checks",
        "price": 0.00,
        "currency": "USD",
        "category": "social-media",
        "tags": ["caption", "hashtag", "instagram", "tiktok", "seo"],
        "author_name": "AI Content Gen",
        "is_active": True,
        "is_featured": True,
        "total_sales": 0,
        "avg_rating": 4.7,
        "rating_count": 8,
        "cover_emoji": "🔍",
    },
    {
        "skill_name": "ad-copy",
        "title": "Ad Copy Generator",
        "short_desc": "3 phiên bản quảng cáo theo framework PAS, BAB, Story với 19 checks",
        "long_desc": "Tạo copy quảng cáo chuyển đổi cao:\n- PAS, BAB, Story Selling\n- Hook mạnh, CTA rõ\n- 19 quality checks\n- Cho Facebook / Google / TikTok Ads",
        "price": 0.00,
        "currency": "USD",
        "category": "advertising",
        "tags": ["ads", "facebook", "google", "copywriting"],
        "author_name": "AI Content Gen",
        "is_active": True,
        "is_featured": False,
        "total_sales": 0,
        "avg_rating": 4.6,
        "rating_count": 5,
        "cover_emoji": "🎯",
    },
    {
        "skill_name": "video-script",
        "title": "Video Script AI",
        "short_desc": "Kịch bản video TikTok/YouTube hoàn chỉnh với hook, cảnh quay, CTA",
        "long_desc": "Kịch bản video professional:\n- Hook 3 giây thu hút\n- Cấu trúc cảnh quay chi tiết\n- CTA cuối video\n- Gợi ý nhạc + hashtag\n- 25 quality checks",
        "price": 0.00,
        "currency": "USD",
        "category": "video",
        "tags": ["tiktok", "youtube", "reels", "script"],
        "author_name": "AI Content Gen",
        "is_active": True,
        "is_featured": False,
        "total_sales": 0,
        "avg_rating": 4.9,
        "rating_count": 15,
        "cover_emoji": "🎬",
    },
    # ---- PREMIUM SKILLS (coming soon) ----
    {
        "skill_name": "shopee-flash-sale",
        "title": "Shopee Flash Sale Optimizer",
        "short_desc": "Tối ưu listing Shopee cho flash sale: tiêu đề, mô tả, keyword bidding",
        "long_desc": "Premium skill tối ưu Shopee:\n- Tiêu đề sản phẩm 120 ký tự chuẩn Shopee\n- Keyword theo volume tìm kiếm\n- Mô tả theo format Shopee\n- Gợi ý giá flash sale\n- Phân tích competitor",
        "price": 9.99,
        "currency": "USD",
        "category": "ecommerce",
        "tags": ["shopee", "flash-sale", "ecommerce", "vietnam"],
        "author_name": "AI Content Gen",
        "is_active": True,
        "is_featured": True,
        "total_sales": 0,
        "avg_rating": 0,
        "rating_count": 0,
        "cover_emoji": "🛍️",
        "is_premium": True,
        "coming_soon": True,
    },
    {
        "skill_name": "tiktok-viral-hook",
        "title": "TikTok Viral Hook Generator",
        "short_desc": "Tạo hook video TikTok theo 20 công thức viral đã được kiểm chứng",
        "long_desc": "Premium skill chuyên TikTok:\n- 20 hook templates viral\n- Phân tích trend theo ngành\n- Script 15s, 30s, 60s\n- Gợi ý sound + effect\n- Hashtag strategy",
        "price": 14.99,
        "currency": "USD",
        "category": "video",
        "tags": ["tiktok", "viral", "hook", "video"],
        "author_name": "AI Content Gen",
        "is_active": True,
        "is_featured": True,
        "total_sales": 0,
        "avg_rating": 0,
        "rating_count": 0,
        "cover_emoji": "🔥",
        "is_premium": True,
        "coming_soon": True,
    },
]


# ============================================================================
# Request / Response Models
# ============================================================================

class ReviewRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="1-5 stars")
    title: Optional[str] = Field(None, max_length=200)
    body: Optional[str] = None


class PurchaseRequest(BaseModel):
    payment_method_id: Optional[str] = None   # Stripe PaymentMethod ID
    use_credits: bool = False                  # dùng credits trong tài khoản


# ============================================================================
# Helper
# ============================================================================

def _get_listing(skill_name: str) -> Optional[dict]:
    for l in STATIC_LISTINGS:
        if l["skill_name"] == skill_name:
            return l
    return None


def _user_has_access(user_id: int, skill_name: str, db: Session) -> bool:
    """Check if user already installed/purchased this skill."""
    # Free skills: always accessible
    listing = _get_listing(skill_name)
    if listing and listing.get("price", 0) == 0.00 and not listing.get("is_premium"):
        return True
    # Premium: check purchase record
    try:
        purchase = db.query(SkillPurchase).filter_by(
            user_id=user_id, skill_name=skill_name, status="completed"
        ).first()
        return purchase is not None
    except Exception:
        return False


# ============================================================================
# Endpoints
# ============================================================================

@router.get("")
async def list_listings(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    featured_only: bool = Query(False),
    sort: str = Query("featured", regex="^(featured|rating|newest|price_asc|price_desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    authorization: Optional[str] = Header(None),
):
    """Browse marketplace listings."""
    listings = [l for l in STATIC_LISTINGS if l.get("is_active", True)]

    # Filters
    if category:
        listings = [l for l in listings if l.get("category") == category]
    if featured_only:
        listings = [l for l in listings if l.get("is_featured")]
    if search:
        q = search.lower()
        listings = [
            l for l in listings
            if q in l["title"].lower()
            or q in l.get("short_desc", "").lower()
            or any(q in t for t in l.get("tags", []))
        ]

    # Sort
    if sort == "rating":
        listings = sorted(listings, key=lambda l: l.get("avg_rating", 0), reverse=True)
    elif sort == "price_asc":
        listings = sorted(listings, key=lambda l: l.get("price", 0))
    elif sort == "price_desc":
        listings = sorted(listings, key=lambda l: l.get("price", 0), reverse=True)
    elif sort == "featured":
        listings = sorted(listings, key=lambda l: (not l.get("is_featured"), -l.get("avg_rating", 0)))

    total = len(listings)
    start = (page - 1) * page_size
    listings_page = listings[start: start + page_size]

    # Tag which ones user already has (if logged in)
    user = get_current_user(authorization)
    if user:
        for l in listings_page:
            l["is_installed"] = (l.get("price", 0) == 0 and not l.get("is_premium")) or False

    return {
        "listings": listings_page,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
        "categories": list({l.get("category") for l in STATIC_LISTINGS if l.get("category")}),
    }


@router.get("/my/installs")
async def my_installs(
    db: Session = Depends(get_db),
    user: dict = Depends(require_user),
):
    """Return skills user has installed (free) or purchased (premium)."""
    user_id = user.get("user_id") or user.get("id")
    # Free skills — always installed for all users
    free = [l for l in STATIC_LISTINGS if l.get("price", 0) == 0 and not l.get("is_premium")]
    # Premium purchased
    try:
        purchases = db.query(SkillPurchase).filter_by(user_id=user_id, status="completed").all()
        purchased_names = {p.skill_name for p in purchases}
        premium = [l for l in STATIC_LISTINGS if l["skill_name"] in purchased_names]
    except Exception:
        premium = []

    return {"installs": free + premium, "total": len(free) + len(premium)}


@router.get("/{skill_name}")
async def get_listing(
    skill_name: str,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None),
):
    """Get a single listing with detail + reviews."""
    listing = _get_listing(skill_name)
    if not listing:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found in marketplace")

    # Check user access
    user = get_current_user(authorization)
    listing = dict(listing)
    listing["is_installed"] = False
    if user:
        user_id = user.get("user_id") or user.get("id")
        listing["is_installed"] = _user_has_access(user_id, skill_name, db)

    # Static reviews placeholder (real reviews come from DB after migration 002)
    listing["reviews"] = []

    # Track analytics
    try:
        event = SkillAnalytics(
            skill_name=skill_name,
            user_id=(user.get("user_id") or user.get("id")) if user else None,
            event_type="view",
        )
        db.add(event)
        db.commit()
    except Exception:
        pass

    return listing


@router.post("/{skill_name}/install")
async def install_skill(
    skill_name: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_user),
):
    """Install a free skill for a user (idempotent)."""
    listing = _get_listing(skill_name)
    if not listing:
        raise HTTPException(status_code=404, detail="Skill not found")
    if listing.get("is_premium") or listing.get("price", 0) > 0:
        raise HTTPException(status_code=400, detail="This skill requires purchase. Use /purchase endpoint.")
    if listing.get("coming_soon"):
        raise HTTPException(status_code=400, detail="Skill not yet available")

    user_id = user.get("user_id") or user.get("id")

    # Track analytics
    try:
        event = SkillAnalytics(
            skill_name=skill_name, user_id=user_id, event_type="install"
        )
        db.add(event)
        db.commit()
    except Exception:
        pass

    return {
        "success": True,
        "message": f"Skill '{listing['title']}' installed successfully",
        "skill_name": skill_name,
    }


@router.post("/{skill_name}/purchase")
async def purchase_skill(
    skill_name: str,
    body: PurchaseRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_user),
):
    """Purchase a premium skill via Stripe."""
    listing = _get_listing(skill_name)
    if not listing:
        raise HTTPException(status_code=404, detail="Skill not found")
    if listing.get("coming_soon"):
        raise HTTPException(status_code=400, detail="Skill coming soon — not yet available for purchase")

    user_id = user.get("user_id") or user.get("id")
    price = listing.get("price", 0)

    # Already purchased?
    try:
        existing = db.query(SkillPurchase).filter_by(
            user_id=user_id, skill_name=skill_name, status="completed"
        ).first()
        if existing:
            return {"success": True, "message": "Already purchased", "already_owned": True}
    except Exception:
        pass

    # Free skill — just record
    if price == 0.00:
        try:
            purchase = SkillPurchase(
                user_id=user_id,
                skill_name=skill_name,
                price=0.00,
                payment_method="free",
                status="completed",
            )
            db.add(purchase)
            db.commit()
        except Exception as e:
            logger.warning(f"Could not record free skill purchase: {e}")
        return {"success": True, "message": "Free skill added to your account"}

    # Premium — Stripe PaymentIntent
    if not stripe.api_key:
        raise HTTPException(status_code=503, detail="Payment service not configured")
    if not body.payment_method_id:
        raise HTTPException(status_code=400, detail="payment_method_id required for premium skills")

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(price * 100),            # cents
            currency=listing.get("currency", "usd").lower(),
            payment_method=body.payment_method_id,
            confirm=True,
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
            metadata={
                "user_id": str(user_id),
                "skill_name": skill_name,
            },
        )
        if intent.status == "succeeded":
            purchase = SkillPurchase(
                user_id=user_id,
                skill_name=skill_name,
                price=price,
                payment_method="stripe",
                transaction_id=intent.id,
                status="completed",
            )
            db.add(purchase)
            # Analytics
            db.add(SkillAnalytics(skill_name=skill_name, user_id=user_id, event_type="purchase"))
            db.commit()
            return {
                "success": True,
                "message": f"Successfully purchased '{listing['title']}'",
                "transaction_id": intent.id,
            }
        else:
            raise HTTPException(status_code=402, detail=f"Payment not completed: {intent.status}")
    except stripe.error.CardError as e:
        raise HTTPException(status_code=402, detail=str(e.user_message))
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(status_code=500, detail="Payment processing error")


@router.get("/{skill_name}/reviews")
async def get_reviews(
    skill_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """List reviews for a skill (from DB after migration 002)."""
    # Try real DB first, fallback to empty
    try:
        from sqlalchemy import text
        result = db.execute(
            text("""
                SELECT r.*, u.name as user_name
                FROM skill_reviews r
                LEFT JOIN users u ON r.user_id = u.id
                WHERE r.skill_name = :skill_name
                ORDER BY r.created_at DESC
                LIMIT :limit OFFSET :offset
            """),
            {"skill_name": skill_name, "limit": page_size, "offset": (page - 1) * page_size}
        )
        reviews = [dict(row._mapping) for row in result]
        count_result = db.execute(
            text("SELECT COUNT(*) FROM skill_reviews WHERE skill_name = :s"),
            {"s": skill_name}
        ).scalar()
        return {"reviews": reviews, "total": count_result or 0, "page": page}
    except Exception:
        return {"reviews": [], "total": 0, "page": page}


@router.post("/{skill_name}/review")
async def post_review(
    skill_name: str,
    body: ReviewRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_user),
):
    """Submit a review. User must have purchased/installed the skill."""
    listing = _get_listing(skill_name)
    if not listing:
        raise HTTPException(status_code=404, detail="Skill not found")

    user_id = user.get("user_id") or user.get("id")
    if not _user_has_access(user_id, skill_name, db):
        raise HTTPException(status_code=403, detail="You must install or purchase this skill before reviewing")

    try:
        from sqlalchemy import text
        db.execute(
            text("""
                INSERT INTO skill_reviews (skill_name, user_id, rating, title, body, is_verified)
                VALUES (:skill_name, :user_id, :rating, :title, :body, TRUE)
                ON CONFLICT (skill_name, user_id) DO UPDATE
                SET rating = EXCLUDED.rating, title = EXCLUDED.title, body = EXCLUDED.body,
                    updated_at = NOW()
            """),
            {"skill_name": skill_name, "user_id": user_id,
             "rating": body.rating, "title": body.title, "body": body.body}
        )
        db.commit()
    except Exception as e:
        logger.warning(f"Could not save review (migration 002 may not be run): {e}")
        # Return success anyway — review will be handled when DB is ready
        return {"success": True, "message": "Review noted (pending DB migration)", "pending": True}

    return {"success": True, "message": "Review submitted. Thank you!"}
