"""
test_gemini_client.py

Purpose:
---------
Validate Gemini connectivity.
"""

from gemini_client import GeminiClient

client = GeminiClient()

response = client.generate(
    "Return exactly the word HELLO."
)

print(response)
