from __future__ import annotations

import subprocess
from typing import Any


class PowerShellExecutor:
    """Execute PowerShell commands."""

    def run(self, command: str, cwd: str | None = None, **kwargs: Any) -> dict[str, Any]:
        """Run a PowerShell command and return the result."""
        result = subprocess.run(
            ["powershell", "-Command", command],
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
