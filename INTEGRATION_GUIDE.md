# SpecWrite MCP Integration Guide

## 🎯 Integration Options

### Option 1: Claude Desktop with uvx (Recommended)

#### Step 1: Create Claude Desktop Configuration

**All Platforms (Recommended uvx approach):**
```json
{
  "mcpServers": {
    "specwrite-mcp": {
      "command": "uvx",
      "args": [
        "--project", "/path/to/specwrite-mcp",
        "python", "/path/to/specwrite-mcp/main.py"
      ]
    }
  }
}
```

**Why uvx is better:**
- ✅ No global installation required
- ✅ Automatic dependency management from `pyproject.toml`
- ✅ Isolated environments
- ✅ Works with any project path
- ✅ Always uses latest dependencies

#### Step 3: Find and Edit Claude Desktop Config

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

#### Step 2: Update Paths and Restart Claude Desktop

**Replace `/path/to/specwrite-mcp`** with your actual path:
- Windows: `"C:\\Users\\YourName\\Projects\\specwrite-mcp"`
- macOS: `"/Users/YourName/Projects/specwrite-mcp"`
- Linux: `"/home/yourname/Projects/specwrite-mcp"`

**Example for Linux:**
```json
{
  "mcpServers": {
    "specwrite-mcp": {
      "command": "uvx",
      "args": [
        "--project", "/home/kali/specwrite-mcp",
        "python", "/home/kali/specwrite-mcp/main.py"
      ]
    }
  }
}
```

#### Step 3: Restart Claude Desktop
- Close Claude Desktop completely
- Reopen Claude Desktop
- The SpecWrite MCP server will be automatically loaded!

### Option 2: Manual Setup via uvx

#### Step 1: Create a wrapper script
```bash
# Create the wrapper script
cat > specwrite-claude.py << 'EOF'
#!/usr/bin/env python3
"""Claude Desktop wrapper for SpecWrite MCP."""

import asyncio
import sys
import os
from mcp.server.stdio import stdio_server
from specwrite_mcp.core.server import SpecWriteServer

async def main():
    server = SpecWriteServer()
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(
            read_stream,
            write_stream,
            server.server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
EOF

# Make it executable
chmod +x specwrite-claude.py
```

#### Step 2: Install dependencies
```bash
uv add mcp fastapi uvicorn pydantic
```

#### Step 3: Add to Claude Desktop Config
```json
{
  "mcpServers": {
    "specwrite-mcp": {
      "command": "uv",
      "args": ["run", "python", "/home/kali/specwrite-mcp/specwrite-claude.py"]
    }
  }
}
```