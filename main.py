"""
main.py — Friday by AVI
Added: sleep (minimize) / wake (restore) feature
Fixed: no duplicate speech, consistent spaces
"""

from __future__ import annotations
import os
import datetime
import threading
import re
import time
import customtkinter as ctk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageSequence

from dotenv import load_dotenv
load_dotenv()

from memory import Memory
from data_tracker import DataTracker
from voice_engine import TTSEngine, STTEngine
from brain import Brain
from pc_control import dispatch as pc_dispatch

TRIGGER_PATTERNS = [r'\bfriday\b', r'\bhey friday\b', r'\bfriday suno\b', r'\bfriday batao\b']

class Friday:
    def __init__(self):
        self.memory = Memory()
        self.tracker = DataTracker()
        self.tts = TTSEngine()
        self.stt = STTEngine()
        self.brain = Brain(memory=self.memory)

        self.running = True
        self.is_sleeping = False
        self.gui = None
        self.memory.user_name = "AVI"

        if self.memory.load():
            print("[Friday] Loaded memory")

        self.tracker.start_session()

    def set_gui(self, gui):
        self.gui = gui

    def _greet(self):
        hour = datetime.datetime.now().hour
        greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
        msg = f"{greeting}, sir. Friday is online and listening. Just say 'Friday' followed by your command."
        self.tts.speak(msg)
        if self.gui:
            self.gui.add_message("Friday", msg)

    def run(self):
        self._greet()
        print("[Friday] Always-listening mode active...")

        while self.running:
            try:
                time.sleep(0.4)
                text = self.stt.listen(timeout=5, phrase_time_limit=8)
                if not text or not str(text).strip():
                    continue

                user_text = str(text).strip()
                lower_text = user_text.lower()

                if any(re.search(pattern, lower_text) for pattern in TRIGGER_PATTERNS):
                    command = user_text
                    for trigger in ["friday", "hey friday", "friday suno", "friday batao"]:
                        command = re.sub(trigger, "", command, flags=re.IGNORECASE).strip()

                    if command:
                        if self.gui:
                            self.gui.add_message("You", user_text)
                        self._process_command(command)
                    else:
                        if self.is_sleeping:
                            self._process_command("wake up")
                        else:
                            if self.gui:
                                self.gui.add_message("You", user_text)
                            self.tts.speak("Yes, sir?")
                            if self.gui:
                                self.gui.add_message("Friday", "Yes, sir?")

            except Exception as e:
                print(f"[Listen Error] {e}")
                time.sleep(0.5)

        self._shutdown()

    def _process_command(self, command: str):
        result = self.brain.think(command)

        if result and result.speech:
            self.tts.speak(result.speech)
            if self.gui:
                self.gui.add_message("Friday", result.speech)

            if result.intent == "sleep":
                self._sleep()
            elif result.intent == "wake":
                self._wake()
            elif result.intent:
                self._execute_action(result.intent, result.slots, result.speech)

    def _sleep(self):
        self.is_sleeping = True
        print("[Friday] Sleeping — window minimized")
        if self.gui:
            self.gui.minimize()

    def _wake(self):
        self.is_sleeping = False
        print("[Friday] Awake — window restored")
        if self.gui:
            self.gui.restore()

    def _execute_action(self, intent: str, slots: dict, already_said: str = ""):
        app_str = str(slots.get("app", "")).lower()
        print(f"[DEBUG] Executing → Intent: {intent} | App: {app_str}")

        if "phone" in app_str:
            print("[DEBUG] Routing to PHONE control")
            try:
                from phone_control import phone_dispatch
                ok, msg = phone_dispatch(app_str, intent=intent)
            except Exception as e:
                print(f"[Phone Import Error] {e}")
                ok, msg = False, "Phone control error occurred."
        else:
            print("[DEBUG] Routing to PC control")
            ok, msg = pc_dispatch(intent, slots)

        if msg and already_said.lower() not in msg.lower():
            self.tts.speak(msg)
            if self.gui:
                self.gui.add_message("Friday", msg)

        self.memory.save()

    def _shutdown(self):
        self.running = False
        self.tracker.end_session()
        self.tts.speak_sync("Goodbye, sir. Have a great day!")
        self.memory.save()
        print("[Friday] Shutdown complete.")


