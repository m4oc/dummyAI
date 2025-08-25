# DummyAI

**DummyAI** is an **OpenAI-compatible mock server** built with **FastAPI**.
It replicates the OpenAI API surface and returns **schema-valid dummy responses** for major endpoints, including chat, completions, embeddings, images, audio, files, models, fine-tuning, moderations, and more.

## Features
- Fully **OpenAI API compatible**
- **Dummy responses** with valid JSON schema
- **Streaming simulation** (SSE) for chat completions
- **File upload support** with placeholder IDs
- **Model listing** and retrieval endpoints
- Lightweight, configurable, and **open source**
- Image APIs return base64-encoded sample PNGs
## Supported endpoints
- `GET /v1/models`, `GET /v1/models/{model}`
- `POST /v1/chat/completions` (streaming)
- `POST /v1/completions`
- `POST /v1/embeddings`
- `POST /v1/images/generations`, `POST /v1/images/edits`, `POST /v1/images/variations`
- `POST /v1/audio/transcriptions`, `POST /v1/audio/translations`
- `POST /v1/files`, `GET /v1/files`, `GET/DELETE /v1/files/{id}`
- `POST /v1/fine_tuning/jobs`, `GET /v1/fine_tuning/jobs`, `GET /v1/fine_tuning/jobs/{id}`
- `POST /v1/moderations`
- `POST /v1/edits`

## Use cases
- Develop OpenAI-based apps **without real API calls**
- Run in **CI/CD pipelines** for integration testing
- Work **offline** without API keys or credits
- Simulate errors or edge cases safely

## Run locally
```bash
uvicorn app.main:app --reload
```

## Docker
Build and run the container:
```bash
docker build -t dummyai .
docker run -p 8000:8000 dummyai
```

## GitHub Actions
The workflow in `.github/workflows/docker.yml` runs the test suite and, on success, builds the image and pushes it to Docker Hub. Set `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets in your repository to enable it.
