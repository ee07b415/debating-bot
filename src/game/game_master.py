# src/game/game_master.py
from  src.models.base_model import BaseModel
from .truth_battle import TruthBattleSystem
from .evidence_system import EvidenceSystem

class GameMaster:
    def __init__(self):
        self.model = BaseModel()
        self.truth_battle = TruthBattleSystem()
        self.evidence_system = EvidenceSystem()
        self.turns_remaining = 10
        
    async def start_game(self):
        opening_context = """
        Present a mysterious series of murders on an isolated island.
        Include supernatural elements but leave subtle hints toward
        a logical explanation.
        """
        return await self.model.generate_response(opening_context)
        
    async def handle_turn(self, action, content):
        if action == "question":
            context = self._build_question_context(content)
            response = await self.model.generate_response(context)
            self._process_response(response)
            return response
            
        elif action == "theory":
            theory = self.truth_battle.present_blue_theory(content)
            response = await self._handle_theory_challenge(theory)
            return response
        
        self.turns_remaining -= 1
        return self.check_game_state()
    
    # TODO: not clear what we should do with this block
    def _process_response(self, response):
        return response
    
    def _build_question_context(self, question):
        return f"""
        Based on established facts:
        {self.evidence_system.established_facts}
        
        Answer the question: {question}
        
        Maintain consistency with red truths:
        {self.truth_battle.red_truths}
        """
    
    async def _handle_theory_challenge(self, theory):
        context = f"""
        Player theory: {theory}
        You must respond with at least {self.truth_battle.facts_required} red truths.
        Use 「」 for red truths.
        """
        return await self.model.generate_response(context)
    
    def check_game_state(self):
        if self.turns_remaining <= 0:
            return self.end_game()
        return None
        
    def end_game(self):
        return self.evidence_system.core_truth