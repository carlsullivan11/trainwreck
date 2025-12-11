from __future__ import annotations

import os
from typing import Any

import httpx


class AbacusClient:
    """Abacus.AI API client."""

    def __init__(self) -> None:
        self.api_key = os.getenv("ABACUS_API_KEY")
        if not self.api_key:
            raise ValueError("ABACUS_API_KEY environment variable not set")
        self.base_url = "https://api.abacus.ai"

    def list_deployments(self) -> list[dict[str, Any]]:
        """List all deployments."""
        url = f"{self.base_url}/v0/deployments"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json().get("deployments", [])

    def create_deployment(self, model_id: str, name: str, **kwargs: Any) -> dict[str, Any]:
        """Create a new deployment."""
        url = f"{self.base_url}/v0/deployments"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "modelId": model_id,
            "name": name,
            **kwargs,
        }
        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()

    def predict(self, deployment_id: str, data: dict[str, Any], deployment_token: str | None = None) -> dict[str, Any]:
        """Run a prediction on a deployment."""
        url = f"{self.base_url}/v0/deployments/{deployment_id}/predict"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if deployment_token:
            headers["X-Deployment-Token"] = deployment_token

        with httpx.Client() as client:
            response = client.post(url, json=data, headers=headers, timeout=60.0)
            response.raise_for_status()
            return response.json()

    def upload_dataset(self, name: str, file_path: str, **kwargs: Any) -> dict[str, Any]:
        """Upload a dataset."""
        url = f"{self.base_url}/v0/datasets"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {"name": name, **kwargs}
            with httpx.Client() as client:
                response = client.post(url, data=data, files=files, headers=headers, timeout=120.0)
                response.raise_for_status()
                return response.json()
