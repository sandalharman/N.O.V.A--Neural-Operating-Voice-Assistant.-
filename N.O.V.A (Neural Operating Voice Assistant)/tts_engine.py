import pyttsx3
from config import VOICE_RATE
_engine=None
def get_engine():
    global _engine
    if _engine is None:
        _engine=pyttsx3.init(); _engine.setProperty("rate",VOICE_RATE)
        voices=_engine.getProperty("voices")
        if voices: _engine.setProperty("voice", voices[0].id)
    return _engine
def speak(text:str):
    print("NOVA:",text)
    try:
        eng=get_engine(); eng.say(text); eng.runAndWait()
    except Exception as e: print("TTS error:",e)
