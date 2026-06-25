import requests
from config import ASSISTANT_NAME, OLLAMA_MODEL, OLLAMA_URL
SYSTEM_PROMPT=f"""You are {ASSISTANT_NAME}, a futuristic desktop AI assistant. Reply clearly, helpfully, and not too long. You are running locally through Ollama."""
def ask_ai(user_text: str) -> str:
    try:
        r=requests.post(OLLAMA_URL,json={"model":OLLAMA_MODEL,"stream":False,"messages":[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_text}]},timeout=120)
        if r.status_code!=200: return "Ollama error: "+r.text
        return r.json().get("message",{}).get("content","I got an empty response from Ollama.").strip()
    except requests.exceptions.ConnectionError:
        return "I cannot connect to Ollama. Make sure Ollama is installed and running."
    except requests.exceptions.ReadTimeout:
        return "Ollama is taking too long. Try llama3.2:1b or restart Ollama."
    except Exception as e:
        return "Ollama AI error: "+str(e)
