import sounddevice as sd
import numpy as np
import time
import threading

class ClapDetector:
    def __init__(self, on_double_clap):
        self.on_double_clap = on_double_clap
        self.running = False
        self.thread = None
        self.last_clap_time = 0
        self.clap_threshold = 0.3
        self.double_clap_window = 0.6

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("[Clap] Double clap to wake/sleep ARIA")

    def stop(self):
        self.running = False

    def _listen_loop(self):
        try:
            with sd.InputStream(samplerate=44100, channels=1, dtype='float32') as stream:
                while self.running:
                    audio, _ = stream.read(1024)
                    volume = np.max(np.abs(audio))
                    if volume > self.clap_threshold:
                        current = time.time()
                        if current - self.last_clap_time < self.double_clap_window:
                            print("[Clap] Double clap detected!")
                            self.on_double_clap()
                            self.last_clap_time = 0
                        else:
                            self.last_clap_time = current
                    time.sleep(0.01)
        except:
            print("[Clap] Microphone issue - using only voice for now.")