from __future__ import annotations

import subprocess
from typing import Any


class BashExecutor:
    """Execute bash commands."""

    def run(self, command: str, cwd: str | None = None, **kwargs: Any) -> dict[str, Any]:
        """Run a bash command and return the result."""
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            **kwargs,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
