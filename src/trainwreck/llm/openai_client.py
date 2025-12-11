from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from trainwreck.llm.base import LLMClient


class OpenAILLMClient(LLMClient):
    """OpenAI LLM client."""

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")

    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion using OpenAI's API."""
        response = self.client.completions.create(
            model=self.model,
            prompt=prompt,
            **kwargs,
        )
        return response.choices[0].text.strip()

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a chat completion using OpenAI's API.""""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore
            **kwargs,
        )
        return response.choices[0].message.content or ""
