from __future__ import annotations

import os
from typing import Any

import httpx

from trainwreck.llm.base import LLMClient


class AbacusLLMClient(LLMClient):
    """Abacus.AI LLM client."""

    def __init__(self) -> None:
        self.api_key = os.getenv("ABACUS_API_KEY")
        if not self.api_key:
            raise ValueError("ABACUS_API_KEY environment variable not set")

        self.deployment_id = os.getenv("ABACUS_DEPLOYMENT_ID")
        if not self.deployment_id:
            raise ValueError("ABACUS_DEPLOYMENT_ID environment variable not set")

        self.deployment_token = os.getenv("ABACUS_DEPLOYMENT_TOKEN")
        self.base_url = "https://api.abacus.ai"

    def complete(self, prompt: str, **kwargs: Any) -> str:
        """Generate a completion using Abacus.AI."""
        return self._predict(prompt, **kwargs)

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a chat completion using Abacus.AI."""
        # Convert messages to a single prompt
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return self._predict(prompt, **kwargs)

    def _predict(self, prompt: str, **kwargs: Any) -> str:
        """Make a prediction request to Abacus.AI."""
        url = f"{self.base_url}/v0/deployments/{self.deployment_id}/predict"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        if self.deployment_token:
            headers["X-Deployment-Token"] = self.deployment_token

        payload = {
            "prompt": prompt,
            **kwargs,
        }

        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return data.get("prediction", "")
