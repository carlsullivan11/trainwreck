from __future__ import annotations

import os
from typing import Any

import httpx

from trainwreck.llm.base import LLMClient


class HuggingFaceTGIClient(LLMClient):
    """Hugging Face Text Generation Inference (TGI) local LLM client."""

    def __init__(self) -> None:
        self.base_url = os.getenv("HF_TGI_BASE_URL", "http://localhost:8080")

    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion using HF TGI."""
        url = f"{self.base_url}/generate"
        payload = {
            "inputs": prompt,
            **kwargs,
        }
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()
            return data.get("generated_text", "")

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a chat completion using HF TGI."""
        # TGI doesn't have a dedicated chat endpoint
        # Convert messages to a single prompt
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return self.complete(prompt, **kwargs)
