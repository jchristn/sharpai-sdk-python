<div align="center">

  <img src="https://github.com/jchristn/sharpai/blob/main/assets/logo.png" width="256" height="256">

</div>

# SharpAI.Sdk

**A Python SDK for interacting with SharpAI server instances - providing Ollama and OpenAI compatible API wrappers for local AI inference.**

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />

  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" />

</p>

<p align="center">

  <a href="https://pypi.org/project/sharpai-sdk-python/">

    <img src="https://img.shields.io/pypi/v/sharpai-sdk-python.svg?style=flat" alt="PyPI Version">

  </a>

  &nbsp;

  <a href="https://pypi.org/project/sharpai-sdk-python">

    <img src="https://img.shields.io/pypi/dm/sharpai-sdk-python.svg" alt="PyPI Downloads">

  </a>

</p>

<p align="center">

  <strong>A Python SDK for SharpAI - Local AI inference with Ollama and OpenAI compatible APIs</strong>

</p>

<p align="center">

  Embeddings • Completions • Chat • Model Management • Streaming Support

</p>

**IMPORTANT** - SharpAI.Sdk assumes you have deployed the SharpAI REST server. If you are integrating a SharpAI library directly into your code, use of this SDK is not necessary.

---

## 🚀 Features

- **Ollama API Compatibility** - Full support for Ollama API endpoints and models
- **OpenAI API Compatibility** - Complete OpenAI API compatibility for seamless integration
- **Model Management** - Download, list, and delete models with progress tracking
- **Multiple Inference Types**:
  - Text embeddings generation
  - Text completions (streaming and non-streaming)
  - Chat completions (streaming and non-streaming)
- **Streaming Support** - Real-time token streaming for completions and chat
- **Async/Await Support** - Full async/await support for all operations
- **Error Handling** - Comprehensive error handling with detailed exception types
- **Configurable Logging** - Built-in request/response logging capabilities
- **Connectivity Validation** - Verify API connectivity before operations
- **Built-in Retry Mechanism** - Automatic retry on failed requests

## 📦 Installation

Install SharpAI.Sdk via pip:

```bash
pip install sharpai-sdk-python
```

Or for development, install the package in editable mode:

```bash
git clone <repository-url>
cd sharpai-sdk-python
pip install -e .
```

### Requirements

- Python 3.8 or higher

### Dependencies

- `httpx`: For making HTTP requests
- `pydantic`: For data validation and serialization
- `typing`: For type hints (built-in)

## 🚀 Quick Start

### Basic Usage

```python
from sharpai_sdk import configure, Connectivity, Ollama, OpenAI

# Configure the SDK
configure(
    endpoint="http://localhost:8000",
    timeout=30,
    retries=3,
)

# Validate connectivity
is_connected = Connectivity.validate()
if is_connected:
    print("✓ Successfully connected to SharpAI API")

# List available models
models = Ollama.list_models()
print(f"Found {len(models.models)} models")

# Generate embeddings using Ollama API
embedding = Ollama.generate_embedding(
    model="leliuga/all-MiniLM-L6-v2-GGUF",
    input_data="Hello, SharpAI!",
)
print(f"Generated embedding with {len(embedding.embedding)} dimensions")

# Generate chat completion using OpenAI-compatible API
chat = OpenAI.create_chat_completion(
    model="QuantFactory/Qwen2.5-3B-GGUF",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"},
    ],
    max_tokens=100,
    temperature=0.7,
)
print(f"Response: {chat.choices[0].message.content}")
```

### With Logging

```python
from sharpai_sdk import configure
from sharpai_sdk.sdk_logging import set_log_level

# Configure the SDK
configure(
    endpoint="http://localhost:8000",
    timeout=30,
    retries=3,
)

# Enable debug logging
set_log_level("DEBUG")
```

## ⚙️ Configuration

SharpAI SDK uses a simple configuration approach. No authentication tokens, tenant GUIDs, or access keys are required.

```python
from sharpai_sdk import configure

configure(
    endpoint="http://localhost:8000",  # Base URL of the SharpAI API
    timeout=30,                         # Request timeout in seconds (default: 10)
    retries=3,                          # Number of retry attempts (default: 3)
)
```

### Timeout Configuration

```python
from sharpai_sdk import configure

configure(
    endpoint="http://localhost:8000",
    timeout=60,    # 60 seconds timeout
    retries=5,      # 5 retry attempts
)
```

