"""AI content generation client.
Supports multiple backends:
- OpenRouter (default): https://openrouter.ai
- 9Router (local): http://localhost:3000 — smart fallback, token saving
"""

import os
import json
import httpx
from dotenv import load_dotenv
from prompts import build_prompt

load_dotenv()

# Backend selection: "openrouter" or "9router"
AI_BACKEND = os.getenv("AI_BACKEND", "openrouter")

# OpenRouter config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# 9Router config (local gateway)
NINEROUTER_URL = os.getenv("NINEROUTER_URL", "http://localhost:3000")
NINEROUTER_API_KEY = os.getenv("NINEROUTER_API_KEY", "")

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# Free models fallback chain (updated May 2026)
FREE_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "minimax/minimax-m2.5:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "liquid/lfm-2.5-1.2b-instruct:free",
    "inclusionai/ring-2.6-1t:free",
    "baidu/cobuddy:free",
]

# 9Router models (via local gateway)
NINEROUTER_MODELS = [
    "kr/claude-sonnet-4.5",           # Kiro AI (free Claude)
    "kr/claude-haiku-4.5",            # Kiro AI (free Claude)
    "cc/claude-sonnet-4-5-20250929",  # Claude Code subscription
    "cc/claude-haiku-4-5-20251001",   # Claude Code subscription
    "oc/gpt-4o-mini",                 # OpenCode Free
    "oc/gpt-4o",                      # OpenCode Free
    "vertex/gemini-2.0-flash",        # Vertex AI (free credits)
    "vertex/gemini-2.5-flash",        # Vertex AI (free credits)
]


def _mock_generate(content_type: str, **kwargs) -> dict:
    """Generate mock content for testing without API key."""
    product_name = kwargs.get("product_name", "Product")

    if content_type == "product_description":
        return {
            "headline": f"Premium {product_name} — Elevate Your Experience",
            "bullets": [
                f"Top-tier quality {product_name.lower()} designed for {kwargs.get('target_audience', 'everyone')}",
                f"Advanced features including {kwargs.get('features', 'premium features')}",
                "Sleek, modern design that complements any lifestyle",
                "Backed by our satisfaction guarantee",
                "Fast shipping & hassle-free returns"
            ],
            "description": f"Discover the perfect blend of style and functionality with our {product_name}. Crafted with attention to detail and designed for {kwargs.get('target_audience', 'modern consumers')}, this {kwargs.get('category', 'product')} delivers exceptional value.",
            "seo_keywords": [
                product_name.lower(),
                f"best {kwargs.get('category', 'product').lower()}",
                f"{product_name.lower()} review",
                f"buy {product_name.lower()} online",
                f"premium {kwargs.get('category', 'product').lower()}"
            ]
        }
    elif content_type == "caption_seo":
        return {
            "seo_title": f"{product_name} | Premium {kwargs.get('category', 'Product')} — Free Shipping",
            "caption": f"🔥 {product_name} — {kwargs.get('features', 'Premium quality')}. Limited stock! Order now with free shipping!",
            "hashtags": [
                product_name.replace(" ", ""),
                kwargs.get("category", "shopping").replace(" ", ""),
                "freeshipping",
                "trending",
                "musthave"
            ],
            "seo_keywords": [
                f"{product_name} {kwargs.get('platform', 'shopee')}",
                f"best {kwargs.get('category', 'product')} {kwargs.get('platform', 'shopee')}",
                f"{product_name} review"
            ]
        }
    elif content_type == "ad_copy":
        return {
            "variations": [
                {
                    "style": "Problem-Agitation-Solution",
                    "hook": f"Tired of low-quality {kwargs.get('category', 'products')} that break after a week?",
                    "body": f"You deserve better. Our {product_name} features {kwargs.get('selling_points', 'premium materials')} — built to last.",
                    "cta": f"🛒 Shop now and save 20% — limited time only!"
                },
                {
                    "style": "Before-After-Bridge",
                    "hook": f"Before: Frustrated with mediocre {kwargs.get('category', 'products')}. After: Loving {product_name}.",
                    "body": f"The bridge? One simple purchase. {kwargs.get('selling_points', 'Premium quality')} makes all the difference.",
                    "cta": f"✨ Try {product_name} risk-free today!"
                },
                {
                    "style": "Story/Testimonial",
                    "hook": f"\"I was skeptical, but {product_name} changed everything\" — Sarah, verified buyer",
                    "body": f"After trying dozens of {kwargs.get('category', 'products')}, Sarah finally found her match.",
                    "cta": f"💬 See why 10,000+ customers love it — shop now!"
                }
            ]
        }
    return {"raw_content": "Mock content generated"}


