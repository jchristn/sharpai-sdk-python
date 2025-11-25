from typing import List, Optional, Union

from ..configuration import get_client
from ..models.ollama_models import (
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


class Ollama:
    """
    Ollama API resource class.
    Provides methods for interacting with Ollama-compatible endpoints.
    """

    @classmethod
    def list_models(cls) -> TagsResponse:
        """
        List all local models.

        Returns:
            TagsResponse: List of available models.
        """
        client = get_client()
        response = client.request("GET", "api/tags")
        return TagsResponse(**response)

    @classmethod
    def pull_model(cls, model: str) -> dict:
        """
        Pull a model from the registry.

        Args:
            model: Name of the model to pull.

        Returns:
            dict: Response from the API.
        """
        client = get_client()
        request_data = PullRequest(model=model).model_dump(
            mode="json", exclude_unset=True
        )
        response = client.request("POST", "api/pull", json=request_data)
        return response

    @classmethod
    def delete_model(cls, name: str) -> dict:
        """
        Delete a model.

        Args:
            name: Name of the model to delete.

        Returns:
            dict: Response from the API.
        """
        client = get_client()
        request_data = DeleteRequest(name=name).model_dump(
            mode="json", exclude_unset=True
        )
        response = client.request("DELETE", "api/delete", json=request_data)
        return response

    @classmethod
    def generate_embedding(
        cls, model: str, input_data: Union[str, List[str]]
    ) -> EmbedResponse:
        """
        Generate embeddings for text input.

        Args:
            model: Name of the embedding model to use.
            input_data: Single string or list of strings to generate embeddings for.

        Returns:
            EmbedResponse: Embedding response with embeddings.
        """
        client = get_client()
        request_data = EmbedRequest(model=model, input=input_data).model_dump(
            mode="json", exclude_unset=True
        )
        response = client.request("POST", "api/embed", json=request_data)
        return EmbedResponse(**response)

    @classmethod
    def generate(
        cls,
        model: str,
        prompt: str,
        stream: Optional[bool] = False,
        options: Optional[dict] = None,
    ) -> GenerateResponse:
        """
        Generate a completion for a prompt.

        Args:
            model: Name of the model to use.
            prompt: The prompt text.
            stream: Whether to stream the response.
            options: Optional generation parameters.

        Returns:
            GenerateResponse: Generated completion response.
        """
        client = get_client()
        request_data = GenerateRequest(
            model=model, prompt=prompt, stream=stream, options=options
        ).model_dump(mode="json", exclude_unset=True)
        response = client.request("POST", "api/generate", json=request_data)
        return GenerateResponse(**response)

    @classmethod
    def chat(
        cls,
        model: str,
        messages: List[dict],
        stream: Optional[bool] = False,
        options: Optional[dict] = None,
    ) -> ChatResponse:
        """
        Generate a chat completion.

        Args:
            model: Name of the model to use.
            messages: List of message dictionaries with 'role' and 'content' keys.
            stream: Whether to stream the response.
            options: Optional generation parameters.

        Returns:
            ChatResponse: Chat completion response.
        """
        client = get_client()
        # Convert dict messages to ChatMessage objects
        chat_messages = [
            ChatMessage(**msg) if isinstance(msg, dict) else msg for msg in messages
        ]
        request_data = ChatRequest(
            model=model, messages=chat_messages, stream=stream, options=options
        ).model_dump(mode="json", exclude_unset=True)
        response = client.request("POST", "api/chat", json=request_data)
        return ChatResponse(**response)
