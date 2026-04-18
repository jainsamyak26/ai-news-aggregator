import os
import json
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()


class DigestOutput(BaseModel):
    title: str
    summary: str


class DigestAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=api_key)
        self.model = "models/gemini-2.5-flash"

    def generate_digest(self, title: str, content: str, article_type: str) -> Optional[DigestOutput]:
        try:
            prompt = f"""
Create a digest for this {article_type}.

Title: {title}

Content: {content[:8000]}

Respond ONLY in JSON:
{{
  "title": "...",
  "summary": "..."
}}
"""

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            text = response.text.strip()

            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]

            parsed = json.loads(text.strip())

            return DigestOutput(**parsed)

        except Exception as e:
            print(f"Error generating digest: {e}")
            return None