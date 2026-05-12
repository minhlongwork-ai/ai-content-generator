"""Video Script Skill Implementation.

Generates engaging video scripts for short-form content:
- TikTok
- Instagram Reels
- YouTube Shorts
"""

from typing import Dict, Any, Optional
from skills.base_skill import BaseSkill


class VideoScriptSkill(BaseSkill):
    """Generate video scripts for short-form content."""
    
    def get_skill_metadata(self) -> Dict[str, Any]:
        """Return skill metadata."""
        return {
            'name': 'video-script',
            'description': 'Generate engaging video scripts for short-form content',
            'category': 'video-marketing',
            'version': '1.0.0',
            'required_inputs': ['product_name', 'category', 'features'],
            'optional_inputs': ['target_audience', 'platform', 'tone', 'language', 'duration', 'n_scenes']
        }
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'platform': 'tiktok',
            'tone': 'energetic',
            'language': 'English',
            'target_audience': 'general',
            'duration': 30,
            'n_scenes': 3,
            'min_hook_duration': 3,
            'max_hook_duration': 5,
            'min_scene_duration': 3,
            'max_scene_duration': 10,
            'min_cta_duration': 3,
            'max_cta_duration': 5,
            'min_scenes': 2,
            'max_scenes': 5,
            'num_hashtags': 5,
            'max_title_length': 60,
            'duration_tolerance': 3,
            'quality_threshold': 75
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
        valid_platforms = ['tiktok', 'reels', 'youtube-shorts']
        if 'platform' in params and params['platform'].lower() not in valid_platforms:
            return False, f"Invalid platform. Must be one of: {', '.join(valid_platforms)}"
        
        # Validate tone if provided
        valid_tones = ['professional', 'casual', 'energetic', 'calm']
        if 'tone' in params and params['tone'].lower() not in valid_tones:
            return False, f"Invalid tone. Must be one of: {', '.join(valid_tones)}"
        
        # Validate duration if provided
        if 'duration' in params:
            duration = params['duration']
            if not isinstance(duration, int) or duration < 10 or duration > 60:
                return False, "duration must be between 10 and 60 seconds"
        
        # Validate n_scenes if provided
        if 'n_scenes' in params:
            n_scenes = params['n_scenes']
            if not isinstance(n_scenes, int) or n_scenes < self.config['min_scenes'] or n_scenes > self.config['max_scenes']:
                return False, f"n_scenes must be between {self.config['min_scenes']} and {self.config['max_scenes']}"
        
        return True, None
    
    def build_prompt(self, params: Dict[str, Any]) -> str:
        """Build AI prompt from parameters."""
        product_name = params['product_name']
        category = params['category']
        features = params['features']
        target_audience = params.get('target_audience', self.config['target_audience'])
        platform = params.get('platform', self.config['platform'])
        tone = params.get('tone', self.config['tone'])
        language = params.get('language', self.config['language'])
        duration = params.get('duration', self.config['duration'])
        n_scenes = params.get('n_scenes', self.config['n_scenes'])
        
        # Build optimized prompt
        prompt = f"""You are an expert video script writer for short-form content. Create an engaging video script.

Product: {product_name}
Category: {category}
Features: {features}
Target Audience: {target_audience}
Platform: {platform}
Tone: {tone}
Language: {language}
Duration: {duration} seconds
Scenes: {n_scenes}

Create a video script with:

1. **Title** (max {self.config['max_title_length']} chars) - catchy, clickable

2. **Hook** ({self.config['min_hook_duration']}-{self.config['max_hook_duration']} seconds) - CRITICAL! 50% drop off in first 3 seconds
   - Pattern interrupt or bold claim
   - Visual: What viewer sees
   - Text: What's said/shown

3. **Scenes** ({n_scenes} scenes, {self.config['min_scene_duration']}-{self.config['max_scene_duration']} seconds each)
   - Scene number
   - Visual: Detailed description of what's shown
   - Narration: Voiceover or on-screen text
   - Duration: Seconds for this scene
   - One idea per scene, show don't tell

4. **CTA** ({self.config['min_cta_duration']}-{self.config['max_cta_duration']} seconds) - Clear action
   - Visual: Product shot, price, button
   - Text: Specific action with urgency
   - Duration: Seconds

5. **Music Suggestion** - Genre, BPM, mood

6. **Hashtags** ({self.config['num_hashtags']} total) - Mix popular + niche

Platform guidelines:
- tiktok: Fast-paced, trending sounds, first 1-2 sec critical
- reels: High quality, Instagram music, first 3 sec critical
- youtube-shorts: SEO matters, up to 60 sec, first 3-5 sec critical

Tone: {tone}
Total duration must be approximately {duration} seconds (hook + scenes + cta)

Output JSON:
{{
  "title": "...",
  "hook": {{
    "text": "...",
    "visual": "...",
    "duration": {self.config['min_hook_duration']}
  }},
  "scenes": [
    {{
      "scene_number": 1,
      "visual": "...",
      "narration": "...",
      "duration": 5
    }}
  ],
  "cta": {{
    "text": "...",
    "visual": "...",
    "duration": {self.config['min_cta_duration']}
  }},
  "music_suggestion": "...",
  "hashtags": ["#...", "#...", "#...", "#...", "#..."]
}}"""
        
        return prompt
    
    def get_required_output_fields(self) -> list[str]:
        """Return required output fields."""
        return ['title', 'hook', 'scenes', 'cta', 'music_suggestion', 'hashtags']
    
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
        
        # 1. Title length
        if 'title' in content:
            title_length = len(content['title'])
            checks['title_length_ok'] = title_length <= self.config['max_title_length']
            if not checks['title_length_ok']:
                issues.append(f"Title too long: {title_length} chars (max {self.config['max_title_length']})")
        
        # 2. Hook validation
        if 'hook' in content and isinstance(content['hook'], dict):
            hook = content['hook']
            checks['hook_has_text'] = 'text' in hook and hook['text']
            checks['hook_has_visual'] = 'visual' in hook and hook['visual']
            checks['hook_has_duration'] = 'duration' in hook and isinstance(hook['duration'], (int, float))
            
            if not checks['hook_has_text']:
                issues.append("Hook missing text")
            if not checks['hook_has_visual']:
                issues.append("Hook missing visual description")
            if not checks['hook_has_duration']:
                issues.append("Hook missing duration")
            
            # Check hook duration
            if checks['hook_has_duration']:
                hook_duration = hook['duration']
                checks['hook_duration_ok'] = (
                    self.config['min_hook_duration'] <= hook_duration <= self.config['max_hook_duration']
                )
                if not checks['hook_duration_ok']:
                    issues.append(f"Hook duration: {hook_duration}s (need {self.config['min_hook_duration']}-{self.config['max_hook_duration']}s)")
        
        # 3. Scenes validation
        if 'scenes' in content and isinstance(content['scenes'], list):
            scenes_count = len(content['scenes'])
            checks['scenes_count_ok'] = (
                self.config['min_scenes'] <= scenes_count <= self.config['max_scenes']
            )
            if not checks['scenes_count_ok']:
                issues.append(f"Wrong number of scenes: {scenes_count} (need {self.config['min_scenes']}-{self.config['max_scenes']})")
            
            # Check each scene
            for i, scene in enumerate(content['scenes'], 1):
                has_visual = 'visual' in scene and scene['visual']
                has_narration = 'narration' in scene and scene['narration']
                has_duration = 'duration' in scene and isinstance(scene['duration'], (int, float))
                
                checks[f'scene_{i}_complete'] = has_visual and has_narration and has_duration
                if not checks[f'scene_{i}_complete']:
                    missing = []
                    if not has_visual: missing.append('visual')
                    if not has_narration: missing.append('narration')
                    if not has_duration: missing.append('duration')
                    issues.append(f"Scene {i} missing: {', '.join(missing)}")
                
                # Check scene duration
                if has_duration:
                    scene_duration = scene['duration']
                    checks[f'scene_{i}_duration_ok'] = (
                        self.config['min_scene_duration'] <= scene_duration <= self.config['max_scene_duration']
                    )
                    if not checks[f'scene_{i}_duration_ok']:
                        issues.append(f"Scene {i} duration: {scene_duration}s (need {self.config['min_scene_duration']}-{self.config['max_scene_duration']}s)")
        
        # 4. CTA validation
        if 'cta' in content and isinstance(content['cta'], dict):
            cta = content['cta']
            checks['cta_has_text'] = 'text' in cta and cta['text']
            checks['cta_has_visual'] = 'visual' in cta and cta['visual']
            checks['cta_has_duration'] = 'duration' in cta and isinstance(cta['duration'], (int, float))
            
            if not checks['cta_has_text']:
                issues.append("CTA missing text")
            if not checks['cta_has_visual']:
                issues.append("CTA missing visual description")
            if not checks['cta_has_duration']:
                issues.append("CTA missing duration")
            
            # Check CTA duration
            if checks['cta_has_duration']:
                cta_duration = cta['duration']
                checks['cta_duration_ok'] = (
                    self.config['min_cta_duration'] <= cta_duration <= self.config['max_cta_duration']
                )
                if not checks['cta_duration_ok']:
                    issues.append(f"CTA duration: {cta_duration}s (need {self.config['min_cta_duration']}-{self.config['max_cta_duration']}s)")
        
        # 5. Total duration check
        total_duration = 0
        if 'hook' in content and isinstance(content['hook'], dict):
            total_duration += content['hook'].get('duration', 0)
        if 'scenes' in content and isinstance(content['scenes'], list):
            total_duration += sum(s.get('duration', 0) for s in content['scenes'])
        if 'cta' in content and isinstance(content['cta'], dict):
            total_duration += content['cta'].get('duration', 0)
        
        target_duration = self.config.get('duration', 30)
        duration_diff = abs(total_duration - target_duration)
        checks['total_duration_ok'] = duration_diff <= self.config['duration_tolerance']
        if not checks['total_duration_ok']:
            issues.append(f"Total duration: {total_duration}s (target: {target_duration}s ±{self.config['duration_tolerance']}s)")
            suggestions.append("Adjust scene durations to match target duration")
        
        # 6. Hashtags validation
        if 'hashtags' in content and isinstance(content['hashtags'], list):
            hashtags_count = len(content['hashtags'])
            checks['hashtags_count_ok'] = hashtags_count == self.config['num_hashtags']
            if not checks['hashtags_count_ok']:
                issues.append(f"Wrong number of hashtags: {hashtags_count} (need {self.config['num_hashtags']})")
            
            # Check hashtags format
            invalid_hashtags = [h for h in content['hashtags'] if not h.startswith('#')]
            checks['hashtags_format_ok'] = len(invalid_hashtags) == 0
            if not checks['hashtags_format_ok']:
                issues.append(f"Hashtags must start with #: {', '.join(invalid_hashtags)}")
        
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
            'has_title': 10,
            'has_hook': 15,
            'has_scenes': 15,
            'has_cta': 15,
            'has_music_suggestion': 5,
            'has_hashtags': 5,
            'title_length_ok': 3,
            'hook_has_text': 5,
            'hook_has_visual': 3,
            'hook_has_duration': 2,
            'hook_duration_ok': 3,
            'scenes_count_ok': 5,
            'cta_has_text': 5,
            'cta_has_visual': 3,
            'cta_has_duration': 2,
            'cta_duration_ok': 3,
            'total_duration_ok': 5,
            'hashtags_count_ok': 2,
            'hashtags_format_ok': 2
        }
        
        # Add weights for each scene (up to 5 scenes)
        for i in range(1, 6):
            weights[f'scene_{i}_complete'] = 3
            weights[f'scene_{i}_duration_ok'] = 2
        
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
