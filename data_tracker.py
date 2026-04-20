import json
from pathlib import Path
from datetime import datetime, date

class DataTracker:
    def __init__(self):
        self.file_path = Path(__file__).parent / "aria_tracker.json"
        self.data = self._load()

    def _load(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"sessions": [], "mood": {}, "tasks": []}

    def start_session(self):
        today = date.today().isoformat()
        self.data["sessions"].append({
            "date": today,
            "start_time": datetime.now().isoformat(),
            "tasks": []
        })
        self._save()

    def end_session(self) -> str:
        if self.data["sessions"]:
            session = self.data["sessions"][-1]
            session["end_time"] = datetime.now().isoformat()
            summary = f"Session ended. Tasks completed today: {len(session['tasks'])}"
            self._save()
            return summary
        return "No active session."

    def mood_asked_today(self) -> bool:
        today = date.today().isoformat()
        return today in self.data.get("mood", {})

    def set_mood(self, mood_text: str):
        today = date.today().isoformat()
        self.data.setdefault("mood", {})[today] = mood_text
        self._save()

    def log_task(self, task_desc: str):
        if self.data["sessions"]:
            today = date.today().isoformat()
            self.data["sessions"][-1]["tasks"].append(task_desc)
            self.data.setdefault("tasks", []).append({"date": today, "task": task_desc})
        self._save()

    def _save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except:
            pass