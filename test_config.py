"""Test script for config module"""
from chatbot import config

print("Testing Configuration Module")
print("=" * 50)
print(f"OpenAI API Key: {'Set' if config.OPENAI_API_KEY else 'Not Set'}")
print(f"Vector Store Path: {config.VECTOR_STORE_PATH}")
print(f"Resume Path: {config.RESUME_PATH}")
print("=" * 50)
print("✓ Config module loaded successfully!")
