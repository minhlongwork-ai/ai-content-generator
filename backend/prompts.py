"""Prompt templates for AI Content Generation."""

PRODUCT_DESCRIPTION_PROMPT = """You are an expert e-commerce copywriter. Write a compelling product description that converts browsers to buyers.

Product Name: {product_name}
Category: {category}
Key Features: {features}
Target Audience: {target_audience}
Language: {language}
Tone: {tone}

Write a product description with:
1. A catchy headline (max 15 words)
2. 3-5 bullet points highlighting key benefits (not just features)
3. A persuasive closing paragraph (2-3 sentences)
4. Include relevant SEO keywords naturally

Output format (JSON):
{{
  "headline": "...",
  "bullets": ["...", "...", "..."],
  "description": "...",
  "seo_keywords": ["...", "..."]
}}"""

CAPTION_SEO_PROMPT = """You are an SEO expert for e-commerce. Generate optimized titles and captions for product listings.

Product: {product_name}
Category: {category}
Key Features: {features}
Platform: {platform}
Language: {language}

Generate:
1. An SEO-optimized title (max 80 characters)
2. A short caption/description (max 160 characters)
3. 5 relevant hashtags (for social media)
4. 3 long-tail SEO keywords

Output format (JSON):
{{
  "seo_title": "...",
  "caption": "...",
  "hashtags": ["...", "...", "...", "...", "..."],
  "seo_keywords": ["...", "...", "..."]
}}"""

AD_COPY_PROMPT = """You are a direct-response copywriter specializing in e-commerce ads. Write high-converting ad copy.

Product: {product_name}
Category: {category}
Key Selling Points: {selling_points}
Target Audience: {target_audience}
Platform: {platform}
Language: {language}
Tone: {tone}

Generate 3 variations of ad copy:
1. **Problem-Agitation-Solution** style
2. **Before-After-Bridge** style
3. **Story/Testimonial** style

Each variation should include:
- Hook (first line that stops the scroll)
- Body (2-3 sentences)
- Call-to-action

Output format (JSON):
{{
  "variations": [
    {{
      "style": "Problem-Agitation-Solution",
      "hook": "...",
      "body": "...",
      "cta": "..."
    }},
    {{
      "style": "Before-After-Bridge",
      "hook": "...",
      "body": "...",
      "cta": "..."
    }},
    {{
      "style": "Story/Testimonial",
      "hook": "...",
      "body": "...",
      "cta": "..."
    }}
  ]
}}"""


VIDEO_SCRIPT_PROMPT = """You are an expert video script writer for short-form content (TikTok, Reels, YouTube Shorts). Create an engaging video script that hooks viewers and keeps them watching.

Product: {product_name}
Category: {category}
Key Features: {features}
Target Audience: {target_audience}
Platform: {platform}
Language: {language}
Tone: {tone}
Duration: {duration} seconds

Create a video script with:
1. **Hook** (first 3-5 seconds) — grab attention immediately
2. **Scenes** ({n_scenes} scenes) — each scene has:
   - Visual description (what viewer sees)
   - Narration text (what voiceover says)
   - Duration (seconds)
3. **Call-to-Action** (last 3-5 seconds) — drive action
4. **Background Music Suggestion** — mood/genre
5. **Hashtags** — 5 relevant hashtags for the platform

Output format (JSON):
{{
  "title": "Video title (max 60 chars)",
  "hook": {{
    "text": "Hook text",
    "visual": "Visual description for hook",
    "duration": 3
  }},
  "scenes": [
    {{
      "scene_number": 1,
      "visual": "What the viewer sees",
      "narration": "Voiceover text for this scene",
      "duration": 5
    }}
  ],
  "cta": {{
    "text": "Call to action text",
    "visual": "Visual description for CTA",
    "duration": 3
  }},
  "music_suggestion": "Upbeat pop, 120 BPM",
  "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3", "#hashtag4", "#hashtag5"]
}}"""


def build_prompt(content_type: str, **kwargs) -> str:
    """Build prompt based on content type and parameters."""
    # Set defaults
    kwargs.setdefault("language", "English")
    kwargs.setdefault("tone", "professional")
    
    if content_type == "product_description":
        return PRODUCT_DESCRIPTION_PROMPT.format(**kwargs)
    elif content_type == "caption_seo":
        return CAPTION_SEO_PROMPT.format(**kwargs)
    elif content_type == "ad_copy":
        return AD_COPY_PROMPT.format(**kwargs)
    elif content_type == "video_script":
        return VIDEO_SCRIPT_PROMPT.format(**kwargs)
    else:
        raise ValueError(f"Unknown content type: {content_type}")
