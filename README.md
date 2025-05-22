# HeyGen MCP Adapter

This project provides a simple REST API for generating videos through HeyGen and checking their status.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   uvicorn server:app --reload
   ```

The API will be available at `http://localhost:8000`.

Refer to `openapi.yaml` for the API specification.

## Authentication

Set the `API_TOKEN` environment variable to define the token expected by the
server (defaults to `dev-token`). Requests to `/video/generate` and
`/video/{video_id}/status` must include this token using the `Authorization`
header:

```bash
curl -H "Authorization: Bearer $API_TOKEN" http://localhost:8000/video/generate
```
