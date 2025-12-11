from __future__ import annotations

from pathlib import Path
from typing import Any

from git import Repo


class GitAdapter:
    """Git operations adapter."""

    def __init__(self, repo_path: Path) -> None:
        self.repo = Repo(repo_path)

    def status(self) -> str:
        """Get git status."""
        return self.repo.git.status()

    def add(self, files: list[str] | str = ".") -> str:
        """Stage files."""
        return self.repo.git.add(files)

    def commit(self, message: str) -> str:
        """Commit staged changes."""
        return self.repo.git.commit("-m", message)

    def push(self, remote: str = "origin", branch: str | None = None) -> str:
        """Push commits to remote."""
        if branch is None:
            branch = self.repo.active_branch.name
        return self.repo.git.push(remote, branch)

    def pull(self, remote: str = "origin", branch: str | None = None) -> str:
        """Pull from remote."""
        if branch is None:
            branch = self.repo.active_branch.name
        return self.repo.git.pull(remote, branch)

    def branch(self, name: str, checkout: bool = True) -> str:
        """Create a new branch."""
        result = self.repo.git.branch(name)
        if checkout:
            self.repo.git.checkout(name)
        return result

    def checkout(self, branch: str) -> str:
        """Checkout a branch."""
        return self.repo.git.checkout(branch)

    def diff(self, *args: Any) -> str:
        """Get diff."""
        return self.repo.git.diff(*args)

    def log(self, max_count: int = 10) -> str:
        """Get commit log."""
        return self.repo.git.log(f"--max-count={max_count}", "--oneline")
