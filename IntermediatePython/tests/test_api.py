# Write tests/test_api.py to disk

import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_normalize_text_happy_path():
    payload = {"text": "Hello Data Engineering world!", "lowercase": False}
    resp = client.post("/normalize-text", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "normalized_text" in data
    assert "char_count" in data
    assert "word_count" in data
    assert isinstance(data["char_count"], int)
    assert isinstance(data["word_count"], int)


def test_normalize_text_invalid_payload_returns_422():
    payload = {"text": "Too short", "lowercase": False}
    resp = client.post("/normalize-text", json=payload)
    assert resp.status_code == 422


def test_normalize_text_lowercase_changes_output():
    payload = {"text": "Hello Data Engineering world!", "lowercase": True}
    resp = client.post("/normalize-text", json=payload)
    assert resp.status_code == 200
    assert resp.json()["normalized_text"].startswith("hello")

def test_extract_keywords_simple_happy_path():
    top_k = 3
    payload = {"text": "Data Engineering is engineering data. Data quality matters a lot.", "top_k": top_k}
    resp = client.post("/keywords-simple", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "keywords" in data
    assert len(data['keywords']) <= top_k

def test_extract_keywords_simple_invalid():
    top_k = 0
    payload = {"text": "Data Engineering is engineering data. Data quality matters a lot.", "top_k": top_k}
    resp = client.post("/keywords-simple", json=payload)
    assert resp.status_code == 400
    top_k = 24
    payload = {"text": "Data Engineering is engineering data. Data quality matters a lot.", "top_k": top_k}
    resp = client.post("/keywords-simple", json=payload)
    assert resp.status_code == 400


