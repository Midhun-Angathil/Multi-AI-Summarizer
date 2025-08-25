import pytest
from fastapi.testclient import TestClient
from backend import main
from unittest.mock import patch, AsyncMock, MagicMock
import httpx

client = TestClient(main.app)

def test_cache_set_and_get():
    main.set_cache("hello", "openai", "test-response")
    assert main.get_cached("hello", "openai") == "test-response"

def test_simulate_response():
    resp = main.simulate_response("FakeProvider", "test")
    assert resp.startswith("[FakeProvider simulated response for query: 'test']")

def test_summarize_responses_all_invalid():
    responses = {"a": "[error]", "b": "[fail]"}
    summary = main.summarize_responses(responses)
    assert summary == "**a**: [error]\n\n---\n\n**b**: [fail]"

def test_summarize_responses_some_valid():
    responses = {"a": "hello", "b": "[fail]"}
    summary = main.summarize_responses(responses)
    assert summary == "**a**: hello\n\n---\n\n**b**: [fail]"

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_call_cohere_success(mock_client, monkeypatch):
    monkeypatch.setenv("COHERE_API_KEY", "fake-key")
    main.CACHE.clear()
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.json.return_value = {"generations": [{"text": "Cohere answer"}]}
    mock_instance.post = AsyncMock(return_value=mock_response)
    result = await main.call_cohere("test")
    assert result == "Cohere answer"

@pytest.mark.asyncio
@patch("openai.ChatCompletion.create")
async def test_call_openai_success(mock_create, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    main.CACHE.clear()
    mock_create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="OpenAI answer"))])
    result = await main.call_openai("test", [])
    assert result == "OpenAI answer"

@pytest.mark.asyncio
async def test_call_gemini_simulated(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "")
    main.CACHE.clear()
    result = await main.call_gemini("test")
    assert "Gemini API key missing" in result

@pytest.mark.asyncio
async def test_call_cohere_simulated(monkeypatch):
    monkeypatch.setenv("COHERE_API_KEY", "")
    main.CACHE.clear()
    result = await main.call_cohere("test")
    assert "Cohere API key missing" in result

@pytest.mark.asyncio
async def test_call_claude_simulated(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    main.CACHE.clear()
    result = await main.call_claude("test")
    assert "simulated response" in result

@pytest.mark.asyncio
async def test_call_perplexity_simulated(monkeypatch):
    monkeypatch.setenv("PERPLEXITY_API_KEY", "")
    main.CACHE.clear()
    result = await main.call_perplexity("test")
    assert "simulated response" in result

def test_ask_endpoint(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "")
    monkeypatch.setenv("COHERE_API_KEY", "")
    monkeypatch.setenv("OPENAI_API_KEY", "")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    monkeypatch.setenv("PERPLEXITY_API_KEY", "")

    payload = {
        "query": "test question",
        "providers": ["gemini", "cohere", "openai", "claude", "perplexity"]
    }
    response = client.post("/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "test question"
    assert "summary" in data
    assert "responses" in data
    assert "sources" in data