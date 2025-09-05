#!/usr/bin/env python3
"""Test script for specwrite-mcp server"""

import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_server():
    """Test the MCP server functionality."""
    
    # Create server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "main.py"],
    )
    
    try:
        # Connect to the server
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize
                await session.initialize()
                
                # List available tools
                tools = await session.list_tools()
                print("Available tools:")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test role switching
                print("\nTesting role switching...")
                result = await session.call_tool("switch_role", {"role": "developer"})
                print(f"Switch to developer: {result.content[0].text}")
                
                # Test project status
                print("\nTesting project status...")
                result = await session.call_tool("get_project_status", {})
                print(f"Project status: {result.content[0].text}")
                
                # Test Gherkin parsing
                print("\nTesting Gherkin parsing...")
                gherkin_content = """
Feature: User Login
  As a user
  I want to login to the system
  So that I can access my account

  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should be logged in
    And I should see my dashboard
"""
                result = await session.call_tool("parse_gherkin", {"feature_content": gherkin_content})
                print(f"Parsed Gherkin: {result.content[0].text}")
                
                # Test creating a specification (should fail as developer)
                print("\nTesting role-based access...")
                result = await session.call_tool("create_spec", {
                    "title": "Test Spec",
                    "description": "A test specification",
                    "content": "This should fail as developer"
                })
                print(f"Create spec result: {result.content[0].text}")
                
                # Switch to product manager and try again
                result = await session.call_tool("switch_role", {"role": "product_manager"})
                print(f"Switch to product manager: {result.content[0].text}")
                
                result = await session.call_tool("create_spec", {
                    "title": "User Authentication",
                    "description": "User login and authentication system",
                    "content": "Implement secure user authentication with JWT tokens"
                })
                print(f"Create spec result: {result.content[0].text}")
                
                print("\nAll tests completed successfully!")
                
    except Exception as e:
        print(f"Error testing server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_server())
    sys.exit(0 if success else 1)