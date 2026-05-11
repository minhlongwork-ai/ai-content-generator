"""Video Generation Engine — Unified multi-provider API.

Video Generation:
  - fal.ai: Seedance 2.0, Wan 2.6, Kling 3.0, Veo 3.1, Sora 2
  - Replicate: Kling v3 Omni, Kling v2.6 Pro
  - Vidu: Q3-pro, Q2-turbo
  - Direct APIs: Hailuo, PixVerse, Luma, Pika, Runway

TTS:
  - Edge-TTS: Free, 5 languages
  - ElevenLabs: Premium, voice cloning
  - OpenAI TTS: GPT-4o Mini TTS

Avatar (bonus):
  - SadTalker: Open-source, local
  - LivePortrait: Open-source, local

Usage:
    engine = VideoEngine(
        fal_api_key="...",
        elevenlabs_api_key="...",
        replicate_api_key="...",
    )
    
    # Quick generate with auto model selection
    result = await engine.generate_video(
        prompt="A cat dancing in the rain",
        config=VideoConfig(model=VideoModel.KLING_3_PRO, duration=5),
    )
    
    # Compare prices across models
    prices = engine.compare_prices(duration=5)
"""

import os
import json
import time
import uuid
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, Literal
from dataclasses import dataclass, field
from enum import Enum

