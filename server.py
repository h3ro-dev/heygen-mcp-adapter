from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from uuid import uuid4
from sqlalchemy import Column, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

engine = create_engine(
    "sqlite:///./videos.db", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
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


class Video(Base):
    __tablename__ = "videos"

    video_id = Column(String, primary_key=True, index=True)
    status = Column(String, default="PENDING")
    video_url = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.post("/video/generate", status_code=202)
async def generate_video(req: VideoRequest, db: Session = Depends(get_db)):
    video_id = f"video_{uuid4().hex}"
    video = Video(video_id=video_id, status="PENDING")
    db.add(video)
    db.commit()
    db.refresh(video)
    # TODO: integrate with HeyGen API for actual video generation
    return {"video_id": video_id, "status": video.status}


@app.get("/video/{video_id}/status", response_model=VideoStatus)
async def get_video_status(video_id: str, db: Session = Depends(get_db)):
    video = db.get(Video, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video ID not found.")
    return {
        "video_id": video.video_id,
        "status": video.status,
        "video_url": video.video_url,
        "error_message": video.error_message,
    }


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

    result = await hg_get_video_status(video_id)
    if result.get("status") == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="Video ID not found.")
    return result
