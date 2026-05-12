"""Skill loader and manager.

Handles loading, caching, and managing skills.
"""

from typing import Dict, Any, Optional, Type
from pathlib import Path
import importlib.util
import sys

from skills.base_skill import BaseSkill


class SkillLoader:
    """Load and manage content generation skills."""
    
    def __init__(self):
        self.skills_cache: Dict[str, Type[BaseSkill]] = {}
        self.skills_dir = Path(__file__).parent / "content"
    
    def load_skill(self, skill_name: str) -> Optional[Type[BaseSkill]]:
        """Load a skill class by name.
        
        Args:
            skill_name: Name of skill (e.g., 'product-description')
            
        Returns:
            Skill class or None if not found
        """
        # Check cache first
        if skill_name in self.skills_cache:
            return self.skills_cache[skill_name]
        
        # Convert skill-name to skill_name for directory
        skill_dir_name = skill_name.replace('-', '_')
        skill_path = self.skills_dir / skill_dir_name / "skill.py"
        
        if not skill_path.exists():
            return None
        
        # Load module dynamically
        try:
            spec = importlib.util.spec_from_file_location(
                f"skills.content.{skill_dir_name}",
                skill_path
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = module
                spec.loader.exec_module(module)
                
                # Find the skill class (should inherit from BaseSkill)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, BaseSkill) and 
                        attr is not BaseSkill):
                        self.skills_cache[skill_name] = attr
                        return attr
        except Exception as e:
            print(f"Error loading skill {skill_name}: {e}")
            return None
        
        return None
    
    def list_skills(self) -> list[Dict[str, Any]]:
        """List all available skills.
        
        Returns:
            List of skill metadata dicts
        """
        skills = []
        
        if not self.skills_dir.exists():
            return skills
        
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            
            skill_name = skill_dir.name.replace('_', '-')
            skill_class = self.load_skill(skill_name)
            
            if skill_class:
                # Instantiate to get metadata
                skill_instance = skill_class()
                metadata = skill_instance.get_skill_metadata()
                metadata['config'] = skill_instance.get_default_config()
                skills.append(metadata)
        
        return skills
    
    def get_skill_instance(
        self, 
        skill_name: str, 
        user_config: Optional[Dict[str, Any]] = None
    ) -> Optional[BaseSkill]:
        """Get an instance of a skill with optional user config.
        
        Args:
            skill_name: Name of skill
            user_config: User-specific configuration overrides
            
        Returns:
            Skill instance or None if not found
        """
        skill_class = self.load_skill(skill_name)
        if not skill_class:
            return None
        
        return skill_class(user_config=user_config)


# Global skill loader instance
_skill_loader = SkillLoader()


def load_skill(skill_name: str, user_config: Optional[Dict[str, Any]] = None) -> Optional[BaseSkill]:
    """Load a skill instance.
    
    Args:
        skill_name: Name of skill (e.g., 'product-description')
        user_config: Optional user configuration overrides
        
    Returns:
        Skill instance or None if not found
    """
    return _skill_loader.get_skill_instance(skill_name, user_config)


def list_skills() -> list[Dict[str, Any]]:
    """List all available skills.
    
    Returns:
        List of skill metadata
    """
    return _skill_loader.list_skills()
