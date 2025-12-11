from __future__ import annotations

import os

from trainwreck.llm.base import LLMClient
from trainwreck.llm.types import LLMProvider


def make_llm_client(provider: str | None = None) -> LLMClient:
    """
    Factory to create an LLM client based on provider name.
    Falls back to MODEL_PROVIDER env var, then 'ollama'.
    """
    provider = provider or os.getenv("MODEL_PROVIDER", "ollama")
    provider = provider.lower()

    if provider == "openai":
        from trainwreck.llm.openai_client import OpenAILLMClient

        return OpenAILLMClient()
    elif provider == "abacus":
        from trainwreck.llm.abacus_client import AbacusLLMClient

        return AbacusLLMClient()
    elif provider == "ollama":
        from trainwreck.llm.local.ollama import OllamaClient

        return OllamaClient()
    elif provider == "lmstudio":
        from trainwreck.llm.local.lmstudio import LMStudioClient

        return LMStudioClient()
    elif provider == "vllm":
        from trainwreck.llm.local.vllm import VLLMClient

        return VLLMClient()
    elif provider == "localai":
        from trainwreck.llm.local.localai import LocalAIClient

        return LocalAIClient()
    elif provider == "llamacpp":
        from trainwreck.llm.local.llamacpp import LlamaCppClient

        return LlamaCppClient()
    elif provider == "oobabooga":
        from trainwreck.llm.local.oobabooga import OobaboogaClient

        return OobaboogaClient()
    elif provider == "koboldcpp":
        from trainwreck.llm.local.koboldcpp import KoboldCppClient

        return KoboldCppClient()
    elif provider == "jan":
        from trainwreck.llm.local.jan import JanClient

        return JanClient()
    elif provider == "gpt4all":
        from trainwreck.llm.local.gpt4all_client import GPT4AllClient

        return GPT4AllClient()
    elif provider == "hf_tgi":
        from trainwreck.llm.local.hf_tgi import HuggingFaceTGIClient

        return HuggingFaceTGIClient()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
