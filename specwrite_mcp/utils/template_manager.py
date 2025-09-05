"""Template management for SpecWrite-MCP."""

import os
import yaml
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, Template


class TemplateManager:
    """Manages all templates and template rendering."""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.jinja_env = self._setup_jinja_environment()
        self._template_cache = {}  # Cache for rendered templates
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load templates from YAML files."""
        templates = {}
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
        
        try:
            # Load product manager templates
            with open(os.path.join(template_dir, "product_manager.yml"), 'r') as f:
                templates["product_manager"] = yaml.safe_load(f)
            
            # Load architect templates
            with open(os.path.join(template_dir, "architect.yml"), 'r') as f:
                templates["architect"] = yaml.safe_load(f)
            
            # Load developer templates
            with open(os.path.join(template_dir, "developer.yml"), 'r') as f:
                templates["developer"] = yaml.safe_load(f)
            
            # Load tester templates
            with open(os.path.join(template_dir, "tester.yml"), 'r') as f:
                templates["tester"] = yaml.safe_load(f)
            
            # Load general templates
            with open(os.path.join(template_dir, "general.yml"), 'r') as f:
                templates["general"] = yaml.safe_load(f)
                
        except Exception as e:
            # Return basic templates if loading fails
            return self._get_basic_templates()
        
        return templates
    
    def _setup_jinja_environment(self) -> Environment:
        """Setup Jinja2 environment for template rendering."""
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
        return Environment(loader=FileSystemLoader(template_dir))
    
    def _get_basic_templates(self) -> Dict[str, Any]:
        """Return basic templates as fallback."""
        return {
            "product_manager": {
                "spec_template": "# Product Specification: {{ title }}\n\n## Business Value\n{{ business_value }}",
                "spec_guidance": "Create a comprehensive product specification...",
            },
            "architect": {
                "system_design_template": "# Technical Design: {{ title }}\n\n## Architecture Overview\n{{ architecture_overview }}",
                "architecture_guidance": "Design a robust system architecture...",
            },
            "developer": {
                "feature_template": "# Feature Implementation: {{ title }}\n\n## Overview\n{{ overview }}",
                "development_guidance": "Implement the feature following best practices...",
            },
            "tester": {
                "test_plan_template": "# Test Plan: {{ title }}\n\n## Overview\n{{ overview }}",
                "testing_guidance": "Create comprehensive test plans...",
            },
            "general": {
                "project_status_template": "# Project Status\n\n## Overview\n{{ overview }}",
                "role_switching_template": "# Role Switch: {{ new_role }}\n\n## Role Information\n- **Role**: {{ new_role }}\n- **Description**: {{ role_description }}\n- **Available Tools**: {{ available_tools | join(', ') }}",
            }
        }
    
    # Product Manager Templates
    def get_spec_creation_guidance(self, title: str, description: str) -> str:
        """Provide guidance for creating specifications."""
        template = Template(self.templates["product_manager"]["spec_guidance"])
        context = {
            "title": title,
            "description": description,
            "business_value": "Describe the business value and problem being solved"
        }
        
        return f"""📋 Specification Creation Guide

🎯 Creating: {title}

📝 Description: {description}

{template.render(**context)}

💡 Ready to create your specification?
1. Use the template above as a starting point
2. Call create_spec() with your complete content
3. I'll validate it and provide quality feedback

📄 Template Preview:
{self.get_spec_template()}"""
    
    def get_spec_template(self) -> str:
        """Return the product specification template."""
        cache_key = "spec_template_default"
        if cache_key in self._template_cache:
            return self._template_cache[cache_key]
            
        template = Template(self.templates["product_manager"]["spec_template"])
        context = {
            "title": "[Feature Name]",
            "business_value": "[Describe the business value and problem being solved]",
            "user_stories": [
                {"user_type": "[user type]", "feature": "[feature]", "benefit": "[benefit]"},
                {"user_type": "[user type]", "feature": "[feature]", "benefit": "[benefit]"}
            ],
            "acceptance_criteria": [
                {"context": "[context]", "action": "[action]", "outcome": "[outcome]"},
                {"context": "[context]", "action": "[action]", "outcome": "[outcome]"}
            ],
            "success_metrics": ["[Define measurable success criteria]"],
            "dependencies": ["[List any dependencies or constraints]"],
            "priority": "Medium",
            "estimated_effort": "TBD"
        }
        result = template.render(**context)
        self._template_cache[cache_key] = result
        return result
    
    def get_review_requirements_guidance(self, title: str, content: str) -> str:
        """Provide guidance for reviewing requirements."""
        template = Template(self.templates["product_manager"]["review_guidance"])
        context = {
            "title": title,
            "content": content
        }
        
        return f"""🔍 Requirements Review Guide

