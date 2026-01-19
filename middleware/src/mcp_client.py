import os
import asyncio
from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class McpHost:
    """
    MIAA Agnostic Interface: MCP Host.
    
    This class acts as the bridge between the Intelligence Layer (LLM) and 
    External Tools (MCP Servers). It abstracts the protocol details, exposing
    simple `list_tools` and `call_tool` methods to the middleware.
    """
    
    def __init__(self, server_command: str, server_args: List[str], env: Optional[Dict[str, str]] = None):
        self.server_params = StdioServerParameters(
            command=server_command,
            args=server_args,
            env=env
        )
        self.session: Optional[ClientSession] = None
        self._exit_stack = None

    async def connect(self):
        """Establishes the connection to the MCP Server via Stdio."""
        print(f"🔌 MCP Host: Connecting to {self.server_params.command}...")
        try:
            # Create an AsyncExitStack to manage the context managers manually
            from contextlib import AsyncExitStack
            self._exit_stack = AsyncExitStack()
            
            # Enter the stdio_client context
            read, write = await self._exit_stack.enter_async_context(stdio_client(self.server_params))
            
            # Enter the ClientSession context
            self.session = await self._exit_stack.enter_async_context(ClientSession(read, write))
            
            await self.session.initialize()
            print("✅ MCP Host: Connected and Initialized.")
            
        except Exception as e:
            print(f"❌ MCP Host Error: Failed to connect. {e}")
            if self._exit_stack:
                await self._exit_stack.aclose()
            self.session = None

    async def disconnect(self):
        """Closes the connection."""
        if self._exit_stack:
            await self._exit_stack.aclose()
            print("🔌 MCP Host: Disconnected.")

    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        Retrieves the list of available tools from the MCP Server 
        and formats them for the Unified Request Object (OpenAI-compatible).
        """
        if not self.session:
            return []

        try:
            result = await self.session.list_tools()
            tools = []
            for tool in result.tools:
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })
            return tools
        except Exception as e:
            print(f"⚠️ MCP Host: Error listing tools - {e}")
            return []

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Executes a tool on the MCP Server.
        """
        if not self.session:
            raise RuntimeError("MCP Session not active")

        try:
            result = await self.session.call_tool(name, arguments)
            # Flatten the result content
            output = ""
            for content in result.content:
                if content.type == "text":
                    output += content.text
                # Handle other content types (image, etc.) if needed
            return output
        except Exception as e:
            return f"Error executing tool {name}: {str(e)}"
