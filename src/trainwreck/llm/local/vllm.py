from __future__ import annotations

import os
from typing import Any

import httpx

from trainwreck.llm.base import LLMClient


class VLLMClient(LLMClient):
    """vLLM local LLM client."""

    def __init__(self) -> None:
        self.base_url = os.getenv("VLLM_BASE_URL", "http://localhost:8000")
        self.model = os.getenv("VLLM_MODEL", "meta-llama/Llama-2-7b-hf")

    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion using vLLM."""
        url = f"{self.base_url}/v1/completions"
        payload = {
            "model": self.model,
            "prompt": prompt,
            **kwargs,
        }
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["text"].strip()

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a chat completion using vLLM."""
        url = f"{self.base_url}/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            **kwargs,
        }
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
