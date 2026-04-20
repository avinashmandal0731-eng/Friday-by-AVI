"""
phone_control.py — UPDATED & STRENGTHENED (More reliable for all apps)
"""
from ppadb.client import Client as AdbClient

adb_client = AdbClient(host="127.0.0.1", port=5037)

def phone_dispatch(raw_command: str, intent: str = None):
    try:
        devices = adb_client.devices()
        if not devices:
            return False, "Phone not connected. Connect USB and enable USB Debugging."

        dev = devices[0]
        cmd = raw_command.lower().strip()

        print(f"[PHONE DEBUG] Intent: {intent} | Command: '{cmd}'")

        is_close = (intent == "close_app") or any(w in cmd for w in ["close", "band", "stop", "quit", "band kar"])

        # ==================== WHATSAPP ====================
        if "whatsapp" in cmd:
            if is_close:
                dev.shell("am force-stop com.whatsapp")
                return True, "Closing WhatsApp on your phone."
            else:
                dev.shell("am start -n com.whatsapp/.Main")
                return True, "Opening WhatsApp on your phone."

        # ==================== YOUTUBE ====================
        if "youtube" in cmd or "yt" in cmd:
            if is_close:
                dev.shell("am force-stop com.google.android.youtube")
                return True, "Closing YouTube on your phone."
            else:
                dev.shell('am start -a android.intent.action.VIEW -d "https://youtube.com"')
                return True, "Opening YouTube on your phone."

        # ==================== INSTAGRAM ====================
        if "instagram" in cmd or "insta" in cmd:
            if is_close:
                dev.shell("am force-stop com.instagram.android")
                return True, "Closing Instagram on your phone."
            else:
                dev.shell("am start -n com.instagram.android/.activity.MainTabActivity")
                return True, "Opening Instagram on your phone."

        # ==================== GALLERY / ALBUMS / PHOTOS (Vivo) ====================
        if any(x in cmd for x in ["gallery", "album", "albums", "photos", "photo", "pictures"]):
            if is_close:
                dev.shell("am force-stop com.vivo.gallery")
                return True, "Closing Gallery on your phone."
            else:
                dev.shell("am start -n com.vivo.gallery/.MainActivity")
                return True, "Opening Gallery on your phone."

        # ==================== CALCULATOR ====================
        if "calculator" in cmd or "calc" in cmd:
            if is_close:
                dev.shell("am force-stop com.android.calculator2")
                return True, "Closing Calculator on your phone."
            else:
                dev.shell("am start -n com.android.calculator2/.Calculator")
                return True, "Opening Calculator on your phone."

        # ==================== CAMERA ====================
        if "camera" in cmd:
            if is_close:
                dev.shell("am force-stop com.android.camera2")
                return True, "Closing Camera on your phone."
            else:
                dev.shell("am start -n com.android.camera2/.CameraActivity")
                return True, "Opening Camera on your phone."

        # ==================== SETTINGS ====================
        if "settings" in cmd:
            if is_close:
                dev.shell("am force-stop com.android.settings")
                return True, "Closing Settings on your phone."
            else:
                dev.shell("am start -n com.android.settings/.Settings")
                return True, "Opening Settings on your phone."

        # ==================== MESSAGES / SMS ====================
        if "message" in cmd or "sms" in cmd or "msg" in cmd:
            if is_close:
                dev.shell("am force-stop com.android.mms")
                return True, "Closing Messages on your phone."
            else:
                dev.shell("am start -n com.android.mms/.ui.ConversationList")
                return True, "Opening Messages on your phone."

        # ==================== PHONE / DIALER ====================
        if "phone" in cmd or "dialer" in cmd or "call" in cmd:
            if is_close:
                dev.shell("am force-stop com.android.dialer")
                return True, "Closing Phone on your phone."
            else:
                dev.shell("am start -n com.android.dialer/.DialtactsActivity")
                return True, "Opening Phone on your phone."

        # ==================== CONTACTS ====================
        if "contact" in cmd or "contacts" in cmd:
            if is_close:
                dev.shell("am force-stop com.android.contacts")
                return True, "Closing Contacts on your phone."
            else:
                dev.shell("am start -n com.android.contacts/.activities.PeopleActivity")
                return True, "Opening Contacts on your phone."

        # ==================== CLOCK ====================
        if "clock" in cmd or "alarm" in cmd:
            if is_close:
                dev.shell("am force-stop com.android.deskclock")
                return True, "Closing Clock on your phone."
            else:
                dev.shell("am start -n com.android.deskclock/.DeskClock")
                return True, "Opening Clock on your phone."

        # ==================== BROWSER / CHROME ====================
        if "browser" in cmd or "chrome" in cmd:
            if is_close:
                dev.shell("am force-stop com.android.chrome")
                return True, "Closing Browser on your phone."
            else:
                dev.shell("am start -n com.android.chrome/com.google.android.apps.chrome.Main")
                return True, "Opening Browser on your phone."

        return False, "Phone command not understood. Try: open gallery on phone or close calculator on phone"

    except Exception as e:
        print(f"[PHONE ERROR] {e}")
        return False, f"Phone error: {str(e)}"