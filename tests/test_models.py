from sharpai_sdk.models.ollama_models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    DeleteRequest,
    EmbedRequest,
    EmbedResponse,
    GenerateRequest,
    GenerateResponse,
    PullRequest,
    TagsResponse,
)
from sharpai_sdk.models.openai_models import (
    OpenAIChatCompletionRequest,
    OpenAIChatCompletionResponse,
    OpenAICompletionRequest,
    OpenAICompletionResponse,
    OpenAIEmbeddingRequest,
    OpenAIEmbeddingResponse,
)


def test_tags_response():
    """Test TagsResponse model."""
    data = {
        "models": [
            {"name": "model1", "size": 1000},
            {"name": "model2", "size": 2000},
        ]
    }
    response = TagsResponse(**data)
    assert len(response.models) == 2
    assert response.models[0].name == "model1"


def test_pull_request():
    """Test PullRequest model."""
    request = PullRequest(model="test-model")
    assert request.model == "test-model"
    data = request.model_dump()
    assert data["model"] == "test-model"


def test_delete_request():
    """Test DeleteRequest model."""
    request = DeleteRequest(name="test-model")
    assert request.name == "test-model"


def test_embed_request_singular():
    """Test EmbedRequest with singular input."""
    request = EmbedRequest(model="test-model", input="test text")
    assert request.model == "test-model"
    assert request.input == "test text"


def test_embed_request_multiple():
    """Test EmbedRequest with multiple inputs."""
    request = EmbedRequest(model="test-model", input=["text1", "text2"])
    assert request.input == ["text1", "text2"]


def test_embed_response():
    """Test EmbedResponse model."""
    # Test with singular embedding
    data = {"embedding": [0.1, 0.2, 0.3]}
    response = EmbedResponse(**data)
    assert response.embedding == [0.1, 0.2, 0.3]

    # Test with multiple embeddings
    data = {
        "embeddings": [
            {"embedding": [0.1, 0.2], "index": 0},
            {"embedding": [0.3, 0.4], "index": 1},
        ]
    }
    response = EmbedResponse(**data)
    assert len(response.embeddings) == 2


def test_generate_request():
    """Test GenerateRequest model."""
    request = GenerateRequest(model="test-model", prompt="test prompt", stream=False)
    assert request.model == "test-model"
    assert request.prompt == "test prompt"
    assert request.stream is False


def test_generate_response():
    """Test GenerateResponse model."""
    data = {
        "model": "test-model",
        "response": "test response",
        "done": True,
    }
    response = GenerateResponse(**data)
    assert response.model == "test-model"
    assert response.response == "test response"
    assert response.done is True


def test_chat_message():
    """Test ChatMessage model."""
    message = ChatMessage(role="user", content="Hello")
    assert message.role == "user"
    assert message.content == "Hello"


def test_chat_request():
    """Test ChatRequest model."""
    messages = [{"role": "user", "content": "Hello"}]
    request = ChatRequest(model="test-model", messages=messages, stream=False)
    assert request.model == "test-model"
    assert len(request.messages) == 1


def test_chat_response():
    """Test ChatResponse model."""
    data = {
        "model": "test-model",
        "message": {"role": "assistant", "content": "Hi"},
        "done": True,
    }
    response = ChatResponse(**data)
    assert response.model == "test-model"
    assert response.message.content == "Hi"


def test_openai_embedding_request():
    """Test OpenAIEmbeddingRequest model."""
    request = OpenAIEmbeddingRequest(model="test-model", input="test")
    assert request.model == "test-model"
    assert request.input == "test"


def test_openai_embedding_response():
    """Test OpenAIEmbeddingResponse model."""
    data = {
        "object": "list",
        "data": [{"object": "embedding", "embedding": [0.1, 0.2], "index": 0}],
        "model": "test-model",
    }
    response = OpenAIEmbeddingResponse(**data)
    assert len(response.data) == 1
    assert response.data[0].embedding == [0.1, 0.2]


def test_openai_completion_request():
    """Test OpenAICompletionRequest model."""
    request = OpenAICompletionRequest(model="test-model", prompt="test", max_tokens=100)
    assert request.model == "test-model"
    assert request.prompt == "test"
    assert request.max_tokens == 100


def test_openai_completion_response():
    """Test OpenAICompletionResponse model."""
    data = {
        "id": "test-id",
        "object": "text_completion",
        "created": 1234567890,
        "model": "test-model",
        "choices": [{"text": "test", "index": 0}],
    }
    response = OpenAICompletionResponse(**data)
    assert len(response.choices) == 1
    assert response.choices[0].text == "test"


def test_openai_chat_completion_request():
    """Test OpenAIChatCompletionRequest model."""
    messages = [{"role": "user", "content": "Hello"}]
    request = OpenAIChatCompletionRequest(model="test-model", messages=messages)
    assert request.model == "test-model"
    assert len(request.messages) == 1


def test_openai_chat_completion_response():
    """Test OpenAIChatCompletionResponse model."""
    data = {
        "id": "test-id",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "test-model",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "Hi"},
            }
        ],
    }
    response = OpenAIChatCompletionResponse(**data)
    assert len(response.choices) == 1
    assert response.choices[0].message.content == "Hi"
