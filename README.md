# HeyGen MCP Adapter

This project provides a simple REST API for generating videos through HeyGen and checking their status.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your HeyGen API credentials as environment variables:
   ```bash
   export HEYGEN_API_KEY=<your-api-key>
   # optional: override base URL if needed
   export HEYGEN_BASE_URL=https://api.heygen.com/v1
   ```

3. Start the server:
   ```bash
   uvicorn server:app --reload
   ```

The API will be available at `http://localhost:8000`.
Video metadata is stored in a local `SQLite` database (`videos.db`) created automatically in the project directory.

Refer to `openapi.yaml` for the API specification.

## Docker

To build and run the application using Docker:

```bash
docker build -t heygen-mcp-adapter .
docker run -p 8000:8000 heygen-mcp-adapter
```

### Using Docker Compose

For development with automatic reloads:

```bash
docker-compose up --build
```
