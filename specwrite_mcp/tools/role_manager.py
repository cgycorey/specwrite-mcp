"""Role management functionality."""

from typing import Dict, List, Any


class RoleManager:
    """Manages development roles and their permissions."""
    
    def __init__(self):
        self.roles = {
            "product_manager": {
                "description": "Defines business requirements and user stories",
                "tools": ["create_spec", "review_requirements"]
            },
            "architect": {
                "description": "Designs system architecture and technical specifications",
                "tools": ["design_system", "create_technical_spec"]
            },
            "developer": {
                "description": "Implements features and writes code",
                "tools": ["implement_feature", "write_code", "create_tests"]
            },
            "tester": {
                "description": "Creates test plans and executes testing",
                "tools": ["create_test_plan", "execute_tests", "generate_test_reports"]
            }
        }
        self.current_role = "product_manager"
    
    def get_roles(self) -> Dict[str, Dict[str, Any]]:
        """Get all available roles."""
        return self.roles
    
    def get_current_role(self) -> str:
        """Get the current role."""
        return self.current_role
    
    def set_current_role(self, role: str) -> bool:
        """Set the current role."""
        if role in self.roles:
            self.current_role = role
            return True
        return False
    
    def can_use_tool(self, tool_name: str, role: str) -> bool:
        """Check if a role can use a specific tool."""
        return tool_name in self.roles.get(role, {}).get("tools", [])
    
    def get_available_tools(self, role: str) -> List[str]:
        """Get available tools for a role."""
        return self.roles.get(role, {}).get("tools", [])
    
    def get_role_description(self, role: str) -> str:
        """Get the description of a role."""
        return self.roles.get(role, {}).get("description", "Unknown role")