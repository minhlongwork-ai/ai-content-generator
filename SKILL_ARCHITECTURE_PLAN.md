# Skill Architecture Implementation Plan

## Mục tiêu
Migrate AI Content Generator từ monolithic prompts sang skill-based architecture, học từ anthropics/financial-services repo.

## Hiện trạng
- **Backend:** FastAPI với monolithic prompts trong `prompts.py`
- **Content types:** product_description, caption_seo, ad_copy, video_script
- **Vấn đề:**
  - Mỗi content type = 1 prompt cứng
  - Khó customize per-user
  - Không có quality checks
  - Khó scale khi thêm content types mới

## Kiến trúc mới (Skill-based)

```
backend/
├── skills/                      # NEW: Skill system
│   ├── __init__.py
│   ├── base_skill.py           # Base class cho tất cả skills
│   ├── skill_loader.py         # Load & manage skills
│   ├── quality_checker.py      # Quality validation
│   └── content/                # Content generation skills
│       ├── __init__.py
│       ├── product_description/
│       │   ├── SKILL.md        # Skill definition (YAML + markdown)
│       │   ├── skill.py        # Implementation
│       │   ├── references/     # Reference docs
│       │   │   └── seo-best-practices.md
│       │   └── templates/      # Templates
│       │       ├── default.txt
│       │       └── premium.txt
│       ├── caption_seo/
│       │   ├── SKILL.md
│       │   └── skill.py
│       ├── ad_copy/
│       │   ├── SKILL.md
│       │   └── skill.py
│       └── video_script/
│           ├── SKILL.md
│           └── skill.py
├── main.py                     # MODIFIED: Use skills instead of prompts
├── ai_client.py                # MODIFIED: Add quality checks
└── prompts.py                  # DEPRECATED: Keep for backward compat
```

## Phase 1: Core Skill System (Tuần này)

### 1.1 Base Skill Class
```python
# backend/skills/base_skill.py
class BaseSkill:
    - validate_input()
    - generate()
    - check_quality()
    - get_default_config()
```

### 1.2 Skill Loader
```python
# backend/skills/skill_loader.py
- load_skill(skill_name)
- list_skills()
- get_skill_config(user_id, skill_name)
```

### 1.3 Quality Checker
```python
# backend/skills/quality_checker.py
- check_word_count()
- check_readability()
- check_seo_score()
- check_grammar()
```

## Phase 2: Migrate Content Types (Tuần sau)

### 2.1 Product Description Skill
- Input: product_name, category, features, target_audience, tone, language
- Output: headline, bullets, description, seo_keywords
- Quality checks: word_count, seo_score, readability

### 2.2 Caption SEO Skill
- Input: product_name, category, features, platform, language
- Output: seo_title, caption, hashtags, seo_keywords
- Quality checks: title_length (<80), caption_length (<160)

### 2.3 Ad Copy Skill
- Input: product_name, category, selling_points, target_audience, platform, tone
- Output: 3 variations (PAS, BAB, Story)
- Quality checks: hook_strength, cta_clarity

### 2.4 Video Script Skill
- Input: product_name, category, features, duration, n_scenes
- Output: hook, scenes, cta, music_suggestion, hashtags
- Quality checks: total_duration, scene_balance

## Phase 3: Database Schema (Tuần sau)

```sql
-- Skills table
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(50),
    is_premium BOOLEAN DEFAULT FALSE,
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- User skill configs
CREATE TABLE user_skill_configs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    skill_name VARCHAR(100),
    config JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, skill_name)
);

-- Generation history with quality scores
CREATE TABLE generations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    skill_name VARCHAR(100),
    input_params JSONB,
    output_content JSONB,
    quality_score JSONB,
    model_used VARCHAR(100),
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Phase 4: API Endpoints (2 tuần)

### New endpoints:
- `GET /api/skills` - List available skills
- `GET /api/skills/{skill_name}` - Get skill details
- `GET /api/skills/{skill_name}/config` - Get user's config
- `POST /api/skills/{skill_name}/config` - Update user's config
- `POST /api/skills/{skill_name}/generate` - Generate with skill

### Modified endpoints:
- `/api/generate/product-description` → use skill internally
- `/api/generate/caption-seo` → use skill internally
- `/api/generate/ad-copy` → use skill internally
- `/api/generate/video-script` → use skill internally

## Phase 5: Frontend UI (2 tuần)

### Components:
- `SkillSelector.jsx` - Select content type (skill)
- `SkillConfigEditor.jsx` - Edit skill config
- `QualityReport.jsx` - Display quality scores
- `SkillMarketplace.jsx` - Browse & buy premium skills (future)

## Benefits

### Immediate:
✓ Cleaner code structure
✓ Easier to add new content types
✓ Quality checks built-in
✓ Per-user customization

### Long-term:
✓ Skill marketplace (revenue)
✓ User-created skills
✓ A/B testing framework
✓ Advanced analytics

## Timeline

- **Week 1 (Tuần này):** Core skill system + 1 skill (product_description)
- **Week 2:** Migrate 3 remaining skills + quality checks
- **Week 3:** Database schema + API endpoints
- **Week 4:** Frontend UI
- **Week 5:** Testing + polish
- **Week 6:** Launch + marketplace prep

## Success Metrics

- Generation speed: 2x faster (cache, optimization)
- Quality score: >80/100 average
- User satisfaction: +30%
- API cost: -40% (optimized prompts)
- Revenue: +50% (premium skills)

## Next Steps

1. ✅ Create this plan
2. ⏳ Implement base_skill.py
3. ⏳ Implement product_description skill
4. ⏳ Test with existing endpoints
5. ⏳ Migrate remaining skills
