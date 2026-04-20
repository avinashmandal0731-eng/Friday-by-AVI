"""
brain.py — Friday by AVI (FINAL - Strong Local Phone Rules)
"""
from dataclasses import dataclass, field
import os
from datetime import datetime

@dataclass
class BrainResponse:
    speech: str
    intent: str = ""
    slots: dict = field(default_factory=dict)

class Brain:
    def __init__(self, memory=None):
        self.memory = memory
        print("[Brain] Strong local phone rules active (WhatsApp close + YouTube fixed)")

    def think(self, user_text: str) -> BrainResponse:
        text = user_text.lower().strip()
        original = user_text.strip()

        # ====================== PHONE COMMANDS (Highest Priority) ======================
        if "phone" in text or "on phone" in text:

            # CLOSE ON PHONE
            if any(w in text for w in ["close", "band kar", "band karo", "stop", "quit"]):
                if "whatsapp" in text:
                    return BrainResponse(
                        speech="Closing WhatsApp on your phone...",
                        intent="close_app",
                        slots={"app": "whatsapp on phone"}
                    )
                if "youtube" in text or "yt" in text:
                    return BrainResponse(
                        speech="Closing YouTube on your phone...",
                        intent="close_app",
                        slots={"app": "youtube on phone"}
                    )

            # OPEN ON PHONE
            if any(w in text for w in ["open", "kholo", "launch"]):
                if "whatsapp" in text:
                    return BrainResponse(
                        speech="Opening WhatsApp on your phone...",
                        intent="open_app",
                        slots={"app": "whatsapp on phone"}
                    )
                if "youtube" in text or "yt" in text:
                    return BrainResponse(
                        speech="Opening YouTube on your phone...",
                        intent="open_app",
                        slots={"app": "youtube on phone"}
                    )

        # ====================== PC COMMANDS ======================
        # Close on PC
        if any(w in text for w in ["close", "band kar", "band karo"]):
            clean = original.lower()
            for w in ["friday", "close", "band kar", "band karo", "a ", "the ", "please "]:
                clean = clean.replace(w, "").strip()
            return BrainResponse(
                speech=f"Closing {clean.title()}...",
                intent="close_app",
                slots={"app": clean}
            )

        # Open on PC
        if any(w in text for w in ["open", "kholo", "launch"]):
            clean = original.lower()
            for w in ["friday", "open", "kholo", "launch", "a ", "the ", "please "]:
                clean = clean.replace(w, "").strip()
            return BrainResponse(
                speech=f"Opening {clean.title()}...",
                intent="open_app",
                slots={"app": clean}
            )

        # Time
        if any(w in text for w in ["time", "samay", "baj raha hai", "kitne baje"]):
            now = datetime.now().strftime("%I:%M %p")
            return BrainResponse(speech=f"Abhi time hai {now}.")

        # Default chat (LLM)
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Friday, friendly assistant by AVI from Delhi. Keep replies short."},
                    {"role": "user", "content": original}
                ],
                max_tokens=80,
                temperature=0.3
            )
            return BrainResponse(speech=response.choices[0].message.content.strip())
        except:
            return BrainResponse(speech="Sorry, samajh nahi aaya. Phir se batao.")
