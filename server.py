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
    script_text: str
    avatar_id: str
    voice_id: str


class VideoStatus(BaseModel):
    video_id: str
    status: str
    video_url: str | None = None
    error_message: str | None = None


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
