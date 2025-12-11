from __future__ import annotations

import os
from typing import Any

import httpx

from trainwreck.llm.base import LLMClient


class LlamaCppClient(LLMClient):
    """llama.cpp server local LLM client."""

    def __init__(self) -> None:
        self.base_url = os.getenv("LLAMACPP_BASE_URL", "http://localhost:8080")

    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion using llama.cpp server."""
        url = f"{self.base_url}/completion"
        payload = {
            "prompt": prompt,
            "stream": False,
            **kwargs,
        }
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()
            return data.get("content", "")

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a chat completion using llama.cpp server."""
        # llama.cpp server may not have a dedicated chat endpoint
        # Convert messages to a single prompt
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return self.complete(prompt, **kwargs)
