"""
pc_control.py — FINAL STRONG VERSION (Browser closing fixed)
"""
import subprocess
import webbrowser
import os
import time

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    HAS_PYAU = True
except:
    HAS_PYAU = False

def dispatch(intent: str, slots: dict):
    try:
        app = str(slots.get("app", "")).lower().strip()
        print(f"[PC_CONTROL DEBUG] Intent: {intent} | App: '{app}'")

        # ====================== CLOSE LOGIC (Very Strong) ======================
        if intent == "close_app":

            # Browser apps (YouTube, Gmail, etc.)
            if app in ["youtube", "gmail", "browser", "chrome"]:
                if HAS_PYAU:
                    try:
                        # Focus Chrome window
                        pyautogui.press('alt')
                        time.sleep(0.4)
                        # Close tab multiple times for reliability
                        for _ in range(3):
                            pyautogui.hotkey('ctrl', 'w')
                            time.sleep(0.3)
                        print("[PC_CONTROL] Closed tab with Ctrl+W (multiple attempts)")
                        return True, f"Closing {app.title()} tab."
                    except:
                        pass

                # Strong fallback - close all Chrome
                subprocess.call("taskkill /IM chrome.exe /F", shell=True)
                return True, f"Closed all Chrome windows (including {app.title()})."

            # Desktop apps
            close_map = {
                "word": "WINWORD.EXE",
                "excel": "EXCEL.EXE",
                "powerpoint": "POWERPNT.EXE",
                "notepad": "notepad.exe",
                "calc": "calc.exe",
                "spotify": "spotify.exe",
                "whatsapp": "WhatsApp.exe",
            }

            if app in close_map:
                exe = close_map[app]
                subprocess.call(f"taskkill /IM {exe} /F", shell=True)
                return True, f"{app.title()} band kar diya."

            # Generic close
            subprocess.call(f"taskkill /IM {app}.exe /F", shell=True)
            return True, f"Closing {app.title()}..."

        # ====================== OPEN LOGIC ======================
        if intent == "open_app":

            # WhatsApp Desktop first
            if "whatsapp" in app:
                desktop_path = r"C:\Users\Avinash\AppData\Local\WhatsApp\WhatsApp.exe"
                if os.path.exists(desktop_path):
                    subprocess.Popen([desktop_path])
                    return True, "Opening WhatsApp desktop app."
                else:
                    webbrowser.open("https://web.whatsapp.com")
                    return True, "Opening WhatsApp in browser."

            # Web apps
            web_apps = {
                "youtube": "https://www.youtube.com",
                "gmail": "https://mail.google.com",
            }
            if app in web_apps:
                webbrowser.open(web_apps[app])
                return True, f"Opening {app.title()} in browser."

            # Desktop apps
            app_map = {
                "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                "notepad": "notepad",
                "calculator": "calc",
                "paint": "mspaint",
                "chrome": "chrome",
                "browser": "chrome",
                "vscode": "code",
                "spotify": "spotify",
                "task manager": "taskmgr",
                "explorer": "explorer",
            }

            if app in app_map:
                cmd = app_map[app]
                if os.path.exists(cmd):
                    subprocess.Popen([cmd])
                else:
                    subprocess.Popen(cmd, shell=True)
                return True, f"{app.title()} khul raha hai."

            subprocess.Popen(app, shell=True)
            return True, f"Trying to open {app.title()}..."

        return False, "Command not understood."

    except Exception as e:
        print(f"[PC_CONTROL ERROR] {e}")
        return False, f"Error: {str(e)}"