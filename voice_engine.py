"""
voice_engine.py — Clean & Simple (No circular import)
"""

import os
import time
import sounddevice as sd
import numpy as np
import speech_recognition as sr

def play_chime():
    """Play a simple chime sound"""
    try:
        sd.play(np.sin(2 * np.pi * 800 * np.linspace(0, 0.2, 44100)), samplerate=44100)
        time.sleep(0.3)
        sd.play(np.sin(2 * np.pi * 1000 * np.linspace(0, 0.2, 44100)), samplerate=44100)
    except:
        pass

class TTSEngine:
    def __init__(self):
        print("[TTS] Initializing pyttsx3...")
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 160)
            self.engine.setProperty('volume', 1.0)
            print("[TTS] pyttsx3 initialized successfully")
            # Test voice
            self.speak("Hello AVI. This is Friday. Can you hear me?")
        except Exception as e:
            print(f"[TTS] pyttsx3 failed: {e}")
            self.engine = None

    def speak(self, text: str):
        print(f"[TTS] Speaking: {text[:80]}...")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
                print("[TTS] Speech completed")
            except Exception as e:
                print(f"[TTS Error] {e}")
        else:
            print(f"[Friday] {text}")

    def speak_sync(self, text: str):
        self.speak(text)

    def stop(self):
        pass


class STTEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300

    def listen(self, timeout: int = 8, phrase_time_limit: int = 10) -> str | None:
        try:
            with sr.Microphone() as source:
                print("[Listening... Speak now]")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            text = self.recognizer.recognize_google(audio)
            if text:
                print(f"[STT] You said: {text}")
                return text.strip()
            return None
        except Exception as e:
            print(f"[STT Error] {e}")
            return None