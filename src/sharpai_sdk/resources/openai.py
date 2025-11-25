from typing import List, Optional, Union

from ..configuration import get_client
from ..models.openai_models import (
    OpenAIChatCompletionRequest,
    OpenAIChatCompletionResponse,
    OpenAICompletionRequest,
    OpenAICompletionResponse,
    OpenAIEmbeddingRequest,
    OpenAIEmbeddingResponse,
)


class OpenAI:
    """
    OpenAI-compatible API resource class.
    Provides methods for interacting with OpenAI-compatible endpoints.
    """

    @classmethod
    def create_embedding(
        cls, model: str, input_data: Union[str, List[str]], user: Optional[str] = None
    ) -> OpenAIEmbeddingResponse:
        """
        Create embeddings for input text.

        Args:
            model: Name of the embedding model to use.
            input_data: Single string or list of strings to generate embeddings for.
            user: Optional user identifier.

        Returns:
            OpenAIEmbeddingResponse: Embedding response in OpenAI format.
        """
        client = get_client()
        request_data = OpenAIEmbeddingRequest(
            model=model, input=input_data, user=user
        ).model_dump(mode="json", exclude_unset=True)
        response = client.request("POST", "v1/embeddings", json=request_data)
        return OpenAIEmbeddingResponse(**response)

    @classmethod
    def create_completion(
        cls,
        model: str,
        prompt: Union[str, List[str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = 1,
        stream: Optional[bool] = False,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        stop: Optional[Union[str, List[str]]] = None,
        user: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> OpenAICompletionResponse:
        """
        Create a completion for the provided prompt.

        Args:
            model: Name of the model to use.
            prompt: Single prompt string or list of prompt strings.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            presence_penalty: Presence penalty value.
            frequency_penalty: Frequency penalty value.
            stop: Stop sequences.
            user: Optional user identifier.
            seed: Random seed for generation.

        Returns:
            OpenAICompletionResponse: Completion response in OpenAI format.
        """
        client = get_client()
        request_data = OpenAICompletionRequest(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stop=stop,
            user=user,
            seed=seed,
        ).model_dump(mode="json", exclude_unset=True)
        response = client.request("POST", "v1/completions", json=request_data)
        return OpenAICompletionResponse(**response)

    @classmethod
    def create_chat_completion(
        cls,
        model: str,
        messages: List[dict],
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = 1,
        stream: Optional[bool] = False,
        stop: Optional[Union[str, List[str]]] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        user: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> OpenAIChatCompletionResponse:
        """
        Create a chat completion.

        Args:
            model: Name of the model to use.
            messages: List of message dictionaries with 'role' and 'content' keys.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Stop sequences.
            max_tokens: Maximum number of tokens to generate.
            presence_penalty: Presence penalty value.
            frequency_penalty: Frequency penalty value.
            user: Optional user identifier.
            seed: Random seed for generation.

        Returns:
            OpenAIChatCompletionResponse: Chat completion response in OpenAI format.
        """
        client = get_client()
        request_data = OpenAIChatCompletionRequest(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            stop=stop,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            user=user,
            seed=seed,
        ).model_dump(mode="json", exclude_unset=True)
        response = client.request("POST", "v1/chat/completions", json=request_data)
        return OpenAIChatCompletionResponse(**response)
