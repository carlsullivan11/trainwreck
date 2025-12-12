from __future__ import annotations

from pathlib import Path
from typing import Any

from trainwreck.agent.step_plan import StepPlan
from trainwreck.tools.abacus import AbacusClient
from trainwreck.tools.bash import BashExecutor
from trainwreck.tools.git import GitAdapter
from trainwreck.tools.mcp import MCPClient
from trainwreck.tools.powershell import PowerShellExecutor


class Executor:
    """Executes a step plan."""

    def __init__(
        self,
        repo_path: Path,
        abacus: AbacusClient | None = None,
        mcp: MCPClient | None = None,
    ) -> None:
        self.repo_path = repo_path
        self.bash = BashExecutor()
        self.powershell = PowerShellExecutor()
        self.git = GitAdapter(repo_path)
        self.abacus = abacus
        self.mcp = mcp

    def execute(self, plan: StepPlan) -> dict[str, Any]:
        """Execute the step plan and return the result."""
        if plan.action == "bash":
            return self._execute_bash(plan)
        elif plan.action == "powershell":
            return self._execute_powershell(plan)
        elif plan.action == "git":
            return self._execute_git(plan)
        elif plan.action == "mcp":
            return self._execute_mcp(plan)
        elif plan.action == "abacus":
            return self._execute_abacus(plan)
        elif plan.action == "write_file":
            return self._write_file(plan)
        elif plan.action == "read_file":
            return self._read_file(plan)
        else:
            return {"error": f"Unknown action: {plan.action}"}

    def _execute_bash(self, plan: StepPlan) -> dict[str, Any]:
        """Execute a bash command."""
        if not plan.command:
            return {"error": "No command provided"}
        result = self.bash.run(plan.command, cwd=str(self.repo_path))
        return {
            "action": "bash",
            "command": plan.command,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "returncode": result["returncode"],
        }

    def _execute_powershell(self, plan: StepPlan) -> dict[str, Any]:
        """Execute a PowerShell command."""
        if not plan.command:
            return {"error": "No command provided"}
        result = self.powershell.run(plan.command, cwd=str(self.repo_path))
        return {
            "action": "powershell",
            "command": plan.command,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "returncode": result["returncode"],
        }

    def _execute_git(self, plan: StepPlan) -> dict[str, Any]:
        """Execute a git command."""
        if not plan.command:
            return {"error": "No command provided"}
        # Parse git command
        parts = plan.command.split()
        if len(parts) < 2 or parts[0] != "git":
            return {"error": "Invalid git command"}

        git_cmd = parts[1]
        args = parts[2:]

        try:
            if git_cmd == "status":
                output = self.git.status()
            elif git_cmd == "add":
                output = self.git.add(args if args else ".")
            elif git_cmd == "commit":
                message = " ".join(args).strip('"').strip("'")
                output = self.git.commit(message)
            elif git_cmd == "push":
                output = self.git.push()
            elif git_cmd == "pull":
                output = self.git.pull()
            elif git_cmd == "branch":
                output = self.git.branch(args[0] if args else "new-branch")
            elif git_cmd == "checkout":
                output = self.git.checkout(args[0] if args else "main")
            elif git_cmd == "diff":
                output = self.git.diff(*args)
            elif git_cmd == "log":
                output = self.git.log()
            else:
                return {"error": f"Unsupported git command: {git_cmd}"}

            return {
                "action": "git",
                "command": plan.command,
                "output": output,
            }
        except Exception as e:
            return {
                "action": "git",
                "command": plan.command,
                "error": str(e),
            }

    def _execute_mcp(self, plan: StepPlan) -> dict[str, Any]:
        """Execute an MCP tool call."""
        if not self.mcp:
            return {"error": "MCP client not initialized"}
        if not plan.tool_name:
            return {"error": "No tool name provided"}

        try:
            result = self.mcp.call_tool(plan.tool_name, plan.arguments or {})
            return {
                "action": "mcp",
                "tool_name": plan.tool_name,
                "result": result,
            }
        except Exception as e:
            return {
                "action": "mcp",
                "tool_name": plan.tool_name,
                "error": str(e),
            }

    def _execute_abacus(self, plan: StepPlan) -> dict[str, Any]:
        """Execute an Abacus.AI API call."""
        if not self.abacus:
            return {"error": "Abacus client not initialized"}

        # This is a simplified example; extend based on your needs
        try:
            deployments = self.abacus.list_deployments()
            return {
                "action": "abacus",
                "result": deployments,
            }
        except Exception as e:
            return {
                "action": "abacus",
                "error": str(e),
            }

    def _write_file(self, plan: StepPlan) -> dict[str, Any]:
        """Write content to a file."""
        if not plan.file_path or not plan.content:
            return {"error": "file_path and content required"}

        file_path = self.repo_path / plan.file_path
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(plan.content)
            return {
                "action": "write_file",
                "file_path": str(file_path),
                "status": "success",
            }
        except Exception as e:
            return {
                "action": "write_file",
                "file_path": str(file_path),
                "error": str(e),
            }

    def _read_file(self, plan: StepPlan) -> dict[str, Any]:
        """Read content from a file."""
        if not plan.file_path:
            return {"error": "file_path required"}

        file_path = self.repo_path / plan.file_path
        try:
            content = file_path.read_text()
            return {
                "action": "read_file",
                "file_path": str(file_path),
                "content": content,
            }
        except Exception as e:
            return {
                "action": "read_file",
                "file_path": str(file_path),
                "error": str(e),
            }