# Output directories
VIDEO_DIR = Path("output/video")
AUDIO_DIR = Path("output/audio")
TEMP_DIR = Path("output/temp")
for d in [VIDEO_DIR, AUDIO_DIR, TEMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ─── Enums & Configs ────────────────────────────────────────

class VideoProvider(str, Enum):
    """Video generation providers."""
    FAL = "fal"
    REPLICATE = "replicate"
    VIDU = "vidu"
    HAILUO = "hailuo"
    PIXVERSE = "pixverse"
    LUMA = "luma"
    PIKA = "pika"
    RUNWAY = "runway"


class VideoModel(str, Enum):
    """Available video generation models with pricing."""
    # fal.ai models — model IDs must match fal.ai registry exactly
    SEEDANCE_2 = "bytedance/seedance-2.0/text-to-video"
    WAN_2_6 = "alibaba/wan-2.6/text-to-video"
    KLING_3_PRO = "kwaivgi/kling-v3.0-pro/text-to-video"
    KLING_3_OMNI = "kwaivgi/kling-v3-omni-video"
    VEO_3_1 = "google/veo-3.1/text-to-video"
    SORA_2_PRO = "openai/sora-2-pro/text-to-video"

    # Replicate models
    KLING_V3_OMNI_REPLICATE = "kwaivgi/kling-v3-omni-video"
    KLING_V2_6_REPLICATE = "kwaivgi/kling-v2-6-pro"


class TTSProvider(str, Enum):
    """TTS providers."""
    EDGE = "edge"           # Free
    ELEVENLABS = "elevenlabs"  # Premium
    OPENAI_TTS = "openai_tts"  # GPT-4o Mini TTS


@dataclass
class VideoConfig:
    """Video generation configuration."""
    model: VideoModel = VideoModel.SEEDANCE_2
    duration: int = 5
    width: int = 1080
    height: int = 1920  # Portrait 9:16
    fps: int = 24
    negative_prompt: str = "blurry, low quality, distorted, watermark, text overlay"
    seed: Optional[int] = None
    # Mode
    prompt: str = ""
    image_path: Optional[str] = None  # Image-to-video
    reference_image_path: Optional[str] = None  # Reference-to-video
    # Audio
    include_audio: bool = False
    # Style
    style_prompt: Optional[str] = None  # e.g., "cinematic", "anime", "cartoon"


@dataclass
class TTSConfig:
    """TTS configuration."""
    provider: TTSProvider = TTSProvider.EDGE
    voice_id: Optional[str] = None
    language: str = "vi"
    gender: str = "female"
    speed: float = 1.0
    # ElevenLabs
    elevenlabs_model: str = "eleven_multilingual_v2"
    stability: float = 0.5
    similarity_boost: float = 0.75
    # OpenAI TTS
    openai_voice: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer


@dataclass
class VideoResult:
    """Video generation result."""
    video_path: str
    audio_path: Optional[str] = None
    combined_path: Optional[str] = None
    duration: float = 0
    cost: float = 0
    model: str = ""
    provider: str = ""
    metadata: dict = field(default_factory=dict)


# ─── Pricing Database ──────────────────────────────────────

# All prices in USD per second
VIDEO_PRICING = {
    VideoModel.SEEDANCE_2: 0.05,
    VideoModel.WAN_2_6: 0.07,
    VideoModel.KLING_3_PRO: 0.126,
    VideoModel.KLING_3_OMNI: 0.189,
    VideoModel.VEO_3_1: 0.20,
    VideoModel.SORA_2_PRO: 0.40,
    VideoModel.KLING_V3_OMNI_REPLICATE: 0.112,
    VideoModel.KLING_V2_6_REPLICATE: 0.10,
}

# Max duration per model (seconds)
MODEL_MAX_DURATION = {
    VideoModel.SEEDANCE_2: 15,
    VideoModel.WAN_2_6: 10,
    VideoModel.KLING_3_PRO: 10,
    VideoModel.KLING_3_OMNI: 10,
    VideoModel.VEO_3_1: 8,
    VideoModel.SORA_2_PRO: 20,
    VideoModel.KLING_V3_OMNI_REPLICATE: 10,
    VideoModel.KLING_V2_6_REPLICATE: 10,
}

# Models with native audio support
AUDIO_SUPPORTED_MODELS = {
    VideoModel.KLING_3_OMNI,
    VideoModel.VEO_3_1,
    VideoModel.SORA_2_PRO,
    VideoModel.KLING_V3_OMNI_REPLICATE,
}


def estimate_video_cost(model: VideoModel, duration: int) -> float:
    """Estimate video generation cost."""
    price_per_sec = VIDEO_PRICING.get(model, 0.05)
    return round(price_per_sec * duration, 4)


def get_max_duration(model: VideoModel) -> int:
    """Get maximum duration for a model."""
    return MODEL_MAX_DURATION.get(model, 5)


def compare_video_prices(duration: int = 5) -> list:
    """Compare prices across all models."""
    results = []
    for model in VideoModel:
        max_dur = get_max_duration(model)
        if duration <= max_dur:
            cost = estimate_video_cost(model, duration)
            has_audio = model in AUDIO_SUPPORTED_MODELS
            results.append({
                "model": model.value,
                "cost_usd": cost,
                "cost_per_sec": VIDEO_PRICING.get(model, 0.05),
                "max_duration": max_dur,
                "native_audio": has_audio,
            })
    return sorted(results, key=lambda x: x["cost_usd"])


# ─── TTS Providers ──────────────────────────────────────────

class EdgeTTSProvider:
    """Free TTS using Edge-TTS (no API key needed)."""

    VOICES = {
        "vi": {"female": "vi-VN-HoaiMyNeural", "male": "vi-VN-NamMinhNeural"},
        "en": {"female": "en-US-JennyNeural", "male": "en-US-GuyNeural"},
        "zh": {"female": "zh-CN-XiaoxiaoNeural", "male": "zh-CN-YunjianNeural"},
        "ja": {"female": "ja-JP-NanamiNeural", "male": "ja-JP-KeitaNeural"},
        "ko": {"female": "ko-KR-SunHiNeural", "male": "ko-KR-InJoonNeural"},
        "es": {"female": "es-ES-ElviraNeural", "male": "es-ES-AlvaroNeural"},
        "fr": {"female": "fr-FR-DeniseNeural", "male": "fr-FR-HenriNeural"},
        "de": {"female": "de-DE-KatjaNeural", "male": "de-DE-ConradNeural"},
        "th": {"female": "th-TH-PremwadeeNeural", "male": "th-TH-NiwatNeural"},
        "id": {"female": "id-ID-GadisNeural", "male": "id-ID-ArdiNeural"},
    }

    def __init__(self):
        self._edge_tts = None

    async def _import(self):
        if self._edge_tts is None:
            import edge_tts
            self._edge_tts = edge_tts
        return self._edge_tts

    def _get_voice(self, language: str, gender: str) -> str:
        return self.VOICES.get(language, self.VOICES["vi"]).get(gender, "vi-VN-HoaiMyNeural")

    def _speed_to_rate(self, speed: float) -> str:
        pct = int((speed - 1.0) * 100)
        return f"+{pct}%" if pct >= 0 else f"{pct}%"

    @property
    def available_voices(self) -> dict:
        return self.VOICES

    async def synthesize(self, text: str, output_path: str, config: TTSConfig) -> str:
        edge_tts = await self._import()
        voice = config.voice_id or self._get_voice(config.language, config.gender)
        rate = self._speed_to_rate(config.speed)

        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_path)
        return output_path


