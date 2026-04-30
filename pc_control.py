"""
pc_control.py — Friday by AVI
Fixed:
  - Comprehensive ALIASES so voice variations all map correctly
  - taskkill return code actually checked → honest success/fail feedback
  - Removed broken pyautogui browser-close (just kills chrome.exe reliably)
  - Multi-word app names handled properly
  - Multiple exe fallbacks for apps that can have different filenames
"""
import subprocess
import webbrowser
import os

# ── App aliases: maps every voice variation to one canonical key ────────────
# Add more here whenever Friday mishears a new variation.
ALIASES: dict[str, str] = {
    # Browsers
    "chrome": "chrome",
    "google chrome": "chrome",
    "browser": "chrome",
    "edge": "edge",
    "microsoft edge": "edge",
    "firefox": "firefox",

    # YouTube / Gmail  (browser tabs — closing kills the browser)
    "youtube": "youtube",
    "yt": "youtube",
    "gmail": "gmail",
    "google": "chrome",

    # Office
    "word": "word",
    "microsoft word": "word",
    "excel": "excel",
    "microsoft excel": "excel",
    "powerpoint": "powerpoint",
    "microsoft powerpoint": "powerpoint",
    "ppt": "powerpoint",

    # System
    "notepad": "notepad",
    "calculator": "calculator",
    "calc": "calculator",
    "paint": "paint",
    "task manager": "task manager",
    "taskmgr": "task manager",
    "file explorer": "file explorer",
    "explorer": "file explorer",
    "this pc": "file explorer",
    "cmd": "cmd",
    "command prompt": "cmd",
    "powershell": "powershell",

    # Dev
    "vs code": "vscode",
    "vscode": "vscode",
    "visual studio code": "vscode",
    "visual studio": "vscode",

    # Media / Social
    "spotify": "spotify",
    "vlc": "vlc",
    "vlc media player": "vlc",
    "discord": "discord",
    "whatsapp": "whatsapp",
    "telegram": "telegram",

    # Other
    "zoom": "zoom",
    "teams": "teams",
    "microsoft teams": "teams",
    "obs": "obs",
    "obs studio": "obs",
    "steam": "steam",
    "epic": "epic",
    "epic games": "epic",
}

# ── Close map: canonical key → exe filename(s) to kill ─────────────────────
# List multiple exes for apps that might use different filenames.
CLOSE_MAP: dict[str, list[str]] = {
    "chrome":       ["chrome.exe"],
    "youtube":      ["chrome.exe"],           # runs in browser
    "gmail":        ["chrome.exe"],           # runs in browser
    "edge":         ["msedge.exe"],
    "firefox":      ["firefox.exe"],

    "word":         ["WINWORD.EXE"],
    "excel":        ["EXCEL.EXE"],
    "powerpoint":   ["POWERPNT.EXE"],

    "notepad":      ["notepad.exe"],
    "calculator":   ["Calculator.exe", "calc.exe"],
    "paint":        ["mspaint.exe"],
    "task manager": ["Taskmgr.exe"],
    "file explorer":["explorer.exe"],
    "cmd":          ["cmd.exe"],
    "powershell":   ["powershell.exe", "pwsh.exe"],

    "vscode":       ["Code.exe"],
    "spotify":      ["Spotify.exe"],
    "vlc":          ["vlc.exe"],
    "discord":      ["Discord.exe"],
    "whatsapp":     ["WhatsApp.exe"],
    "telegram":     ["Telegram.exe"],
    "zoom":         ["Zoom.exe"],
    "teams":        ["Teams.exe"],
    "obs":          ["obs64.exe", "obs.exe"],
    "steam":        ["steam.exe"],
    "epic":         ["EpicGamesLauncher.exe"],
}

# ── Open map: canonical key → how to launch ────────────────────────────────
# "shell_cmd"  → subprocess with shell=True  (for system commands like 'calc')
# "path"       → direct executable path (Popen without shell)
# "url"        → webbrowser.open
# "ms_store"   → start ms-<protocol>: for store apps