### Logging Configuration

```python
from sharpai_sdk import configure
from sharpai_sdk.sdk_logging import set_log_level, log_info

# Set logging level
set_log_level("DEBUG")

# Add log
log_info("INFO", "This is an info message")
```

Available log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## 📖 API Reference

### Connectivity Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Connectivity.validate | Validate API connectivity | None | bool | `HEAD /` |

### Ollama API Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Ollama.list_models | List all local models | None | TagsResponse | `GET /api/tags` |
| Ollama.pull_model | Pull a model from registry | model: str | dict | `POST /api/pull` |
| Ollama.delete_model | Delete a model | name: str | dict | `DELETE /api/delete` |
| Ollama.generate_embedding | Generate embeddings | model: str<br>input_data: Union[str, List[str]] | EmbedResponse | `POST /api/embed` |
| Ollama.generate | Generate text completion | model: str<br>prompt: str<br>stream: bool = False<br>options: dict = None | GenerateResponse | `POST /api/generate` |
| Ollama.chat | Generate chat completion | model: str<br>messages: List[dict]<br>stream: bool = False<br>options: dict = None | ChatResponse | `POST /api/chat` |

### OpenAI-Compatible API Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| OpenAI.create_embedding | Create embeddings | model: str<br>input_data: Union[str, List[str]]<br>user: str = None | OpenAIEmbeddingResponse | `POST /v1/embeddings` |
| OpenAI.create_completion | Create text completion | model: str<br>prompt: Union[str, List[str]]<br>max_tokens: int = None<br>temperature: float = None<br>top_p: float = None<br>n: int = 1<br>stream: bool = False<br>presence_penalty: float = None<br>frequency_penalty: float = None<br>stop: Union[str, List[str]] = None<br>user: str = None<br>seed: int = None | OpenAICompletionResponse | `POST /v1/completions` |
| OpenAI.create_chat_completion | Create chat completion | model: str<br>messages: List[dict]<br>temperature: float = None<br>top_p: float = None<br>n: int = 1<br>stream: bool = False<br>stop: Union[str, List[str]] = None<br>max_tokens: int = None<br>presence_penalty: float = None<br>frequency_penalty: float = None<br>user: str = None<br>seed: int = None | OpenAIChatCompletionResponse | `POST /v1/chat/completions` |

## Core Components

### Base Models

- `TagsResponse`: Response model for listing models
- `EmbedResponse`: Response model for embeddings (Ollama)
- `GenerateResponse`: Response model for text generation (Ollama)
- `ChatResponse`: Response model for chat completions (Ollama)
- `OpenAIEmbeddingResponse`: Response model for embeddings (OpenAI)
- `OpenAICompletionResponse`: Response model for text completions (OpenAI)
- `OpenAIChatCompletionResponse`: Response model for chat completions (OpenAI)

## 🔧 Ollama API Methods

### Connectivity Validation

```python
from sharpai_sdk import configure, Connectivity

configure(endpoint="http://localhost:8000")

# Validate connectivity
is_connected = Connectivity.validate()
if is_connected:
    print("✓ Successfully connected to SharpAI API")
else:
    print("✗ Failed to connect to SharpAI API")
```

### Model Management

#### List Models

```python
from sharpai_sdk import configure, Ollama

configure(endpoint="http://localhost:8000")

# List all available models
models = Ollama.list_models()
print(f"Found {len(models.models)} models:")
for model in models.models:
    print(f"  - {model.name}")
```

#### Generate Embeddings

```python
from sharpai_sdk import configure, Ollama

configure(endpoint="http://localhost:8000")

# Generate embedding for a single text
embedding = Ollama.generate_embedding(
    model="leliuga/all-MiniLM-L6-v2-GGUF",
    input_data="Hello, SharpAI!",
)
print(f"Embedding dimensions: {len(embedding.embedding)}")

# Generate embeddings for multiple texts
embeddings = Ollama.generate_embedding(
    model="leliuga/all-MiniLM-L6-v2-GGUF",
    input_data=["Why is the sky blue?", "Why is the grass green?"],
)
print(f"Generated {len(embeddings.embeddings)} embeddings")
```

#### Generate Text Completion