🎯 Reviewing: {title}

{template.render(**context)}

💡 Review Tips:
• Check for clarity and completeness
• Ensure acceptance criteria are testable
• Verify business value is clearly articulated
• Identify any missing requirements or edge cases

📊 Next Steps:
1. Use the checklist above to review the requirements
2. Call review_requirements() with your feedback
3. I'll help track the review process"""
    
    # Architect Templates
    def get_architecture_guidance(self, title: str, description: str) -> str:
        """Provide guidance for system architecture design."""
        template = Template(self.templates["architect"]["architecture_guidance"])
        context = {
            "title": title,
            "description": description
        }
        
        return f"""🏗️ Architecture Design Guide

🎯 Designing: {title}

📝 Description: {description}

{template.render(**context)}

💡 Ready to design your architecture?
1. Use the guidance above to plan your design
2. Call design_system() with your complete architecture
3. I'll validate it and provide quality feedback

📄 System Design Template:
{self.get_system_design_template()}"""
    
    def get_architecture_template(self) -> str:
        """Return the architecture design template."""
        template = Template(self.templates["architect"]["technical_spec_template"])
        context = {
            "title": "[System/Component Name]",
            "overview": "[Brief overview of the technical specification]",
            "functional_requirements": ["[Functional requirement 1]", "[Functional requirement 2]"],
            "non_functional_requirements": ["[Non-functional requirement 1]", "[Non-functional requirement 2]"],
            "implementation_approach": "[Detailed implementation strategy]",
            "unit_test_coverage": "80%",
            "integration_test_coverage": "70%",
            "performance_requirements": "< 2s for 95% of requests",
            "load_testing_strategy": "Simulate 1000 concurrent users",
            "success_criteria": ["[Success criterion 1]", "[Success criterion 2]"]
        }
        return template.render(**context)
    
    def get_system_design_template(self) -> str:
        """Return the system design template."""
        template = Template(self.templates["architect"]["system_design_template"])
        context = {
            "title": "[System/Component Name]",
            "architecture_overview": "[High-level system architecture diagram and description]",
            "system_components": [
                {
                    "name": "[Component Name]",
                    "purpose": "[Component purpose]",
                    "technology": "[Technology used]",
                    "responsibilities": "[Component responsibilities]"
                }
            ],
            "apis": [
                {
                    "name": "[Endpoint Name]",
                    "method": "GET/POST/PUT/DELETE",
                    "path": "/api/resource",
                    "description": "[Endpoint purpose]",
                    "request_schema": "[Request schema]",
                    "response_schema": "[Response schema]",
                    "authentication": "[Auth requirements]"
                }
            ],
            "database_tables": [
                {
                    "name": "[Table Name]",
                    "columns": "[List columns with types]",
                    "indexes": "[Define indexes]",
                    "relationships": "[Foreign key relationships]"
                }
            ],
            "technology_stack": [
                {"category": "Backend", "technology": "[Technology]"},
                {"category": "Database", "technology": "[Technology]"},
                {"category": "Frontend", "technology": "[Technology]"}
            ],
            "performance_requirements": ["[Performance requirement 1]", "[Performance requirement 2]"],
            "security_requirements": ["[Security requirement 1]", "[Security requirement 2]"],
            "scalability_requirements": ["[Scalability requirement 1]", "[Scalability requirement 2]"],
            "integrations": [
                {
                    "name": "[Integration Name]",
                    "description": "[Integration description]"
                }
            ],
            "deployment_architecture": "[Deployment and infrastructure architecture description]"
        }
        return template.render(**context)
    
    # Developer Templates
    def get_implementation_guidance(self, title: str, description: str) -> str:
        """Provide guidance for feature implementation."""
        template = Template(self.templates["developer"]["development_guidance"])
        context = {
            "title": title,
            "description": description
        }
        
        return f"""💻 Implementation Guide

🎯 Implementing: {title}

📝 Description: {description}

{template.render(**context)}

💡 Ready to implement your feature?
1. Use the guidance above to plan your implementation
2. Call implement_feature() with your complete implementation
3. I'll validate it and provide quality feedback

📄 Feature Implementation Template:
{self.get_feature_template()}"""
    
    def get_feature_template(self) -> str:
        """Return the feature implementation template."""
        template = Template(self.templates["developer"]["feature_template"])
        context = {
            "title": "[Feature Name]",
            "overview": "[Brief overview of the feature to be implemented]",
            "requirements": ["[Requirement 1]", "[Requirement 2]"],
            "files": [
                {
                    "path": "[file_path.py]",
                    "language": "python",
                    "content": "[Code implementation with comments]"
                }
            ],
            "implementation_details": "[Detailed implementation approach]",
            "error_handling": [
                {
                    "scenario": "[Error scenario]",
                    "exception": "[Exception type]",
                    "handling": "[How to handle the exception]",
                    "recovery": "[How to recover from the error]"
                }
            ],
            "performance_considerations": ["[Performance consideration 1]", "[Performance consideration 2]"],
            "unit_tests": [
                {
                    "name": "test_[feature_name]",
                    "description": "[Test description]",
                    "code": "[Test code with assertions]"
                }
            ],
            "integration_tests": [
                {
                    "name": "test_[feature_name]_integration",
                    "description": "[Integration test description]",
                    "code": "[Integration test code]"
                }
            ],
            "dependencies": [
                {
                    "name": "[dependency_name]",
                    "version": "[version]",
                    "purpose": "[purpose]"
                }
            ],
            "deployment_notes": "[Deployment instructions and considerations]"
        }
        return template.render(**context)
    
    def get_code_writing_guidance(self, title: str, description: str) -> str:
        """Provide guidance for code writing."""
        return f"""💻 Code Writing Guide

🎯 Writing Code: {title}

📝 Description: {description}

## Code Structure Guidelines
• Follow your project's coding standards
• Use meaningful variable and function names
• Include proper documentation and comments
• Handle errors gracefully
• Consider performance implications
• Write testable code

## Best Practices
• Keep functions small and focused
• Use appropriate design patterns
• Follow DRY (Don't Repeat Yourself) principle
• Write defensive code
• Consider edge cases
• Include proper logging

📄 Code Template:
{self.get_code_template()}"""
    
    def get_code_template(self) -> str:
        """Return the code writing template."""
        template = Template(self.templates["developer"]["code_template"])
        context = {
            "title": "[Code Title]",
            "purpose": "[Purpose of this code implementation]",
            "files": [
                {
                    "path": "[file_path.py]",
                    "language": "python",
                    "content": "[Code implementation]"
                }
            ],
            "functions": [
                {
                    "name": "[function_name]",
                    "language": "python",
                    "signature": "def function_name(param1, param2):",
                    "purpose": "[Function purpose]",
                    "parameters": "[Parameter descriptions]",
                    "returns": "[Return value description]",
                    "raises": "[Exceptions that may be raised]"
                }
            ],
            "configuration": [
                {
                    "name": "[config_name]",
                    "type": "[config_type]",
                    "default": "[default_value]",
                    "description": "[Configuration description]"
                }
            ],
            "usage_examples": [
                {
                    "title": "[Example Title]",
                    "language": "python",
                    "code": "[Example code]",
                    "output": "[Expected output]"
                }
            ],
            "dependencies": [
                {
                    "name": "[dependency_name]",
                    "purpose": "[Purpose of dependency]"
                }
            ]
        }
        return template.render(**context)
    
    def get_test_creation_guidance(self, title: str, description: str) -> str:
        """Provide guidance for test creation."""
        template = Template(self.templates["developer"]["test_template"])
        context = {
            "title": title,
            "description": description,
            "test_framework": "pytest",
            "coverage_target": "80%",
            "test_data": "Mock data setup"
        }
        
        return f"""🧪 Test Creation Guide

🎯 Creating Tests: {title}

📝 Description: {description}

{template.render(**context)}

💡 Testing Best Practices:
• Write clear, descriptive test names
• Follow Arrange-Act-Assert pattern
• Test both positive and negative scenarios
• Mock external dependencies
• Maintain good test coverage
• Use assertions effectively

📊 Test Types to Include:
• Unit tests for individual components
• Integration tests for component interactions
• Edge case testing for error conditions
• Performance tests for critical paths"""
    
    # Tester Templates
    def get_test_plan_guidance(self, title: str, description: str) -> str:
        """Provide guidance for test plan creation."""
        template = Template(self.templates["tester"]["testing_guidance"])
        context = {
            "title": title,
            "description": description
        }
        
        return f"""🧪 Test Plan Guide

🎯 Creating Test Plan: {title}

📝 Description: {description}

{template.render(**context)}

💡 Ready to create your test plan?
1. Use the guidance above to plan your testing strategy
2. Call create_test_plan() with your complete test plan
3. I'll validate it and provide quality feedback

📄 Test Plan Template:
{self.get_test_plan_template()}"""
    
    def get_test_plan_template(self) -> str:
        """Return the test plan template."""
        template = Template(self.templates["tester"]["test_plan_template"])
        context = {
            "title": "[Feature/System Name]",
            "overview": "[Overview of the testing strategy]",
            "in_scope": ["[Feature 1]", "[Feature 2]"],
            "out_of_scope": ["[Feature 3]", "[Feature 4]"],
            "unit_test_coverage": "80%",
            "unit_test_framework": "pytest",
            "unit_test_components": ["[Component 1]", "[Component 2]"],
            "integration_test_coverage": "70%",
            "integration_test_framework": "pytest",
            "integration_test_areas": ["[API endpoints]", "[Data flow]"],
            "system_test_coverage": "60%",
            "system_test_type": "End-to-end testing",
            "system_test_scenarios": ["[Scenario 1]", "[Scenario 2]"],
            "performance_requirements": "< 2s for 95% of requests",
            "load_testing": "1000 concurrent users",
            "stress_testing": "2000 concurrent users",
            "security_tests": [
                "Authentication and authorization testing",
                "Input validation testing",
                "SQL injection testing",
                "XSS testing"
            ],
            "test_cases": [
                {
                    "name": "[Test Case Name]",
                    "priority": "High/Medium/Low",
                    "type": "Functional/Non-functional",
                    "preconditions": "[Setup requirements]",
                    "test_data": "[Test data needed]",
                    "steps": ["[Step 1]", "[Step 2]"],
                    "expected_results": "[Expected outcomes]",
                    "acceptance_criteria": "[Pass/fail conditions]"
                }
            ],
            "hardware_requirements": ["[Hardware requirement 1]", "[Hardware requirement 2]"],
            "software_requirements": ["[Software requirement 1]", "[Software requirement 2]"],
            "test_data_setup": "[Test data preparation instructions]",
            "entry_criteria": ["[Entry criterion 1]", "[Entry criterion 2]"],
            "exit_criteria": ["[Exit criterion 1]", "[Exit criterion 2]"],
            "deliverables": ["[Deliverable 1]", "[Deliverable 2]"]
        }
        return template.render(**context)
    
    def get_test_execution_guidance(self, title: str, test_plan: str) -> str:
        """Provide guidance for test execution."""
        return f"""🧪 Test Execution Guide

🎯 Executing Tests: {title}

📋 Test Plan: {test_plan}

## Test Execution Process
1. **Prepare Test Environment**
   - Setup test data and configurations
   - Ensure all dependencies are available
   - Verify environment matches requirements

2. **Execute Test Cases**
   - Follow test procedures step by step
   - Document actual results
   - Capture screenshots for GUI tests
   - Log any issues or deviations

3. **Record Results**
   - Document pass/fail status
   - Capture performance metrics
   - Log defects with reproduction steps
   - Track test coverage

4. **Generate Reports**
   - Create test execution reports
   - Analyze test results
   - Identify trends and patterns
   - Provide recommendations

💡 Execution Tips:
• Execute tests in the specified order
• Document any deviations from the test plan
• Capture sufficient evidence for results
• Communicate issues promptly
• Maintain detailed execution logs"""
    
    def get_test_report_guidance(self, title: str, execution_results: str) -> str:
        """Provide guidance for test reporting."""
        return f"""📊 Test Report Guide

🎯 Creating Report: {title}

📋 Execution Results: {execution_results}

## Report Structure
1. **Executive Summary**
   - High-level overview of test results
   - Key findings and recommendations
   - Quality assessment

2. **Test Coverage Analysis**
   - Requirements coverage
   - Code coverage metrics
   - Test type distribution

3. **Defect Analysis**
   - Defect distribution by severity
   - Defect trends over time
   - Root cause analysis

4. **Quality Metrics**
   - Pass/fail rates
   - Performance metrics
   - Quality KPIs

5. **Recommendations**
   - Process improvements
   - Additional testing needed
   - Quality enhancement suggestions

💡 Reporting Tips:
• Use clear, concise language
• Include visualizations where helpful
• Focus on actionable insights
• Tailor content to audience
• Provide both technical and business perspectives"""
    
    # General Templates
    def get_project_status_template(self) -> str:
        """Return the project status template."""
        template = Template(self.templates["general"]["project_status_template"])
        context = {
            "project_name": "[Project Name]",
            "current_phase": "[Current Phase]",
            "overall_progress": "[Progress]%",
            "last_updated": "[Last Updated]",
            "phases": [
                {
                    "name": "[Phase Name]",
                    "status": "[Status]",
                    "progress": "[Progress]%",
                    "key_deliverables": "[Key deliverables]",
                    "next_milestone": "[Next milestone]"
                }
            ],
            "total_specs": "[Total]",
            "completed_specs": "[Completed]",
            "total_tech_designs": "[Total]",
            "completed_tech_designs": "[Completed]",
            "total_features": "[Total]",
            "completed_features": "[Completed]",
            "total_test_plans": "[Total]",
            "completed_test_plans": "[Completed]",
            "recent_activity": [
                {
                    "timestamp": "[Timestamp]",
                    "description": "[Activity description]"
                }
            ],
            "upcoming_tasks": [
                {
                    "due_date": "[Due Date]",
                    "description": "[Task description]",
                    "assignee": "[Assignee]"
                }
            ],
            "blockers": [
                {
                    "severity": "[Severity]",
                    "description": "[Blocker description]",
                    "owner": "[Owner]"
                }
            ],
            "avg_spec_quality": "[Score]/10",
            "avg_design_quality": "[Score]/10",
            "avg_code_quality": "[Score]/10",
            "avg_test_quality": "[Score]/10",
            "test_coverage": "[Coverage]%",
            "defect_density": "[Defects]/KLOC"
        }
        return template.render(**context)
    
    def get_gherkin_feature_template(self) -> str:
        """Return the Gherkin feature template."""
        template = Template(self.templates["general"]["gherkin_feature_template"])
        context = {
            "feature_name": "[Feature Name]",
            "feature_description": "[Feature description]",
            "scenarios": [
                {
                    "name": "[Scenario Name]",
                    "steps": [
                        {
                            "keyword": "Given",
                            "text": "[Step text]"
                        }
                    ]
                }
            ],
            "backgrounds": [],
            "rules": []
        }
        return template.render(**context)
    
    def get_role_switching_template(self, new_role: str, role_description: str, available_tools: list) -> str:
        """Return the role switching template."""
        template = Template(self.templates["general"]["role_switching_template"])
        context = {
            "new_role": new_role,
            "role_description": role_description,
            "available_tools": available_tools,
            "current_phase": "[Current Phase]",
            "responsibilities": [
                "[Responsibility 1]",
                "[Responsibility 2]",
                "[Responsibility 3]"
            ],
            "tool_purpose": "[Tool purpose]",
            "tool_usage": "[How to use the tool]",
            "best_practices": [
                "[Best practice 1]",
                "[Best practice 2]",
                "[Best practice 3]"
            ],
            "completed_work": [
                {
                    "type": "[Work type]",
                    "title": "[Work title]",
                    "completion_date": "[Date]"
                }
            ],
            "work_in_progress": [
                {
                    "type": "[Work type]",
                    "title": "[Work title]",
                    "progress": "[Progress]%"
                }
            ],
            "upcoming_tasks": [
                {
                    "title": "[Task title]",
                    "due_date": "[Due date]"
                }
            ]
        }
        return template.render(**context)