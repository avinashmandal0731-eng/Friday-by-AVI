import json
from pathlib import Path

class Memory:
    def __init__(self):
        self.file_path = Path(__file__).parent / "aria_memory.json"
        self.user_name: str | None = None
        self.conversation_history: list = []

    def load(self) -> bool:
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.user_name = data.get("user_name")
                    self.conversation_history = data.get("history", [])
                return True
            except:
                return False
        return False

    def save(self) -> bool:
        try:
            data = {
                "user_name": self.user_name,
                "history": self.conversation_history[-20:]
            }
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except:
            return False

    def add_turn(self, user_text: str, aria_text: str):
        self.conversation_history.append({"user": user_text, "aria": aria_text})

    def __len__(self):
        return len(self.conversation_history)