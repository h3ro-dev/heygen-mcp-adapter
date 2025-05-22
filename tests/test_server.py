import httpx
import pytest
from fastapi.testclient import TestClient

from server import app, video_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_store():
    video_store.clear()
    yield
    video_store.clear()


def test_generate_and_status_success(monkeypatch):
    async def mock_create(req):
        return {"video_url": "http://example.com/out.mp4"}

    monkeypatch.setattr("server.create_video_with_heygen", mock_create)

    payload = {"script_text": "hello", "avatar_id": "a1", "voice_id": "v1"}
    resp = client.post("/video/generate", json=payload)
    assert resp.status_code == 202
    body = resp.json()
    video_id = body["video_id"]
    assert body["status"] == "COMPLETE"

    status_resp = client.get(f"/video/{video_id}/status")
    assert status_resp.status_code == 200
    status_body = status_resp.json()
    assert status_body["status"] == "COMPLETE"
    assert status_body["video_url"] == "http://example.com/out.mp4"
    assert status_body["error_message"] is None


def test_generate_error(monkeypatch):
    async def mock_create(req):
        raise httpx.HTTPError("boom")

    monkeypatch.setattr("server.create_video_with_heygen", mock_create)

    payload = {"script_text": "bad", "avatar_id": "a1", "voice_id": "v1"}
    resp = client.post("/video/generate", json=payload)
    assert resp.status_code == 202
    body = resp.json()
    video_id = body["video_id"]
    assert body["status"] == "ERROR"

    status_resp = client.get(f"/video/{video_id}/status")
    assert status_resp.status_code == 200
    status_body = status_resp.json()
    assert status_body["status"] == "ERROR"
    assert status_body["error_message"] == "boom"


def test_unknown_video_status():
    resp = client.get("/video/does-not-exist/status")
    assert resp.status_code == 404
