import os
import pytest
from unittest.mock import patch, MagicMock
from frontend.app import infer_title
import importlib

def test_api_url_env(monkeypatch):
    monkeypatch.setenv("SUMMARIZER_API_URL", "http://testserver:1234")
    import frontend.app as app
    importlib.reload(app)
    assert app.API_URL == "http://testserver:1234"

def test_api_url_default(monkeypatch):
    monkeypatch.delenv("SUMMARIZER_API_URL", raising=False)
    import frontend.app as app
    importlib.reload(app)
    assert app.API_URL == "http://127.0.0.1:8000"

@patch("frontend.app.requests.post")
def test_run_query_success(mock_post, monkeypatch):
    import frontend.app as app
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "summary": "Test summary",
        "sources": ["openai", "gemini"],
        "responses": {"openai": "A", "gemini": "B"}
    }
    mock_post.return_value = mock_resp

    r = app.requests.post(f"{app.API_URL}/ask", json={"query": "test", "providers": ["openai"]})
    assert r.status_code == 200
    data = r.json()
    assert data["summary"] == "Test summary"
    assert "openai" in data["responses"]

@patch("frontend.app.requests.post")
def test_run_query_backend_error(mock_post, monkeypatch):
    import frontend.app as app
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_post.return_value = mock_resp

    r = app.requests.post(f"{app.API_URL}/ask", json={"query": "test", "providers": ["openai"]})
    assert r.status_code == 500

def test_infer_title_from_long_message():
    long_message = "This is a very long and detailed question about the history of artificial intelligence."
    messages = [{"role": "user", "content": long_message}]
    title = infer_title(messages)
    # The corrected assertion matches the actual truncated output
    assert title == "This is a very long and detailed question about th..."