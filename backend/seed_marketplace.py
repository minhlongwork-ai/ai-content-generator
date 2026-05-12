from database import get_db_session
from models import SkillListing, Skill
import decimal

MARKETPLACE_DATA = [
    {
        "skill_name": "product-description",
        "title": "Mô Tả Sản Phẩm Pro",
        "short_desc": "Tạo mô tả sản phẩm chuyên nghiệp, tối ưu SEO với 11 quality checks",
        "long_desc": "Skill tạo mô tả sản phẩm toàn diện:\n- Headline hấp dẫn\n- Bullet points lợi ích\n- Mô tả đầy đủ\n- Từ khóa SEO\n- 11 quality checks tự động\n- Hỗ trợ Tiếng Việt & Tiếng Anh",
        "price": 0.00,
        "category": "ecommerce",
        "tags": ["seo", "shopee", "tiktok-shop", "product"],
        "author_name": "AI Content Gen",
        "is_featured": True,
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
        "category": "social-media",
        "tags": ["caption", "hashtag", "instagram", "tiktok", "seo"],
        "author_name": "AI Content Gen",
        "is_featured": True,
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
        "category": "advertising",
        "tags": ["ads", "facebook", "google", "copywriting"],
        "author_name": "AI Content Gen",
        "is_featured": False,
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
        "category": "video",
        "tags": ["tiktok", "youtube", "reels", "script"],
        "author_name": "AI Content Gen",
        "is_featured": False,
        "avg_rating": 4.9,
        "rating_count": 15,
        "cover_emoji": "🎬",
    },
    {
        "skill_name": "shopee-flash-sale",
        "title": "Shopee Flash Sale Optimizer",
        "short_desc": "Tối ưu listing Shopee cho flash sale: tiêu đề, mô tả, keyword bidding",
        "long_desc": "Premium skill tối ưu Shopee:\n- Tiêu đề sản phẩm 120 ký tự chuẩn Shopee\n- Keyword theo volume tìm kiếm\n- Mô tả theo format Shopee\n- Gợi ý giá flash sale",
        "price": 9.99,
        "category": "ecommerce",
        "tags": ["shopee", "flash-sale", "ecommerce", "vietnam"],
        "author_name": "AI Content Gen",
        "is_featured": True,
        "cover_emoji": "🛍️",
    },
    {
        "skill_name": "tiktok-viral-hook",
        "title": "TikTok Viral Hook Generator",
        "short_desc": "Tạo hook video TikTok theo 20 công thức viral đã được kiểm chứng",
        "long_desc": "Premium skill chuyên TikTok:\n- 20 hook templates viral\n- Phân tích trend theo ngành\n- Script 15s, 30s, 60s\n- Gợi ý sound + effect",
        "price": 14.99,
        "category": "video",
        "tags": ["tiktok", "viral", "hook", "video"],
        "author_name": "AI Content Gen",
        "is_featured": True,
        "cover_emoji": "🔥",
    },
]

def seed_marketplace():
    with get_db_session() as db:
        for data in MARKETPLACE_DATA:
            # Ensure skill exists in 'skills' table first
            skill_name = data["skill_name"]
            skill = db.query(Skill).filter_by(name=skill_name).first()
            if not skill:
                skill = Skill(
                    name=skill_name,
                    description=data["short_desc"],
                    category=data["category"],
                    price=data["price"],
                    is_premium=data["price"] > 0,
                    author=data["author_name"],
                    tags=data["tags"]
                )
                db.add(skill)
                db.flush()
                print(f"✓ Created base skill: {skill_name}")

            # Create or update listing
            existing = db.query(SkillListing).filter_by(skill_name=skill_name).first()
            if not existing:
                listing = SkillListing(**data)
                db.add(listing)
                print(f"✓ Added listing: {data['title']}")
            else:
                print(f"  Listing already exists: {data['title']}")
        
        db.commit()
    print("✓ Marketplace seeding complete!")

if __name__ == "__main__":
    seed_marketplace()
