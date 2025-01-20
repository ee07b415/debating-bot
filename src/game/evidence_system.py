# src/game/evidence_system.py
class EvidenceSystem:
    def __init__(self):
        self.core_truth = {
            "actual_events": {
                "killer": "Eva",
                "motive": "inheritance dispute",
                "method": "Used master key to create locked rooms",
                "timeline": {
                    "first_murder": "9:30 PM - Study",
                    "second_murder": "10:15 PM - Guest Room",
                    "evidence_planted": "10:45 PM - Magic circles drawn"
                }
            }
        }
        
        self.established_facts = {
            "red_truths": set(),
            "physical_evidence": {},
            "witness_statements": {},
            "contradictions_found": []
        }
    
    def add_evidence(self, evidence_type, detail):
        if evidence_type == "physical":
            self.established_facts["physical_evidence"][detail["name"]] = detail
            return f"Evidence added: {detail['name']}"
            
        elif evidence_type == "statement":
            self.established_facts["witness_statements"][detail["who"]] = detail["says"]
            return f"Statement recorded from {detail['who']}"