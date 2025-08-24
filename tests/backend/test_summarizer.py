import pytest
from backend import summarizer
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_summarize_responses_success(mock_client, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    summarizer.OPENAI_KEY = "fake-key"
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Summary answer"}}]
    }
    mock_instance.post = AsyncMock(return_value=mock_response)
    result = await summarizer.summarize_responses("What is AI?", {"openai": "AI is intelligence by machines."})
    assert result == "Summary answer"