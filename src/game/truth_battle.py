# src/game/truth_battle.py
import time

class TruthBattleSystem:
    def __init__(self):
        self.red_truths = {}  # Undeniable facts
        self.blue_theories = {}  # Player theories
        self.facts_required = 3
    
    def declare_red_truth(self, statement, source="npc"):
        truth_id = len(self.red_truths)
        self.red_truths[truth_id] = {
            "statement": statement,
            "timestamp": time.time(),
            "source": source
        }
        return f"「{statement}」"

    def present_blue_theory(self, theory, evidence=None):
        theory_id = len(self.blue_theories)
        self.blue_theories[theory_id] = {
            "theory": theory,
            "evidence": evidence,
            "status": "unchallenged",
            "timestamp": time.time()
        }
        return f"『{theory}』"

    def check_contradiction(self, statement, context):
        contradictions = []
        for truth_id, truth in self.red_truths.items():
            if self._check_logical_contradiction(statement, truth):
                contradictions.append({
                    "type": "red_truth_violation",
                    "truth": truth,
                    "statement": statement,
                    "reason": self._get_contradiction_reason(statement, truth)
                })
        return contradictions
    
    def _check_logical_contradiction(self, statement, truth):
        # Basic contradiction checking (can be expanded)
        return False