"""
Complete demo script showcasing all SharpAI SDK features.
This script demonstrates connectivity validation, Ollama APIs, and OpenAI-compatible APIs.
"""

from sharpai_sdk import configure, Connectivity, Ollama, OpenAI

# Configure the SDK
configure(
    endpoint="http://localhost:8000",
    timeout=30,
    retries=3,
)


def validate_connectivity():
    """Validate connectivity to the SharpAI API."""
    print("\n[Step 1] Validating connectivity...")
    is_connected = Connectivity.validate()
    if is_connected:
        print("✓ Successfully connected to SharpAI API")
    else:
        print("✗ Failed to connect to SharpAI API")
        print("Please ensure the API server is running")
        exit(1)


def list_models():
    """List available models."""
    print("\n[Step 2] Listing available models...")
    try:
        models = Ollama.list_models()
        print(f"✓ Found {len(models.models)} available models")
        if models.models:
            print("  Available models:")
            for model in models.models[:5]:  # Show first 5
                print(f"    - {model.name}")
            if len(models.models) > 5:
                print(f"    ... and {len(models.models) - 5} more")
    except Exception as e:
        print(f"✗ Error listing models: {e}")


def generate_embedding_ollama():
    """Generate embeddings using Ollama API."""
    print("\n[Step 3] Generating embeddings (Ollama API)...")
    try:
        embed_response = Ollama.generate_embedding(
            model="leliuga/all-MiniLM-L6-v2-GGUF",
            input_data="Hello, SharpAI!",
        )
        if embed_response.embedding:
            print(
                f"✓ Generated embedding with {len(embed_response.embedding)} dimensions"
            )
    except Exception as e:
        print(f"✗ Error generating embeddings: {e}")


def generate_embedding_openai():
    """Generate embeddings using OpenAI-compatible API."""
    print("\n[Step 4] Generating embeddings (OpenAI-compatible API)...")
    try:
        embed_response = OpenAI.create_embedding(
            model="leliuga/all-MiniLM-L6-v2-GGUF",
            input_data="Hello, SharpAI!",
        )
        print(f"✓ Generated {len(embed_response.data)} embedding(s)")
    except Exception as e:
        print(f"✗ Error generating embeddings: {e}")


def generate_completion_ollama():
    """Generate text completion using Ollama API."""
    print("\n[Step 5] Generating text completion (Ollama API)...")
    try:
        completion = Ollama.generate(
            model="QuantFactory/Qwen2.5-3B-GGUF",
            prompt="What is artificial intelligence?",
            stream=False,
            options={"num_predict": 50, "temperature": 0.7},
        )
        if completion.response:
            print(f"✓ Generated completion: {completion.response[:150]}...")
    except Exception as e:
        print(f"✗ Error generating completion: {e}")


def generate_chat_completion_ollama():
    """Generate chat completion using Ollama API."""
    print("\n[Step 6] Generating chat completion (Ollama API)...")
    try:
        chat = Ollama.chat(
            model="QuantFactory/Qwen2.5-3B-GGUF",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is Python?"},
            ],
            stream=False,
            options={"num_predict": 50, "temperature": 0.7},
        )
        if chat.message and chat.message.content:
            print(f"✓ Generated chat response: {chat.message.content[:150]}...")
    except Exception as e:
        print(f"✗ Error generating chat completion: {e}")


def generate_chat_completion_openai():
    """Generate chat completion using OpenAI-compatible API."""
    print("\n[Step 7] Generating chat completion (OpenAI-compatible API)...")
    try:
        chat = OpenAI.create_chat_completion(
            model="QuantFactory/Qwen2.5-3B-GGUF",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is Python?"},
            ],
            max_tokens=100,
            temperature=0.7,
        )
        if chat.choices:
            message = chat.choices[0].message
            print(f"✓ Generated chat response: {message.content[:150]}...")
    except Exception as e:
        print(f"✗ Error generating chat completion: {e}")


print("=" * 70)
print("SharpAI SDK Complete Demo")
print("=" * 70)

validate_connectivity()
list_models()
generate_embedding_ollama()
generate_embedding_openai()
generate_completion_ollama()
generate_chat_completion_ollama()
generate_chat_completion_openai()

print("\n" + "=" * 70)
print("Demo completed successfully!")
print("=" * 70)