```python
from sharpai_sdk import configure, Ollama

configure(endpoint="http://localhost:8000")

# Non-streaming completion
completion = Ollama.generate(
    model="QuantFactory/Qwen2.5-3B-GGUF",
    prompt="What is artificial intelligence?",
    stream=False,
    options={
        "num_predict": 100,
        "temperature": 0.8,
    },
)
print(f"Completion: {completion.response}")

# Streaming completion
print("Streaming completion:")
for chunk in Ollama.generate(
    model="QuantFactory/Qwen2.5-3B-GGUF",
    prompt="What is artificial intelligence?",
    stream=True,
    options={
        "num_predict": 100,
        "temperature": 0.8,
    },
):
    if chunk.response:
        print(chunk.response, end="", flush=True)
print()  # New line after streaming
```

#### Generate Chat Completion

```python
from sharpai_sdk import configure, Ollama

configure(endpoint="http://localhost:8000")

# Non-streaming chat completion
chat = Ollama.chat(
    model="QuantFactory/Qwen2.5-3B-GGUF",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is Python?"},
    ],
    stream=False,
    options={
        "num_predict": 100,
        "temperature": 0.8,
    },
)
if chat.message and chat.message.content:
    print(f"Response: {chat.message.content}")

# Streaming chat completion
print("Streaming chat:")
for chunk in Ollama.chat(
    model="QuantFactory/Qwen2.5-3B-GGUF",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is Python?"},
    ],
    stream=True,
    options={
        "num_predict": 100,
        "temperature": 0.8,
    },
):
    if chunk.message and chunk.message.content:
        print(chunk.message.content, end="", flush=True)
print()  # New line after streaming
```

#### Pulling Models

```python
from sharpai_sdk import configure, Ollama

configure(endpoint="http://localhost:8000")

# Pull a model from registry
pull_response = Ollama.pull_model(model="TheBloke/Llama-2-7B-Chat-GGUF")
print("Model pull initiated")

# Note: The pull_model method returns a dictionary with status information
# For streaming progress updates, you may need to check the response periodically
```

#### Listing Models

```python
from sharpai_sdk import configure, Ollama

configure(endpoint="http://localhost:8000")

# List all available models
models = Ollama.list_models()
if models and models.models:
    print(f"Found {len(models.models)} models:")
    for model in models.models:
        print(f"  - {model.name}")
        if hasattr(model, 'size') and model.size:
            print(f"    Size: {model.size} bytes")
```

#### Deleting Models

```python
from sharpai_sdk import configure, Ollama

configure(endpoint="http://localhost:8000")

# Delete a model
delete_response = Ollama.delete_model(name="llama3")
print("Model deleted")
```

## 🤖 OpenAI API Methods

### Create Embeddings

```python
from sharpai_sdk import configure, OpenAI

configure(endpoint="http://localhost:8000")

# Create embedding for a single text
embedding = OpenAI.create_embedding(
    model="leliuga/all-MiniLM-L6-v2-GGUF",
    input_data="test",
)
print(f"Generated {len(embedding.data)} embedding(s)")
print(f"Embedding dimensions: {len(embedding.data[0].embedding)}")

# Create embeddings for multiple texts
embeddings = OpenAI.create_embedding(
    model="leliuga/all-MiniLM-L6-v2-GGUF",
    input_data=["hello, world", "foo to the bar"],
)
print(f"Generated {len(embeddings.data)} embeddings")
```

#### Create Text Completion

```python
from sharpai_sdk import configure, OpenAI

configure(endpoint="http://localhost:8000")

# Non-streaming completion
completion = OpenAI.create_completion(
    model="QuantFactory/Qwen2.5-3B-GGUF",
    prompt="Write a brief explanation of machine learning in simple terms.",
    max_tokens=150,
    temperature=0.7,
    top_p=0.9,
    n=1,
    stream=False,
    presence_penalty=0.0,
    frequency_penalty=0.3,
    stop=["###", "END"],
)
print(f"Completion: {completion.choices[0].text}")

# Streaming completion
print("Streaming completion:")
for chunk in OpenAI.create_completion(
    model="QuantFactory/Qwen2.5-3B-GGUF",
    prompt="Write a brief explanation of machine learning in simple terms.",
    max_tokens=150,
    temperature=0.7,
    stream=True,
):
    if chunk.choices and chunk.choices[0].text:
        print(chunk.choices[0].text, end="", flush=True)
print()  # New line after streaming

# Create completions for multiple prompts
completions = OpenAI.create_completion(
    model="QuantFactory/Qwen2.5-3B-GGUF",
    prompt=[
        "Write a brief explanation of machine learning in simple terms.",
        "Give me a brief overview of the C programming language.",
    ],
    max_tokens=150,
    temperature=0.7,
)
for i, choice in enumerate(completions.choices):
    print(f"Completion {i}: {choice.text}")
```

