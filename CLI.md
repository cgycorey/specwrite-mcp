# SpecWrite-MCP CLI Reference

## Quick Commands

### Basic Operations
```bash
# Run the MCP server
uv run python main.py

# Run comprehensive tests
uv run python tests/test_comprehensive.py

# Run basic server test
uv run python tests/test_server.py

# Install dependencies
uv sync

# Update dependencies
uv sync --upgrade
```

### Development
```bash
# Run with debug logging
uv run python -c "import logging; logging.basicConfig(level=logging.DEBUG); from main import asyncio; asyncio.run(main())"

# Test package import
uv run python -c "from specwrite_mcp.core.server import SpecWriteServer; print('Import successful')"

# Check package structure
uv run python -c "import specwrite_mcp; print(dir(specwrite_mcp))"
```

## MCP Integration Commands

### Claude Desktop Configuration
```bash
# Find Claude config location
# macOS:
echo "~/Library/Application Support/Claude/claude_desktop_config.json"

# Windows:
echo "%APPDATA%\Claude\claude_desktop_config.json"

# Edit configuration (macOS)
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Test MCP Connection
```bash
# Test server directly
uv run python test_server.py

# Run server in background for testing
uv run python main.py &
SERVER_PID=$!

# Test with comprehensive suite
uv run python test_comprehensive.py

