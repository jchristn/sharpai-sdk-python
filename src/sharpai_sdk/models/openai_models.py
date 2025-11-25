from typing import List, Optional, Union

from pydantic import BaseModel


class OpenAIEmbeddingRequest(BaseModel):
    """Request model for OpenAI-style embeddings."""

    model: str
    input: Union[str, List[str]]
    user: Optional[str] = None


class EmbeddingObject(BaseModel):
    """Single embedding object in OpenAI format."""

    object: str = "embedding"
    embedding: List[float]
    index: int


class OpenAIEmbeddingResponse(BaseModel):
    """Response from /v1/embeddings endpoint."""

    object: str = "list"
    data: List[EmbeddingObject]
    model: str
    usage: Optional[dict] = None


class CompletionMessage(BaseModel):
    """Message in completion request."""

    role: Optional[str] = None
    content: str


class OpenAICompletionRequest(BaseModel):
    """Request model for OpenAI-style completions."""

    model: str
    prompt: Union[str, List[str]]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = 1
    stream: Optional[bool] = False
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    stop: Optional[Union[str, List[str]]] = None
    user: Optional[str] = None
    seed: Optional[int] = None


class CompletionChoice(BaseModel):
    """Single completion choice."""

    text: str
    index: int
    logprobs: Optional[dict] = None
    finish_reason: Optional[str] = None


class OpenAICompletionResponse(BaseModel):
    """Response from /v1/completions endpoint."""

    id: str
    object: str = "text_completion"
    created: int
    model: str
    choices: List[CompletionChoice]
    usage: Optional[dict] = None


class ChatCompletionMessage(BaseModel):
    """Message in chat completion request."""

    role: str
    content: str
    name: Optional[str] = None


class OpenAIChatCompletionRequest(BaseModel):
    """Request model for OpenAI-style chat completions."""

    model: str
    messages: List[ChatCompletionMessage]
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    user: Optional[str] = None
    seed: Optional[int] = None


class ChatCompletionChoice(BaseModel):
    """Single chat completion choice."""

    index: int
    message: ChatCompletionMessage
    finish_reason: Optional[str] = None


class OpenAIChatCompletionResponse(BaseModel):
    """Response from /v1/chat/completions endpoint."""

    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Optional[dict] = None
