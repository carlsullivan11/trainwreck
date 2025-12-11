from __future__ import annotations

import json
from typing import Any

from trainwreck.agent.step_plan import StepPlan
from trainwreck.llm.base import LLMClient


class Planner:
    """Plans the next development step based on goal and context."""

    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def plan(self, goal: str, context: dict[str, Any]) -> StepPlan:
        """Generate a step plan for the given goal and context."""
        prompt = self._build_prompt(goal, context)
        response = self.llm.chat(
            messages=[
                {
                    "role": "system",
                    "content": "You are TrainWreck, a vibe coding agent. Plan the next development step.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return self._parse_plan(response)

    def _build_prompt(self, goal: str, context: dict[str, Any]) -> str:
        """Build the planning prompt."""
        repo_state = context.get("repo_state", "")
        history = context.get("history", [])
        history_str = "\n".join([f"- {h['description']}: {h['outcome']}" for h in history[-5:]])

        return f"""
Goal: {goal}

Repository State:
{repo_state}

Recent History:
{history_str}

Plan the next step to achieve the goal. Respond with a JSON object:
{{
  "action": "bash|powershell|git|mcp|abacus|write_file|read_file",
  "description": "What this step does",
  "command": "command to run (if applicable)",
  "file_path": "path to file (if applicable)",
  "content": "file content (if applicable)",
  "tool_name": "MCP tool name (if applicable)",
  "arguments": {{"key": "value"}} (if applicable)
}}
"""

    def _parse_plan(self, response: str) -> StepPlan:
        """Parse the LLM response into a StepPlan."""
        try:
            # Extract JSON from response (handle markdown code blocks)
            response = response.strip()
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1])
            data = json.loads(response)
            return StepPlan(**data)
        except (json.JSONDecodeError, TypeError):
            # Fallback: create a simple bash step
            return StepPlan(
                action="bash",
                description="Parse error, listing files",
                command="ls -la",
            )
