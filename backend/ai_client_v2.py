"""AI client with skill system integration.

Modified to work with skill-based architecture while maintaining
backward compatibility with existing endpoints.
"""

import os
from typing import Dict, Any, Optional
import httpx
from dotenv import load_dotenv

from skills.skill_loader import load_skill

load_dotenv()

# Backend selection
AI_BACKEND = os.getenv("AI_BACKEND", "openrouter")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
NINEROUTER_URL = os.getenv("NINEROUTER_URL", "http://localhost:3000")
NINEROUTER_API_KEY = os.getenv("NINEROUTER_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# Free models fallback
FREE_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "minimax/minimax-m2.5:free",
]

# 9Router models
NINEROUTER_MODELS = [
    "kr/claude-sonnet-4.5",
    "kr/claude-haiku-4.5",
    "cc/claude-sonnet-4-5-20250929",
    "oc/gpt-4o-mini",
    "vertex/gemini-2.0-flash",
]


def _parse_response(data: dict) -> dict:
    """Parse OpenAI-compatible response."""
    import json
    
    choice = data.get("choices", [{}])[0]
    msg = choice.get("message", {})
    content = msg.get("content")
    
    if not content and msg.get("reasoning"):
        content = msg["reasoning"]
    
    if content:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            else:
                cleaned = cleaned.rsplit("```", 1)[0]
            cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
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
    """AI client with skill system integration."""
    
    def __init__(self, model: str = None, user_api_key: str = None):
        self.model = model or DEFAULT_MODEL
        self.user_api_key = user_api_key
    
    async def generate_with_skill(
        self, 
        skill_name: str, 
        params: Dict[str, Any],
        user_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate content using a skill.
        
        This is the NEW way - uses skill system with quality checks.
        
        Args:
            skill_name: Name of skill (e.g., 'product-description')
            params: Input parameters
            user_config: Optional user configuration overrides
            
        Returns:
            {
                'success': True,
                'content': {...},
                'quality_report': {...},
                'model': 'gpt-4',
                'skill': 'product-description'
            }
        """
        # Load skill
        skill = load_skill(skill_name, user_config)
        if not skill:
            return {
                'success': False,
                'error': f'Skill not found: {skill_name}'
            }
        
        # Validate input
        is_valid, error = skill.validate_input(params)
        if not is_valid:
            return {
                'success': False,
                'error': error,
                'skill': skill_name
            }
        
        # Build prompt
        prompt = skill.build_prompt(params)
        
        # Call AI
        if MOCK_MODE:
            # Mock response for testing
            mock_content = self._generate_mock_content(skill_name, params)
            quality = skill.check_quality(mock_content)
            return {
                'success': True,
                'content': mock_content,
                'quality_report': quality,
                'model': 'mock',
                'skill': skill_name,
                'backend': 'mock'
            }
        
        # Real AI call
        if AI_BACKEND == "9router":
            result = await self._generate_9router(prompt)
        else:
            result = await self._generate_openrouter(prompt)
        
        if not result['success']:
            return result
        
        content = result['content']
        
        # Quality check
        quality = skill.check_quality(content)
        
        # If quality is low, try to improve (future: could regenerate)
        if not quality['passed']:
            # For now, just return with quality report
            # Future: implement auto-regeneration or improvement
            pass
        
        return {
            'success': True,
            'content': content,
            'quality_report': quality,
            'model': result.get('model'),
            'skill': skill_name,
            'backend': result.get('backend')
        }
    
    def _generate_mock_content(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock content for testing."""
        if skill_name == 'product-description':
            product_name = params.get('product_name', 'Product')
            return {
                'headline': f'Premium {product_name} — Elevate Your Experience',
                'bullets': [
                    f'Top-tier quality designed for {params.get("target_audience", "everyone")}',
                    f'Advanced features including {params.get("features", "premium features")}',
                    'Sleek, modern design that complements any lifestyle'
                ],
                'description': f'Discover the perfect blend of style and functionality with our {product_name}.',
                'seo_keywords': [
                    product_name.lower(),
                    f'best {params.get("category", "product").lower()}',
                    f'{product_name.lower()} review'
                ]
            }
        return {'raw_content': 'Mock content'}
    
    async def generate(self, content_type: str, **kwargs) -> dict:
        """Generate content (OLD way - backward compatibility).
        
        Maps old content_type to new skill names.
        """
        # Map old content_type to skill names
        skill_map = {
            'product_description': 'product-description',
            'caption_seo': 'caption-seo',
            'ad_copy': 'ad-copy',
            'video_script': 'video-script'
        }
        
        skill_name = skill_map.get(content_type)
        if not skill_name:
            # Fallback to old behavior for unmigrated content types
            return await self._generate_legacy(content_type, **kwargs)
        
        # Use skill system
        result = await self.generate_with_skill(skill_name, kwargs)
        
        # Transform to old format for backward compatibility
        if result['success']:
            return {
                'success': True,
                'model': result.get('model'),
                'content': result['content'],
                'content_type': content_type,
                'backend': result.get('backend'),
                'quality_report': result.get('quality_report')  # NEW: quality info
            }
        else:
            return result
    
    async def _generate_legacy(self, content_type: str, **kwargs) -> dict:
        """Legacy generation for unmigrated content types."""
        from prompts import build_prompt
        
        prompt = build_prompt(content_type, **kwargs)
        
        if AI_BACKEND == "9router":
            result = await self._generate_9router(prompt)
        else:
            result = await self._generate_openrouter(prompt)
        
        if result['success']:
            return {
                'success': True,
                'model': result.get('model'),
                'content': result['content'],
                'content_type': content_type,
                'backend': result.get('backend')
            }
        return result
    
    async def _generate_9router(self, prompt: str) -> dict:
        """Generate via 9Router."""
        for model in NINEROUTER_MODELS:
            try:
                result = await self._call_9router(prompt, model)
                if result:
                    return {
                        'success': True,
                        'model': f'9r/{model}',
                        'content': result,
                        'backend': '9router'
                    }
            except Exception as e:
                print(f"9Router model {model} failed: {e}")
                continue
        
        return {'success': False, 'error': 'All 9Router models failed'}
    
    async def _generate_openrouter(self, prompt: str) -> dict:
        """Generate via OpenRouter."""
        api_key = self.user_api_key or OPENROUTER_API_KEY
        if not api_key or api_key == "your_api_key_here":
            return {
                'success': False,
                'error': 'OpenRouter API key not configured'
            }
        
        models_to_try = [self.model] + [m for m in FREE_MODELS if m != self.model]
        for model in models_to_try:
            try:
                result = await self._call_openrouter(prompt, model, api_key)
                if result:
                    return {
                        'success': True,
                        'model': model,
                        'content': result,
                        'backend': 'openrouter'
                    }
            except Exception as e:
                print(f"OpenRouter model {model} failed: {e}")
                continue
        
        return {'success': False, 'error': 'All OpenRouter models failed'}
    
    async def _call_9router(self, prompt: str, model: str) -> dict:
        """Call 9Router API."""
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
                    "response_format": {"type": "json_object"}
                }
            )
            
            if response.status_code == 200:
                return _parse_response(response.json())
            else:
                raise Exception(f"9Router error {response.status_code}")
    
    async def _call_openrouter(self, prompt: str, model: str, api_key: str) -> dict:
        """Call OpenRouter API."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
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
                return _parse_response(response.json())
            else:
                raise Exception(f"API error {response.status_code}")
    
    async def health_check(self) -> dict:
        """Check API connectivity."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if AI_BACKEND == "9router":
                    response = await client.get(f"{NINEROUTER_URL}/v1/models")
                else:
                    key = self.user_api_key or OPENROUTER_API_KEY
                    response = await client.get(
                        f"{OPENROUTER_BASE_URL}/models",
                        headers={"Authorization": f"Bearer {key}"} if key else {}
                    )
                return {
                    "status": "healthy" if response.status_code == 200 else "error",
                    "status_code": response.status_code,
                    "backend": AI_BACKEND
                }
        except Exception as e:
            return {"status": "error", "message": str(e), "backend": AI_BACKEND}
