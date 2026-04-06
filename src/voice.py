import os

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

load_dotenv()

class VoiceEngine:
    def __init__(self):
        api_key = os.getenv("ELEVEN_API_KEY")
        if not api_key:
            raise ValueError(
                "ELEVEN_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        self.client = ElevenLabs(api_key=api_key)
        # Choose a professional sales voice ID (e.g., 'Brian' or 'Nicole')
        # self.voice_id = "nPczCjzI2devNBz1zW7u" # Example: 'Brian'
        self.voice_id = "nPczCjzI2devNBz1zQrb"

    def speak(self, text):
        audio = self.client.text_to_speech.convert(
            voice_id=self.voice_id,
            text=text,
            model_id="eleven_turbo_v2_5",
        )
        play(audio)