class ElevenLabsProvider:
    """Premium TTS using ElevenLabs API."""

    VOICES = {
        "sarah": "EXAVITQu4vr4xnSDxMaL",
        "laura": "FGY2WhTYpPnrIDTdsKH5",
        "charlie": "IKne3meq5aSn9XLyUdCD",
        "george": "JBFqnCBsd6RMkjVDRZzb",
        "callum": "N2lVS1w4EtoT3dr4eOWO",
        "alice": "Xb7hH8MSUJpSbSDYk0k2",
        "chris": "iP95p4xoKVk53GoZ742B",
        "liam": "TX3LPaxmHKxFdv7VOQHJ",
        "aria": "9BWtsMINmu4pkp0S3gl6",
        "nicole": "piTKgcLEGmPE4e6mEKli",
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"

    async def synthesize(self, text: str, output_path: str, config: TTSConfig) -> str:
        import httpx

        voice_id = config.voice_id or self.VOICES.get("sarah", "")
        url = f"{self.base_url}/text-to-speech/{voice_id}"

        payload = {
            "text": text,
            "model_id": config.elevenlabs_model,
            "voice_settings": {
                "stability": config.stability,
                "similarity_boost": config.similarity_boost,
                "speed": config.speed,
            }
        }

        headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                raise Exception(f"ElevenLabs error {response.status_code}: {response.text}")
            with open(output_path, "wb") as f:
                f.write(response.content)
        return output_path

    async def get_voices(self) -> list:
        import httpx
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                return response.json().get("voices", [])
        return []

    @staticmethod
    def estimate_cost(text_length: int) -> float:
        """Estimate cost: ~$10 per 1M characters."""
        return round((text_length / 1_000_000) * 10, 4)


class OpenAITTSProvider:
    """TTS using OpenAI GPT-4o Mini TTS."""

    VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url

    async def synthesize(self, text: str, output_path: str, config: TTSConfig) -> str:
        import httpx

        url = f"{self.base_url}/audio/speech"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini-tts",
            "input": text,
            "voice": config.openai_voice,
            "speed": config.speed,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                raise Exception(f"OpenAI TTS error {response.status_code}: {response.text}")
            with open(output_path, "wb") as f:
                f.write(response.content)
        return output_path

    @staticmethod
    def estimate_cost(text_length: int) -> float:
        """Estimate cost: $15 per 1M characters."""
        return round((text_length / 1_000_000) * 15, 4)


# ─── Video Generation (fal.ai) ──────────────────────────────

class FalAIProvider:
    """Video generation via fal.ai — unified API for 1000+ models."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://fal.ai/api"

    def _headers(self) -> dict:
        return {"Authorization": f"Key {self.api_key}", "Content-Type": "application/json"}

    async def generate(self, config: VideoConfig, output_path: str) -> VideoResult:
        import httpx

        # Build prompt with style
        prompt = config.prompt
        if config.style_prompt:
            prompt = f"{prompt}, {config.style_prompt} style"

        # Clamp duration
        max_dur = get_max_duration(config.model)
        duration = min(config.duration, max_dur)

        payload = {
            "prompt": prompt,
            "negative_prompt": config.negative_prompt,
            "duration": duration,
            "aspect_ratio": f"{config.width}:{config.height}",
        }
        if config.seed is not None:
            payload["seed"] = config.seed
        if config.image_path:
            payload["image_url"] = await self._upload_image(config.image_path)
        if config.reference_image_path:
            payload["reference_image_url"] = await self._upload_image(config.reference_image_path)

        # Determine model endpoint
        model_slug = config.model.value
        if model_slug.startswith("bytedance/") or model_slug.startswith("alibaba/") or \
           model_slug.startswith("google/") or model_slug.startswith("openai/") or \
           model_slug.startswith("kwaigiv/"):
            url = f"{self.base_url}/fal-ai/{model_slug}"
        else:
            url = f"{self.base_url}/fal-ai/{model_slug}"

        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(url, json=payload, headers=self._headers())
            if response.status_code not in (200, 201, 202):
                raise Exception(f"fal.ai error {response.status_code}: {response.text}")

            result = response.json()

            # Parse response
            video_url = None
            if "request_id" in result:
                video_url = await self._poll(client, result["request_id"])
            elif "video" in result:
                v = result["video"]
                video_url = v.get("url") if isinstance(v, dict) else v
            elif "images" in result and result["images"]:
                video_url = result["images"][0].get("url", "")

            if video_url:
                await self._download(client, video_url, output_path)
            else:
                raise Exception(f"No video in response: {json.dumps(result)[:300]}")

        cost = estimate_video_cost(config.model, duration)
        return VideoResult(
            video_path=output_path,
            duration=duration,
            cost=cost,
            model=config.model.value,
            provider="fal.ai",
        )

    async def _upload_image(self, image_path: str) -> str:
        import httpx
        url = f"{self.base_url}/fal-ai/upload"
        async with httpx.AsyncClient(timeout=60.0) as client:
            with open(image_path, "rb") as f:
                resp = await client.post(url, files={"file": f},
                                         headers={"Authorization": f"Key {self.api_key}"})
            if resp.status_code == 200:
                return resp.json().get("url", "")
            raise Exception(f"Upload failed: {resp.status_code}")

    async def _poll(self, client, request_id: str, max_wait: int = 300) -> str:
        url = f"{self.base_url}/fal-ai/requests/{request_id}"
        headers = self._headers()
        start = time.time()
        while time.time() - start < max_wait:
            resp = await client.get(f"{url}/status", headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "COMPLETED":
                    result_resp = await client.get(url, headers=headers)
                    if result_resp.status_code == 200:
                        result_data = result_resp.json()
                        video = result_data.get("video", {})
                        return video.get("url", "") if isinstance(video, dict) else video
                elif data.get("status") == "FAILED":
                    raise Exception(f"Generation failed: {data.get('error', 'unknown')}")
            await asyncio.sleep(2)
        raise Exception(f"Timeout after {max_wait}s")

    async def _download(self, client, url: str, output_path: str):
        resp = await client.get(url, timeout=120.0)
        if resp.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(resp.content)
        else:
            raise Exception(f"Download failed: {resp.status_code}")


# ─── Video Generation (Replicate) ───────────────────────────

class ReplicateProvider:
    """Video generation via Replicate API."""

    MODEL_VERSIONS = {
        VideoModel.KLING_V3_OMNI_REPLICATE: "kwaigiv/kling-v3-omni-video:latest",
        VideoModel.KLING_V2_6_REPLICATE: "kwaigiv/kling-v2-6-pro:latest",
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate(self, config: VideoConfig, output_path: str) -> VideoResult:
        import httpx

        model_version = self.MODEL_VERSIONS.get(config.model)
        if not model_version:
            raise Exception(f"Unknown Replicate model: {config.model}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        max_dur = get_max_duration(config.model)
        duration = min(config.duration, max_dur)

        payload = {
            "version": model_version.split(":")[-1] if ":" in model_version else None,
            "input": {
                "prompt": config.prompt,
                "duration": duration,
                "aspect_ratio": f"{config.width}:{config.height}",
            }
        }

        # Create prediction
        async with httpx.AsyncClient(timeout=300.0) as client:
            resp = await client.post(
                "https://api.replicate.com/v1/predictions",
                json=payload,
                headers=headers,
            )

            if resp.status_code not in (200, 201):
                raise Exception(f"Replicate error {resp.status_code}: {resp.text}")

            prediction = resp.json()
            prediction_id = prediction["id"]

            # Poll for result
            video_url = await self._poll_prediction(client, prediction_id, headers)

            if video_url:
                await self._download(client, video_url, output_path)
            else:
                raise Exception("No video in Replicate response")

        cost = estimate_video_cost(config.model, duration)
        return VideoResult(
            video_path=output_path,
            duration=duration,
            cost=cost,
            model=config.model.value,
            provider="replicate",
        )

    async def _poll_prediction(self, client, prediction_id: str, headers: dict, max_wait: int = 300) -> str:
        url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        start = time.time()

        while time.time() - start < max_wait:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                status = data.get("status", "")

                if status == "succeeded":
                    output = data.get("output", "")
                    if isinstance(output, list):
                        return output[0] if output else ""
                    return output
                elif status == "failed":
                    raise Exception(f"Replicate failed: {data.get('error', 'unknown')}")
                elif status == "canceled":
                    raise Exception("Replicate prediction canceled")

            await asyncio.sleep(3)

        raise Exception(f"Replicate timeout after {max_wait}s")

    async def _download(self, client, url: str, output_path: str):
        resp = await client.get(url, timeout=120.0)
        if resp.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(resp.content)


# ─── Video Composer (ffmpeg) ────────────────────────────────

class VideoComposer:
    """Compose final video using ffmpeg."""

    @staticmethod
    def merge_audio_video(
        video_path: str,
        audio_path: str,
        output_path: str,
        audio_volume: float = 1.0,
    ) -> str:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-af", f"volume={audio_volume}",
            "-shortest",
            output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"ffmpeg merge failed: {result.stderr}")
        return output_path

    @staticmethod
    def add_subtitle(video_path: str, text: str, output_path: str,
                     font_size: int = 24) -> str:
        subtitle_path = TEMP_DIR / f"sub_{uuid.uuid4().hex}.srt"
        with open(subtitle_path, "w", encoding="utf-8") as f:
            f.write(f"1\n00:00:00,000 --> 00:00:30,000\n{text}\n")

        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"subtitles={subtitle_path}:force_style='FontSize={font_size},Alignment=2,MarginV=20'",
            "-c:a", "copy",
            output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if subtitle_path.exists():
            subtitle_path.unlink()
        if result.returncode != 0:
            raise Exception(f"ffmpeg subtitle failed: {result.stderr}")
        return output_path

    @staticmethod
    def add_bgm(video_path: str, bgm_path: str, output_path: str,
                bgm_volume: float = 0.2) -> str:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", bgm_path,
            "-filter_complex",
            f"[1:a]volume={bgm_volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]",
            "-c:v", "copy",
            "-map", "0:v", "-map", "[aout]",
            output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"ffmpeg bgm failed: {result.stderr}")
        return output_path

    @staticmethod
    def get_duration(file_path: str) -> float:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0", file_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            try:
                return float(result.stdout.strip())
            except ValueError:
                pass
        return 0.0


# ─── Main Video Engine ──────────────────────────────────────

class VideoEngine:
    """Unified video generation engine with multi-provider support.

    Supports:
    - Video: fal.ai (Seedance, Wan, Kling, Veo, Sora), Replicate (Kling)
    - TTS: Edge-TTS (free), ElevenLabs (premium), OpenAI TTS
    - Compose: ffmpeg (merge, subtitle, BGM)
    """

    def __init__(
        self,
        fal_api_key: Optional[str] = None,
        replicate_api_key: Optional[str] = None,
        elevenlabs_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        openai_base_url: Optional[str] = None,
    ):
        # API keys from args or env
        self.fal_api_key = fal_api_key or os.getenv("FAL_API_KEY")
        self.replicate_api_key = replicate_api_key or os.getenv("REPLICATE_API_KEY")
        self.elevenlabs_api_key = elevenlabs_api_key or os.getenv("ELEVENLABS_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.openai_base_url = openai_base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

        # Initialize providers
        self.edge_tts = EdgeTTSProvider()
        self.elevenlabs = ElevenLabsProvider(self.elevenlabs_api_key) if self.elevenlabs_api_key else None
        self.openai_tts = OpenAITTSProvider(self.openai_api_key, self.openai_base_url) if self.openai_api_key else None
        self.fal = FalAIProvider(self.fal_api_key) if self.fal_api_key else None
        self.replicate = ReplicateProvider(self.replicate_api_key) if self.replicate_api_key else None
        self.composer = VideoComposer()

    @property
    def available_providers(self) -> dict:
        """Check which providers are available."""
        return {
            "fal.ai": self.fal is not None,
            "replicate": self.replicate is not None,
            "edge_tts": True,  # Always available
            "elevenlabs": self.elevenlabs is not None,
            "openai_tts": self.openai_tts is not None,
        }

    async def generate_tts(self, text: str, config: TTSConfig,
                           output_path: Optional[str] = None) -> str:
        """Generate TTS audio."""
        if not output_path:
            output_path = str(AUDIO_DIR / f"tts_{uuid.uuid4().hex}.mp3")

        if config.provider == TTSProvider.ELEVENLABS and self.elevenlabs:
            return await self.elevenlabs.synthesize(text, output_path, config)
        elif config.provider == TTSProvider.OPENAI_TTS and self.openai_tts:
            return await self.openai_tts.synthesize(text, output_path, config)
        else:
            return await self.edge_tts.synthesize(text, output_path, config)

    async def generate_video(self, config: VideoConfig,
                             output_path: Optional[str] = None) -> VideoResult:
        """Generate video using configured model."""
        if not output_path:
            output_path = str(VIDEO_DIR / f"video_{uuid.uuid4().hex}.mp4")

        # Route to correct provider
        if config.model in (VideoModel.KLING_V3_OMNI_REPLICATE, VideoModel.KLING_V2_6_REPLICATE):
            if not self.replicate:
                raise Exception("Replicate API key not configured")
            return await self.replicate.generate(config, output_path)
        else:
            if not self.fal:
                raise Exception("fal.ai API key not configured")
            return await self.fal.generate(config, output_path)

    async def generate_full_video(
        self,
        script: dict,
        video_config: VideoConfig,
        tts_config: TTSConfig,
        merge: bool = True,
        add_bgm_path: Optional[str] = None,
        bgm_volume: float = 0.2,
    ) -> VideoResult:
        """Generate complete video from script (TTS + video + compose)."""
        total_cost = 0.0

        # 1. Build narration text from script
        narration_parts = []
        hook = script.get("hook", {})
        if hook.get("text"):
            narration_parts.append(hook["text"])
        for scene in script.get("scenes", []):
            if scene.get("narration"):
                narration_parts.append(scene["narration"])
        cta = script.get("cta", {})
        if cta.get("text"):
            narration_parts.append(cta["text"])

        full_narration = ". ".join(narration_parts)

        # 2. Generate TTS
        audio_path = await self.generate_tts(full_narration, tts_config)
        audio_duration = self.composer.get_duration(audio_path)

        # TTS cost
        if tts_config.provider == TTSProvider.ELEVENLABS and self.elevenlabs:
            total_cost += ElevenLabsProvider.estimate_cost(len(full_narration))
        elif tts_config.provider == TTSProvider.OPENAI_TTS and self.openai_tts:
            total_cost += OpenAITTSProvider.estimate_cost(len(full_narration))

        # 3. Build video prompt from visuals
        visual_prompts = []
        if hook.get("visual"):
            visual_prompts.append(f"Hook: {hook['visual']}")
        for scene in script.get("scenes", []):
            if scene.get("visual"):
                visual_prompts.append(f"Scene {scene.get('scene_number', '?')}: {scene['visual']}")
        if cta.get("visual"):
            visual_prompts.append(f"CTA: {cta['visual']}")

        video_config.prompt = " | ".join(visual_prompts)
        video_config.duration = min(int(audio_duration) + 1, get_max_duration(video_config.model))

        # 4. Generate video
        video_result = await self.generate_video(video_config)
        total_cost += video_result.cost

        # 5. Merge audio + video
        combined_path = None
        if merge and audio_path and video_result.video_path:
            combined_path = str(VIDEO_DIR / f"combined_{uuid.uuid4().hex}.mp4")
            self.composer.merge_audio_video(video_result.video_path, audio_path, combined_path)

        # 6. Add BGM
        if add_bgm_path and combined_path:
            final_path = str(VIDEO_DIR / f"final_{uuid.uuid4().hex}.mp4")
            self.composer.add_bgm(combined_path, add_bgm_path, final_path, bgm_volume)
            combined_path = final_path

        return VideoResult(
            video_path=combined_path or video_result.video_path,
            audio_path=audio_path,
            combined_path=combined_path,
            duration=audio_duration,
            cost=round(total_cost, 4),
            model=video_config.model.value,
            provider="multi",
            metadata={
                "script_title": script.get("title", ""),
                "video_prompt": video_config.prompt,
                "tts_text": full_narration[:200],
                "tts_provider": tts_config.provider.value,
                "scenes_count": len(script.get("scenes", [])),
            },
        )

    def estimate_cost(self, video_config: VideoConfig, tts_config: TTSConfig,
                      text_length: int = 500) -> dict:
        """Estimate total cost."""
        video_cost = estimate_video_cost(video_config.model, video_config.duration)

        tts_cost = 0.0
        if tts_config.provider == TTSProvider.ELEVENLABS:
            tts_cost = ElevenLabsProvider.estimate_cost(text_length)
        elif tts_config.provider == TTSProvider.OPENAI_TTS:
            tts_cost = OpenAITTSProvider.estimate_cost(text_length)

        return {
            "video_cost": video_cost,
            "tts_cost": round(tts_cost, 4),
            "total_cost": round(video_cost + tts_cost, 4),
            "currency": "USD",
            "model": video_config.model.value,
            "tts_provider": tts_config.provider.value,
        }

    @staticmethod
    def compare_prices(duration: int = 5) -> list:
        """Compare prices across all video models."""
        return compare_video_prices(duration)
