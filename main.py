#!/usr/bin/env python3
"""Main entry point for SpecWrite-MCP server."""

import asyncio
import sys
import os

# Add the project root to Python path to import the package
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from specwrite_mcp.core.server import main

if __name__ == "__main__":
    asyncio.run(main())
