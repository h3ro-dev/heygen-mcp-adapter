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
Video metadata is stored in a local `SQLite` database (`videos.db`) created automatically in the project directory.

Refer to `openapi.yaml` for the API specification.