def _parse_response(data: dict) -> dict:
    """Parse OpenAI-compatible response, handling various formats."""
    choice = data.get("choices", [{}])[0]
    msg = choice.get("message", {})
    content = msg.get("content")
    # Fallback: some models put output in reasoning field
    if not content and msg.get("reasoning"):
        content = msg["reasoning"]
    if content:
        # Strip markdown code blocks (```json ... ``` or ``` ... ```)
        cleaned = content.strip()
        if cleaned.startswith("```"):
            # Remove opening ```json or ```
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
            # Remove closing ```
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            else:
                # Handle case where closing ``` is on its own line with trailing text
                cleaned = cleaned.rsplit("```", 1)[0]
            cleaned = cleaned.strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Try to extract JSON object from mixed content
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(cleaned[start:end+1])
                except json.JSONDecodeError:
                    pass
            return {"raw_content": content}
    raise Exception("Empty response from model")


class AIClient:
    """Client for AI content generation via OpenRouter or 9Router."""

    def __init__(self, model: str = None):
        self.model = model or DEFAULT_MODEL

    async def generate(self, content_type: str, **kwargs) -> dict:
        """Generate content based on type and parameters."""
        if MOCK_MODE:
            return {
                "success": True,
                "model": "mock",
                "content": _mock_generate(content_type, **kwargs),
                "content_type": content_type,
                "mock": True
            }

        prompt = build_prompt(content_type, **kwargs)

        if AI_BACKEND == "9router":
            return await self._generate_9router(content_type, prompt)
        else:
            return await self._generate_openrouter(content_type, prompt)

    async def _generate_9router(self, content_type: str, prompt: str) -> dict:
        """Generate via 9Router local gateway."""
        for model in NINEROUTER_MODELS:
            try:
                result = await self._call_9router(prompt, model)
                if result:
                    return {
                        "success": True,
                        "model": f"9r/{model}",
                        "content": result,
                        "content_type": content_type,
                        "backend": "9router"
                    }
            except Exception as e:
                print(f"9Router model {model} failed: {e}")
                continue

        return {
            "success": False,
            "error": "All 9Router models failed",
            "content_type": content_type
        }

    async def _generate_openrouter(self, content_type: str, prompt: str) -> dict:
        """Generate via OpenRouter."""
        if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_api_key_here":
            return {
                "success": False,
                "error": "OpenRouter API key not configured",
                "content_type": content_type
            }

        models_to_try = [DEFAULT_MODEL] + [m for m in FREE_MODELS if m != DEFAULT_MODEL]
        for model in models_to_try:
            try:
                result = await self._call_openrouter(prompt, model)
                if result:
                    return {
                        "success": True,
                        "model": model,
                        "content": result,
                        "content_type": content_type,
                        "backend": "openrouter"
                    }
            except Exception as e:
                print(f"OpenRouter model {model} failed: {e}")
                continue

        return {
            "success": False,
            "error": "All OpenRouter models failed",
            "content_type": content_type
        }

    async def _call_9router(self, prompt: str, model: str) -> dict:
        """Call 9Router local gateway (OpenAI-compatible)."""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{NINEROUTER_URL}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {NINEROUTER_API_KEY or '9router-local'}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2048,
                    "response_format": {"type": "json_object"},
                    "stream": False
                }
            )

            if response.status_code == 200:
                data = response.json()
                return _parse_response(data)
            else:
                raise Exception(f"9Router error {response.status_code}: {response.text}")

    async def _call_openrouter(self, prompt: str, model: str) -> dict:
        """Call OpenRouter API."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "AI Content Generator"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2048,
                    "response_format": {"type": "json_object"}
                }
            )

            if response.status_code == 200:
                data = response.json()
                return _parse_response(data)
            else:
                raise Exception(f"API error {response.status_code}: {response.text}")

    async def health_check(self) -> dict:
        """Check API connectivity."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if AI_BACKEND == "9router":
                    response = await client.get(f"{NINEROUTER_URL}/v1/models")
                else:
                    response = await client.get(
                        f"{OPENROUTER_BASE_URL}/models",
                        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
                    )
                return {
                    "status": "healthy" if response.status_code == 200 else "error",
                    "status_code": response.status_code,
                    "backend": AI_BACKEND
                }
        except Exception as e:
            return {"status": "error", "message": str(e), "backend": AI_BACKEND}
