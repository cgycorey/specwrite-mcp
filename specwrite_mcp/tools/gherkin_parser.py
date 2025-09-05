"""Gherkin feature file parsing functionality."""

import json
from typing import Dict, List, Any
from gherkin import Parser


class GherkinParser:
    """Parses Gherkin feature files."""
    
    def __init__(self):
        self.parser = Parser()
    
    def parse_feature(self, feature_content: str) -> Dict[str, Any]:
        """Parse Gherkin feature content and return structured data."""
        try:
            parsed = self.parser.parse(feature_content)
            
            # Extract feature information
            feature_info = {
                "name": parsed.get("feature", {}).get("name", "Unknown"),
                "description": parsed.get("feature", {}).get("description", ""),
                "language": parsed.get("feature", {}).get("language", "en"),
                "scenarios": []
            }
            
            # Extract scenarios
            feature = parsed.get("feature", {})
            if "children" in feature:
                for child in feature["children"]:
                    if "scenario" in child:
                        scenario_data = child["scenario"]
                        scenario = {
                            "name": scenario_data.get("name", ""),
                            "description": scenario_data.get("description", ""),
                            "steps": []
                        }
                        
                        if "steps" in scenario_data:
                            for step in scenario_data["steps"]:
                                scenario["steps"].append({
                                    "keyword": step.get("keyword", ""),
                                    "keyword_type": step.get("keywordType", ""),
                                    "text": step.get("text", "")
                                })
                        
                        feature_info["scenarios"].append(scenario)
            
            return feature_info
            
        except Exception as e:
            raise ValueError(f"Error parsing Gherkin: {str(e)}")
    
    def validate_feature(self, feature_content: str) -> List[str]:
        """Validate Gherkin feature content and return list of errors."""
        errors = []
        
        try:
            parsed = self.parser.parse(feature_content)
            
            # Check if feature has a name
            if not parsed.get("feature", {}).get("name"):
                errors.append("Feature must have a name")
            
            # Check if feature has at least one scenario
            scenarios = parsed.get("feature", {}).get("children", [])
            scenario_count = sum(1 for child in scenarios if "scenario" in child)
            
            if scenario_count == 0:
                errors.append("Feature must have at least one scenario")
            
            # Check if scenarios have steps
            for child in scenarios:
                if "scenario" in child:
                    scenario_data = child["scenario"]
                    steps = scenario_data.get("steps", [])
                    
                    if len(steps) == 0:
                        errors.append(f"Scenario '{scenario_data.get('name', 'Unknown')}' must have at least one step")
                    
                    # Check if scenario has Given-When-Then structure
                    step_keywords = [step.get("keywordType", "") for step in steps]
                    has_context = "Context" in step_keywords  # Given
                    has_action = "Action" in step_keywords    # When
                    has_outcome = "Outcome" in step_keywords  # Then
                    
                    if not (has_context and has_action and has_outcome):
                        errors.append(f"Scenario '{scenario_data.get('name', 'Unknown')}' should follow Given-When-Then structure")
            
        except Exception as e:
            errors.append(f"Invalid Gherkin syntax: {str(e)}")
        
        return errors