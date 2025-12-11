from typing import Literal

LLMProvider = Literal[
    "openai",
    "abacus",
    "ollama",
    "lmstudio",
    "vllm",
    "localai",
    "llamacpp",
    "oobabooga",
    "koboldcpp",
    "jan",
    "gpt4all",
    "hf_tgi",
]
