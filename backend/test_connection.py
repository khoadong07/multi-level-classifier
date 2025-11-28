#!/usr/bin/env python3
"""Test API connection"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
import openai

# Load .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

print("=" * 60)
print("Testing API Connection")
print("=" * 60)

base_url = os.getenv("OPENAI_BASE_URL")
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")

print(f"\n📡 Configuration:")
print(f"   Base URL: {base_url}")
print(f"   API Key: {api_key}")
print(f"   Model: {model}")

print(f"\n🔌 Testing connection...")

try:
    client = openai.OpenAI(base_url=base_url, api_key=api_key)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello' in one word."}
        ],
        temperature=0,
        max_tokens=10
    )
    
    result = response.choices[0].message.content
    print(f"✅ Connection successful!")
    print(f"   Response: {result}")
    print(f"\n✅ API is working correctly!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print(f"\n⚠️  Please check:")
    print(f"   1. Base URL is correct and accessible")
    print(f"   2. API key is valid")
    print(f"   3. Model name is correct")
    sys.exit(1)

print("=" * 60)