class FridayGUI:
    def __init__(self, friday):
        self.friday = friday
        friday.set_gui(self)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Friday by AVI")
        self.root.geometry("1280x760")

        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)

        left_frame = ctk.CTkFrame(self.root, fg_color="#111118")
        left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        ctk.CTkLabel(
            left_frame, text="Conversation",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 15))

        self.chat_area = scrolledtext.ScrolledText(
            left_frame, wrap="word", font=("Segoe UI", 14),
            state="disabled", bg="#1a1a24", fg="#e0e0ff", padx=20, pady=15
        )
        self.chat_area.pack(fill="both", expand=True, padx=12, pady=10)

        right_frame = ctk.CTkFrame(self.root, fg_color="#1a1a24")
        right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.orb_label = ctk.CTkLabel(right_frame, text="")
        self.orb_label.pack(pady=30)

        self.gif_path = "Orb animation WIP.gif"
        self.load_gif()

        self.status_label = ctk.CTkLabel(
            right_frame, text="Always Listening...",
            font=ctk.CTkFont(size=18), text_color="#00ff88"
        )
        self.status_label.pack(pady=5)

        self.voice_btn = ctk.CTkButton(
            right_frame, text="🎤 Voice Input", height=60,
            fg_color="#00b4ff", command=self.voice_input
        )
        self.voice_btn.pack(pady=15, padx=30, fill="x")

        self.input_entry = ctk.CTkEntry(
            right_frame, placeholder_text="Type here or say 'Friday ...'", height=50
        )
        self.input_entry.pack(pady=10, padx=30, fill="x")

        send_btn = ctk.CTkButton(
            right_frame, text="Send", height=48, command=self.send_message
        )
        send_btn.pack(pady=8, padx=30, fill="x")

        bottom_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        bottom_frame.pack(pady=20, fill="x")
        ctk.CTkButton(
            bottom_frame, text="Exit",
            fg_color="#ff3366", command=self.shutdown
        ).pack(side="left", padx=8, expand=True)

        self.input_entry.bind("<Return>", lambda e: self.send_message())
        threading.Thread(target=self.friday.run, daemon=True).start()

        self.current_frame = 0
        if hasattr(self, 'frames') and self.frames:
            self.animate_gif()

    # ── Sleep / Wake ────────────────────────────────────────────────────────

    def minimize(self):
        self.root.after(0, self._do_minimize)

    def _do_minimize(self):
        self.status_label.configure(text="Sleeping... 💤", text_color="#888888")
        self.root.iconify()

    def restore(self):
        self.root.after(0, self._do_restore)

    def _do_restore(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.status_label.configure(text="Always Listening...", text_color="#00ff88")

    # ── GIF ─────────────────────────────────────────────────────────────────

    def load_gif(self):
        try:
            full_path = os.path.join(os.getcwd(), self.gif_path)
            img = Image.open(full_path)
            self.frames = [
                ImageTk.PhotoImage(
                    frame.convert("RGBA").resize((400, 400), Image.Resampling.LANCZOS)
                )
                for frame in ImageSequence.Iterator(img)
            ]
            self.orb_label.configure(image=self.frames[0])
        except Exception as e:
            print(f"[GIF Error] {e}")
            self.fallback_label = ctk.CTkLabel(
                self.orb_label.master, text="🌟", font=ctk.CTkFont(size=160)
            )
            self.fallback_label.place(x=120, y=100)

    def animate_gif(self):
        if not hasattr(self, 'frames') or not self.frames:
            return
        self.orb_label.configure(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(65, self.animate_gif)

    # ── Chat ─────────────────────────────────────────────────────────────────

    def add_message(self, sender: str, message: str):
        self.chat_area.configure(state="normal")
        if sender == "Friday":
            self.chat_area.insert("end", "Friday: ", "friday")
            self.chat_area.insert("end", f"{message}\n\n", "response")
        else:
            self.chat_area.insert("end", "You: ", "user")
            self.chat_area.insert("end", f"{message}\n\n", "user_text")
        self.chat_area.tag_config("friday", foreground="#00ddff", font=("Segoe UI", 14, "bold"))
        self.chat_area.tag_config("user",   foreground="#00ffcc", font=("Segoe UI", 14, "bold"))
        self.chat_area.see("end")
        self.chat_area.configure(state="disabled")

    def send_message(self):
        text = self.input_entry.get().strip()
        if not text:
            return
        self.input_entry.delete(0, "end")
        self.add_message("You", text)
        threading.Thread(
            target=self.friday._process_command, args=(text,), daemon=True
        ).start()

    def voice_input(self):
        self.status_label.configure(text="Listening...", text_color="#00ff88")
        text = self.friday.stt.listen()
        self.status_label.configure(text="Always Listening...", text_color="#00ff88")
        if text and text.strip():
            self.add_message("You", text)
            threading.Thread(
                target=self.friday._process_command, args=(text,), daemon=True
            ).start()

    def shutdown(self):
        self.add_message("Friday", "Shutting down...")
        self.friday._shutdown()
        self.root.after(1000, self.root.quit)


if __name__ == "__main__":
    friday = Friday()
    gui = FridayGUI(friday)
    gui.root.mainloop()
