# src/models/truth_model.py
from .base_model import BaseModel

class TruthModel(BaseModel):
    def __init__(self):
        super().__init__()
        
    async def generate_with_truth_constraints(self, prompt, red_truths, required_truth_count=1):
        # Enhance prompt with truth requirements
        enhanced_prompt = f"""
        You must maintain consistency with these established facts:
        {self._format_red_truths(red_truths)}
        
        You must include at least {required_truth_count} new red truth(s) in your response.
        Use 「」 to denote red truths.
        
        {prompt}
        """
        
        response = await self.generate_response(enhanced_prompt)
        return response
    
    def _format_red_truths(self, red_truths):
        return "\n".join([f"「{truth['statement']}」" for truth in red_truths.values()])
    
    async def validate_theory(self, theory, established_facts):
        validation_prompt = f"""
        Theory to validate: {theory}
        Established facts: {established_facts}
        
        Determine if this theory:
        1. Contradicts any established facts
        2. Is logically possible
        3. Has sufficient evidence
        
        Respond with specific contradictions if found.
        """
        return await self.generate_response(validation_prompt)