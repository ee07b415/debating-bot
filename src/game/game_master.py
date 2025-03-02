# src/game/game_master.py
import asyncio
from src.models.base_model import BaseModel
from .truth_battle import TruthBattleSystem

class GameMaster:
    def __init__(self):
        self.model = BaseModel()
        self.truth_battle = TruthBattleSystem()
        self.turns_remaining = 10
        # Start audio processing task
        self.audio_task = asyncio.create_task(self.audio_manager.process_audio_queue())
        
    async def _speak_response(self, response):
        """Queue response for audio playback and return the text"""
        if response:
            await self.audio_manager.queue_audio(response)
            # Give a short time for audio to start processing
            await asyncio.sleep(0.1)
        return response
        
    async def start_game(self):
        """Start the game with an opening narrative"""
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
            self.turns_remaining -= 1
            await self._speak_response(response)
            return response
            
        elif action == "theory":
            theory = self.truth_battle.present_blue_theory(content)
            response = await self._handle_theory_challenge(theory)
            self.turns_remaining -= 1
            await self._speak_response(response)
            return response
        
        self.turns_remaining -= 1
        return self.check_game_state()
    
    # TODO: not clear what we should do with this block
    def _process_response(self, response):
        return response
    
    def _build_question_context(self, question):
        return f"""
        Based on established facts:
        
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
    
    async def end_game(self):
        """Clean up and end the game"""
        # Stop audio processing
        if hasattr(self, 'audio_manager'):
            await self.audio_manager.stop_audio()
        
        # Cancel audio task
        if hasattr(self, 'audio_task'):
            try:
                self.audio_task.cancel()
                await self.audio_task
            except asyncio.CancelledError:
                pass
        
        # Return final narrative
        return """
        The truth behind the mystery is revealed:
        [Insert your game's conclusion here]
        """

    def __del__(self):
        """Ensure cleanup on object destruction"""
        if hasattr(self, 'audio_manager'):
            asyncio.create_task(self.audio_manager.stop_audio())