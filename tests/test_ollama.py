from unittest.mock import Mock, patch

import pytest

from sharpai_sdk.configuration import configure
from sharpai_sdk.resources.ollama import Ollama


@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    configure(endpoint="http://localhost:8000")
    client = Mock()
    with patch("sharpai_sdk.resources.ollama.get_client", return_value=client):
        yield client


def test_list_models(mock_client):
    """Test listing models."""
    mock_response = {
        "models": [
            {"name": "model1", "size": 1000},
            {"name": "model2", "size": 2000},
        ]
    }
    mock_client.request.return_value = mock_response

    result = Ollama.list_models()
    assert len(result.models) == 2
    assert result.models[0].name == "model1"
    mock_client.request.assert_called_once_with("GET", "api/tags")


def test_pull_model(mock_client):
    """Test pulling a model."""
    mock_response = {"status": "pulling"}
    mock_client.request.return_value = mock_response

    result = Ollama.pull_model("test-model")
    assert result == mock_response
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "api/pull"
    assert call_args[1]["json"]["model"] == "test-model"


def test_delete_model(mock_client):
    """Test deleting a model."""
    mock_response = {"status": "deleted"}
    mock_client.request.return_value = mock_response

    result = Ollama.delete_model("test-model")
    assert result == mock_response
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[0][0] == "DELETE"
    assert call_args[0][1] == "api/delete"
    assert call_args[1]["json"]["name"] == "test-model"


def test_generate_embedding_singular(mock_client):
    """Test generating embedding for single input."""
    mock_response = {"embedding": [0.1, 0.2, 0.3, 0.4, 0.5]}
    mock_client.request.return_value = mock_response

    result = Ollama.generate_embedding("test-model", "test input")
    assert result.embedding == [0.1, 0.2, 0.3, 0.4, 0.5]
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "api/embed"
    assert call_args[1]["json"]["model"] == "test-model"
    assert call_args[1]["json"]["input"] == "test input"


def test_generate_embedding_multiple(mock_client):
    """Test generating embeddings for multiple inputs."""
    mock_response = {
        "embeddings": [
            {"embedding": [0.1, 0.2], "index": 0},
            {"embedding": [0.3, 0.4], "index": 1},
        ]
    }
    mock_client.request.return_value = mock_response

    result = Ollama.generate_embedding("test-model", ["input1", "input2"])
    assert len(result.embeddings) == 2
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[1]["json"]["input"] == ["input1", "input2"]


def test_generate(mock_client):
    """Test generating a completion."""
    mock_response = {
        "model": "test-model",
        "response": "This is a test response",
        "done": True,
    }
    mock_client.request.return_value = mock_response

    result = Ollama.generate("test-model", "test prompt", stream=False)
    assert result.response == "This is a test response"
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "api/generate"
    assert call_args[1]["json"]["model"] == "test-model"
    assert call_args[1]["json"]["prompt"] == "test prompt"


def test_chat(mock_client):
    """Test generating a chat completion."""
    mock_response = {
        "model": "test-model",
        "message": {"role": "assistant", "content": "Hello!"},
        "done": True,
    }
    mock_client.request.return_value = mock_response

    messages = [{"role": "user", "content": "Hello"}]
    result = Ollama.chat("test-model", messages, stream=False)
    assert result.message.content == "Hello!"
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "api/chat"
    assert call_args[1]["json"]["model"] == "test-model"
    assert call_args[1]["json"]["messages"] == messages
