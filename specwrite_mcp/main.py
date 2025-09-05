"""Main entry point for SpecWrite-MCP server."""

import asyncio
import sys
from specwrite_mcp.core.server import main

if __name__ == "__main__":
    asyncio.run(main())