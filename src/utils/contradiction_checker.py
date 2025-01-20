# src/utils/contradiction_checker.py
from typing import Dict, List, Tuple
import re

class ContradictionChecker:
    def __init__(self):
        self.contradiction_types = {
            "temporal": self._check_temporal_contradiction,
            "spatial": self._check_spatial_contradiction,
            "logical": self._check_logical_contradiction,
            "physical": self._check_physical_contradiction
        }
    
    def check_statement(self, statement: str, established_facts: Dict) -> List[Dict]:
        """Main method to check for all types of contradictions"""
        contradictions = []
        
        for check_type, check_func in self.contradiction_types.items():
            if result := check_func(statement, established_facts):
                contradictions.append({
                    "type": check_type,
                    "details": result,
                    "statement": statement
                })
                
        return contradictions
    
    def _check_temporal_contradiction(self, statement: str, facts: Dict) -> Dict:
        """Check for time-based contradictions"""
        # Extract time information from statement
        time_pattern = r"(\d{1,2}):(\d{2})\s*(?:AM|PM|am|pm)?"
        times_in_statement = re.findall(time_pattern, statement)
        
        for time_str in times_in_statement:
            for fact in facts.get("red_truths", []):
                if times_conflict(time_str, fact):
                    return {
                        "conflicting_time": time_str,
                        "conflicting_fact": fact,
                        "reason": "Temporal impossibility detected"
                    }
        return None
    
    def _check_spatial_contradiction(self, statement: str, facts: Dict) -> Dict:
        """Check for location-based contradictions"""
        # Extract location information
        locations = self._extract_locations(statement)
        
        for location in locations:
            if conflict := self._check_location_conflict(location, facts):
                return {
                    "location": location,
                    "conflict": conflict,
                    "reason": "Character cannot be in multiple locations"
                }
        return None
    
    def _check_logical_contradiction(self, statement: str, facts: Dict) -> Dict:
        """Check for logical impossibilities"""
        # Example: If A implies B, and B implies C, then A must imply C
        for fact in facts.get("red_truths", []):
            if logical_conflict := self._find_logical_conflict(statement, fact):
                return {
                    "statement": statement,
                    "conflicting_fact": fact,
                    "reason": logical_conflict
                }
        return None
    
    def _check_physical_contradiction(self, statement: str, facts: Dict) -> Dict:
        """Check for violations of physical possibility"""
        physical_rules = {
            "locked_room": self._check_locked_room_rules,
            "weapon_usage": self._check_weapon_possibility,
            "movement_speed": self._check_movement_timing
        }
        
        for rule_name, check_func in physical_rules.items():
            if violation := check_func(statement, facts):
                return {
                    "rule": rule_name,
                    "violation": violation
                }
        return None
    
    def _extract_locations(self, text: str) -> List[str]:
        """Helper to extract location mentions from text"""
        # Simple location extraction (can be enhanced)
        common_locations = ["study", "library", "bedroom", "kitchen", "garden"]
        found_locations = []
        
        for location in common_locations:
            if location.lower() in text.lower():
                found_locations.append(location)
                
        return found_locations
    
    def _check_location_conflict(self, location: str, facts: Dict) -> str:
        """Check if location creates impossible situation"""
        for fact in facts.get("red_truths", []):
            if location in fact and self._is_conflicting_location(location, fact):
                return f"Conflicts with established fact: {fact}"
        return None
    
    def _find_logical_conflict(self, statement: str, fact: str) -> str:
        """Find logical conflicts between statement and fact"""
        # Implement logical contradiction detection
        # This is a placeholder for more sophisticated logic
        return None
    
    def _check_locked_room_rules(self, statement: str, facts: Dict) -> str:
        """Check if locked room mechanics are violated"""
        if "locked room" in statement.lower():
            # Implement locked room puzzle rules
            pass
        return None
    
    def _check_weapon_possibility(self, statement: str, facts: Dict) -> str:
        """Check if weapon usage is physically possible"""
        # Implement weapon usage validation
        return None
    
    def _check_movement_timing(self, statement: str, facts: Dict) -> str:
        """Check if movement between locations is physically possible"""
        # Implement movement timing validation
        return None

def times_conflict(time_str: Tuple[str, str], fact: str) -> bool:
    """Helper function to check if times conflict"""
    # Implementation of time conflict checking
    return False