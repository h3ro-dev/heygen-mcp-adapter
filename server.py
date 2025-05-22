from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import httpx


async def create_video_with_heygen(req: "VideoRequest") -> dict:
    """Send the video generation request to HeyGen.

    This function is a thin wrapper around the HeyGen API. It will be mocked in
    tests. In a real implementation it would authenticate and send the request
    to the HeyGen service.
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.heygen.com/v1/videos", json=req.dict()
        )
        response.raise_for_status()
        return response.json()

from heygen_client import generate_video as hg_generate_video, get_video_status as hg_get_video_status

app = FastAPI(title="HeyGen MCP Adapter API")


class VideoRequest(BaseModel):
    script_text: str
    avatar_id: str
    voice_id: str


class VideoStatus(BaseModel):
    video_id: str
    status: str
    video_url: str | None = None
    error_message: str | None = None




@app.post("/video/generate", status_code=202)
async def generate_video(req: VideoRequest):
    video_id = f"video_{uuid4().hex}"
    video_store[video_id] = {"status": "PENDING"}
    try:
        data = await create_video_with_heygen(req)
        video_store[video_id].update(
            {"status": "COMPLETE", "video_url": data.get("video_url")}
        )
    except Exception as exc:  # pragma: no cover - defensive programming
        video_store[video_id].update({"status": "ERROR", "error_message": str(exc)})
    return {"video_id": video_id, "status": video_store[video_id]["status"]}
    try:
        video_id = await hg_generate_video(req.script_text, req.avatar_id, req.voice_id)
    except Exception as exc:  # httpx.HTTPError etc.
        raise HTTPException(status_code=500, detail="Failed to initiate video generation") from exc
    return {"video_id": video_id, "status": "PENDING"}


@app.get("/video/{video_id}/status", response_model=VideoStatus)
async def get_video_status(video_id: str):
    result = await hg_get_video_status(video_id)
    if result.get("status") == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="Video ID not found.")
    return result