OPEN_MAP: dict[str, dict] = {
    "chrome":       {"type": "shell_cmd", "cmd": "start chrome"},
    "edge":         {"type": "shell_cmd", "cmd": "start msedge"},
    "firefox":      {"type": "shell_cmd", "cmd": "start firefox"},

    "youtube":      {"type": "url",       "cmd": "https://www.youtube.com"},
    "gmail":        {"type": "url",       "cmd": "https://mail.google.com"},

    "word":         {"type": "shell_cmd", "cmd": "start winword"},
    "excel":        {"type": "shell_cmd", "cmd": "start excel"},
    "powerpoint":   {"type": "shell_cmd", "cmd": "start powerpnt"},

    "notepad":      {"type": "shell_cmd", "cmd": "notepad"},
    "calculator":   {"type": "shell_cmd", "cmd": "start calc"},
    "paint":        {"type": "shell_cmd", "cmd": "start mspaint"},
    "task manager": {"type": "shell_cmd", "cmd": "start taskmgr"},
    "file explorer":{"type": "shell_cmd", "cmd": "start explorer"},
    "cmd":          {"type": "shell_cmd", "cmd": "start cmd"},
    "powershell":   {"type": "shell_cmd", "cmd": "start powershell"},

    "vscode":       {"type": "shell_cmd", "cmd": "code"},
    "spotify":      {"type": "shell_cmd", "cmd": "start spotify"},
    "vlc":          {"type": "shell_cmd", "cmd": "start vlc"},
    "discord":      {"type": "shell_cmd", "cmd": "start discord"},
    "whatsapp":     {"type": "whatsapp",  "cmd": ""},   # special handling below
    "telegram":     {"type": "shell_cmd", "cmd": "start telegram"},
    "zoom":         {"type": "shell_cmd", "cmd": "start zoom"},
    "teams":        {"type": "shell_cmd", "cmd": "start teams"},
    "steam":        {"type": "shell_cmd", "cmd": "start steam"},
    "epic":         {"type": "shell_cmd", "cmd": "start EpicGamesLauncher"},
}

# WhatsApp desktop path (personalised to your machine)
WHATSAPP_PATH = r"C:\Users\Avinash\AppData\Local\WhatsApp\WhatsApp.exe"


# ── Helpers ─────────────────────────────────────────────────────────────────

def _taskkill(exe: str) -> bool:
    """Kill a process by exe name. Returns True only if taskkill succeeds."""
    result = subprocess.run(
        f"taskkill /IM {exe} /F",
        shell=True,
        capture_output=True
    )
    success = result.returncode == 0
    if success:
        print(f"[PC] Killed: {exe}")
    else:
        print(f"[PC] Not running or failed: {exe} (code {result.returncode})")
    return success


def _resolve(app_raw: str) -> str:
    """Map raw voice text → canonical app key via ALIASES."""
    app = app_raw.lower().strip()
    # Direct alias lookup
    if app in ALIASES:
        return ALIASES[app]
    # Partial match fallback (e.g. "vs cod" → "vscode")
    for alias, canonical in ALIASES.items():
        if alias in app or app in alias:
            return canonical
    return app   # return as-is; might still work for generic close


# ── Main dispatch ────────────────────────────────────────────────────────────

def dispatch(intent: str, slots: dict):
    try:
        raw_app = str(slots.get("app", "")).strip()
        app     = _resolve(raw_app)
        print(f"[PC] Intent: {intent} | Raw: '{raw_app}' | Resolved: '{app}'")

        # ── CLOSE ──────────────────────────────────────────────────────────
        if intent == "close_app":
            exes = CLOSE_MAP.get(app)

            if exes:
                killed_any = False
                for exe in exes:
                    if _taskkill(exe):
                        killed_any = True
                if killed_any:
                    return True, f"{app.title()} closed, sir."
                else:
                    return False, f"{app.title()} already closed or not running."
            else:
                # Generic fallback — try <app>.exe
                guessed_exe = app.replace(" ", "") + ".exe"
                if _taskkill(guessed_exe):
                    return True, f"Closed {app.title()}."
                return False, f"Sorry, couldn't find {app.title()} running. Is it open?"

        # ── OPEN ───────────────────────────────────────────────────────────
        if intent == "open_app":
            entry = OPEN_MAP.get(app)

            if entry:
                kind = entry["type"]
                cmd  = entry["cmd"]

                if kind == "url":
                    webbrowser.open(cmd)
                    return True, f"Opening {app.title()} in your browser."

                elif kind == "whatsapp":
                    if os.path.exists(WHATSAPP_PATH):
                        subprocess.Popen([WHATSAPP_PATH])
                        return True, "Opening WhatsApp."
                    else:
                        webbrowser.open("https://web.whatsapp.com")
                        return True, "Opening WhatsApp Web."

                elif kind == "shell_cmd":
                    subprocess.Popen(cmd, shell=True)
                    return True, f"Opening {app.title()}, sir."

            else:
                # Generic fallback — try launching directly
                subprocess.Popen(raw_app, shell=True)
                return True, f"Trying to open {raw_app.title()}."

        return False, "Command not understood."

    except Exception as e:
        print(f"[PC ERROR] {e}")
        return False, f"Something went wrong: {e}"
