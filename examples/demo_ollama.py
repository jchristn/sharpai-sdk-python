"""
Demo script for Ollama API endpoints.
Demonstrates usage of the Ollama resource class.
"""

from sharpai_sdk import configure, Ollama

# Configure the SDK
configure(
    endpoint="http://localhost:8000",
    timeout=30,
    retries=3,
)


def list_models():
    """List local models."""
    print("\n1. Listing local models...")
    try:
        models_response = Ollama.list_models()
        print(f"Found {len(models_response.models)} models:")
        for model in models_response.models:
            print(f"  - {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")


def generate_embedding_singular():
    """Generate embeddings (singular)."""
    print("\n2. Generating embeddings (singular)...")
    try:
        embed_response = Ollama.generate_embedding(
            model="leliuga/all-MiniLM-L6-v2-GGUF",
            input_data="asdf",
        )
        if embed_response.embedding:
            print(
                f"Generated embedding with {len(embed_response.embedding)} dimensions"
            )
        elif embed_response.embeddings:
            print(f"Generated {len(embed_response.embeddings)} embeddings")
    except Exception as e:
        print(f"Error generating embeddings: {e}")


def generate_embedding_multiple():
    """Generate embeddings (multiple)."""
    print("\n3. Generating embeddings (multiple)...")
    try:
        embed_response = Ollama.generate_embedding(
            model="leliuga/all-MiniLM-L6-v2-GGUF",
            input_data=["Why is the sky blue?", "Why is the grass green?"],
        )
        if embed_response.embeddings:
            print(f"Generated {len(embed_response.embeddings)} embeddings")
            for i, emb in enumerate(embed_response.embeddings):
                print(f"  Embedding {i}: {len(emb.embedding)} dimensions")
    except Exception as e:
        print(f"Error generating embeddings: {e}")


def generate_completion():
    """Generate a completion."""
    print("\n4. Generating a completion...")
    try:
        generate_response = Ollama.generate(
            model="QuantFactory/Qwen2.5-3B-GGUF",
            prompt="why is the sky blue",
            stream=False,
            options={
                "num_predict": 100,
                "temperature": 0.8,
            },
        )
        if generate_response.response:
            print(f"Generated response: {generate_response.response[:200]}...")
    except Exception as e:
        print(f"Error generating completion: {e}")


def generate_chat_completion():
    """Generate a chat completion."""
    print("\n5. Generating a chat completion...")
    try:
        chat_response = Ollama.chat(
            model="QuantFactory/Qwen2.5-3B-GGUF",
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful AI assistant. be nice",
                },
                {"role": "user", "content": "what can you tell me about botox"},
            ],
            stream=False,
            options={
                "num_predict": 100,
                "temperature": 0.8,
            },
        )
        if chat_response.message and chat_response.message.content:
            print(f"Chat response: {chat_response.message.content[:200]}...")
    except Exception as e:
        print(f"Error generating chat completion: {e}")


print("=" * 60)
print("Ollama API Demo")
print("=" * 60)

list_models()
generate_embedding_singular()
generate_embedding_multiple()
generate_completion()
generate_chat_completion()

print("\n" + "=" * 60)
print("Demo completed!")
print("=" * 60)
