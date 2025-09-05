"""Main entry point for SpecWrite-MCP server."""

import asyncio
from specwrite_mcp.core.server import main as async_main

def main():
    """Synchronous wrapper for the async main function."""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()