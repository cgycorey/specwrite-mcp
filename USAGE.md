# SpecWrite-MCP Usage Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Basic Usage](#basic-usage)
3. [Role-Based Workflow](#role-based-workflow)
4. [Gherkin Integration](#gherkin-integration)
5. [MCP Integration](#mcp-integration)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Installation and Setup

```bash
# Clone and setup
git clone <repository-url>
cd specwrite-mcp
uv sync

# Test the installation
uv run python test_comprehensive.py
```

### 2. Running the Server

```bash
# Start the MCP server
uv run python main.py
```

The server will start and listen for MCP protocol messages.

## Basic Usage

### Starting a New Project

1. **Begin as Product Manager** (default role):
```python
# Check current role and available tools
get_project_status()
# Shows: current_role: "product_manager"
```

2. **Create Your First Specification**:
```python
create_spec(
    title="E-commerce Platform",
    description="Online shopping platform with user accounts and payment processing",
    content="Users should be able to browse products, add to cart, checkout securely"
)
```

3. **Review Requirements**:
```python
review_requirements(
    title="Security Requirements Review",
    description="Review authentication and payment security",
    content="Ensure PCI compliance, secure password storage, JWT tokens"
)
```

### Switching Roles

```python
# Switch to Architect role
switch_role(role="architect")
# Response: "Switched to architect role. Available tools: design_system, create_technical_spec"

# Switch to Developer role
switch_role(role="developer")
# Response: "Switched to developer role. Available tools: implement_feature, write_code, create_tests"

# Switch to Tester role
switch_role(role="tester")
# Response: "Switched to tester role. Available tools: create_test_plan, execute_tests, generate_test_reports"
```

## Role-Based Workflow

### Phase 1: Product Manager

```python
# Start as Product Manager
switch_role(role="product_manager")

# Create user stories
create_spec(
    title="User Authentication",
    description="User registration and login system",
    content="Users can register with email/password, login, and reset passwords"
)

create_spec(
    title="Product Catalog",
    description="Browse and search products",
    content="Users can browse categories, search products, view details"
)

# Review requirements
review_requirements(
    title="Security Audit",
    description="Security requirements review",
    content="All user data must be encrypted, passwords hashed, sessions secure"
)
```

### Phase 2: Architect

```python
# Switch to Architect
switch_role(role="architect")

# Design system architecture
design_system(
    title="System Architecture",
    description="Microservices architecture for e-commerce platform",
    content="User Service, Product Service, Order Service, Payment Service, API Gateway"
)

# Create technical specifications
create_technical_spec(
    title="Authentication Service",
    description="JWT-based authentication service",
    content="REST API with JWT tokens, password hashing with bcrypt, rate limiting"
)

create_technical_spec(
    title="Database Schema",
    description="Database design for e-commerce platform",
    content="PostgreSQL with users, products, orders, payments tables, proper indexing"
)
```

### Phase 3: Developer

```python
# Switch to Developer
switch_role(role="developer")

# Implement features
implement_feature(
    title="User Registration API",
    description="POST /api/auth/register endpoint",
    content="Validate email, hash password, create user record, return JWT token"
)

implement_feature(
    title="Product Search API",
    description="GET /api/products/search endpoint",
    content="Full-text search, pagination, filtering by category, price range"
)

# Write code
write_code(
    title="JWT Middleware",
    description="Authentication middleware for protected routes",
    content="Extract JWT token, validate signature, attach user to request"
)

write_code(
    title="Database Models",
    description="SQLAlchemy models for users and products",
    content="User, Product, Category models with relationships and constraints"
)

# Create tests
create_tests(
    title="Authentication Tests",
    description="Unit tests for registration and login",
    content="Test valid registration, duplicate email, invalid password, login success/failure"
)
```

### Phase 4: Tester

```python
# Switch to Tester
switch_role(role="tester")

# Create test plans
create_test_plan(
    title="Authentication Test Plan",
    description="Comprehensive testing of user authentication",
    content="Unit tests, integration tests, security tests, performance tests"
)

create_test_plan(
    title="API Integration Tests",
    description="End-to-end API testing",
    content="Test all endpoints, error handling, rate limiting, data validation"
)

# Execute tests
execute_tests(
    title="Run Authentication Tests",
    description="Execute authentication test suite",
    content="45/47 tests passed, 2 edge case failures identified"
)

execute_tests(
    title="Run Performance Tests",
    description="Load testing and performance analysis",
    content="1000 concurrent users, response times < 500ms, no errors"
)

# Generate reports
generate_test_reports(
    title="Test Summary Report",
    description="Comprehensive test results and metrics",
    content="Coverage: 94%, Critical bugs: 0, Performance: acceptable, Security: passed"
)
```

## Gherkin Integration

### Parsing Feature Files

```python
# Parse a Gherkin feature file
gherkin_content = """
Feature: User Authentication
  As a user
  I want to authenticate with the system
  So that I can access my account securely

  Scenario: Successful registration
    Given I am on the registration page
    When I enter valid email and password
    And I click the register button
    Then I should see a success message
    And I should be logged in automatically

  Scenario: Login with valid credentials
    Given I am a registered user
    And I am on the login page
    When I enter my email and password
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

result = parse_gherkin(feature_content=gherkin_content)
```

### Expected Output

```json
{
  "name": "User Authentication",
  "description": "  As a user\n  I want to authenticate with the system\n  So that I can access my account securely",
  "language": "en",
  "scenarios": [
    {
      "name": "Successful registration",
      "description": "",
      "steps": [
        {"keyword": "Given ", "keyword_type": "Context", "text": "I am on the registration page"},
        {"keyword": "When ", "keyword_type": "Action", "text": "I enter valid email and password"},
        {"keyword": "And ", "keyword_type": "Conjunction", "text": "I click the register button"},
        {"keyword": "Then ", "keyword_type": "Outcome", "text": "I should see a success message"},
        {"keyword": "And ", "keyword_type": "Conjunction", "text": "I should be logged in automatically"}
      ]
    },
    {
      "name": "Login with valid credentials",
      "description": "",
      "steps": [
        {"keyword": "Given ", "keyword_type": "Context", "text": "I am a registered user"},
        {"keyword": "And ", "keyword_type": "Conjunction", "text": "I am on the login page"},
        {"keyword": "When ", "keyword_type": "Action", "text": "I enter my email and password"},
        {"keyword": "And ", "keyword_type": "Conjunction", "text": "I click the login button"},
        {"keyword": "Then ", "keyword_type": "Outcome", "text": "I should be redirected to my dashboard"},
        {"keyword": "And ", "keyword_type": "Conjunction", "text": "I should see a welcome message"}
      ]
    }
  ]
}
```

## MCP Integration

### Claude Desktop Setup

1. **Locate Claude Desktop Configuration**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add SpecWrite-MCP Server**:

```json
{
  "mcpServers": {
    "specwrite": {
      "command": "uv",
      "args": ["run", "python", "/absolute/path/to/specwrite-mcp/main.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/specwrite-mcp"
      }
    }
  }
}
```

3. **Restart Claude Desktop**

### Using with Claude

Once configured, you can use SpecWrite-MCP tools directly in Claude:

```
Human: I need to create a new project for a task management application. Can you help me start by creating some specifications?

Claude: I'll help you create specifications for your task management application. Let me start by checking the current project status and then create some initial specifications.

[Uses get_project_status tool]
[Uses create_spec tool to create task management specifications]
```

### Other MCP Clients

For any MCP-compatible client, use this configuration:

```json
{
  "command": "uv",
  "args": ["run", "python", "/path/to/specwrite-mcp/main.py"],
  "cwd": "/path/to/specwrite-mcp"
}
```

## Advanced Usage

### Project State Management

```python
# Check project progress
get_project_status()
# Returns:
{
  "current_role": "product_manager",
  "specifications_count": 3,
  "technical_designs_count": 2,
  "code_implementations_count": 4,
  "test_plans_count": 2,
  "test_results_count": 1
}
```

### Custom Workflow Extensions

You can extend the system by modifying the role configuration:

```python
# In specwrite_mcp/tools/role_manager.py
ROLES = {
    "product_manager": {
        "description": "Defines business requirements and user stories",
        "tools": ["create_spec", "review_requirements", "create_user_stories"]
    },
    # Add custom roles and tools as needed
}
```

### Error Handling

The server provides clear error messages:

```python
# Try to use a tool not available for current role
create_spec()  # As developer
# Returns: "This tool is only available to product managers. Current role: developer"

# Try to switch to invalid role
switch_role(role="invalid_role")
# Returns: "Invalid role. Available roles: product_manager, architect, developer, tester"
```

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Ensure you're using uv run
   uv run python main.py
   
   # Check Python path
   export PYTHONPATH=/path/to/specwrite-mcp:$PYTHONPATH
   ```

2. **MCP Connection Issues**:
   ```bash
   # Test server directly
   uv run python test_server.py
   
   # Check if server is running
   ps aux | grep "python main.py"
   ```

3. **Role Access Issues**:
   ```bash
   # Check current role
   get_project_status()
   
   # Switch to correct role
   switch_role(role="product_manager")
   ```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tips

- Use `uv run` for consistent environment
- Keep Gherkin files reasonable in size
- Monitor project state for large projects
- Use role switching appropriately for workflow

### Getting Help

- Check the comprehensive test files for examples
- Review the test suite: `uv run python test_comprehensive.py`
- Create an issue on GitHub for bugs or feature requests