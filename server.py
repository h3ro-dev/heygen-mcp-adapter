from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
