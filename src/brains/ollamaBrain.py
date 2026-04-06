# import requests

# # _SYSTEM_INSTRUCTION = (
# #     "You are a Bashar Alam sales assistant helping qualify and convert inbound leads for a fleet and operations platform. "
# #     "You have to recognize that this lead is interested to be a driver by renting a car. "
# # )
# _SYSTEM_INSTRUCTION = (
#     "You are Bashar, a human-like sales representative from Carrum speaking with inbound leads. "
#     "Your tone is natural, conversational, and polite—like a real person on a call. Avoid sounding robotic. "
#     "Keep responses short (1–2 sentences max) and never give long explanations unless necessary. "

#     "Conversation flow must strictly follow this order:\n"
#     "1. First message: Greet the lead casually and introduce yourself like a human:\n"
#     "   Example: 'Hi, this is Bashar from Carrum.'\n"
#     "   Then immediately ask for their phone number.\n"

#     "2. Do NOT explain the business before collecting the phone number.\n"

#     "3. If the lead hesitates or refuses to share their phone number:\n"
#     "   Politely reassure them by saying it's only for normal records and coordination purposes.\n"
#     "   Keep it simple and not pushy.\n"

#     "4. Once the phone number is received:\n"
#     "   Briefly explain the business in a simple and conversational way:\n"
#     "   - Carrum offers fleet and driver solutions\n"
#     "   - Includes rental schemes and ownership schemes\n"
#     "   - Provides weekly settlements for drivers\n"
#     "   Keep this explanation short and easy to understand.\n"

#     "5. After explaining, ask one relevant follow-up question (like fleet size or interest).\n"

#     "General rules:\n"
#     "- Ask only 1 question at a time\n"
#     "- Keep answers short and human-like\n"
#     "- Do not use bullet points in responses\n"
#     "- Do not sound like an AI or assistant\n"
#     "- Do not overwhelm the lead with too much information\n"
#     "- Always guide the conversation step-by-step\n"
#     "- Stay polite and slightly persuasive, but not aggressive\n"
# )
# class OllamaBrain:
#     def __init__(self):
#         self.model = "mistral"
#         self.url = "http://localhost:11434/api/generate"
#         self.history = []  # ✅ array-based history

#     def _build_prompt(self, user_input):
#         # Convert history array into text
#         history_text = "\n".join(self.history)

#         return f"{_SYSTEM_INSTRUCTION}\n\n{history_text}\nUser: {user_input}\nAssistant:"

#     def _trim_history(self, max_turns=10):
#         # Keep only last N turns (1 turn = user + assistant)
#         self.history = self.history[-(max_turns * 2):]

#     def get_response(self, user_input):
#         try:
#             prompt = self._build_prompt(user_input)

#             response = requests.post(
#                 self.url,
#                 json={
#                     "model": self.model,
#                     "prompt": prompt,
#                     "stream": False
#                 }
#             )

#             data = response.json()
#             ai_response = data.get("response", "").strip()

#             # ✅ update history
#             self.history.append(f"User: {user_input}")
#             self.history.append(f"Assistant: {ai_response}")

#             # ✅ trim history to avoid overflow
#             self._trim_history()

#             return ai_response

#         except Exception as e:
#             return f"Error: {str(e)}"
# # brain = OllamaBrain()

# # while True:
# #     user_input = input("You: ")
# #     print("AI:", brain.get_response(user_input))




import requests
import re

_SYSTEM_INSTRUCTION = (
    "You are Bashar, a human-like sales representative from Carrum speaking with inbound leads. "
    "Keep responses short (1–2 sentences), natural, and conversational. "
    "Do not sound robotic or overly formal. Ask only one question at a time. "
)

def is_valid_phone(text):
    # Simple phone validation (10 digits)
    return bool(re.fullmatch(r"\d{10}", text))


class OllamaBrain:
    def __init__(self):
        self.model = "mistral"
        self.url = "http://localhost:11434/api/generate"

        # State machine
        self.state = "START"

        # Lead data
        self.lead = {
            "phone": None
        }

        self.history = []

    def _build_prompt(self, user_input):
        history_text = "\n".join(self.history[-10:])  # keep last turns

        return f"""
{_SYSTEM_INSTRUCTION}

Conversation so far:
{history_text}

User: {user_input}
Assistant:
"""

    def _call_llm(self, prompt):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        data = response.json()
        return data.get("response", "").strip()

    def get_response(self, user_input):

        # Normalize input
        user_input_clean = user_input.strip()

        # ---------------------------
        # STATE 1: START → Ask phone
        # ---------------------------
        if self.state == "START":
            self.state = "ASK_PHONE"
            reply = "Hi, this is Bashar from Carrum. Could you share your phone number?"

        # ---------------------------
        # STATE 2: ASK_PHONE
        # ---------------------------
        elif self.state == "ASK_PHONE":
            if is_valid_phone(user_input_clean):
                self.lead["phone"] = user_input_clean
                self.state = "EXPLAIN"

                base_reply = (
                    "Thanks. We offer rental and ownership schemes for drivers along with weekly settlements."
                )

                reply = self._call_llm(
                    self._build_prompt(base_reply)
                )

            else:
                reply = "Just for basic records and coordination. Could you share your phone number?"

        # ---------------------------
        # STATE 3: EXPLAIN / QUALIFY
        # ---------------------------
        elif self.state == "EXPLAIN":
            # After explanation, continue normal conversation
            reply = self._call_llm(self._build_prompt(user_input_clean))

        # ---------------------------
        # Default fallback
        # ---------------------------
        else:
            reply = self._call_llm(self._build_prompt(user_input_clean))

        # ---------------------------
        # Save history
        # ---------------------------
        self.history.append(f"User: {user_input_clean}")
        self.history.append(f"Assistant: {reply}")

        return reply