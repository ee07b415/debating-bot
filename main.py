# src/main.py
import asyncio
import os
from  src.game.game_master import GameMaster

async def main():
    os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = r"C:\Program Files\eSpeak NG\libespeak-ng.dll"
    os.environ["PHONEMIZER_ESPEAK_PATH"] = r"C:\Program Files\eSpeak NG\espeak-ng.exe"

    game = GameMaster()
    
    # Start the game
    print("\n=== Welcome to the Detective Mystery Game ===")
    opening = await game.start_game()
    print("\nMystery Teller:", opening)
    
    # Game loop
    while game.turns_remaining > 0:
        print(f"\nTurns remaining: {game.turns_remaining}")
        print("\nActions available:")
        print("1. Ask a question (/question)")
        print("2. Present a theory (/theory)")
        print("3. Quit (/quit)")
        
        action = input("\nWhat would you like to do? ")
        
        if action.startswith("/quit"):
            break
            
        elif action.startswith("/question"):
            question = input("Enter your question: ")
            response = await game.handle_turn("question", question)
            print("\nResponse:", response)
            
        elif action.startswith("/theory"):
            theory = input("Present your theory: ")
            response = await game.handle_turn("theory", theory)
            print("\nResponse:", response)
        
        else:
            print("Invalid action. Please try again.")
    
    # End game and reveal truth
    print("\n=== Game Over ===")
    truth = game.end_game()
    print("\nThe truth behind the mystery:")
    print(truth)

if __name__ == "__main__":
    # Run the game
    asyncio.run(main())