import speech_recognition as sr
def listen_once(timeout=6, phrase_time_limit=8)->str:
    rec=sr.Recognizer(); rec.energy_threshold=300; rec.dynamic_energy_threshold=True
    with sr.Microphone() as source:
        print("Listening..."); rec.adjust_for_ambient_noise(source,duration=0.6); audio=rec.listen(source,timeout=timeout,phrase_time_limit=phrase_time_limit)
    try:
        text=rec.recognize_google(audio); print("You:",text); return text.lower().strip()
    except Exception: return ""
