"""Product Description Skill Implementation.

Generates compelling e-commerce product descriptions with:
- Catchy headlines
- Benefit-focused bullet points
- Persuasive descriptions
- SEO keywords
"""

from typing import Dict, Any, Optional
from skills.base_skill import BaseSkill


class ProductDescriptionSkill(BaseSkill):
    """Generate product descriptions for e-commerce."""
    
    def get_skill_metadata(self) -> Dict[str, Any]:
        """Return skill metadata."""
        return {
            'name': 'product-description',
            'description': 'Generate compelling e-commerce product descriptions',
            'category': 'e-commerce',
            'version': '1.0.0',
            'required_inputs': ['product_name', 'category', 'features'],
            'optional_inputs': ['target_audience', 'tone', 'language']
        }
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'tone': 'professional',
            'language': 'English',
            'target_audience': 'general',
            'max_headline_words': 15,
            'min_bullets': 3,
            'max_bullets': 5,
            'max_bullet_words': 20,
            'min_description_sentences': 2,
            'max_description_sentences': 3,
            'min_seo_keywords': 3,
            'max_seo_keywords': 5,
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
        
        return True, None
    
    def build_prompt(self, params: Dict[str, Any]) -> str:
        """Build AI prompt from parameters."""
        # Merge params with config
        product_name = params['product_name']
        category = params['category']
        features = params['features']
        target_audience = params.get('target_audience', self.config['target_audience'])
        tone = params.get('tone', self.config['tone'])
        language = params.get('language', self.config['language'])
        
        # Build optimized prompt (shorter than original monolithic prompt)
        prompt = f"""You are an expert e-commerce copywriter. Write a compelling product description.

Product: {product_name}
Category: {category}
Features: {features}
Audience: {target_audience}
Tone: {tone}
Language: {language}

Generate:
1. Headline (max {self.config['max_headline_words']} words) - catchy, benefit-focused
2. Bullets ({self.config['min_bullets']}-{self.config['max_bullets']} points) - benefits not features, max {self.config['max_bullet_words']} words each
3. Description ({self.config['min_description_sentences']}-{self.config['max_description_sentences']} sentences) - persuasive closing
4. SEO keywords ({self.config['min_seo_keywords']}-{self.config['max_seo_keywords']}) - long-tail, natural

Output JSON:
{{
  "headline": "...",
  "bullets": ["...", "...", "..."],
  "description": "...",
  "seo_keywords": ["...", "...", "..."]
}}"""
        
        return prompt
    
    def get_required_output_fields(self) -> list[str]:
        """Return required output fields."""
        return ['headline', 'bullets', 'description', 'seo_keywords']
    
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
        
        # 1. Headline length
        if 'headline' in content:
            headline_words = len(content['headline'].split())
            checks['headline_length_ok'] = headline_words <= self.config['max_headline_words']
            if not checks['headline_length_ok']:
                issues.append(f"Headline too long: {headline_words} words (max {self.config['max_headline_words']})")
                suggestions.append("Shorten headline to be more punchy")
        
        # 2. Bullets count
        if 'bullets' in content and isinstance(content['bullets'], list):
            bullets_count = len(content['bullets'])
            checks['bullets_count_ok'] = (
                self.config['min_bullets'] <= bullets_count <= self.config['max_bullets']
            )
            if not checks['bullets_count_ok']:
                issues.append(f"Wrong number of bullets: {bullets_count} (need {self.config['min_bullets']}-{self.config['max_bullets']})")
            
            # Check each bullet length
            long_bullets = []
            for i, bullet in enumerate(content['bullets']):
                bullet_words = len(bullet.split())
                if bullet_words > self.config['max_bullet_words']:
                    long_bullets.append(i + 1)
            
            checks['bullets_length_ok'] = len(long_bullets) == 0
            if long_bullets:
                issues.append(f"Bullets too long: #{', #'.join(map(str, long_bullets))} (max {self.config['max_bullet_words']} words)")
                suggestions.append("Shorten bullet points for better readability")
        
        # 3. Description sentences
        if 'description' in content:
            sentences = content['description'].split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            sentence_count = len(sentences)
            checks['description_length_ok'] = (
                self.config['min_description_sentences'] <= sentence_count <= self.config['max_description_sentences']
            )
            if not checks['description_length_ok']:
                issues.append(f"Description has {sentence_count} sentences (need {self.config['min_description_sentences']}-{self.config['max_description_sentences']})")
        
        # 4. SEO keywords count
        if 'seo_keywords' in content and isinstance(content['seo_keywords'], list):
            keywords_count = len(content['seo_keywords'])
            checks['seo_keywords_count_ok'] = (
                self.config['min_seo_keywords'] <= keywords_count <= self.config['max_seo_keywords']
            )
            if not checks['seo_keywords_count_ok']:
                issues.append(f"Wrong number of SEO keywords: {keywords_count} (need {self.config['min_seo_keywords']}-{self.config['max_seo_keywords']})")
            
            # Check for duplicates
            unique_keywords = set(k.lower() for k in content['seo_keywords'])
            checks['no_duplicate_keywords'] = len(unique_keywords) == len(content['seo_keywords'])
            if not checks['no_duplicate_keywords']:
                issues.append("Duplicate SEO keywords found")
                suggestions.append("Use unique, diverse keywords")
        
        # 5. Benefits vs Features check (heuristic)
        if 'bullets' in content and isinstance(content['bullets'], list):
            benefit_words = ['you', 'your', 'keeps', 'helps', 'ensures', 'delivers', 'provides']
            bullets_with_benefits = sum(
                1 for bullet in content['bullets']
                if any(word in bullet.lower() for word in benefit_words)
            )
            benefit_ratio = bullets_with_benefits / len(content['bullets']) if content['bullets'] else 0
            checks['benefits_focused'] = benefit_ratio >= 0.6
            if not checks['benefits_focused']:
                suggestions.append("Focus more on benefits (what user gets) rather than features (what product has)")
        
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
            'has_headline': 20,
            'has_bullets': 20,
            'has_description': 20,
            'has_seo_keywords': 15,
            'headline_length_ok': 5,
            'bullets_count_ok': 5,
            'bullets_length_ok': 5,
            'description_length_ok': 5,
            'seo_keywords_count_ok': 3,
            'no_duplicate_keywords': 2,
            'benefits_focused': 5
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
