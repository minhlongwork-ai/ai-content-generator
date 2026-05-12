"""Base skill class for AI Content Generator.

Inspired by anthropics/financial-services skill architecture.
All content generation skills inherit from this base class.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json


class BaseSkill(ABC):
    """Base class for all content generation skills.
    
    Each skill defines:
    - Input validation rules
    - Generation logic
    - Quality checks
    - Default configuration
    """
    
    def __init__(self, user_config: Optional[Dict[str, Any]] = None):
        """Initialize skill with optional user configuration.
        
        Args:
            user_config: User-specific overrides for default config
        """
        self.default_config = self.get_default_config()
        self.user_config = user_config or {}
        self.config = {**self.default_config, **self.user_config}
    
    @abstractmethod
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration for this skill.
        
        Example:
            {
                'tone': 'professional',
                'length': 1200,
                'language': 'English',
                'quality_threshold': 70
            }
        """
        pass
    
    @abstractmethod
    def get_skill_metadata(self) -> Dict[str, Any]:
        """Return skill metadata.
        
        Returns:
            {
                'name': 'product-description',
                'description': 'Generate product descriptions',
                'category': 'e-commerce',
                'version': '1.0',
                'required_inputs': ['product_name', 'category', 'features'],
                'optional_inputs': ['target_audience', 'tone', 'language']
            }
        """
        pass
    
    @abstractmethod
    def validate_input(self, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate input parameters.
        
        Args:
            params: Input parameters from user
            
        Returns:
            (is_valid, error_message)
            
        Example:
            if 'product_name' not in params:
                return False, "Missing required field: product_name"
            return True, None
        """
        pass
    
    @abstractmethod
    def build_prompt(self, params: Dict[str, Any]) -> str:
        """Build AI prompt from parameters and config.
        
        This is where the skill's expertise lives - the prompt template
        that produces high-quality output.
        
        Args:
            params: Validated input parameters
            
        Returns:
            Formatted prompt string
        """
        pass
    
    def check_quality(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Check quality of generated content.
        
        Override this in subclasses for skill-specific checks.
        Base implementation provides common checks.
        
        Args:
            content: Generated content (parsed JSON)
            
        Returns:
            {
                'score': 85,  # 0-100
                'passed': True,
                'checks': {
                    'has_required_fields': True,
                    'word_count': 1247,
                    'readability': 68,
                    'seo_score': 82
                },
                'issues': [],
                'suggestions': []
            }
        """
        checks = {}
        issues = []
        suggestions = []
        
        # Check if content is dict
        if not isinstance(content, dict):
            return {
                'score': 0,
                'passed': False,
                'checks': {},
                'issues': ['Content is not a valid JSON object'],
                'suggestions': ['Ensure AI returns valid JSON']
            }
        
        # Check for required fields (override in subclass)
        required_fields = self.get_required_output_fields()
        for field in required_fields:
            has_field = field in content and content[field]
            checks[f'has_{field}'] = has_field
            if not has_field:
                issues.append(f'Missing required field: {field}')
        
        # Calculate overall score
        score = self.calculate_quality_score(content, checks)
        threshold = self.config.get('quality_threshold', 70)
        
        return {
            'score': score,
            'passed': score >= threshold,
            'checks': checks,
            'issues': issues,
            'suggestions': suggestions
        }
    
    def get_required_output_fields(self) -> list[str]:
        """Return list of required output fields.
        
        Override in subclass.
        """
        return []
    
    def calculate_quality_score(self, content: Dict[str, Any], checks: Dict[str, Any]) -> int:
        """Calculate overall quality score (0-100).
        
        Override in subclass for custom scoring logic.
        """
        if not checks:
            return 50
        
        # Simple average of boolean checks
        passed_checks = sum(1 for v in checks.values() if v is True)
        total_checks = len(checks)
        
        if total_checks == 0:
            return 50
        
        return int((passed_checks / total_checks) * 100)
    
    def improve_content(self, content: Dict[str, Any], quality_report: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to improve content based on quality issues.
        
        Override in subclass for skill-specific improvements.
        
        Args:
            content: Original content
            quality_report: Quality check results
            
        Returns:
            Improved content (or original if no improvements possible)
        """
        # Base implementation: return as-is
        # Subclasses can implement auto-fixes
        return content
    
    async def generate(self, params: Dict[str, Any], ai_client) -> Dict[str, Any]:
        """Main generation method - orchestrates the full workflow.
        
        1. Validate input
        2. Build prompt
        3. Call AI
        4. Parse response
        5. Check quality
        6. Improve if needed
        7. Return result
        
        Args:
            params: Input parameters
            ai_client: AIClient instance for calling LLM
            
        Returns:
            {
                'success': True,
                'content': {...},
                'quality_report': {...},
                'model': 'gpt-4',
                'metadata': {...}
            }
        """
        # Step 1: Validate
        is_valid, error = self.validate_input(params)
        if not is_valid:
            return {
                'success': False,
                'error': error,
                'skill': self.get_skill_metadata()['name']
            }
        
        # Step 2: Build prompt
        prompt = self.build_prompt(params)
        
        # Step 3: Call AI (using existing ai_client)
        # Note: ai_client.generate() expects content_type, but we'll call it directly
        # We need to modify this to work with existing AIClient
        
        # For now, return the prompt - we'll integrate with AIClient next
        return {
            'success': True,
            'prompt': prompt,
            'config': self.config,
            'skill': self.get_skill_metadata()['name'],
            'note': 'Skill system ready - integration with AIClient pending'
        }
    
    def get_template(self, template_name: str = 'default') -> Optional[str]:
        """Load a template file for this skill.
        
        Templates live in skills/content/{skill_name}/templates/
        
        Args:
            template_name: Template filename (without extension)
            
        Returns:
            Template content or None if not found
        """
        # Implementation will load from filesystem
        # For now, return None
        return None
    
    def get_reference(self, reference_name: str) -> Optional[str]:
        """Load a reference document for this skill.
        
        References live in skills/content/{skill_name}/references/
        
        Args:
            reference_name: Reference filename
            
        Returns:
            Reference content or None if not found
        """
        # Implementation will load from filesystem
        # For now, return None
        return None
