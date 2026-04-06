from src.brain import SalesBrain
from src.voice import VoiceEngine
from src.brains.ollamaBrain import OllamaBrain

# ollama list
def start_prototype():
    # Initialize our AI components
    # brain = SalesBrain()
    brain = OllamaBrain()
    voice = VoiceEngine()

    print("\n--- 🚀 PRIMO SALES AGENT STARTING ---")
    print("Agent: (Waiting for you to type a lead inquiry...)\n")
    while True:
        # 1. Capture User (Lead) Text Input
        user_text = input("Lead: ")
        
        if user_text.lower() in ['exit', 'quit', 'stop']:
            print("Shutting down agent...")
            break

        # 2. Gemini Processes Logic (The 'Brain')
        print("Agent is thinking...")
        ai_reply = brain.get_response(user_text)
        
        # 3. Output Text to Console
        print(f"Agent says: {ai_reply}")

        # 4. ElevenLabs Speaks (The 'Voice')
        try:
            voice.speak(ai_reply)
        except Exception as e:
            print(f"Voice playback failed: {e}")

if __name__ == "__main__":
    start_prototype()