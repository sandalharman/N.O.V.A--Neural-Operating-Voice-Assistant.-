import time
import numpy as np
import sounddevice as sd
from config import CLAP_THRESHOLD, CLAPS_TO_WAKE

def wait_for_clap_wake(callback):
    print("Clap detector running. Clap twice to wake NOVA.")
    clap_times = []
    cooldown = 0.25
    last_clap = 0

    def audio_callback(indata, frames, time_info, status):
        nonlocal clap_times, last_clap
        volume = float(np.linalg.norm(indata))
        now = time.time()

        if volume > CLAP_THRESHOLD and now - last_clap > cooldown:
            last_clap = now
            clap_times.append(now)
            clap_times = [t for t in clap_times if now - t < 1.5]
            print("Clap detected:", len(clap_times))

            if len(clap_times) >= CLAPS_TO_WAKE:
                clap_times = []
                callback()

    try:
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100):
            while True:
                time.sleep(0.1)
    except Exception as e:
        print("Clap detector error:", e)
