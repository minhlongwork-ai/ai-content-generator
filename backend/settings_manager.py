"""Settings manager — Load/save API keys and model config from .env file."""

import os
from pathlib import Path
from typing import Optional

ENV_FILE = Path(".env")


def load_settings() -> dict:
    """Load all settings from .env file."""
    settings = {}
    
    if ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    settings[key] = value
    
    return settings


def save_settings(settings: dict):
    """Save settings to .env file, preserving comments and structure."""
    # Read existing file to preserve comments
    existing_lines = []
    if ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            existing_lines = f.readlines()
    
    # Build set of keys we're updating
    updated_keys = set(settings.keys())
    
    # Update existing lines
    new_lines = []
    for line in existing_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key, _, _ = stripped.partition("=")
            key = key.strip()
            if key in settings:
                value = settings[key]
                # Mask sensitive values in log
                new_lines.append(f'{key}={value}\n')
                updated_keys.discard(key)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Add any new keys that weren't in the file
    for key in updated_keys:
        new_lines.append(f'{key}={settings[key]}\n')
    
    with open(ENV_FILE, "w") as f:
        f.writelines(new_lines)
    
    # Reload environment variables
    from dotenv import load_dotenv
    load_dotenv(override=True)


def get_masked_settings() -> dict:
    """Get settings with API keys masked (for frontend display)."""
    settings = load_settings()
    masked = {}
    
    sensitive_keys = [
        "OPENROUTER_API_KEY",
        "FAL_API_KEY",
        "REPLICATE_API_KEY",
        "ELEVENLABS_API_KEY",
        "OPENAI_API_KEY",
        "NINEROUTER_API_KEY",
    ]
    
    for key, value in settings.items():
        if key in sensitive_keys and value:
            # Show first 8 chars and last 4 chars
            if len(value) > 12:
                masked[key] = value[:8] + "..." + value[-4:]
            else:
                masked[key] = "***"
        else:
            masked[key] = value
    
    return masked


def check_api_keys() -> dict:
    """Check which API keys are configured."""
    settings = load_settings()
    
    return {
        "openrouter": bool(settings.get("OPENROUTER_API_KEY")),
        "fal": bool(settings.get("FAL_API_KEY")),
        "replicate": bool(settings.get("REPLICATE_API_KEY")),
        "elevenlabs": bool(settings.get("ELEVENLABS_API_KEY")),
        "openai": bool(settings.get("OPENAI_API_KEY")),
        "9router": bool(settings.get("NINEROUTER_URL")),
    }
