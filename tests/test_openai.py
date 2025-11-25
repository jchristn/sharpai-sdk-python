from unittest.mock import Mock, patch

import pytest

from sharpai_sdk.configuration import configure
from sharpai_sdk.resources.openai import OpenAI


@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    configure(endpoint="http://localhost:8000")
    client = Mock()
    with patch("sharpai_sdk.resources.openai.get_client", return_value=client):
        yield client


def test_create_embedding_singular(mock_client):
    """Test creating embedding for single input."""
    mock_response = {
        "object": "list",
        "data": [{"object": "embedding", "embedding": [0.1, 0.2, 0.3], "index": 0}],
        "model": "test-model",
    }
    mock_client.request.return_value = mock_response

    result = OpenAI.create_embedding("test-model", "test input")
    assert len(result.data) == 1
    assert result.data[0].embedding == [0.1, 0.2, 0.3]
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "v1/embeddings"
    assert call_args[1]["json"]["model"] == "test-model"
    assert call_args[1]["json"]["input"] == "test input"


def test_create_embedding_multiple(mock_client):
    """Test creating embeddings for multiple inputs."""
    mock_response = {
        "object": "list",
        "data": [
            {"object": "embedding", "embedding": [0.1, 0.2], "index": 0},
            {"object": "embedding", "embedding": [0.3, 0.4], "index": 1},
        ],
        "model": "test-model",
    }
    mock_client.request.return_value = mock_response

    result = OpenAI.create_embedding("test-model", ["input1", "input2"])
    assert len(result.data) == 2
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[1]["json"]["input"] == ["input1", "input2"]


def test_create_completion(mock_client):
    """Test creating a completion."""
    mock_response = {
        "id": "test-id",
        "object": "text_completion",
        "created": 1234567890,
        "model": "test-model",
        "choices": [
            {
                "text": "This is a completion",
                "index": 0,
                "finish_reason": "stop",
            }
        ],
    }
    mock_client.request.return_value = mock_response

    result = OpenAI.create_completion(
        "test-model", "test prompt", max_tokens=100, temperature=0.7
    )
    assert len(result.choices) == 1
    assert result.choices[0].text == "This is a completion"
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "v1/completions"
    assert call_args[1]["json"]["model"] == "test-model"
    assert call_args[1]["json"]["prompt"] == "test prompt"
    assert call_args[1]["json"]["max_tokens"] == 100
    assert call_args[1]["json"]["temperature"] == 0.7


def test_create_chat_completion(mock_client):
    """Test creating a chat completion."""
    mock_response = {
        "id": "test-id",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "test-model",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "Hello!"},
                "finish_reason": "stop",
            }
        ],
    }
    mock_client.request.return_value = mock_response

    messages = [{"role": "user", "content": "Hello"}]
    result = OpenAI.create_chat_completion(
        "test-model", messages, max_tokens=100, temperature=0.7
    )
    assert len(result.choices) == 1
    assert result.choices[0].message.content == "Hello!"
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "v1/chat/completions"
    assert call_args[1]["json"]["model"] == "test-model"
    assert call_args[1]["json"]["messages"] == messages
    assert call_args[1]["json"]["max_tokens"] == 100


def test_create_completion_with_all_params(mock_client):
    """Test creating completion with all optional parameters."""
    mock_response = {
        "id": "test-id",
        "object": "text_completion",
        "created": 1234567890,
        "model": "test-model",
        "choices": [{"text": "test", "index": 0}],
    }
    mock_client.request.return_value = mock_response

    _ = OpenAI.create_completion(
        model="test-model",
        prompt="test",
        max_tokens=150,
        temperature=0.7,
        top_p=0.9,
        n=2,
        stream=False,
        presence_penalty=0.5,
        frequency_penalty=0.3,
        stop=["END"],
        user="user-123",
        seed=42,
    )

    call_args = mock_client.request.call_args
    json_data = call_args[1]["json"]
    assert json_data["max_tokens"] == 150
    assert json_data["temperature"] == 0.7
    assert json_data["top_p"] == 0.9
    assert json_data["n"] == 2
    assert json_data["presence_penalty"] == 0.5
    assert json_data["frequency_penalty"] == 0.3
    assert json_data["stop"] == ["END"]
    assert json_data["user"] == "user-123"
    assert json_data["seed"] == 42
