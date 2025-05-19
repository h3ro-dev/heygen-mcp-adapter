# HeyGen MCP Adapter PRD

## Overview
The HeyGen MCP Adapter provides an internal service for generating videos through the HeyGen platform and retrieving their status. The adapter exposes a simple REST API that other services can call.

## Current Progress
- The initial API contract is defined in `openapi.yaml`.
- A minimal FastAPI server has been created with placeholder logic for the endpoints defined in the OpenAPI spec.

## Remaining Work
- Integrate the server with the real HeyGen API for video creation and status polling.
- Replace the in-memory store with persistent storage.
- Add authentication and authorization for the adapter endpoints.
- Improve validation and error handling.
- Write unit and integration tests.
- Provide Docker and deployment configurations.
- Expand CI beyond Semgrep to include automated testing.

