from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class ModelInfo(BaseModel):
    """Model information from tags endpoint."""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    modified_at: Optional[str] = Field(None, alias="modified_at")
    size: Optional[int] = None
    digest: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class TagsResponse(BaseModel):
    """Response from /api/tags endpoint."""

    models: List[ModelInfo] = Field(default_factory=list)


class PullRequest(BaseModel):
    """Request model for pulling a model."""

    model: str


class DeleteRequest(BaseModel):
    """Request model for deleting a model."""

    name: str


class EmbedRequest(BaseModel):
    """Request model for generating embeddings."""

    model: str
    input: Union[str, List[str]]


class EmbeddingData(BaseModel):
    """Single embedding data."""

    embedding: List[float]
    index: Optional[int] = None


class EmbedResponse(BaseModel):
    """Response from /api/embed endpoint."""

    embedding: Optional[List[float]] = None
    embeddings: Optional[List[EmbeddingData]] = None


class GenerateOptions(BaseModel):
    """Options for generate request."""

    num_keep: Optional[int] = None
    seed: Optional[int] = None
    num_predict: Optional[int] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    min_p: Optional[float] = None
    tfs_z: Optional[float] = None
    typical_p: Optional[float] = None
    repeat_last_n: Optional[int] = None
    temperature: Optional[float] = None
    repeat_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    mirostat: Optional[int] = None
    mirostat_tau: Optional[float] = None
    mirostat_eta: Optional[float] = None
    penalize_newline: Optional[bool] = None
    stop: Optional[List[str]] = None
    numa: Optional[bool] = None
    num_ctx: Optional[int] = None
    num_batch: Optional[int] = None
    num_gpu: Optional[int] = None
    main_gpu: Optional[int] = None
    low_vram: Optional[bool] = None
    f16_kv: Optional[bool] = None
    vocab_only: Optional[bool] = None
    use_mmap: Optional[bool] = None
    use_mlock: Optional[bool] = None
    num_thread: Optional[int] = None


class GenerateRequest(BaseModel):
    """Request model for generating completions."""

    model: str
    prompt: str
    stream: Optional[bool] = False
    options: Optional[GenerateOptions] = None


class GenerateResponse(BaseModel):
    """Response from /api/generate endpoint."""

    model: Optional[str] = None
    created_at: Optional[str] = None
    response: Optional[str] = None
    done: Optional[bool] = None
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None


class ChatMessage(BaseModel):
    """Chat message model."""

    role: str
    content: str
    name: Optional[str] = None


class ChatRequest(BaseModel):
    """Request model for chat completions."""

    model: str
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    options: Optional[GenerateOptions] = None


class ChatResponse(BaseModel):
    """Response from /api/chat endpoint."""

    model: Optional[str] = None
    created_at: Optional[str] = None
    message: Optional[ChatMessage] = None
    done: Optional[bool] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None
