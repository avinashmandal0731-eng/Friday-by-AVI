# 🤖 Friday — AI Voice Assistant by AVI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70b-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows)
![Status](https://img.shields.io/badge/Status-Active_Development-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**A locally-running Windows AI voice assistant with bilingual support, wake-word detection, LLM-powered responses, and a custom animated GUI.**

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Environment Variables](#-environment-variables)
- [How to Run](#-how-to-run)
- [How It Works](#-how-it-works)
- [File Overview](#-file-overview)
- [Known Issues & Fixes](#-known-issues--fixes)
- [Future Plans](#-future-plans)
- [Author](#-author)

---

## 📌 About the Project

**Friday** is a locally-running AI voice assistant built for Windows, inspired by JARVIS from Iron Man.  
It listens for a wake word, understands commands in both **Hindi and English**, talks back using text-to-speech, and can control your PC — all powered by a local GUI with animated visuals.

This project was built as part of my AI/Engineering portfolio, demonstrating real-world integration of speech recognition, LLM inference via Groq API, PC automation, and GUI design.

---

## ✨ Features

- 🎙️ **Wake Word Detection** — Activates only when you say the trigger word (hands-free)
- 🗣️ **Language Support** — Understands and responds in  English
- 🤖 **LLM-Powered Brain** — Uses Groq API (LLaMA 3.3-70B) for intelligent responses
- 🖥️ **PC Control** — Open apps, control volume, take screenshots, manage windows via voice
- 📱 **Phone Control** — Basic phone interaction support
- 🧠 **Memory System** — Remembers user data across sessions using local JSON storage
- 📊 **Activity Tracker** — Tracks and logs assistant activity
- 🎨 **Custom Animated GUI** — Built with Tkinter, includes orb animation and visual feedback
- 🔐 **Secure API Handling** — All credentials stored in `.env`, never hardcoded
- ⚡ **Local & Fast** — Runs entirely on your Windows machine, no cloud dependency except Groq

---

## 📁 Project Structure

```
friday-ai-assistant/
│
├── main.py              # Entry point — launches the GUI and starts all modules
├── brain.py             # Core AI logic — sends prompts to Groq LLM, parses intent tags
├── voice_engine.py      # Speech recognition (input) and TTS (output) engine
├── pc_control.py        # Voice-controlled PC automation (apps, volume, screenshots)
├── phone_control.py     # Phone interaction support module
├── memory.py            # Stores and retrieves user memory from aria_memory.json
├── data_tracker.py      # Logs and tracks assistant usage/activity
│
├── .env                 # 🔐 SECRET — API keys (never uploaded to GitHub)
├── .env.example         # ✅ Safe template showing required environment variables
├── .gitignore           # Tells Git which files/folders to ignore
│
├── aria_memory.json     # Auto-generated at runtime — stores user memory
├── aria_tracker.json    # Auto-generated at runtime — stores activity data
├── Orb animation WIP.gif  # Animated orb used in GUI
│
├── requirements.txt     # All Python dependencies
└── README.md            # This file
```

---

## 🛠️ Tech Stack

| Category | Tool / Library |
|---|---|
| Language | Python 3.10+ |
| LLM Inference | Groq API — LLaMA 3.3-70B Versatile |
| Speech Input | `SpeechRecognition` + Google Web Speech API |
| Voice Output | `pyttsx3` (offline TTS) |
| GUI | `Tkinter` with animated GIF orb |
| PC Automation | `pyautogui`, `os`, `subprocess` |
| Memory Storage | Local JSON files |
| Secret Management | `python-dotenv` + `.env` file |
| Wake Word | Custom keyword detection logic |

---

## ✅ Prerequisites

Before setting up, make sure you have:

- Windows 10 or 11
- Python 3.10 or higher → [Download here](https://www.python.org/downloads/)
- A free Groq API key → [Get it here](https://console.groq.com/)
- A working microphone connected to your PC
- Git installed → [Download here](https://git-scm.com/)

---

## 🚀 Installation & Setup

Follow every step carefully. Don't skip any.

**Step 1 — Clone the repository**
```bash
git clone https://github.com/YourUsername/friday-ai-assistant.git
```

**Step 2 — Move into the project folder**
```bash
cd friday-ai-assistant
```

**Step 3 — Create a virtual environment**
```bash
python -m venv venv
```

**Step 4 — Activate the virtual environment**
```bash
venv\Scripts\activate
```
> You should see `(venv)` at the start of your terminal line. That means it's active.

**Step 5 — Install all required libraries**
```bash
pip install -r requirements.txt
```
> This may take 1–3 minutes. Let it finish completely.

**Step 6 — Set up your secret API key**

Copy the example env file:
```bash
copy .env.example .env
```
Then open the `.env` file in Notepad and replace `your_groq_api_key_here` with your actual Groq API key.

**Step 7 — Run the assistant**
```bash
python main.py
```

---

## 🔐 Environment Variables

Create a `.env` file in the root folder (copy from `.env.example`):

```env
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ **Never share your `.env` file or paste your API key anywhere publicly.**  
> The `.gitignore` in this project already prevents it from being uploaded to GitHub.

---

## ▶️ How to Run

Once everything is set up:

1. Make sure your **microphone is connected and working**
2. Activate the virtual environment: `venv\Scripts\activate`
3. Run: `python main.py`
4. The GUI will open with the animated orb
5. Say the **wake word** to activate Friday
6. Give your command in Hindi or English
7. Friday will respond with voice + visual feedback

**Example commands you can try:**
- *"Friday, open Chrome"*
- *"Friday, what's the time?"*
- *"Friday, take a screenshot"*
- *"Friday, volume up"*
- *"Friday, tell me a joke"*

---

## ⚙️ How It Works

```
You speak → Microphone → voice_engine.py (Speech Recognition)
                                  ↓
                          Wake word detected?
                                  ↓ Yes
                          brain.py → Groq API (LLaMA 3.3-70B)
                                  ↓
                     Intent tags parsed from LLM response
                                  ↓
           ┌──────────────────────┼──────────────────────┐
           ↓                      ↓                      ↓
    pc_control.py          memory.py              voice_engine.py
   (PC automation)     (Save/recall info)        (TTS — speaks back)
                                  ↓
                          GUI updates (Tkinter orb animates)
```

---

## 📄 File Overview

| File | Purpose |
|---|---|
| `main.py` | Starts everything — launches GUI, connects all modules |
| `brain.py` | Sends your command to Groq LLM, reads intent tags in response |
| `voice_engine.py` | Listens to your mic, converts speech to text; converts text to speech |
| `pc_control.py` | Handles PC commands like opening apps, screenshots, volume |
| `phone_control.py` | Handles phone-related interactions |
| `memory.py` | Reads/writes user info to `aria_memory.json` |
| `data_tracker.py` | Logs what Friday does to `aria_tracker.json` |

---

## 🐛 Known Issues & Fixes

| Issue | Fix |
|---|---|
| Microphone not detected | Check Windows sound settings → make sure mic is set as default input |
| `ModuleNotFoundError` on run | Make sure venv is activated and `pip install -r requirements.txt` was run |
| API key error / 401 | Check your `.env` file — make sure the key is correct with no spaces |
| TTS not speaking | Check if speakers/headphones are connected and volume is up |
| GUI not opening | Make sure `Tkinter` is installed (comes with standard Python on Windows) |
| Wake word not working | Speak clearly, reduce background noise, check mic sensitivity |

---

## 🔮 Future Plans

- [ ] Add custom ML model for offline intent classification
- [ ] Add a demo GIF to this README showing Friday in action
- [ ] Support for more PC commands (browser control, file management)
- [ ] Settings panel inside the GUI
- [ ] Voice profile — recognize who is speaking
- [ ] Android companion app for phone control

---

## 👤 Author

**AVI**  
📍 Delhi, India  
🎓 Engineering student | AI & Cybersecurity enthusiast  
🔗 [GitHub](https://github.com/YourUsername) | [LinkedIn](https://linkedin.com/in/YourProfile)

> 💡 This project is part of my portfolio for the **Open Doors Russian Scholarship Olympiad** (Engineering & Technology track).

---

## 📜 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute with credit.

---

<div align="center">
Made with ❤️ and Python by AVI &nbsp;|&nbsp; Friday is always listening 👂
</div>
