"""TTS (Text-to-Speech) service using Edge-TTS.
Free, no API key required, supports multiple languages.
"""

import asyncio
import uuid
import os
from pathlib import Path
from typing import Optional

# Audio output directory
AUDIO_DIR = Path("output/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


# Common Edge-TTS voices by language
VOICES = {
    "en": {
        "female": "en-US-JennyNeural",
        "male": "en-US-GuyNeural",
    },
    "vi": {
        "female": "vi-VN-HoaiMyNeural",
        "male": "vi-VN-NamMinhNeural",
    },
    "zh": {
        "female": "zh-CN-XiaoxiaoNeural",
        "male": "zh-CN-YunjianNeural",
    },
    "ja": {
        "female": "ja-JP-NanamiNeural",
        "male": "ja-JP-KeitaNeural",
    },
    "ko": {
        "female": "ko-KR-SunHiNeural",
        "male": "ko-KR-InJoonNeural",
    },
}

# Default voice
DEFAULT_VOICE = "vi-VN-HoaiMyNeural"


def _get_voice(language: str = "vi", gender: str = "female") -> str:
    """Get voice ID by language and gender."""
    lang_voices = VOICES.get(language, VOICES["vi"])
    return lang_voices.get(gender, DEFAULT_VOICE)


def _speed_to_rate(speed: float) -> str:
    """Convert speed multiplier to Edge-TTS rate string.
    
    Args:
        speed: Speed multiplier (0.5-2.0, 1.0 = normal)
    
    Returns:
        Rate string like "+20%" or "-10%"
    """
    percentage = int((speed - 1.0) * 100)
    if percentage >= 0:
        return f"+{percentage}%"
    else:
        return f"{percentage}%"


async def generate_audio(
    text: str,
    voice: Optional[str] = None,
    language: str = "vi",
    gender: str = "female",
    speed: float = 1.0,
    output_path: Optional[str] = None,
) -> str:
    """Generate audio from text using Edge-TTS.
    
    Args:
        text: Text to convert to speech
        voice: Voice ID (auto-selected from language/gender if not provided)
        language: Language code (en, vi, zh, ja, ko)
        gender: Voice gender (female, male)
        speed: Speech speed (0.5-2.0, 1.0 = normal)
        output_path: Custom output path (auto-generated if None)
    
    Returns:
        Path to generated audio file
    
    Raises:
        ImportError: If edge-tts is not installed
        RuntimeError: If TTS generation fails
    """
    try:
        import edge_tts
    except ImportError:
        raise ImportError(
            "edge-tts is required. Install with: pip install edge-tts==7.2.7"
        )
    
    # Select voice
    final_voice = voice or _get_voice(language, gender)
    
    # Convert speed to rate
    rate = _speed_to_rate(speed)
    
    # Generate output path
    if not output_path:
        filename = f"{uuid.uuid4().hex}.mp3"
        output_path = str(AUDIO_DIR / filename)
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Generate audio
    try:
        communicate = edge_tts.Communicate(text, final_voice, rate=rate)
        await communicate.save(output_path)
        return output_path
    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {e}")


async def generate_audio_from_script(
    script: dict,
    voice: Optional[str] = None,
    language: str = "vi",
    gender: str = "female",
    speed: float = 1.0,
) -> dict:
    """Generate audio from a video script.
    
    Generates separate audio for hook, each scene narration, and CTA.
    Also generates a combined full narration audio.
    
    Args:
        script: Video script dict from LLM
        voice: Voice ID
        language: Language code
        gender: Voice gender
        speed: Speech speed
    
    Returns:
        Dict with audio paths:
        {
            "full_narration": "path/to/full.mp3",
            "hook": "path/to/hook.mp3",
            "scenes": [
                {"scene_number": 1, "audio": "path/to/scene1.mp3", "duration": 5},
                ...
            ],
            "cta": "path/to/cta.mp3",
            "total_duration": 30.5  # seconds (estimated from audio)
        }
    """
    result = {
        "full_narration": None,
        "hook": None,
        "scenes": [],
        "cta": None,
        "total_duration": 0,
    }
    
    # Build full narration text
    full_text_parts = []
    
    # Hook audio
    hook_text = script.get("hook", {}).get("text", "")
    if hook_text:
        hook_path = await generate_audio(
            text=hook_text,
            voice=voice,
            language=language,
            gender=gender,
            speed=speed,
        )
        result["hook"] = hook_path
        full_text_parts.append(hook_text)
    
    # Scene audios
    scenes = script.get("scenes", [])
    total_duration = 0
    
    for scene in scenes:
        narration = scene.get("narration", "")
        duration = scene.get("duration", 5)
        scene_num = scene.get("scene_number", 0)
        
        if narration:
            scene_path = await generate_audio(
                text=narration,
                voice=voice,
                language=language,
                gender=gender,
                speed=speed,
            )
            result["scenes"].append({
                "scene_number": scene_num,
                "audio": scene_path,
                "duration": duration,
            })
            full_text_parts.append(narration)
            total_duration += duration
    
    # CTA audio
    cta_text = script.get("cta", {}).get("text", "")
    if cta_text:
        cta_path = await generate_audio(
            text=cta_text,
            voice=voice,
            language=language,
            gender=gender,
            speed=speed,
        )
        result["cta"] = cta_path
        full_text_parts.append(cta_text)
        cta_duration = script.get("cta", {}).get("duration", 3)
        total_duration += cta_duration
    
    # Hook duration
    hook_duration = script.get("hook", {}).get("duration", 3)
    total_duration += hook_duration
    
    result["total_duration"] = total_duration
    
    # Generate full narration (combined)
    if full_text_parts:
        full_text = ". ".join(full_text_parts)
        full_path = await generate_audio(
            text=full_text,
            voice=voice,
            language=language,
            gender=gender,
            speed=speed,
        )
        result["full_narration"] = full_path
    
    return result


def get_available_voices() -> dict:
    """Get available voices grouped by language."""
    return VOICES


def delete_audio(audio_path: str) -> bool:
    """Delete an audio file.
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        True if deleted, False if not found
    """
    try:
        path = Path(audio_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception:
        return False
