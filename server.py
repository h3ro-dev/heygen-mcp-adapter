import os
from fastapi import FastAPI, HTTPException, Header, Depends, status
from pydantic import BaseModel
from uuid import uuid4

API_TOKEN = os.getenv("API_TOKEN", "dev-token")

app = FastAPI(title="HeyGen MCP Adapter API")


def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    token = authorization.removeprefix("Bearer ").strip()
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


class VideoRequest(BaseModel):
    script_text: str
    avatar_id: str
    voice_id: str


class VideoStatus(BaseModel):
    video_id: str
    status: str
    video_url: str | None = None
    error_message: str | None = None


video_store: dict[str, dict] = {}


@app.post("/video/generate", status_code=202, dependencies=[Depends(verify_token)])
async def generate_video(req: VideoRequest):
    video_id = f"video_{uuid4().hex}"
    video_store[video_id] = {"status": "PENDING"}
    # TODO: integrate with HeyGen API for actual video generation
    return {"video_id": video_id, "status": "PENDING"}


@app.get("/video/{video_id}/status", response_model=VideoStatus, dependencies=[Depends(verify_token)])
async def get_video_status(video_id: str):
    data = video_store.get(video_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Video ID not found.")
    return {
        "video_id": video_id,
        "status": data.get("status", "PENDING"),
        "video_url": data.get("video_url"),
        "error_message": data.get("error_message"),
    }
