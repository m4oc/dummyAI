import os
import sys
import base64
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app

client = TestClient(app)

def test_list_models():
    resp = client.get("/v1/models")
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"][0]["id"] == "dummy-model"

def test_retrieve_model():
    resp = client.get("/v1/models/dummy-model")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "dummy-model"


def test_chat_usage_counts():
    body = {"model": "dummy-model", "messages": [{"role": "user", "content": "Hello world"}]}
    resp = client.post("/v1/chat/completions", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["usage"] == {
        "prompt_tokens": 2,
        "completion_tokens": len("Hello this is a dummy response.".split()),
        "total_tokens": 2 + len("Hello this is a dummy response.".split()),
    }


def test_completion_usage_counts():
    body = {"prompt": "Hi there"}
    resp = client.post("/v1/completions", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["usage"] == {
        "prompt_tokens": 2,
        "completion_tokens": len("dummy completion".split()),
        "total_tokens": 2 + len("dummy completion".split()),
    }


def test_embedding_usage_counts():
    body = {"input": "hi"}
    resp = client.post("/v1/embeddings", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["usage"] == {"prompt_tokens": 1, "total_tokens": 1}


def test_image_generation_returns_base64():
    resp = client.post("/v1/images/generations")
    assert resp.status_code == 200
    data = resp.json()
    img_b64 = data["data"][0]["b64_json"]
    img_bytes = base64.b64decode(img_b64)
    assert len(img_bytes) > 0
