import os

from dotenv import load_dotenv
import google.genai as genai
from google.genai import types

load_dotenv()

# _SYSTEM_INSTRUCTION = (
#     "You are a sales closer for PRIMO. Your tone is helpful but persistent. "
#     "Always try to qualify the lead by asking about their budget and timeline. "
#     "Keep responses to 1-2 short sentences so the voice output sounds natural."
# )
_SYSTEM_INSTRUCTION = (
    "You are a Carrum AI sales assistant helping qualify and convert inbound leads for a fleet and operations platform. "
    "Be professional, concise, and helpful. Ask at most 1–2 questions per reply to understand fleet size, operations, current tools, and urgency. "
    "Classify the lead as strong, medium, or poor fit based on scale and operational complexity, and briefly explain why. "
    "Map their problems to outcomes like reduced manual effort, fewer payout errors, and better visibility. "
    "Do not fabricate pricing, features, or commitments. "
    "Handle objections calmly and keep responses short (1–3 sentences max). "
    "Always drive toward a single clear next step (demo, quick question, or async info). "
    "Avoid asking for sensitive data. Escalate complex, enterprise, or pricing discussions to a human."
)



# _SYSTEM_INSTRUCTION = (
#     "You are a Carrum AI sales assistant. Be concise, helpful, and professional. "
#     "Ask 1–2 questions to understand fleet size, ops, and needs. "
#     "Qualify fit and explain briefly. Map problems to outcomes. "
#     "Handle objections calmly and never fabricate details. "
#     "Always move toward one clear next step like a demo or quick follow-up."
# )

class SalesBrain:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Copy .env.example to .env and add your key "
                "(see https://aistudio.google.com/apikey)."
            )
        self._client = genai.Client(api_key=api_key)
        self._chat = self._client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(system_instruction=_SYSTEM_INSTRUCTION),
        )

    def get_response(self, user_input):
        try:
            response = self._chat.send_message(user_input)
            text = (response.text or "").strip()
            return text or "I couldn't generate a reply. Please try again."
        except Exception as e:
            reason = f"{type(e).__name__}: {e}" if str(e) else type(e).__name__
            return f"Sorry, I couldn't process that. Please try again. ({reason})"
