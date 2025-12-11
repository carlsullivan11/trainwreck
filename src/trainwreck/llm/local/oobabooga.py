from __future__ import annotations

import os
from typing import Any

import httpx

from trainwreck.llm.base import LLMClient


class OobaboogaClient(LLMClient):
    """Oobabooga Text Generation WebUI local LLM client."""

    def __init__(self) -> None:
        self.base_url = os.getenv("OOBABOOGA_BASE_URL", "http://localhost:5000")

    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion using Oobabooga."""
        url = f"{self.base_url}/api/v1/generate"
        payload = {
            "prompt": prompt,
            **kwargs,
        }
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()
            return data["results"][0]["text"]

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a chat completion using Oobabooga."""
        url = f"{self.base_url}/api/v1/chat"
        payload = {
            "messages": messages,
            **kwargs,
        }
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()
            return data["results"][0]["text"]
