import pytest
from backend import providers
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_ask_openai_success(mock_client, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    providers.OPENAI_KEY = "fake-key"
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.json.return_value = {"choices": [{"message": {"content": "OpenAI answer"}}]}
    mock_instance.post = AsyncMock(return_value=mock_response)
    result = await providers.ask_openai("test")
    assert result == "OpenAI answer"

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_ask_claude_success(mock_client, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-key")
    providers.ANTHROPIC_KEY = "fake-key"
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.json.return_value = {"content": [{"text": "Claude answer"}]}
    mock_instance.post = AsyncMock(return_value=mock_response)
    result = await providers.ask_claude("test")
    assert result == "Claude answer"

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_ask_gemini_success(mock_client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    providers.GEMINI_KEY = "fake-key"
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Gemini answer"}]}}]
    }
    mock_instance.post = AsyncMock(return_value=mock_response)
    result = await providers.ask_gemini("test")
    assert result == "Gemini answer"

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_ask_cohere_success(mock_client, monkeypatch):
    monkeypatch.setenv("COHERE_API_KEY", "fake-key")
    providers.COHERE_KEY = "fake-key"
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.json.return_value = {"text": "Cohere answer"}
    mock_instance.post = AsyncMock(return_value=mock_response)
    result = await providers.ask_cohere("test")
    assert result == "Cohere answer"

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_ask_perplexity_success(mock_client, monkeypatch):
    monkeypatch.setenv("PERPLEXITY_API_KEY", "fake-key")
    providers.PERPLEXITY_KEY = "fake-key"
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.json.return_value = {"choices": [{"message": {"content": "Perplexity answer"}}]}
    mock_instance.post = AsyncMock(return_value=mock_response)
    result = await providers.ask_perplexity("test")
    assert result == "Perplexity answer"