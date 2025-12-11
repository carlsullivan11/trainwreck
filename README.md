# TrainWreck

**TrainWreck** is a *vibe coding agent* with:

- A **Plan → Act → Reflect** feedback loop
- Support for **top local model stacks** (Ollama, LM Studio, vLLM, LocalAI, llama.cpp, Oobabooga, KoboldCpp, Jan, GPT4All, HF TGI)
- Integration with **Abacus.AI APIs**
- Ability to run **bash** and **PowerShell** commands
- **Git** integration (commit, push, pull, branch)
- **MCP (Model Context Protocol)** client support
- A clean, extensible architecture inspired by "vibe coding" and `codepuppy`-style structure

---

## Features

- **Multi-LLM Support**: OpenAI, Abacus.AI, and 10+ local model stacks
- **Feedback Loop**: Iterative planning, execution, and reflection
- **Tool Execution**: Bash, PowerShell, Git, MCP, Abacus.AI
- **Memory**: SQLite-backed conversation and step history
- **Extensible**: Easy to add new LLM providers or tools

---

## Architecture

```
src/trainwreck
├── cli.py              # CLI entrypoint
├── agent/              # Core agent logic (planner, executor, reflector, loop)
├── llm/                # LLM abstraction + provider clients
├── tools/              # Tool adapters (bash, powershell, git, mcp, abacus)
└── memory/             # Memory store(s)
```

### Agent Flow

1. **Planner**: Takes the goal + context → generates a `StepPlan`
2. **Executor**: Runs the plan (bash, git, API calls, etc.) → produces output
3. **Reflector**: Scores the output, suggests improvements
4. **FeedbackLoop**: Iterates until goal is met or max iterations reached

---

## Installation

### Prerequisites

- Python 3.11+
- Poetry (recommended) or pip

### Clone & Install

```bash
git clone https://github.com/yourusername/trainwreck.git
cd trainwreck
poetry install
```

Or with pip:

```bash
pip install -e .
```

### Optional: GPT4All

```bash
poetry install -E gpt4all
```

---

## Configuration

TrainWreck uses environment variables for LLM provider configuration.

### OpenAI

```bash
export MODEL_PROVIDER=openai
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4  # optional, default: gpt-4
```

### Abacus.AI

```bash
export MODEL_PROVIDER=abacus
export ABACUS_API_KEY=your-abacus-key
export ABACUS_DEPLOYMENT_ID=your-deployment-id
export ABACUS_DEPLOYMENT_TOKEN=your-deployment-token  # optional
```

### Local Models

#### Ollama

```bash
export MODEL_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434  # optional
export OLLAMA_MODEL=llama2  # optional
```

#### LM Studio

```bash
export MODEL_PROVIDER=lmstudio
export LMSTUDIO_BASE_URL=http://localhost:1234  # optional
export LMSTUDIO_MODEL=local-model  # optional
```

#### vLLM

```bash
export MODEL_PROVIDER=vllm
export VLLM_BASE_URL=http://localhost:8000
export VLLM_MODEL=meta-llama/Llama-2-7b-hf
```

#### LocalAI

```bash
export MODEL_PROVIDER=localai
export LOCALAI_BASE_URL=http://localhost:8080
export LOCALAI_MODEL=gpt-3.5-turbo
```

#### llama.cpp server

```bash
export MODEL_PROVIDER=llamacpp
export LLAMACPP_BASE_URL=http://localhost:8080
```

#### Oobabooga Text Generation WebUI

```bash
export MODEL_PROVIDER=oobabooga
export OOBABOOGA_BASE_URL=http://localhost:5000
```

#### KoboldCpp

```bash
export MODEL_PROVIDER=koboldcpp
export KOBOLDCPP_BASE_URL=http://localhost:5001
```

#### Jan

```bash
export MODEL_PROVIDER=jan
export JAN_BASE_URL=http://localhost:1337
export JAN_MODEL=mistral-ins-7b-q4
```

#### GPT4All

```bash
export MODEL_PROVIDER=gpt4all
export GPT4ALL_MODEL_NAME=mistral-7b-openorca.Q4_0.gguf
```

#### Hugging Face TGI

```bash
export MODEL_PROVIDER=hf_tgi
export HF_TGI_BASE_URL=http://localhost:8080
```

---

## Usage

### Basic Run

```bash
poetry run trainwreck run   --goal "Add unit tests for the auth module"   --model ollama   --repo .
```

### With MCP Server

```bash
poetry run trainwreck run   --goal "Refactor the data access layer"   --model lmstudio   --repo .   --mcp-server "node ./mcp-server/index.js"
```

### Custom Max Iterations

```bash
trainwreck run   --goal "Implement OAuth2 flow"   --model openai   --repo /path/to/project   --max-iters 30
```

---

## Development

### Setup

```bash
poetry install --with dev
poetry run pre-commit install
```

### Linting & Formatting

```bash
poetry run ruff check src/
poetry run black src/
poetry run isort src/
```

### Type Checking

```bash
poetry run mypy src/
```

### Testing

```bash
poetry run pytest
```

---

## Integration Notes

### Abacus.AI

The `AbacusClient` in `trainwreck.tools.abacus` provides methods to:

- List deployments
- Create/update deployments
- Run predictions
- Manage datasets

Set `ABACUS_API_KEY`, `ABACUS_DEPLOYMENT_ID`, and optionally `ABACUS_DEPLOYMENT_TOKEN`.

### MCP (Model Context Protocol)

TrainWreck can connect to MCP servers for extended tool capabilities. Pass `--mcp-server` with the command to start your MCP server:

```bash
--mcp-server "node ./mcp-server/index.js"
```

The `MCPClient` will communicate via stdio.

---

## License

MIT

---

## Contributing

Contributions welcome! Please open an issue or PR.

---

## Roadmap

- [ ] Add more tool adapters (Docker, Kubernetes, etc.)
- [ ] Web UI for monitoring feedback loops
- [ ] Plugin system for custom tools
- [ ] Multi-agent collaboration
- [ ] Enhanced memory with vector search

---

**TrainWreck** – vibe coding, powered by feedback loops and local AI.