# Stop background server
kill $SERVER_PID
```

## Role Management Commands

### Quick Role Testing
```bash
# Test role switching
uv run python -c "
import asyncio
import sys
sys.path.insert(0, '.')
from test_server import test_server
asyncio.run(test_server())
"
```

### Available Roles and Tools
| Role | Available Tools |
|------|----------------|
| `product_manager` | `create_spec`, `review_requirements` |
| `architect` | `design_system`, `create_technical_spec` |
| `developer` | `implement_feature`, `write_code`, `create_tests` |
| `tester` | `create_test_plan`, `execute_tests`, `generate_test_reports` |

## Project Management Commands

### Check Project Status
```bash
# Get current project status
uv run python -c "
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def check_status():
    params = StdioServerParameters(
        command='uv', args=['run', 'python', 'main.py']
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool('get_project_status', {})
            print(json.dumps(result.content[0].text, indent=2))

asyncio.run(check_status())
"
```

### Sample Workflow Commands
```bash
# Complete development workflow example
uv run python -c "
import asyncio
from test_comprehensive import test_comprehensive_functionality
asyncio.run(test_comprehensive_functionality())
"
```

## Gherkin Testing Commands

### Test Gherkin Parsing
```bash
# Test Gherkin feature parsing
uv run python -c "
from specwrite_mcp.tools.gherkin_parser import GherkinParser

parser = GherkinParser()
feature = '''
Feature: Test Feature
  Scenario: Test Scenario
    Given I have a test
    When I run the test
    Then it should pass
'''

result = parser.parse_feature(feature)
print('Parsed Gherkin:', json.dumps(result, indent=2))
"
```

### Validate Gherkin Syntax
```bash
# Test Gherkin validation
uv run python -c "
from specwrite_mcp.tools.gherkin_parser import GherkinParser

parser = GherkinParser()
feature = '''
Feature: Invalid Feature
# Missing scenarios
'''

errors = parser.validate_feature(feature)
print('Validation errors:', errors)
"
```

## Testing Commands

### Run Specific Tests
```bash
# Test only role-based access control
uv run python -c "
import asyncio
from test_comprehensive import test_comprehensive_functionality
# Run specific test scenarios
asyncio.run(test_comprehensive_functionality())
" | grep -A 5 -B 5 "Role-based access control"

# Test Gherkin parsing only
uv run python -c "
import asyncio
from test_comprehensive import test_comprehensive_functionality
asyncio.run(test_comprehensive_functionality())
" | grep -A 10 -B 2 "Gherkin parsing"
```

### Performance Testing
```bash
# Test server performance
uv run python -c "
import time
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def performance_test():
    params = StdioServerParameters(command='uv', args=['run', 'python', 'main.py'])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test multiple tool calls
            start = time.time()
            for i in range(10):
                await session.call_tool('get_project_status', {})
            end = time.time()
            
            print(f'10 tool calls in {end - start:.2f} seconds')
            print(f'Average: {(end - start) / 10:.3f} seconds per call')

asyncio.run(performance_test())
"
```

## Environment Setup Commands

### Python Environment
```bash
# Check Python version
python --version
# Should be 3.12+

# Check uv installation
uv --version

# Create virtual environment (if needed)
uv venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows

# Install dependencies
uv sync

# Check installed packages
uv pip list
```

### Project Structure
```bash
# View project structure
tree -I '.venv|__pycache__|*.pyc' .

# Check Python files
find . -name "*.py" | grep -v .venv | sort

# Check test files
find . -name "*test*.py" | sort
```

## Debug Commands

### Enable Debug Logging
```bash
# Run with debug output
uv run python -c "
import logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
import asyncio
from main import main
asyncio.run(main())
"
```

### Check Import Paths
```bash
# Test all imports
uv run python -c "
import sys
print('Python path:', sys.path[:3])
print()

# Test package imports
try:
    from specwrite_mcp.core.server import SpecWriteServer
    print('✅ SpecWriteServer import successful')
except Exception as e:
    print('❌ SpecWriteServer import failed:', e)

try:
    from specwrite_mcp.tools.role_manager import RoleManager
    print('✅ RoleManager import successful')
except Exception as e:
    print('❌ RoleManager import failed:', e)

try:
    from specwrite_mcp.tools.gherkin_parser import GherkinParser
    print('✅ GherkinParser import successful')
except Exception as e:
    print('❌ GherkinParser import failed:', e)

try:
    from specwrite_mcp.state.project_state import ProjectState
    print('✅ ProjectState import successful')
except Exception as e:
    print('❌ ProjectState import failed:', e)
"
```

### Server Health Check
```bash
# Quick server health check
timeout 10s uv run python main.py &
SERVER_PID=$!
sleep 2
if ps aux | grep -q "[p]ython main.py"; then
    echo "✅ Server started successfully"
    kill $SERVER_PID 2>/dev/null
else
    echo "❌ Server failed to start"
fi
```

## Troubleshooting Commands

### Common Issues
```bash
# Check if port is available (if using HTTP server)
lsof -i :8080  # or whatever port

# Check process conflicts
ps aux | grep "python main.py"

# Clean up Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Reinstall dependencies
uv sync --reinstall

# Check file permissions
ls -la main.py
ls -la specwrite_mcp/
```

### Network Testing (for MCP clients)
```bash
# Test basic connectivity
curl -s http://localhost:8080/health  # if you have health endpoint

# Test MCP protocol (advanced)
uv run python -c "
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_connection():
    try:
        params = StdioServerParameters(command='uv', args=['run', 'python', 'main.py'])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                print(f'✅ Connected successfully, {len(tools.tools)} tools available')
                return True
    except Exception as e:
        print(f'❌ Connection failed: {e}')
        return False

result = asyncio.run(test_connection())
print('Connection test:', 'PASS' if result else 'FAIL')
"
```

## Quick Reference Card

### Essential Commands
```bash
# Start server          → uv run python main.py
# Run tests             → uv run python test_comprehensive.py
# Install deps          → uv sync
# Update deps           → uv sync --upgrade
# Check status          → See Project Management Commands above
# Test Gherkin          → See Gherkin Testing Commands above
```

### Common Workflows
```bash
# Development workflow:
1. uv sync                          # Setup
2. uv run python test_comprehensive.py  # Test
3. uv run python main.py              # Run server
4. [Configure MCP client]              # Connect
5. [Use tools via MCP client]         # Work

# Testing workflow:
1. uv run python test_server.py       # Basic test
2. uv run python test_comprehensive.py # Full test suite
3. [Make changes]                     # Develop
4. Repeat                            # Iterate
```