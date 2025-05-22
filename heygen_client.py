import os
from typing import Any, Dict

import httpx

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
HEYGEN_BASE_URL = os.getenv("HEYGEN_BASE_URL", "https://api.heygen.com/v1")

if HEYGEN_API_KEY is None:
    raise RuntimeError("HEYGEN_API_KEY environment variable not set")

async def generate_video(script_text: str, avatar_id: str, voice_id: str) -> str:
    """Submit a video generation request to HeyGen and return the HeyGen video ID."""
    url = f"{HEYGEN_BASE_URL}/videos/generate"
    payload = {
        "script": script_text,
        "avatar_id": avatar_id,
        "voice_id": voice_id,
    }
    headers = {
        "Authorization": f"Bearer {HEYGEN_API_KEY}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("video_id")

async def get_video_status(video_id: str) -> Dict[str, Any]:
    """Fetch status information for a HeyGen video."""
    url = f"{HEYGEN_BASE_URL}/videos/{video_id}"
    headers = {
        "Authorization": f"Bearer {HEYGEN_API_KEY}",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, timeout=15)
        if resp.status_code == 404:
            return {"video_id": video_id, "status": "NOT_FOUND"}
        resp.raise_for_status()
        data = resp.json()
        return {
            "video_id": video_id,
            "status": data.get("status"),
            "video_url": data.get("video_url"),
            "error_message": data.get("error_message"),
        }
