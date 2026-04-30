"""
voice_engine.py — Friday by AVI
TTS: edge-tts (Microsoft Neural Voice — Jarvis-quality)
STT: SpeechRecognition (Google Web Speech, unchanged)
"""

import os
import time
import asyncio
import threading
import queue
import tempfile

import sounddevice as sd
import numpy as np
import speech_recognition as sr

# ──────────────────────────────────────────────
#  Choose your voice:
#  en-GB-RyanNeural   → British male (closest to Jarvis)
#  en-US-GuyNeural    → American male, smooth
#  en-US-ChristopherNeural → American male, deep
# ──────────────────────────────────────────────
VOICE = "en-GB-SoniaNeural"
RATE  = "+0%"    # speed: "+10%" faster, "-10%" slower
PITCH = "-5Hz"   # slightly lower = more authoritative


# ──────────────────────────────────────────────
#  Audio helpers
# ──────────────────────────────────────────────
def play_chime():
    """Short two-tone chime to signal wake."""
    try:
        for freq in (800, 1000):
            tone = np.sin(2 * np.pi * freq * np.linspace(0, 0.15, int(44100 * 0.15))).astype(np.float32)
            sd.play(tone, samplerate=44100)
            sd.wait()
    except Exception:
        pass


def _play_mp3(path: str):
    """
    Play an MP3 file using pygame.mixer.
    Falls back to a subprocess call if pygame is unavailable.
    """
    try:
        import pygame
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(50)
        pygame.mixer.music.unload()
    except Exception as pg_err:
        # Last-resort fallback: Windows Media Player via PowerShell
        try:
            import subprocess
            subprocess.run(
                ["powershell", "-c",
                 f"(New-Object Media.SoundPlayer '{path}').PlaySync()"],
                capture_output=True
            )
        except Exception:
            print(f"[TTS] Could not play audio: {pg_err}")


# ──────────────────────────────────────────────
#  TTS Engine
# ──────────────────────────────────────────────
class TTSEngine:
    """
    Queue-based edge-tts wrapper.
    Speaks from any thread without COM/main-thread restrictions.
    """

    def __init__(self):
        self._queue: queue.Queue = queue.Queue()
        self._worker_thread = threading.Thread(
            target=self._worker_loop, daemon=True, name="TTS-Worker"
        )
        self._worker_thread.start()
        print(f"[TTS] edge-tts ready | voice: {VOICE}")
        # Startup confirmation
        self.speak("Friday online. Ready to assist, AVI.")

    # ── public API ─────────────────────────────

    def speak(self, text: str):
        """Non-blocking — queues text and returns immediately."""
        if not text or not text.strip():
            return
        print(f"[TTS] → {text[:90]}{'...' if len(text) > 90 else ''}")
        self._queue.put(text.strip())

    def speak_sync(self, text: str):
        """Blocking — waits until speech finishes. Use for shutdown messages."""
        self._speak_now(text)

    def stop(self):
        """Signal the worker to exit cleanly."""
        self._queue.put(None)

    # ── internals ──────────────────────────────

    def _worker_loop(self):
        while True:
            item = self._queue.get()
            if item is None:       # poison pill
                break
            self._speak_now(item)
            self._queue.task_done()

    def _speak_now(self, text: str):
        """Generate speech with edge-tts and play it."""
        tmp_path = None
        try:
            import edge_tts                     # pip install edge-tts

            # Write to a temp file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tmp_path = f.name

            # edge-tts is async; run it in a fresh event loop (thread-safe)
            async def _generate():
                communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
                await communicate.save(tmp_path)

            asyncio.run(_generate())

            # Play the generated audio
            _play_mp3(tmp_path)

        except ImportError:
            print("[TTS] edge-tts not installed. Run: pip install edge-tts pygame")
            print(f"[Friday] {text}")
        except Exception as e:
            print(f"[TTS Error] {e}")
            print(f"[Friday] {text}")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass


# ──────────────────────────────────────────────
#  STT Engine  (unchanged — was working fine)
# ──────────────────────────────────────────────
class STTEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        print("[STT] SpeechRecognition ready.")

    def listen(self, timeout: int = 8, phrase_time_limit: int = 10) -> str | None:
        try:
            with sr.Microphone() as source:
                print("[STT] Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
            text = self.recognizer.recognize_google(audio)
            if text:
                print(f"[STT] You said: {text}")
                return text.strip()
            return None
        except sr.WaitTimeoutError:
            return None          # silence — normal, don't print anything
        except Exception as e:
            print(f"[STT Error] {e}")
            return None
