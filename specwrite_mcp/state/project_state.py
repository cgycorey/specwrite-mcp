"""Project state management functionality."""

from typing import Dict, List, Any


class ProjectState:
    """Manages project state and tracks progress."""
    
    def __init__(self):
        self.state = {
            "specifications": [],
            "technical_designs": [],
            "code_implementations": [],
            "test_plans": [],
            "test_results": []
        }
    
    def add_item(self, category: str, item: Dict[str, Any]) -> bool:
        """Add an item to a specific category."""
        if category in self.state:
            self.state[category].append(item)
            return True
        return False
    
    def get_items(self, category: str) -> List[Dict[str, Any]]:
        """Get all items in a specific category."""
        return self.state.get(category, [])
    
    def get_status(self) -> Dict[str, Any]:
        """Get current project status."""
        return {
            "specifications_count": len(self.state["specifications"]),
            "technical_designs_count": len(self.state["technical_designs"]),
            "code_implementations_count": len(self.state["code_implementations"]),
            "test_plans_count": len(self.state["test_plans"]),
            "test_results_count": len(self.state["test_results"])
        }
    
    def get_full_state(self) -> Dict[str, Any]:
        """Get the complete project state."""
        return self.state.copy()
    
    def clear_category(self, category: str) -> bool:
        """Clear all items in a specific category."""
        if category in self.state:
            self.state[category] = []
            return True
        return False
    
    def clear_all(self) -> None:
        """Clear all project state."""
        for category in self.state:
            self.state[category] = []
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a progress summary of the project."""
        status = self.get_status()
        total_items = sum(status.values())
        
        if total_items == 0:
            return {
                "progress_percentage": 0,
                "stage": "Not Started",
                "total_items": 0,
                "completed_items": 0
            }
        
        # Define stages based on item counts
        specs = status["specifications_count"]
        designs = status["technical_designs_count"]
        code = status["code_implementations_count"]
        tests = status["test_plans_count"]
        results = status["test_results_count"]
        
        # Determine current stage
        if specs == 0:
            stage = "Requirements"
        elif designs == 0:
            stage = "Architecture"
        elif code == 0:
            stage = "Development"
        elif tests == 0:
            stage = "Testing"
        elif results == 0:
            stage = "Execution"
        else:
            stage = "Complete"
        
        # Calculate progress (simplified)
        progress_items = min(specs, 1) + min(designs, 1) + min(code, 1) + min(tests, 1) + min(results, 1)
        progress_percentage = (progress_items / 5) * 100
        
        return {
            "progress_percentage": progress_percentage,
            "stage": stage,
            "total_items": total_items,
            "completed_items": progress_items
        }