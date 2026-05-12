-- Migration: Add skill system tables
-- Version: 001
-- Date: 2026-05-12
-- Description: Add tables for skill system (skills, user configs, generations, purchases)

-- ============================================================================
-- 1. Skills table
-- ============================================================================
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(50),
    version VARCHAR(20) DEFAULT '1.0.0',
    is_premium BOOLEAN DEFAULT FALSE,
    price DECIMAL(10,2) DEFAULT 0.00,
    author VARCHAR(100),
    tags TEXT[],
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_skills_name ON skills(name);
CREATE INDEX IF NOT EXISTS idx_skills_category ON skills(category);
CREATE INDEX IF NOT EXISTS idx_skills_is_premium ON skills(is_premium);

-- Insert default skills
INSERT INTO skills (name, description, category, version, is_premium, price, author, tags) VALUES
    ('product-description', 'Generate compelling e-commerce product descriptions', 'e-commerce', '1.0.0', FALSE, 0.00, 'AI Content Generator', ARRAY['product', 'description', 'seo', 'e-commerce']),
    ('caption-seo', 'Generate SEO-optimized titles, captions, and hashtags', 'e-commerce', '1.0.0', FALSE, 0.00, 'AI Content Generator', ARRAY['seo', 'caption', 'title', 'hashtags', 'social-media']),
    ('ad-copy', 'Generate high-converting ad copy using proven formulas', 'marketing', '1.0.0', FALSE, 0.00, 'AI Content Generator', ARRAY['ad-copy', 'marketing', 'copywriting', 'conversion']),
    ('video-script', 'Generate engaging video scripts for short-form content', 'video-marketing', '1.0.0', FALSE, 0.00, 'AI Content Generator', ARRAY['video', 'script', 'tiktok', 'reels', 'youtube-shorts'])
ON CONFLICT (name) DO NOTHING;

-- ============================================================================
-- 2. User skill configs table
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_skill_configs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    config JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, skill_name)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_user_skill_configs_user_id ON user_skill_configs(user_id);
CREATE INDEX IF NOT EXISTS idx_user_skill_configs_skill_name ON user_skill_configs(skill_name);

-- Foreign key (if users table exists)
-- ALTER TABLE user_skill_configs ADD CONSTRAINT fk_user_skill_configs_user 
--     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- ============================================================================
-- 3. Generations table (history with quality scores)
-- ============================================================================
CREATE TABLE IF NOT EXISTS generations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    input_params JSONB NOT NULL,
    output_content JSONB NOT NULL,
    quality_score JSONB,
    model_used VARCHAR(100),
    backend VARCHAR(50),
    tokens_used INTEGER,
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_generations_user_id ON generations(user_id);
CREATE INDEX IF NOT EXISTS idx_generations_skill_name ON generations(skill_name);
CREATE INDEX IF NOT EXISTS idx_generations_created_at ON generations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_generations_user_skill ON generations(user_id, skill_name);

-- Foreign key (if users table exists)
-- ALTER TABLE generations ADD CONSTRAINT fk_generations_user 
--     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- ============================================================================
-- 4. Skill purchases table (for marketplace)
-- ============================================================================
CREATE TABLE IF NOT EXISTS skill_purchases (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    transaction_id VARCHAR(100),
    status VARCHAR(20) DEFAULT 'completed',
    purchased_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, skill_name)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_skill_purchases_user_id ON skill_purchases(user_id);
CREATE INDEX IF NOT EXISTS idx_skill_purchases_skill_name ON skill_purchases(skill_name);
CREATE INDEX IF NOT EXISTS idx_skill_purchases_purchased_at ON skill_purchases(purchased_at DESC);

-- Foreign key (if users table exists)
-- ALTER TABLE skill_purchases ADD CONSTRAINT fk_skill_purchases_user 
--     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- ============================================================================
-- 5. Skill analytics table (for tracking usage)
-- ============================================================================
CREATE TABLE IF NOT EXISTS skill_analytics (
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL,
    user_id INTEGER,
    event_type VARCHAR(50) NOT NULL, -- 'view', 'generate', 'purchase', 'config_update'
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_skill_analytics_skill_name ON skill_analytics(skill_name);
CREATE INDEX IF NOT EXISTS idx_skill_analytics_event_type ON skill_analytics(event_type);
CREATE INDEX IF NOT EXISTS idx_skill_analytics_created_at ON skill_analytics(created_at DESC);

-- ============================================================================
-- 6. Helper functions
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
DROP TRIGGER IF EXISTS update_skills_updated_at ON skills;
CREATE TRIGGER update_skills_updated_at
    BEFORE UPDATE ON skills
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_skill_configs_updated_at ON user_skill_configs;
CREATE TRIGGER update_user_skill_configs_updated_at
    BEFORE UPDATE ON user_skill_configs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 7. Views for analytics
-- ============================================================================

-- View: Skill usage statistics
CREATE OR REPLACE VIEW skill_usage_stats AS
SELECT 
    skill_name,
    COUNT(*) as total_generations,
    COUNT(DISTINCT user_id) as unique_users,
    AVG((quality_score->>'score')::numeric) as avg_quality_score,
    AVG(duration_ms) as avg_duration_ms,
    SUM(tokens_used) as total_tokens_used,
    MAX(created_at) as last_used_at
FROM generations
GROUP BY skill_name;

-- View: User generation history summary
CREATE OR REPLACE VIEW user_generation_summary AS
SELECT 
    user_id,
    skill_name,
    COUNT(*) as generation_count,
    AVG((quality_score->>'score')::numeric) as avg_quality_score,
    MAX(created_at) as last_generated_at,
    MIN(created_at) as first_generated_at
FROM generations
GROUP BY user_id, skill_name;

-- View: Premium skill revenue
CREATE OR REPLACE VIEW skill_revenue AS
SELECT 
    skill_name,
    COUNT(*) as purchase_count,
    SUM(price) as total_revenue,
    AVG(price) as avg_price,
    MAX(purchased_at) as last_purchase_at
FROM skill_purchases
WHERE status = 'completed'
GROUP BY skill_name;

-- ============================================================================
-- Migration complete
-- ============================================================================

-- Verify tables created
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
    AND table_name IN ('skills', 'user_skill_configs', 'generations', 'skill_purchases', 'skill_analytics')
ORDER BY table_name;
