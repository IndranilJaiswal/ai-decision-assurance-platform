"""
gemini_client.py

Purpose:
---------
Provides a reusable Gemini client for
AI Assurance Platform agents.

Current Consumers:
------------------

claim_discovery_agent.py

Future Consumers:
-----------------

remediation_agent.py
explanation_agent.py
"""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not configured"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text
