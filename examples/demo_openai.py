"""
Demo script for OpenAI-compatible API endpoints.
Demonstrates usage of the OpenAI resource class.
"""

from sharpai_sdk import configure, OpenAI

# Configure the SDK
configure(
    endpoint="http://localhost:8000",
    timeout=30,
    retries=3,
)


def create_embedding_singular():
    """Generate embeddings (singular)."""
    print("\n1. Generating embeddings (singular)...")
    try:
        embed_response = OpenAI.create_embedding(
            model="leliuga/all-MiniLM-L6-v2-GGUF",
            input_data="test",
        )
        print(f"Generated {len(embed_response.data)} embedding(s)")
        if embed_response.data:
            print(f"  Embedding dimensions: {len(embed_response.data[0].embedding)}")
    except Exception as e:
        print(f"Error generating embeddings: {e}")


def create_embedding_multiple():
    """Generate embeddings (multiple)."""
    print("\n2. Generating embeddings (multiple)...")
    try:
        embed_response = OpenAI.create_embedding(
            model="leliuga/all-MiniLM-L6-v2-GGUF",
            input_data=["hello, world", "foo to the bar"],
        )
        print(f"Generated {len(embed_response.data)} embeddings")
        for i, emb in enumerate(embed_response.data):
            print(f"  Embedding {i}: {len(emb.embedding)} dimensions")
    except Exception as e:
        print(f"Error generating embeddings: {e}")


def create_completion_single():
    """Generate completion (single)."""
    print("\n3. Generating completion (single)...")
    try:
        completion_response = OpenAI.create_completion(
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
        print(f"Generated {len(completion_response.choices)} completion(s)")
        if completion_response.choices:
            print(f"  Completion: {completion_response.choices[0].text[:200]}...")
    except Exception as e:
        print(f"Error generating completion: {e}")


def create_completion_multiple():
    """Generate completion (multiple prompts)."""
    print("\n4. Generating completion (multiple prompts)...")
    try:
        completion_response = OpenAI.create_completion(
            model="QuantFactory/Qwen2.5-3B-GGUF",
            prompt=[
                "Write a brief explanation of machine learning in simple terms.",
                "Give me a brief overview of the C programming language.",
            ],
            max_tokens=150,
            temperature=0.7,
            top_p=0.9,
            n=1,
            stream=False,
            presence_penalty=0.0,
            frequency_penalty=0.3,
            stop=["###", "END"],
        )
        print(f"Generated {len(completion_response.choices)} completion(s)")
        for i, choice in enumerate(completion_response.choices):
            print(f"  Completion {i}: {choice.text[:150]}...")
    except Exception as e:
        print(f"Error generating completion: {e}")


def create_chat_completion():
    """Generate chat completion."""
    print("\n5. Generating chat completion...")
    try:
        chat_response = OpenAI.create_chat_completion(
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
        print(f"Generated {len(chat_response.choices)} chat completion(s)")
        if chat_response.choices:
            message = chat_response.choices[0].message
            print(f"  Role: {message.role}")
            print(f"  Content: {message.content[:200]}...")
    except Exception as e:
        print(f"Error generating chat completion: {e}")


print("=" * 60)
print("OpenAI-Compatible API Demo")
print("=" * 60)

create_embedding_singular()
create_embedding_multiple()
create_completion_single()
create_completion_multiple()
create_chat_completion()