#### Create Chat Completion

```python
from sharpai_sdk import configure, OpenAI

configure(endpoint="http://localhost:8000")

# Create chat completion
chat = OpenAI.create_chat_completion(
    model="QuantFactory/Qwen2.5-3B-GGUF",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant specializing in technical topics.",
            "name": "system_instructor",
        },
        {
            "role": "user",
            "content": "Explain how neural networks work, briefly",
            "name": "john_doe",
        },
    ],
    temperature=0.7,
    top_p=0.9,
    n=1,
    stream=False,
    stop=["\n\n", "END"],
    max_tokens=1000,
    presence_penalty=0.0,
    frequency_penalty=0.3,
    user="user-123456",
    seed=42,
)
if chat.choices:
    message = chat.choices[0].message
    print(f"Role: {message.role}")
    print(f"Content: {message.content}")
```

## Error Handling

The SDK includes comprehensive error handling with specific exception types:

- `AuthenticationError`: Authentication issues
- `AuthorizationError`: Authorization issues
- `BadRequestError`: Invalid request parameters
- `ConflictError`: Resource conflict errors
- `DeserializationError`: Data deserialization errors
- `InactiveError`: Resource inactive errors
- `InUseError`: Resource in use errors
- `InvalidRangeError`: Invalid range errors
- `NotEmptyError`: Resource not empty errors
- `ResourceNotFoundError`: Requested resource not found
- `ServerError`: Server-side issues
- `TimeoutError`: Request timeout
- `SdkException`: Base SDK exception

Example error handling:

```python
from sharpai_sdk import Ollama
from sharpai_sdk.exceptions import ResourceNotFoundError, BadRequestError

try:
    models = Ollama.list_models()
except ResourceNotFoundError as e:
    print(f"Resource not found: {e}")
except BadRequestError as e:
    print(f"Bad request: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Logging

The SDK includes a built-in logging system that can be configured:

```python
from sharpai_sdk.sdk_logging import set_log_level, log_info

# Set logging level
set_log_level("DEBUG")

# Add log
log_info("INFO", "This is an info message")
```

Available log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## Advanced Configuration

### Custom Timeout and Retries

```python
from sharpai_sdk import configure

configure(
    endpoint="http://localhost:8000",
    timeout=60,    # 60 seconds timeout
    retries=5,     # 5 retry attempts
)
```

### Error Handling with Retries

The SDK automatically retries failed requests based on the configured retry count. Retries are performed for:
- Network errors
- Timeout errors
- Transient server errors (5xx status codes)

## Development

### Setting up Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. To set up pre-commit:

```bash
# Install pre-commit
pip install pre-commit

# Install the pre-commit hooks
pre-commit install

# (Optional) Run pre-commit on all files
pre-commit run --all-files
```

The pre-commit hooks will run automatically on `git commit`. They help maintain:

- Code formatting (using ruff)
- Import sorting
- Code quality checks
- And other project-specific checks

### Running Tests

The project uses `tox` for running tests in isolated environments. Make sure you have tox installed:

```bash
pip install tox
```

To run the default test environment:

```bash
tox
```

To run specific test environments:

```bash
# Run only the tests
tox -e default

# Run tests with coverage report
tox -- --cov sharpai_sdk --cov-report term-missing

# Build documentation
tox -e docs

# Build the package
tox -e build

# Clean build artifacts
tox -e clean
```

### Development Installation

For development, you can install the package with all test dependencies:

```bash
pip install -e ".[testing]"
```

### Running Examples

The SDK includes example scripts in the `examples/` directory:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run connectivity demo
python examples/demo_connectivity.py

# Run Ollama API demo
python examples/demo_ollama.py

# Run OpenAI-compatible API demo
python examples/demo_openai.py

# Run complete demo
python examples/demo_complete.py
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## Feedback and Issues

Have feedback or found an issue? Please file an issue in our GitHub repository.

## Version History

Please refer to [CHANGELOG.md](CHANGELOG.md) for a detailed version history.

## License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## Acknowledgments

This project has been set up using PyScaffold 4.5. For details and usage information on PyScaffold see https://pyscaffold.org/.
