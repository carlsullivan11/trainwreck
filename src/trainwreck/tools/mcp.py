from __future__ import annotations

import json
import subprocess
from typing import Any


class MCPClient:
    """Model Context Protocol client."""

    def __init__(self, server_command: list[str]) -> None:
        """
        Initialize MCP client with a server command.
        Example: ['node', './mcp-server/index.js']
        """
        self.process = subprocess.Popen(
            server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call a tool on the MCP server."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }
        self._send(request)
        response = self._receive()
        return response

    def list_tools(self) -> list[dict[str, Any]]:
        """List available tools from the MCP server."""
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
        }
        self._send(request)
        response = self._receive()
        return response.get("result", {}).get("tools", [])

    def _send(self, message: dict[str, Any]) -> None:
        """Send a JSON-RPC message to the server."""
        if self.process.stdin:
            self.process.stdin.write(json.dumps(message) + "\n")
            self.process.stdin.flush()

    def _receive(self) -> dict[str, Any]:
        """Receive a JSON-RPC message from the server."""
        if self.process.stdout:
            line = self.process.stdout.readline()
            return json.loads(line)
        return {}

    def close(self) -> None:
        """Close the MCP server process."""
        if self.process:
            self.process.terminate()
            self.process.wait()
