import os
import sys
import base64
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app

client = TestClient(app)

def test_list_models_trailing_slash():
    resp = client.get("/v1/models/")
    assert resp.status_code == 200
    data = resp.json()
    assert any(m["id"] == "dummy-model" for m in data["data"])

def test_retrieve_model():
    resp = client.get("/v1/models/dummy-model")
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"id": "dummy-model", "object": "model"}


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


def test_images_edits_returns_base64():
    resp = client.post("/v1/images/edits")
    assert resp.status_code == 200
    data = resp.json()
    img_b64 = data["data"][0]["b64_json"]
    img_bytes = base64.b64decode(img_b64)
    assert len(img_bytes) > 0


def test_images_variations_returns_base64():
    resp = client.post("/v1/images/variations")
    assert resp.status_code == 200
    data = resp.json()
    img_b64 = data["data"][0]["b64_json"]
    img_bytes = base64.b64decode(img_b64)
    assert len(img_bytes) > 0


def test_audio_transcription():
    resp = client.post(
        "/v1/audio/transcriptions",
        files={"file": ("audio.wav", b"dummy", "audio/wav")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["text"] == "dummy transcription"


def test_audio_translation():
    resp = client.post(
        "/v1/audio/translations",
        files={"file": ("audio.wav", b"dummy", "audio/wav")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["text"] == "dummy translation"


def test_file_endpoints():
    upload_resp = client.post(
        "/v1/files",
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    assert upload_resp.status_code == 200
    file_data = upload_resp.json()
    file_id = file_data["id"]
    list_resp = client.get("/v1/files")
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert any(f["id"] == file_id for f in list_data["data"])
    retrieve_resp = client.get(f"/v1/files/{file_id}")
    assert retrieve_resp.status_code == 200
    retrieve_data = retrieve_resp.json()
    assert retrieve_data["id"] == file_id


def test_image_generation_returns_base64():
    resp = client.post("/v1/images/generations")
    assert resp.status_code == 200
    data = resp.json()
    img_b64 = data["data"][0]["b64_json"]
    img_bytes = base64.b64decode(img_b64)
    assert len(img_bytes) > 0
