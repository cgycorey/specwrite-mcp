"""Core MCP server implementation."""

import asyncio
import logging
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server

from specwrite_mcp.tools.role_manager import RoleManager
from specwrite_mcp.state.project_state import ProjectState
from specwrite_mcp.utils.template_manager import TemplateManager
from specwrite_mcp.handlers.tool_handlers import ToolHandlers
from specwrite_mcp.validation.validation_manager import ValidationManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpecWriteServer:
    """Main MCP server for SpecWrite functionality."""
    
    def __init__(self):
        self.server = Server("specwrite-mcp")
        
        # Initialize components
        self.role_manager = RoleManager()
        self.project_state = ProjectState()
        self.template_manager = TemplateManager()
        self.validation_manager = ValidationManager()
        self.tool_handlers = ToolHandlers(
            self.role_manager,
            self.project_state,
            self.template_manager,
            self.validation_manager
        )
        
        # Register handlers
        self.server.list_tools()(self.handle_list_tools)
        self.server.call_tool()(self.handle_call_tool)
    
    async def handle_list_tools(self):
        """List available tools."""
        return self.tool_handlers.list_tools()
    
    async def handle_call_tool(self, name, arguments):
        """Handle tool calls."""
        return await self.tool_handlers.call_tool(name, arguments)


def create_server():
    """Create and return a new SpecWriteServer instance."""
    return SpecWriteServer()


async def main():
    """Main entry point for the MCP server."""
    server = SpecWriteServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(
            read_stream,
            write_stream,
            server.server.create_initialization_options()
        )