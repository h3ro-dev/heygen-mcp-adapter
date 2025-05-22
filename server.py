from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from uuid import uuid4

app = FastAPI(title="HeyGen MCP Adapter API")


class VideoRequest(BaseModel):
    script_text: str = Field(
        ..., min_length=1, max_length=5000, description="The script content for the video."
    )
    avatar_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9_-]+$",
        description="The ID of the HeyGen avatar to use.",
    )
    voice_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9_-]+$",
        description="The ID of the HeyGen voice to use.",
    )


class VideoStatus(BaseModel):
    video_id: str
    status: str
    video_url: Optional[HttpUrl] = None
    error_message: Optional[str] = None


video_store: dict[str, dict] = {}


@app.post("/video/generate", status_code=202)
async def generate_video(req: VideoRequest):
    try:
        video_id = f"video_{uuid4().hex}"
        video_store[video_id] = {"status": "PENDING"}
        # TODO: integrate with HeyGen API for actual video generation
        return {"video_id": video_id, "status": "PENDING"}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to initiate video generation.") from exc


@app.get("/video/{video_id}/status", response_model=VideoStatus)
async def get_video_status(video_id: str):
    try:
        data = video_store.get(video_id)
        if data is None:
            raise HTTPException(status_code=404, detail="Video ID not found.")
        return {
            "video_id": video_id,
            "status": data.get("status", "PENDING"),
            "video_url": data.get("video_url"),
            "error_message": data.get("error_message"),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to retrieve video status.") from exc
