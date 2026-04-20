import customtkinter as ctk
from tkinter import scrolledtext
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ARIAGUI:
    def __init__(self, aria_instance):
        self.aria = aria_instance  # your main ARIA class
        
        self.root = ctk.CTk()
        self.root.title("ARIA - Adaptive Real-time Intelligent Assistant")
        self.root.geometry("900x600")

        # Title
        title = ctk.CTkLabel(self.root, text="ARIA", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=10)

        # Conversation area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap="word", font=("Consolas", 12), state="disabled", bg="#1f1f1f", fg="white")
        self.chat_area.pack(padx=20, pady=10, fill="both", expand=True)

        # Status label
        self.status = ctk.CTkLabel(self.root, text="Status: Awake | Listening...", font=ctk.CTkFont(size=14))
        self.status.pack(pady=5)

        # Input box + Send button
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.pack(padx=20, pady=10, fill="x")

        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Type here or speak...", height=40)
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0,10))

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=100, command=self.send_text)
        self.send_btn.pack(side="right")

        # Buttons row
        btn_frame = ctk.CTkFrame(self.root)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Wake Up", command=self.wake_up).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Go to Sleep", command=self.sleep).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Exit", fg_color="red", command=self.shutdown).pack(side="left", padx=5)

        # Start listening in background
        threading.Thread(target=self.start_listening, daemon=True).start()

    def add_message(self, sender: str, message: str):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", f"{sender}: {message}\n\n")
        self.chat_area.see("end")
        self.chat_area.configure(state="disabled")

    def send_text(self):
        text = self.user_input.get().strip()
        if text:
            self.add_message("You", text)
            self.user_input.delete(0, "end")
            # Process through your ARIA
            threading.Thread(target=self.process_input, args=(text,), daemon=True).start()

    def process_input(self, text):
        # Call your existing _process_input or similar
        self.aria._process_input(text)

    def start_listening(self):
        # Integrate with your existing STT loop here later
        pass

    def wake_up(self):
        self.aria._wake_up()
        self.add_message("ARIA", "I'm awake.")

    def sleep(self):
        self.aria._go_to_sleep()
        self.add_message("ARIA", "Going to sleep.")

    def shutdown(self):
        self.add_message("ARIA", "Shutting down...")
        self.aria._shutdown()
        self.root.quit()

# To launch GUI instead of console mode, modify main.py later