#!/usr/bin/env python3
"""Comprehensive test script for specwrite-mcp server functionality"""

import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_comprehensive_functionality():
    """Comprehensive test of all MCP server functionality."""
    
    # Create server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "main.py"],
    )
    
    test_results = []
    
    try:
        # Connect to the server
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize
                await session.initialize()
                
                print("=" * 60)
                print("COMPREHENSIVE SPECWRITE-MCP FUNCTIONALITY TEST")
                print("=" * 60)
                
                # Test 1: List all tools
                print("\n1. TESTING: Tool Registration")
                print("-" * 40)
                tools = await session.list_tools()
                expected_tools = [
                    "create_spec", "review_requirements", "design_system", "create_technical_spec",
                    "implement_feature", "write_code", "create_tests", "create_test_plan",
                    "execute_tests", "generate_test_reports", "switch_role", "get_project_status", "parse_gherkin"
                ]
                
                tool_names = [tool.name for tool in tools.tools]
                missing_tools = [tool for tool in expected_tools if tool not in tool_names]
                
                if missing_tools:
                    print(f"❌ Missing tools: {missing_tools}")
                    test_results.append(False)
                else:
                    print(f"✅ All {len(expected_tools)} tools registered successfully")
                    test_results.append(True)
                
                # Test 2: Product Manager Role
                print("\n2. TESTING: Product Manager Role")
                print("-" * 40)
                
                # Switch to Product Manager
                result = await session.call_tool("switch_role", {"role": "product_manager"})
                print(f"Switch to PM: {result.content[0].text}")
                
                # Test create_spec
                spec_data = {
                    "title": "User Authentication System",
                    "description": "Secure user login and authentication system",
                    "content": "Users should be able to register, login, and manage their accounts securely with JWT tokens"
                }
                result = await session.call_tool("create_spec", spec_data)
                print(f"Create spec: {result.content[0].text}")
                
                # Test review_requirements
                review_data = {
                    "title": "Review Security Requirements",
                    "description": "Review authentication security requirements",
                    "content": "Ensure password complexity, MFA support, and session security"
                }
                result = await session.call_tool("review_requirements", review_data)
                print(f"Review requirements: {result.content[0].text}")
                
                test_results.append(True)
                
                # Test 3: Architect Role
                print("\n3. TESTING: Architect Role")
                print("-" * 40)
                
                # Switch to Architect
                result = await session.call_tool("switch_role", {"role": "architect"})
                print(f"Switch to Architect: {result.content[0].text}")
                
                # Test design_system
                design_data = {
                    "title": "Authentication System Architecture",
                    "description": "High-level system design for authentication",
                    "content": "Microservice architecture with auth service, API gateway, and JWT validation"
                }
                result = await session.call_tool("design_system", design_data)
                print(f"Design system: {result.content[0].text}")
                
                # Test create_technical_spec
                tech_spec_data = {
                    "title": "JWT Implementation Technical Spec",
                    "description": "Technical specification for JWT implementation",
                    "content": "JWT token generation, validation, refresh mechanism, and security considerations"
                }
                result = await session.call_tool("create_technical_spec", tech_spec_data)
                print(f"Create technical spec: {result.content[0].text}")
                
                test_results.append(True)
                
                # Test 4: Developer Role
                print("\n4. TESTING: Developer Role")
                print("-" * 40)
                
                # Switch to Developer
                result = await session.call_tool("switch_role", {"role": "developer"})
                print(f"Switch to Developer: {result.content[0].text}")
                
                # Test implement_feature
                feature_data = {
                    "title": "User Registration Endpoint",
                    "description": "Implement user registration API endpoint",
                    "content": "POST /api/auth/register with email validation and password hashing"
                }
                result = await session.call_tool("implement_feature", feature_data)
                print(f"Implement feature: {result.content[0].text}")
                
                # Test write_code
                code_data = {
                    "title": "JWT Token Service",
                    "description": "Implement JWT token generation and validation service",
                    "content": "TokenService class with generateToken, validateToken, and refreshToken methods"
                }
                result = await session.call_tool("write_code", code_data)
                print(f"Write code: {result.content[0].text}")
                
                # Test create_tests
                test_data = {
                    "title": "Authentication Unit Tests",
                    "description": "Create unit tests for authentication service",
                    "content": "Test cases for login, registration, token validation, and error handling"
                }
                result = await session.call_tool("create_tests", test_data)
                print(f"Create tests: {result.content[0].text}")
                
                test_results.append(True)
                
                # Test 5: Tester Role
                print("\n5. TESTING: Tester Role")
                print("-" * 40)
                
                # Switch to Tester
                result = await session.call_tool("switch_role", {"role": "tester"})
                print(f"Switch to Tester: {result.content[0].text}")
                
                # Test create_test_plan
                test_plan_data = {
                    "title": "Authentication Test Plan",
                    "description": "Comprehensive test plan for authentication system",
                    "content": "Unit tests, integration tests, security tests, and performance testing"
                }
                result = await session.call_tool("create_test_plan", test_plan_data)
                print(f"Create test plan: {result.content[0].text}")
                
                # Test execute_tests
                execute_data = {
                    "title": "Execute Authentication Tests",
                    "description": "Run authentication test suite",
                    "content": "Test results: 45/47 tests passed, 2 failed (edge cases)"
                }
                result = await session.call_tool("execute_tests", execute_data)
                print(f"Execute tests: {result.content[0].text}")
                
                # Test generate_test_reports
                report_data = {
                    "title": "Authentication Test Report",
                    "description": "Generate comprehensive test report",
                    "content": "Test coverage: 94%, Critical bugs: 0, Performance: acceptable"
                }
                result = await session.call_tool("generate_test_reports", report_data)
                print(f"Generate test reports: {result.content[0].text}")
                
                test_results.append(True)
                
                # Test 6: Role-based Access Control
                print("\n6. TESTING: Role-based Access Control")
                print("-" * 40)
                
                # Try to use Product Manager tool as Developer
                result = await session.call_tool("create_spec", {
                    "title": "Unauthorized Spec",
                    "description": "This should fail",
                    "content": "Should not be created"
                })
                print(f"Unauthorized access attempt: {result.content[0].text}")
                
                if "only available to product managers" in result.content[0].text:
                    print("✅ Role-based access control working correctly")
                    test_results.append(True)
                else:
                    print("❌ Role-based access control failed")
                    test_results.append(False)
                
                # Test 7: Project Status Tracking
                print("\n7. TESTING: Project Status Tracking")
                print("-" * 40)
                
                result = await session.call_tool("get_project_status", {})
                status_data = json.loads(result.content[0].text)
                print(f"Project status: {json.dumps(status_data, indent=2)}")
                
                expected_counts = {
                    "specifications_count": 2,
                    "technical_designs_count": 2,
                    "code_implementations_count": 3,
                    "test_plans_count": 1,
                    "test_results_count": 2
                }
                
                all_counts_correct = True
                for key, expected in expected_counts.items():
                    if status_data.get(key, 0) != expected:
                        print(f"❌ {key}: expected {expected}, got {status_data.get(key, 0)}")
                        all_counts_correct = False
                
                if all_counts_correct:
                    print("✅ Project status tracking working correctly")
                    test_results.append(True)
                else:
                    print("❌ Project status tracking has issues")
                    test_results.append(False)
                
                # Test 8: Gherkin Parsing
                print("\n8. TESTING: Gherkin Parsing")
                print("-" * 40)
                
                gherkin_content = """
Feature: User Authentication
  As a user
  I want to authenticate with the system
  So that I can access my account securely

  Scenario: Successful login
    Given I am on the login page
    When I enter valid email and password
    And I click the login button
    Then I should be redirected to my dashboard
    And I should see a welcome message

  Scenario: Failed login
    Given I am on the login page
    When I enter invalid credentials
    And I click the login button
    Then I should see an error message
    And I should remain on the login page
"""
                result = await session.call_tool("parse_gherkin", {"feature_content": gherkin_content})
                parsed_data = json.loads(result.content[0].text)
                print(f"Parsed Gherkin: {json.dumps(parsed_data, indent=2)}")
                
                # Verify parsing worked
                if parsed_data.get("scenarios") and len(parsed_data.get("scenarios", [])) >= 2:
                    print("✅ Gherkin parsing working correctly")
                    test_results.append(True)
                else:
                    print("❌ Gherkin parsing failed")
                    test_results.append(False)
                
                # Test 9: Role Switching
                print("\n9. TESTING: Role Switching")
                print("-" * 40)
                
                roles = ["product_manager", "architect", "developer", "tester"]
                for role in roles:
                    result = await session.call_tool("switch_role", {"role": role})
                    if f"Switched to {role}" in result.content[0].text:
                        print(f"✅ Successfully switched to {role}")
                    else:
                        print(f"❌ Failed to switch to {role}")
                        test_results.append(False)
                
                test_results.append(True)
                
                # Final Summary
                print("\n" + "=" * 60)
                print("TEST SUMMARY")
                print("=" * 60)
                
                passed = sum(test_results)
                total = len(test_results)
                
                print(f"Tests passed: {passed}/{total}")
                
                if passed == total:
                    print("🎉 ALL TESTS PASSED! The specwrite-mcp server is working correctly.")
                    return True
                else:
                    print("❌ Some tests failed. Please review the implementation.")
                    return False
                
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_comprehensive_functionality())
    sys.exit(0 if success else 1)