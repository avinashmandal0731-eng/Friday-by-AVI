"""
brain.py — Friday by AVI
Added: sleep / wake intent detection
"""
from dataclasses import dataclass, field
import os
import re
from datetime import datetime

@dataclass
class BrainResponse:
    speech: str
    intent: str = ""
    slots: dict = field(default_factory=dict)


_FILLER = re.compile(
    r'\b(friday|please|a|the)\b', re.IGNORECASE
)
_QUALIFIER = re.compile(
    r'\bon (my )?(phone|pc|computer|laptop)\b', re.IGNORECASE
)

def _extract_app(text: str, command_words: list) -> str:
    clean = text.lower()
    for w in command_words:
        clean = re.sub(r'\b' + re.escape(w) + r'\b', '', clean)
    clean = _QUALIFIER.sub('', clean)
    clean = _FILLER.sub('', clean)
    return re.sub(r'\s+', ' ', clean).strip()


class Brain:
    def __init__(self, memory=None):
        self.memory = memory
        print("[Brain] Initialized — sleep/wake + regex extraction active")

    def think(self, user_text: str) -> BrainResponse:
        text     = user_text.lower().strip()
        original = user_text.strip()

        # ── SLEEP ─────────────────────────────────────────────────────────
        sleep_triggers = ["sleep", "so ja", "so jao", "chup ho", "minimize", "rest"]
        if any(w in text for w in sleep_triggers):
            return BrainResponse(
                speech="Going to sleep. Say 'Friday wake up' when you need me.",
                intent="sleep"
            )

        # ── WAKE ──────────────────────────────────────────────────────────
        wake_triggers = ["wake up", "wake", "come back", "i need you"]
        if any(w in text for w in wake_triggers):
            return BrainResponse(
                speech="I'm back, sir. What do you need?",
                intent="wake"
            )

        # ── PHONE COMMANDS ────────────────────────────────────────────────
        is_phone = bool(re.search(r'\bon (my )?phone\b', text))
        if is_phone:
            is_close = any(w in text for w in ["close", "stop", "quit", "shut"])

            phone_apps = {
                "whatsapp": "whatsapp",
                "youtube": "youtube", "yt": "youtube",
                "instagram": "instagram", "insta": "instagram",
                "gallery": "gallery", "photos": "gallery",
                "calculator": "calculator", "calc": "calculator",
                "camera": "camera",
                "settings": "settings",
                "chrome": "chrome", "browser": "chrome",
                "spotify": "spotify",
            }

            detected = None
            for keyword, canonical in phone_apps.items():
                if keyword in text:
                    detected = canonical
                    break

            if detected:
                verb   = "Closing" if is_close else "Opening"
                intent = "close_app" if is_close else "open_app"
                return BrainResponse(
                    speech=f"{verb} {detected.title()} on your phone...",
                    intent=intent,
                    slots={"app": f"{detected} on phone"}
                )

        # ── PC CLOSE ──────────────────────────────────────────────────────
        close_words = ["close", "shut", "quit", "exit", "stop"]
        if any(w in text for w in close_words):
            app = _extract_app(original, close_words)
            if app:
                return BrainResponse(
                    speech=f"Closing {app.title()}.",
                    intent="close_app",
                    slots={"app": app}
                )

        # ── PC OPEN ───────────────────────────────────────────────────────
        open_words = ["open", "launch", "start"]
        if any(w in text for w in open_words):
            app = _extract_app(original, open_words)
            if app:
                return BrainResponse(
                    speech=f"Opening {app.title()}.",
                    intent="open_app",
                    slots={"app": app}
                )

        # ── TIME ──────────────────────────────────────────────────────────
        if any(w in text for w in ["time", "clock", "what time"]):
            now = datetime.now().strftime("%I:%M %p")
            return BrainResponse(speech=f"The time is {now}, sir.")

        # ── DEFAULT: LLM ──────────────────────────────────────────────────
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL")
            )
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content":
                     "You are Friday, a sharp and professional AI assistant. "
                     "Address the user as 'sir' at all times. "
                     "Reply in 1-2 short sentences. English only. Be direct and helpful."},
                    {"role": "user", "content": original}
                ],
                max_tokens=80,
                temperature=0.3
            )
            return BrainResponse(speech=resp.choices[0].message.content.strip())
        except Exception as e:
            print(f"[Brain LLM Error] {e}")
            return BrainResponse(speech="Sorry, I didn't catch that. Please repeat.")
