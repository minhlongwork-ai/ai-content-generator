-- Migration 002: Marketplace tables
-- Run after 001_add_skill_system_tables.sql

-- ============================================================
-- 1. skill_listings — danh sách skills trên marketplace
-- ============================================================
CREATE TABLE IF NOT EXISTS skill_listings (
    id              SERIAL PRIMARY KEY,
    skill_name      VARCHAR(100) NOT NULL REFERENCES skills(name) ON DELETE CASCADE,
    title           VARCHAR(200) NOT NULL,
    short_desc      TEXT,
    long_desc       TEXT,
    cover_image_url TEXT,
    price           DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    currency        VARCHAR(10) DEFAULT 'USD',
    category        VARCHAR(50),
    tags            TEXT[],
    author_id       INTEGER,                    -- NULL = official Antigravity skill
    author_name     VARCHAR(100),
    is_active       BOOLEAN DEFAULT TRUE,
    is_featured     BOOLEAN DEFAULT FALSE,
    total_sales     INTEGER DEFAULT 0,
    avg_rating      DECIMAL(3,2) DEFAULT 0.00,
    rating_count    INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(skill_name)
);

-- ============================================================
-- 2. skill_reviews — đánh giá từ người dùng đã mua
-- ============================================================
CREATE TABLE IF NOT EXISTS skill_reviews (
    id          SERIAL PRIMARY KEY,
    skill_name  VARCHAR(100) NOT NULL REFERENCES skills(name) ON DELETE CASCADE,
    user_id     INTEGER NOT NULL,
    rating      SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title       VARCHAR(200),
    body        TEXT,
    is_verified BOOLEAN DEFAULT FALSE,   -- đã mua mới được review
    created_at  TIMESTAMP DEFAULT NOW(),
    updated_at  TIMESTAMP DEFAULT NOW(),
    UNIQUE(skill_name, user_id)
);

-- ============================================================
-- 3. skill_installs — track user đã install skill nào
-- ============================================================
CREATE TABLE IF NOT EXISTS skill_installs (
    id           SERIAL PRIMARY KEY,
    user_id      INTEGER NOT NULL,
    skill_name   VARCHAR(100) NOT NULL REFERENCES skills(name) ON DELETE CASCADE,
    purchase_id  INTEGER REFERENCES skill_purchases(id),
    installed_at TIMESTAMP DEFAULT NOW(),
    is_active    BOOLEAN DEFAULT TRUE,
    UNIQUE(user_id, skill_name)
);

-- ============================================================
-- Indexes
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_listings_category    ON skill_listings(category);
CREATE INDEX IF NOT EXISTS idx_listings_is_featured ON skill_listings(is_featured);
CREATE INDEX IF NOT EXISTS idx_listings_author_id   ON skill_listings(author_id);
CREATE INDEX IF NOT EXISTS idx_reviews_skill_name   ON skill_reviews(skill_name);
CREATE INDEX IF NOT EXISTS idx_reviews_user_id      ON skill_reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_installs_user_id     ON skill_installs(user_id);

-- ============================================================
-- Function: update avg_rating tự động khi có review mới
-- ============================================================
CREATE OR REPLACE FUNCTION update_skill_avg_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE skill_listings
    SET avg_rating   = (SELECT AVG(rating) FROM skill_reviews WHERE skill_name = NEW.skill_name),
        rating_count = (SELECT COUNT(*)    FROM skill_reviews WHERE skill_name = NEW.skill_name),
        updated_at   = NOW()
    WHERE skill_name = NEW.skill_name;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_rating ON skill_reviews;
CREATE TRIGGER trg_update_rating
AFTER INSERT OR UPDATE ON skill_reviews
FOR EACH ROW EXECUTE FUNCTION update_skill_avg_rating();

-- ============================================================
-- Seed data — 4 built-in skills + 2 premium
-- ============================================================
INSERT INTO skill_listings (skill_name, title, short_desc, long_desc, price, category, tags, author_name, is_active, is_featured)
VALUES
(
  'product-description',
  'Mô Tả Sản Phẩm Pro',
  'Tạo mô tả sản phẩm chuyên nghiệp, tối ưu SEO với 11 quality checks',
  E'Skill tạo mô tả sản phẩm toàn diện:\n- Headline hấp dẫn\n- Bullet points lợi ích\n- Mô tả đầy đủ\n- Từ khóa SEO\n- 11 quality checks tự động\n- Hỗ trợ Tiếng Việt & Tiếng Anh',
  0.00,
  'ecommerce', ARRAY['seo', 'shopee', 'tiktok-shop', 'product'], 'AI Content Gen', TRUE, TRUE
),
(
  'caption-seo',
  'Caption & SEO Creator',
  'Caption tối ưu cho mạng xã hội + hashtag thông minh, 13 quality checks',
  E'Tạo caption chuẩn SEO cho mọi nền tảng:\n- Facebook / Instagram / TikTok\n- SEO title dưới 60 ký tự\n- Hashtag phân tầng (viral + niche + brand)\n- 13 quality checks\n- Hỗ trợ đa ngôn ngữ',
  0.00,
  'social-media', ARRAY['caption', 'hashtag', 'instagram', 'tiktok', 'seo'], 'AI Content Gen', TRUE, TRUE
),
(
  'ad-copy',
  'Ad Copy Generator',
  '3 phiên bản quảng cáo theo framework PAS, BAB, Story với 19 checks',
  E'Tạo copy quảng cáo chuyển đổi cao:\n- PAS (Problem-Agitate-Solution)\n- BAB (Before-After-Bridge)\n- Story Selling\n- Hook, body, CTA mạnh\n- 19 quality checks\n- Cho Facebook Ads / Google Ads / TikTok Ads',
  0.00,
  'advertising', ARRAY['ads', 'facebook', 'google', 'copywriting', 'conversion'], 'AI Content Gen', TRUE, FALSE
),
(
  'video-script',
  'Video Script AI',
  'Kịch bản video TikTok/YouTube hoàn chỉnh với hook, cảnh quay, CTA, 25 checks',
  E'Kịch bản video professional:\n- Hook 3 giây thu hút\n- Cấu trúc cảnh quay chi tiết\n- CTA cuối video\n- Gợi ý nhạc nền\n- Hashtag video\n- 25 quality checks\n- Phù hợp TikTok, YouTube Shorts, Reels',
  0.00,
  'video', ARRAY['tiktok', 'youtube', 'reels', 'script', 'video'], 'AI Content Gen', TRUE, FALSE
)
ON CONFLICT (skill_name) DO NOTHING;
