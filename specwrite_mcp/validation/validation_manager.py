"""Validation manager for SpecWrite MCP server."""

from typing import Dict, List, Any


class ValidationManager:
    """Handles all validation operations for the SpecWrite server."""
    
    def validate_spec_content(self, content: str) -> Dict[str, Any]:
        """Validate specification content and return score."""
        score = 0
        issues = []
        
        # Check for required sections
        required_sections = ["Business Value", "User Stories", "Acceptance Criteria", "Success Metrics"]
        for section in required_sections:
            if section.lower() not in content.lower():
                issues.append(f"Missing required section: {section}")
            else:
                score += 2
        
        # Check for user story format
        if "as a" in content.lower() and "i want" in content.lower() and "so that" in content.lower():
            score += 1
        else:
            issues.append("User stories should follow 'As a [user], I want [feature] so that [benefit]' format")
        
        # Check for acceptance criteria format
        if "given" in content.lower() and "when" in content.lower() and "then" in content.lower():
            score += 1
        else:
            issues.append("Acceptance criteria should follow 'Given [context], when [action], then [outcome]' format")
        
        # Check content length and quality
        if len(content) < 200:
            issues.append("Specification is too brief. Add more detail to each section.")
        elif len(content) > 5000:
            issues.append("Specification is very long. Consider breaking it into smaller, focused specs.")
        else:
            score += 1
        
        # Check for measurable metrics
        if any(metric in content.lower() for metric in ["%", "time", "number", "count", "rate"]):
            score += 1
        else:
            issues.append("Success metrics should be measurable and specific")
        
        return {
            "valid": len(issues) == 0,
            "score": min(score, 10),
            "message": "\n".join(issues) if issues else "Specification meets all requirements"
        }
    
    def validate_architecture_content(self, content: str) -> Dict[str, Any]:
        """Validate architecture design content."""
        score = 0
        issues = []
        
        # Check for required sections
        required_sections = ["Architecture Overview", "API Design", "Database Schema", "Technology Stack"]
        for section in required_sections:
            if section.lower() not in content.lower():
                issues.append(f"Missing required section: {section}")
            else:
                score += 2
        
        # Check for API details
        if "post" in content.lower() or "get" in content.lower() or "put" in content.lower():
            score += 1
        else:
            issues.append("API design should include HTTP methods (GET, POST, PUT, DELETE)")
        
        # Check for database schema
        if "table" in content.lower() or "schema" in content.lower():
            score += 1
        else:
            issues.append("Database schema should include table definitions")
        
        # Check for security considerations
        if "security" in content.lower() or "auth" in content.lower():
            score += 1
        else:
            issues.append("Architecture should consider security requirements")
        
        return {
            "valid": len(issues) == 0,
            "score": min(score, 10),
            "message": "\n".join(issues) if issues else "Architecture design meets all requirements"
        }
    
    def validate_implementation_content(self, content: str, specs: list, tech_designs: list) -> Dict[str, Any]:
        """Validate implementation content."""
        score = 0
        issues = []
        
        # Check if implementation references specifications
        spec_titles = [spec["title"].lower() for spec in specs]
        content_lower = content.lower()
        
        if any(title in content_lower for title in spec_titles):
            score += 2
        else:
            issues.append("Implementation should reference the specifications it's implementing")
        
        # Check for code structure
        if "```" in content or "code" in content.lower():
            score += 2
        else:
            issues.append("Implementation should include code examples or structure")
        
        # Check for tests
        if "test" in content.lower():
            score += 2
        else:
            issues.append("Implementation should include test cases")
        
        # Check for error handling
        if "error" in content.lower() or "exception" in content.lower():
            score += 1
        else:
            issues.append("Implementation should consider error handling")
        
        # Check for integration points
        if "api" in content.lower() or "database" in content.lower():
            score += 1
        else:
            issues.append("Implementation should describe integration points")
        
        return {
            "valid": len(issues) == 0,
            "score": min(score, 10),
            "message": "\n".join(issues) if issues else "Implementation meets all requirements"
        }
    
    def validate_test_plan_content(self, content: str, implementations: list) -> Dict[str, Any]:
        """Validate test plan content."""
        score = 0
        issues = []
        
        # Check for required sections
        required_sections = ["Test Scope", "Test Strategy", "Test Cases", "Exit Criteria"]
        for section in required_sections:
            if section.lower() not in content.lower():
                issues.append(f"Missing required section: {section}")
            else:
                score += 2
        
        # Check for test types
        test_types = ["unit", "integration", "system"]
        found_types = [t for t in test_types if t in content.lower()]
        score += len(found_types)
        
        if len(found_types) < 2:
            issues.append("Test plan should include multiple test types (unit, integration, system)")
        
        # Check for test cases
        if "test case" in content.lower() or "scenario" in content.lower():
            score += 1
        else:
            issues.append("Test plan should include specific test cases or scenarios")
        
        # Check for acceptance criteria
        if "acceptance" in content.lower() or "criteria" in content.lower():
            score += 1
        else:
            issues.append("Test cases should have acceptance criteria")
        
        return {
            "valid": len(issues) == 0,
            "score": min(score, 10),
            "message": "\n".join(issues) if issues else "Test plan meets all requirements"
        }
    
    def validate_requirements_review(self, content: str, specs: list) -> Dict[str, Any]:
        """Validate requirements review content."""
        score = 0
        issues = []
        
        # Check for required sections
        required_sections = ["Review Scope", "Requirements Assessment", "Identified Issues", "Recommendations"]
        for section in required_sections:
            if section.lower() not in content.lower():
                issues.append(f"Missing required section: {section}")
            else:
                score += 2
        
        # Check if review references specifications
        spec_titles = [spec["title"].lower() for spec in specs]
        content_lower = content.lower()
        
        if any(title in content_lower for title in spec_titles):
            score += 1
        else:
            issues.append("Requirements review should reference the specifications being reviewed")
        
        # Check for prioritization
        if "priority" in content_lower or "high" in content_lower or "medium" in content_lower:
            score += 1
        else:
            issues.append("Issues should be prioritized (High, Medium, Low)")
        
        return {
            "valid": len(issues) == 0,
            "score": min(score, 10),
            "message": "\n".join(issues) if issues else "Requirements review meets all requirements"
        }
    
    def validate_technical_spec_content(self, content: str, tech_designs: list) -> Dict[str, Any]:
        """Validate technical specification content."""
        score = 0
        issues = []
        
        # Check for required sections
        required_sections = ["Implementation Details", "Interfaces", "Error Handling", "Testing Strategy"]
        for section in required_sections:
            if section.lower() not in content.lower():
                issues.append(f"Missing required section: {section}")
            else:
                score += 2
        
        # Check if references architecture designs
        design_titles = [design["title"].lower() for design in tech_designs]
        content_lower = content.lower()
        
        if any(title in content_lower for title in design_titles):
            score += 1
        else:
            issues.append("Technical specification should reference the architecture design")
        
        # Check for technical details
        if "api" in content_lower or "database" in content_lower or "interface" in content_lower:
            score += 1
        else:
            issues.append("Technical specification should include implementation details")
        
        return {
            "valid": len(issues) == 0,
            "score": min(score, 10),
            "message": "\n".join(issues) if issues else "Technical specification meets all requirements"
        }
    
    def validate_code_content(self, content: str, implementations: list) -> Dict[str, Any]:
        """Validate code content."""
        score = 0
        issues = []
        
        # Check for code structure
        if "```" in content or "class" in content.lower() or "def" in content.lower():
            score += 3
        else:
            issues.append("Code implementation should include actual code examples")
        
        # Check for error handling
        if "error" in content.lower() or "exception" in content.lower() or "try" in content.lower():
            score += 2
        else:
            issues.append("Code should include error handling")
        
        # Check for tests
        if "test" in content.lower():
            score += 2
        else:
            issues.append("Implementation should include tests")
        
        # Check if references feature implementations
        impl_titles = [impl["title"].lower() for impl in implementations]
        content_lower = content.lower()
        
        if any(title in content_lower for title in impl_titles):
            score += 2
        else:
            issues.append("Code should reference the features being implemented")
        
        return {
            "valid": len(issues) == 0,
            "score": min(score, 10),
            "message": "\n".join(issues) if issues else "Code implementation meets all requirements"
        }
    
    def validate_test_content(self, content: str, implementations: list) -> Dict[str, Any]:
        """Validate test content."""
        score = 0
        issues = []
        
        # Check for test structure
        if "test" in content.lower() and ("assert" in content.lower() or "unittest" in content.lower()):
            score += 3
        else:
            issues.append("Tests should include proper test structure and assertions")
        
        # Check for different test types
        test_types = ["unit", "integration", "mock"]
        found_types = [t for t in test_types if t in content.lower()]
        score += len(found_types)
        
        if len(found_types) < 1:
            issues.append("Tests should include unit tests and/or integration tests")
        
        # Check if references implementations
        impl_titles = [impl["title"].lower() for impl in implementations]
        content_lower = content.lower()
        
        if any(title in content_lower for title in impl_titles):
            score += 2
        else:
            issues.append("Tests should reference the implementations being tested")
        
        # Check for test data setup
        if "setup" in content.lower() or "fixture" in content.lower() or "mock" in content.lower():
            score += 2
        else:
            issues.append("Tests should include proper setup and data preparation")
        
        return {
            "valid": len(issues) == 0,
            "score": min(score, 10),
            "message": "\n".join(issues) if issues else "Test implementation meets all requirements"
        }