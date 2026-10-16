import time
import threading
from pathlib import Path

from playsound3 import playsound


BASE_DIR = Path(__file__).resolve().parent.parent
BELL_FILE = BASE_DIR / "assets" / "bell.mp3"


class BellController:
    def __init__(self, sound_file=BELL_FILE):
        self.sound_file = Path(sound_file)
        self.current_sound = None
        self.ringing = False

    def ring_bell(self, duration=10):
        if self.ringing:
            return

        print("Looking for bell file at:")
        print(self.sound_file)
        print("File exists:", self.sound_file.is_file())

        if not self.sound_file.is_file():
            print("Bell playback error: file not found")
            return

        self.ringing = True

        threading.Thread(
            target=self._play_bell,
            args=(duration,),
            daemon=True
        ).start()

    def _play_bell(self, duration):
        try:
            start_time = time.time()

            while time.time() - start_time < duration and self.ringing:
                self.current_sound = playsound(
                    str(self.sound_file),
                    block=False
                )

                time.sleep(1)

        except Exception as e:
            print("Bell playback error:", e)

        finally:
            self.ringing = False

    def stop_bell(self):
        self.ringing = False

        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception as e:
                print("Could not stop bell:", e)
