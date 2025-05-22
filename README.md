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
