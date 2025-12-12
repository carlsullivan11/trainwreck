from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import click

from trainwreck.agent.executor import Executor
from trainwreck.agent.loop import FeedbackLoop
from trainwreck.agent.planner import Planner
from trainwreck.agent.reflector import Reflector
from trainwreck.llm.factory import make_llm_client
from trainwreck.memory.sqlite_store import SQLiteMemoryStore
from trainwreck.tools.abacus import AbacusClient
from trainwreck.tools.mcp import MCPClient


@click.group()
def cli() -> None:
    """trainwreck - vibe coding agent with feedback loops."""
    pass


@cli.command()
@click.option("--goal", required=True, help="Development goal for TrainWreck.")
@click.option("--model", default=None, help="LLM provider (overrides MODEL_PROVIDER).")
@click.option("--repo", default=".", help="Path to git repository.")
@click.option("--max-iters", default=20, show_default=True, help="Maximum feedback iterations.")
@click.option(
    "--mcp-server",
    default=None,
    help="MCP server command, e.g. 'node ./mcp-server/index.js'.",
)
def run(
    goal: str,
    model: Optional[str],
    repo: str,
    max_iters: int,
    mcp_server: Optional[str],
) -> None:
    """Run the TrainWreck agent on a given goal."""
    repo_path = Path(repo).resolve()
    if not repo_path.exists():
        raise click.BadParameter(f"Repository path does not exist: {repo_path}")

    provider = model or os.getenv("MODEL_PROVIDER", "ollama")

    llm = make_llm_client(provider=provider)
    planner = Planner(llm=llm)

    abacus: AbacusClient | None = None
    if os.getenv("ABACUS_API_KEY"):
        abacus = AbacusClient()

    mcp: MCPClient | None = None
    if mcp_server:
        mcp = MCPClient(server_command=mcp_server.split())

    executor = Executor(
        repo_path=repo_path,
        abacus=abacus,
        mcp=mcp,
    )
    reflector = Reflector()

    # Persist history in a local SQLite DB inside the repo
    memory_db_path = repo_path / ".trainwreck.db"
    memory = SQLiteMemoryStore(memory_db_path)

    click.echo(f"🚀 TrainWreck starting with model provider: {provider}")
    click.echo(f"📁 Repo: {repo_path}")
    click.echo(f"🎯 Goal: {goal}")
    click.echo(f"🔁 Max iterations: {max_iters}\n")

    loop = FeedbackLoop(planner, executor, reflector, memory=memory)
    history = loop.iterate(goal=goal, max_iters=max_iters)

    click.echo("\n📊 Summary:")
    click.echo(f"Iterations: {len(history)}")
    successes = sum(1 for h in history if h["score"] >= 0.9)
    click.echo(f"Successful steps (score >= 0.9): {successes}")

    if mcp is not None:
        mcp.close()


if __name__ == "__main__":
    cli()
