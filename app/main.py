from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from pathlib import Path
import asyncio
import json
import time


# base64-encoded 1x1 PNG
_SAMPLE_IMAGE_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII="
)


def _count_tokens(text: str) -> int:
    """Naively count tokens by splitting on whitespace."""
    if not isinstance(text, str):
        return 0
    return len(text.split())


def _calc_usage(prompt_text: str, completion_text: str) -> dict:
    prompt_tokens = _count_tokens(prompt_text)
    completion_tokens = _count_tokens(completion_text)
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }

app = FastAPI(title="DummyAI")

# Load model data once at startup for faster responses
_MODELS = json.loads((Path(__file__).resolve().parent.parent / "models.json").read_text())
_MODEL_LOOKUP = {m["id"]: m for m in _MODELS}


def _now() -> int:
    return int(time.time())


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    model = body.get("model", "dummy-model")
    completion_text = "Hello this is a dummy response."
    prompt_text = " ".join(m.get("content", "") for m in body.get("messages", []))
    tokens = completion_text.split()
    usage = _calc_usage(prompt_text, completion_text)
    if body.get("stream"):
        async def event_generator():
            for token in tokens:
                chunk = {
                    "id": "chatcmpl-dummy",
                    "object": "chat.completion.chunk",
                    "created": _now(),
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": token + " "},
                            "finish_reason": None,
                        }
                    ],
                }
                yield json.dumps(chunk)
                await asyncio.sleep(0.05)
            final_chunk = {
                "id": "chatcmpl-dummy",
                "object": "chat.completion.chunk",
                "created": _now(),
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop",
                    }
                ],
                "usage": usage,
            }
            yield json.dumps(final_chunk)
            yield "[DONE]"
        return EventSourceResponse(event_generator())

    resp = {
        "id": "chatcmpl-dummy",
        "object": "chat.completion",
        "created": _now(),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": completion_text},
                "finish_reason": "stop",
            }
        ],
        "usage": usage,
    }
    return JSONResponse(resp)


@app.get("/v1/models")
@app.get("/v1/models/")
async def list_models():
    return JSONResponse({"object": "list", "data": _MODELS})


@app.get("/v1/models/{model_id}")
async def retrieve_model(model_id: str):
    model = _MODEL_LOOKUP.get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return JSONResponse(model)


@app.post("/v1/completions")
async def completions(request: Request):
    body = await request.json()
    prompt_field = body.get("prompt", "")
    if isinstance(prompt_field, list):
        prompt_text = " ".join(p for p in prompt_field if isinstance(p, str))
    elif isinstance(prompt_field, str):
        prompt_text = prompt_field
    else:
        prompt_text = ""
    completion_text = "dummy completion"
    usage = _calc_usage(prompt_text, completion_text)
    resp = {
        "id": "cmpl-dummy",
        "object": "text_completion",
        "created": _now(),
        "model": "dummy-model",
        "choices": [
            {
                "index": 0,
                "text": completion_text,
                "finish_reason": "stop",
            }
        ],
        "usage": usage,
    }
    return JSONResponse(resp)


@app.post("/v1/embeddings")
async def embeddings(request: Request):
    body = await request.json()
    input_field = body.get("input", "")
    if isinstance(input_field, list):
        prompt_text = " ".join(str(i) for i in input_field)
    else:
        prompt_text = str(input_field)
    tokens = _count_tokens(prompt_text)
    resp = {
        "object": "list",
        "data": [{"object": "embedding", "index": 0, "embedding": [0.0, 0.0, 0.0]}],
        "model": "dummy-embedding-model",
        "usage": {"prompt_tokens": tokens, "total_tokens": tokens},
    }
    return JSONResponse(resp)


@app.post("/v1/images/generations")
async def images():
    resp = {
        "created": _now(),
        "data": [{"b64_json": _SAMPLE_IMAGE_B64}],
    }
    return JSONResponse(resp)


@app.post("/v1/images/edits")
async def images_edits():
    resp = {"created": _now(), "data": [{"b64_json": _SAMPLE_IMAGE_B64}]}
    return JSONResponse(resp)


@app.post("/v1/images/variations")
async def images_variations():
    resp = {"created": _now(), "data": [{"b64_json": _SAMPLE_IMAGE_B64}]}
    return JSONResponse(resp)


@app.post("/v1/audio/transcriptions")
async def audio_transcriptions(file: UploadFile = File(...)):
    return JSONResponse({"text": "dummy transcription"})


@app.post("/v1/audio/translations")
async def audio_translations(file: UploadFile = File(...)):
    return JSONResponse({"text": "dummy translation"})


@app.post("/v1/files")
async def files(file: UploadFile = File(...)):
    return JSONResponse({"id": "file-dummy", "object": "file", "filename": file.filename})


@app.get("/v1/files")
async def list_files():
    return JSONResponse({"object": "list", "data": [{"id": "file-dummy", "object": "file"}]})


@app.get("/v1/files/{file_id}")
async def retrieve_file(file_id: str):
    return JSONResponse({"id": file_id, "object": "file", "filename": "dummy.txt"})


@app.delete("/v1/files/{file_id}")
async def delete_file(file_id: str):
    return JSONResponse({"id": file_id, "object": "file", "deleted": True})


@app.post("/v1/fine_tuning/jobs")
async def fine_tuning_jobs():
    return JSONResponse({"id": "ft-job-dummy", "object": "fine_tuning.job"})


@app.get("/v1/fine_tuning/jobs")
async def list_ft_jobs():
    return JSONResponse({"object": "list", "data": [{"id": "ft-job-dummy", "object": "fine_tuning.job"}]})


@app.get("/v1/fine_tuning/jobs/{job_id}")
async def retrieve_ft_job(job_id: str):
    return JSONResponse({"id": job_id, "object": "fine_tuning.job", "status": "succeeded"})


@app.post("/v1/moderations")
async def moderations():
    return JSONResponse({"id": "modr-dummy", "model": "dummy-moderation", "results": [{"flagged": False}]})


@app.post("/v1/edits")
async def edits():
    return JSONResponse({"object": "edit", "choices": [{"text": "dummy edit"}]})

