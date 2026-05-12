"""Caption SEO Skill Implementation.

Generates SEO-optimized titles, captions, and hashtags for:
- E-commerce product listings
- Social media posts
- Product pages
"""

from typing import Dict, Any, Optional
from skills.base_skill import BaseSkill


class CaptionSeoSkill(BaseSkill):
    """Generate SEO-optimized captions and titles."""
    
    def get_skill_metadata(self) -> Dict[str, Any]:
        """Return skill metadata."""
        return {
            'name': 'caption-seo',
            'description': 'Generate SEO-optimized titles, captions, and hashtags',
            'category': 'e-commerce',
            'version': '1.0.0',
            'required_inputs': ['product_name', 'category', 'features'],
            'optional_inputs': ['platform', 'language']
        }
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'platform': 'shopee',
            'language': 'English',
            'max_title_length': 80,
            'max_caption_length': 160,
            'num_hashtags': 5,
            'num_seo_keywords': 3,
            'min_keyword_words': 3,
            'quality_threshold': 70
        }
    
    def validate_input(self, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate input parameters."""
        required = ['product_name', 'category', 'features']
        
        for field in required:
            if field not in params or not params[field]:
                return False, f"Missing required field: {field}"
        
        # Validate product_name length
        if len(params['product_name']) > 100:
            return False, "product_name too long (max 100 characters)"
        
        # Validate features
        if len(params['features']) < 10:
            return False, "features too short (min 10 characters)"
        
        # Validate platform if provided
        valid_platforms = ['shopee', 'lazada', 'amazon', 'instagram', 'facebook', 'tiktok']
        if 'platform' in params and params['platform'].lower() not in valid_platforms:
            return False, f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        
        return True, None
    
    def build_prompt(self, params: Dict[str, Any]) -> str:
        """Build AI prompt from parameters."""
        product_name = params['product_name']
        category = params['category']
        features = params['features']
        platform = params.get('platform', self.config['platform'])
        language = params.get('language', self.config['language'])
        
        # Build optimized prompt
        prompt = f"""You are an SEO expert for e-commerce. Generate optimized titles and captions.

Product: {product_name}
Category: {category}
Features: {features}
Platform: {platform}
Language: {language}

Generate:
1. SEO title (max {self.config['max_title_length']} chars) - keyword-rich, front-load important terms
2. Caption (max {self.config['max_caption_length']} chars) - compelling, benefit-focused
3. Hashtags ({self.config['num_hashtags']} total) - mix popular and niche, start with #
4. SEO keywords ({self.config['num_seo_keywords']} total) - long-tail (min {self.config['min_keyword_words']} words each)

Platform guidelines:
- shopee: ALL CAPS for emphasis, include specs
- lazada: Title case, brand name
- amazon: Formal, detailed specs
- instagram: Casual, emoji-friendly
- facebook: Conversational
- tiktok: Trendy, short

Output JSON:
{{
  "seo_title": "...",
  "caption": "...",
  "hashtags": ["#...", "#...", "#...", "#...", "#..."],
  "seo_keywords": ["...", "...", "..."]
}}"""
        
        return prompt
    
    def get_required_output_fields(self) -> list[str]:
        """Return required output fields."""
        return ['seo_title', 'caption', 'hashtags', 'seo_keywords']
    
    def check_quality(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Check quality of generated content."""
        # Start with base checks
        result = super().check_quality(content)
        
        if not result['passed']:
            return result
        
        checks = result['checks']
        issues = result['issues']
        suggestions = result['suggestions']
        
        # Skill-specific quality checks
        
        # 1. SEO title length
        if 'seo_title' in content:
            title_length = len(content['seo_title'])
            checks['title_length_ok'] = title_length <= self.config['max_title_length']
            if not checks['title_length_ok']:
                issues.append(f"SEO title too long: {title_length} chars (max {self.config['max_title_length']})")
                suggestions.append("Shorten title while keeping key keywords")
            
            # Check if title contains product name
            product_name_in_title = any(
                word.lower() in content['seo_title'].lower() 
                for word in content.get('product_name', '').split()[:3]  # First 3 words
            )
            checks['title_has_product_name'] = product_name_in_title
            if not product_name_in_title:
                suggestions.append("Include product name in SEO title")
        
        # 2. Caption length
        if 'caption' in content:
            caption_length = len(content['caption'])
            checks['caption_length_ok'] = caption_length <= self.config['max_caption_length']
            if not checks['caption_length_ok']:
                issues.append(f"Caption too long: {caption_length} chars (max {self.config['max_caption_length']})")
                suggestions.append("Shorten caption to fit mobile preview")
        
        # 3. Hashtags count
        if 'hashtags' in content and isinstance(content['hashtags'], list):
            hashtags_count = len(content['hashtags'])
            checks['hashtags_count_ok'] = hashtags_count == self.config['num_hashtags']
            if not checks['hashtags_count_ok']:
                issues.append(f"Wrong number of hashtags: {hashtags_count} (need exactly {self.config['num_hashtags']})")
            
            # Check hashtags format
            invalid_hashtags = [h for h in content['hashtags'] if not h.startswith('#')]
            checks['hashtags_format_ok'] = len(invalid_hashtags) == 0
            if not checks['hashtags_format_ok']:
                issues.append(f"Hashtags must start with #: {', '.join(invalid_hashtags)}")
            
            # Check for duplicate hashtags
            unique_hashtags = set(h.lower() for h in content['hashtags'])
            checks['no_duplicate_hashtags'] = len(unique_hashtags) == len(content['hashtags'])
            if not checks['no_duplicate_hashtags']:
                issues.append("Duplicate hashtags found")
        
        # 4. SEO keywords count
        if 'seo_keywords' in content and isinstance(content['seo_keywords'], list):
            keywords_count = len(content['seo_keywords'])
            checks['keywords_count_ok'] = keywords_count == self.config['num_seo_keywords']
            if not checks['keywords_count_ok']:
                issues.append(f"Wrong number of SEO keywords: {keywords_count} (need exactly {self.config['num_seo_keywords']})")
            
            # Check keywords are long-tail (3+ words)
            short_keywords = [
                k for k in content['seo_keywords'] 
                if len(k.split()) < self.config['min_keyword_words']
            ]
            checks['keywords_longtail_ok'] = len(short_keywords) == 0
            if not checks['keywords_longtail_ok']:
                issues.append(f"Keywords too short (need {self.config['min_keyword_words']}+ words): {', '.join(short_keywords)}")
                suggestions.append("Use long-tail keywords (3+ words) for better SEO")
            
            # Check for duplicate keywords
            unique_keywords = set(k.lower() for k in content['seo_keywords'])
            checks['no_duplicate_keywords'] = len(unique_keywords) == len(content['seo_keywords'])
            if not checks['no_duplicate_keywords']:
                issues.append("Duplicate SEO keywords found")
        
        # Recalculate score
        score = self.calculate_quality_score(content, checks)
        
        return {
            'score': score,
            'passed': score >= self.config['quality_threshold'],
            'checks': checks,
            'issues': issues,
            'suggestions': suggestions
        }
    
    def calculate_quality_score(self, content: Dict[str, Any], checks: Dict[str, Any]) -> int:
        """Calculate quality score with weighted checks."""
        if not checks:
            return 50
        
        # Weighted scoring
        weights = {
            'has_seo_title': 20,
            'has_caption': 20,
            'has_hashtags': 15,
            'has_seo_keywords': 15,
            'title_length_ok': 8,
            'title_has_product_name': 5,
            'caption_length_ok': 8,
            'hashtags_count_ok': 3,
            'hashtags_format_ok': 2,
            'no_duplicate_hashtags': 2,
            'keywords_count_ok': 3,
            'keywords_longtail_ok': 4,
            'no_duplicate_keywords': 2
        }
        
        total_weight = 0
        earned_weight = 0
        
        for check, passed in checks.items():
            weight = weights.get(check, 1)
            total_weight += weight
            if passed:
                earned_weight += weight
        
        if total_weight == 0:
            return 50
        
        return int((earned_weight / total_weight) * 100)
