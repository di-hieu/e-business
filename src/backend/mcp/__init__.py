"""
SC Chatbot MCP Server

Model Context Protocol server implementation.
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator
import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

@asynccontextmanager
async def mcp_server() -> AsyncIterator[Server]:
    server = Server("sc-chatbot")
    async with server.connect(
        stdio_server(),
        server_name="SC Chatbot MCP Server",
        server_version="1.0.0",
    ) as (read, write):
        async def handle_read():
            while True:
                message = await read()
                await write(message)
        asyncio.create_task(handle_read())
        yield server