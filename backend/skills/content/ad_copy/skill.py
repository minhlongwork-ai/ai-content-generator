"""Ad Copy Skill Implementation.

Generates high-converting ad copy using proven copywriting formulas:
- PAS (Problem-Agitation-Solution)
- BAB (Before-After-Bridge)
- Story/Testimonial
"""

from typing import Dict, Any, Optional
from skills.base_skill import BaseSkill


class AdCopySkill(BaseSkill):
    """Generate high-converting ad copy."""
    
    def get_skill_metadata(self) -> Dict[str, Any]:
        """Return skill metadata."""
        return {
            'name': 'ad-copy',
            'description': 'Generate high-converting ad copy using proven formulas',
            'category': 'marketing',
            'version': '1.0.0',
            'required_inputs': ['product_name', 'category', 'selling_points'],
            'optional_inputs': ['target_audience', 'platform', 'tone', 'language']
        }
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'platform': 'facebook',
            'tone': 'professional',
            'language': 'English',
            'target_audience': 'general',
            'num_variations': 3,
            'min_hook_words': 10,
            'max_hook_words': 20,
            'min_body_words': 20,
            'max_body_words': 60,
            'min_cta_words': 3,
            'max_cta_words': 10,
            'quality_threshold': 75
        }
    
    def validate_input(self, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate input parameters."""
        required = ['product_name', 'category', 'selling_points']
        
        for field in required:
            if field not in params or not params[field]:
                return False, f"Missing required field: {field}"
        
        # Validate product_name length
        if len(params['product_name']) > 100:
            return False, "product_name too long (max 100 characters)"
        
        # Validate selling_points
        if len(params['selling_points']) < 10:
            return False, "selling_points too short (min 10 characters)"
        
        # Validate platform if provided
        valid_platforms = ['facebook', 'instagram', 'google', 'tiktok', 'youtube']
        if 'platform' in params and params['platform'].lower() not in valid_platforms:
            return False, f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        
        # Validate tone if provided
        valid_tones = ['professional', 'casual', 'urgent', 'luxury']
        if 'tone' in params and params['tone'].lower() not in valid_tones:
            return False, f"Invalid tone. Must be one of: {', '.join(valid_tones)}"
        
        return True, None
    
    def build_prompt(self, params: Dict[str, Any]) -> str:
        """Build AI prompt from parameters."""
        product_name = params['product_name']
        category = params['category']
        selling_points = params['selling_points']
        target_audience = params.get('target_audience', self.config['target_audience'])
        platform = params.get('platform', self.config['platform'])
        tone = params.get('tone', self.config['tone'])
        language = params.get('language', self.config['language'])
        
        # Build optimized prompt
        prompt = f"""You are a direct-response copywriter specializing in e-commerce ads. Write high-converting ad copy.

Product: {product_name}
Category: {category}
Selling Points: {selling_points}
Target Audience: {target_audience}
Platform: {platform}
Tone: {tone}
Language: {language}

Generate {self.config['num_variations']} variations using these formulas:

1. **Problem-Agitation-Solution (PAS)**
   - Hook: Identify pain point ({self.config['min_hook_words']}-{self.config['max_hook_words']} words)
   - Body: Agitate problem, present solution ({self.config['min_body_words']}-{self.config['max_body_words']} words)
   - CTA: Clear action ({self.config['min_cta_words']}-{self.config['max_cta_words']} words)

2. **Before-After-Bridge (BAB)**
   - Hook: Contrast current vs desired state
   - Body: Show transformation, explain how
   - CTA: Action-oriented with benefit

3. **Story/Testimonial**
   - Hook: Relatable quote or character
   - Body: Customer success story
   - CTA: Social proof + action

Guidelines:
- Focus on BENEFITS not features
- Use specific numbers
- Create urgency (when appropriate)
- Platform tone: {platform} = {"casual, emoji-friendly" if platform in ["instagram", "tiktok"] else "professional, clear"}
- Tone: {tone}

Output JSON:
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
        
        return prompt
    
    def get_required_output_fields(self) -> list[str]:
        """Return required output fields."""
        return ['variations']
    
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
        
        # 1. Variations count
        if 'variations' in content and isinstance(content['variations'], list):
            variations_count = len(content['variations'])
            checks['variations_count_ok'] = variations_count == self.config['num_variations']
            if not checks['variations_count_ok']:
                issues.append(f"Wrong number of variations: {variations_count} (need {self.config['num_variations']})")
            
            # Check each variation
            expected_styles = ['Problem-Agitation-Solution', 'Before-After-Bridge', 'Story/Testimonial']
            actual_styles = [v.get('style', '') for v in content['variations']]
            
            checks['styles_correct'] = all(
                style in expected_styles for style in actual_styles
            )
            if not checks['styles_correct']:
                issues.append(f"Invalid styles found. Expected: {', '.join(expected_styles)}")
            
            # Check each variation has required fields
            for i, variation in enumerate(content['variations'], 1):
                has_hook = 'hook' in variation and variation['hook']
                has_body = 'body' in variation and variation['body']
                has_cta = 'cta' in variation and variation['cta']
                
                checks[f'variation_{i}_complete'] = has_hook and has_body and has_cta
                if not checks[f'variation_{i}_complete']:
                    missing = []
                    if not has_hook: missing.append('hook')
                    if not has_body: missing.append('body')
                    if not has_cta: missing.append('cta')
                    issues.append(f"Variation {i} missing: {', '.join(missing)}")
                
                # Check hook length
                if has_hook:
                    hook_words = len(variation['hook'].split())
                    checks[f'variation_{i}_hook_length_ok'] = (
                        self.config['min_hook_words'] <= hook_words <= self.config['max_hook_words']
                    )
                    if not checks[f'variation_{i}_hook_length_ok']:
                        issues.append(f"Variation {i} hook: {hook_words} words (need {self.config['min_hook_words']}-{self.config['max_hook_words']})")
                
                # Check body length
                if has_body:
                    body_words = len(variation['body'].split())
                    checks[f'variation_{i}_body_length_ok'] = (
                        self.config['min_body_words'] <= body_words <= self.config['max_body_words']
                    )
                    if not checks[f'variation_{i}_body_length_ok']:
                        issues.append(f"Variation {i} body: {body_words} words (need {self.config['min_body_words']}-{self.config['max_body_words']})")
                
                # Check CTA length
                if has_cta:
                    cta_words = len(variation['cta'].split())
                    checks[f'variation_{i}_cta_length_ok'] = (
                        self.config['min_cta_words'] <= cta_words <= self.config['max_cta_words']
                    )
                    if not checks[f'variation_{i}_cta_length_ok']:
                        issues.append(f"Variation {i} CTA: {cta_words} words (need {self.config['min_cta_words']}-{self.config['max_cta_words']})")
                    
                    # Check CTA has action verb
                    action_verbs = ['shop', 'get', 'buy', 'order', 'try', 'discover', 'join', 'claim', 'grab', 'see', 'learn', 'start']
                    has_action_verb = any(verb in variation['cta'].lower() for verb in action_verbs)
                    checks[f'variation_{i}_cta_has_action'] = has_action_verb
                    if not has_action_verb:
                        suggestions.append(f"Variation {i} CTA: Use action verb (Shop, Get, Try, etc.)")
            
            # Check for duplicate hooks
            hooks = [v.get('hook', '') for v in content['variations'] if v.get('hook')]
            unique_hooks = set(h.lower() for h in hooks)
            checks['no_duplicate_hooks'] = len(unique_hooks) == len(hooks)
            if not checks['no_duplicate_hooks']:
                issues.append("Duplicate hooks found - each variation should be unique")
        
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
            'has_variations': 30,
            'variations_count_ok': 10,
            'styles_correct': 10,
            'no_duplicate_hooks': 5
        }
        
        # Add weights for each variation (3 variations)
        for i in range(1, 4):
            weights[f'variation_{i}_complete'] = 10
            weights[f'variation_{i}_hook_length_ok'] = 3
            weights[f'variation_{i}_body_length_ok'] = 3
            weights[f'variation_{i}_cta_length_ok'] = 2
            weights[f'variation_{i}_cta_has_action'] = 2
        
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
