from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class StepPlan:
    """A single step in the development plan."""

    action: Literal["bash", "powershell", "git", "mcp", "abacus", "write_file", "read_file"]
    description: str
    command: str | None = None
    file_path: str | None = None
    content: str | None = None
    tool_name: str | None = None
    arguments: dict | None = None
