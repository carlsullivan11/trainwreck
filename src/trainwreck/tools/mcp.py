from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


class MCPServerConnection:
    """Single MCP server connection."""

    def __init__(self, name: str, command: list[str]) -> None:
        self.name = name
        self.command = command
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.tools: list[dict[str, Any]] = []
        self._request_id = 0

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call a tool on this MCP server."""
        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
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
        """List available tools from this MCP server."""
        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": "tools/list",
        }
        self._send(request)
        response = self._receive()
        tools = response.get("result", {}).get("tools", [])
        self.tools = tools
        return tools

    def _send(self, message: dict[str, Any]) -> None:
        """Send a JSON-RPC message to the server."""
        if self.process.stdin:
            self.process.stdin.write(json.dumps(message) + "\n")
            self.process.stdin.flush()

    def _receive(self) -> dict[str, Any]:
        """Receive a JSON-RPC message from the server."""
        if self.process.stdout:
            line = self.process.stdout.readline()
            if line:
                return json.loads(line)
        return {}

    def close(self) -> None:
        """Close this MCP server process."""
        if self.process:
            self.process.terminate()
            self.process.wait()


class MCPClient:
    """Model Context Protocol client with multi-server support."""

    def __init__(self, server_command: list[str] | None = None) -> None:
        self.servers: dict[str, MCPServerConnection] = {}
        self.tool_to_server: dict[str, str] = {}

        if server_command:
            self.add_server("default", server_command)

    def add_server(self, name: str, command: list[str]) -> None:
        """Add and connect to an MCP server."""
        try:
            server = MCPServerConnection(name, command)
            tools = server.list_tools()

            for tool in tools:
                tool_name = tool.get("name", "")
                if tool_name:
                    self.tool_to_server[tool_name] = name

            self.servers[name] = server
        except Exception as e:
            print(f"Warning: Failed to connect to MCP server '{name}': {e}")

    def load_config(self, config_path: Path) -> None:
        """Load MCP servers from a configuration file."""
        if not config_path.exists():
            return

        try:
            with open(config_path) as f:
                config = json.load(f)

            servers = config.get("mcp_servers", [])
            for server_config in servers:
                name = server_config.get("name", "")
                command = server_config.get("command", [])
                enabled = server_config.get("enabled", True)

                if name and command and enabled:
                    self.add_server(name, command)
        except Exception as e:
            print(f"Warning: Failed to load MCP config from {config_path}: {e}")

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call a tool on the appropriate MCP server."""
        server_name = self.tool_to_server.get(tool_name)

        if not server_name:
            return {"error": f"Tool '{tool_name}' not found in any MCP server"}

        server = self.servers.get(server_name)
        if not server:
            return {"error": f"MCP server '{server_name}' not connected"}

        return server.call_tool(tool_name, arguments)

    def list_tools(self) -> list[dict[str, Any]]:
        """List all available tools from all connected MCP servers."""
        all_tools = []
        for server_name, server in self.servers.items():
            for tool in server.tools:
                tool_with_server = tool.copy()
                tool_with_server["mcp_server"] = server_name
                all_tools.append(tool_with_server)
        return all_tools

    def get_tools_summary(self) -> str:
        """Get a formatted summary of all available MCP tools."""
        if not self.servers:
            return "No MCP servers connected."

        summary = []
        for server_name, server in self.servers.items():
            summary.append(f"\n{server_name}: {len(server.tools)} tools")
            for tool in server.tools:
                tool_name = tool.get("name", "unknown")
                description = tool.get("description", "")
                summary.append(f"  - {tool_name}: {description}")

        return "\n".join(summary)

    def close(self) -> None:
        """Close all MCP server processes."""
        for server in self.servers.values():
            server.close()
