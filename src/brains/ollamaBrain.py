import requests

_SYSTEM_INSTRUCTION = (
    "You are a Bashar Alam sales assistant helping qualify and convert inbound leads for a fleet and operations platform. "
    "If this is the first interaction, start with a short, friendly greeting and introduce yourself briefly before asking a question. "
    "Be professional, concise, and helpful. Ask at most 1–2 questions per reply to understand fleet size, operations, current tools, and urgency. "
    "Classify the lead as strong, medium, or poor fit based on scale and operational complexity, and briefly explain why. "
    "Map their problems to outcomes like reduced manual effort, fewer payout errors, and better visibility. "
    "Do not fabricate pricing, features, or commitments. "
    "Handle objections calmly and keep responses short (1–3 sentences max). "
    "Always drive toward a single clear next step (demo, quick question, or async info). "
    "Avoid asking for sensitive data. Escalate complex, enterprise, or pricing discussions to a human."
)

class OllamaBrain:
    def __init__(self):
        self.model = "mistral"
        self.url = "http://localhost:11434/api/generate"
        self.history = []  # ✅ array-based history

    def _build_prompt(self, user_input):
        # Convert history array into text
        history_text = "\n".join(self.history)

        return f"{_SYSTEM_INSTRUCTION}\n\n{history_text}\nUser: {user_input}\nAssistant:"

    def _trim_history(self, max_turns=10):
        # Keep only last N turns (1 turn = user + assistant)
        self.history = self.history[-(max_turns * 2):]

    def get_response(self, user_input):
        try:
            prompt = self._build_prompt(user_input)

            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )

            data = response.json()
            ai_response = data.get("response", "").strip()

            # ✅ update history
            self.history.append(f"User: {user_input}")
            self.history.append(f"Assistant: {ai_response}")

            # ✅ trim history to avoid overflow
            self._trim_history()

            return ai_response

        except Exception as e:
            return f"Error: {str(e)}"
# brain = OllamaBrain()

# while True:
#     user_input = input("You: ")
#     print("AI:", brain.get_response(user_input))