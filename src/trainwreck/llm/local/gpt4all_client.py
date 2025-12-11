from __future__ import annotations

import os
from typing import Any

from trainwreck.llm.base import LLMClient


class GPT4AllClient(LLMClient):
    """GPT4All local LLM client."""

    def __init__(self) -> None:
        try:
            from gpt4all import GPT4All
        except ImportError:
            raise ImportError("gpt4all is not installed. Install with: poetry install -E gpt4all")

        model_name = os.getenv("GPT4ALL_MODEL_NAME", "mistral-7b-openorca.Q4_0.gguf")
        self.model = GPT4All(model_name)

    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion using GPT4All."""
        response = self.model.generate(prompt, **kwargs)
        return response

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a chat completion using GPT4All."""
        # GPT4All doesn't have a native chat API, convert to prompt
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return self.complete(prompt, **kwargs)
