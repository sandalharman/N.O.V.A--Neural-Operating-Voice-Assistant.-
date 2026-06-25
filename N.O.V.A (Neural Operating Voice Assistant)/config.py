import os
from dotenv import load_dotenv
load_dotenv()
ASSISTANT_NAME=os.getenv("ASSISTANT_NAME","NOVA")
VOICE_RATE=int(os.getenv("VOICE_RATE","175"))
CLAP_THRESHOLD=float(os.getenv("CLAP_THRESHOLD","0.55"))
CLAPS_TO_WAKE=int(os.getenv("CLAPS_TO_WAKE","2"))
MEMORY_FILE="memory.json"
SCREENSHOT_DIR="screenshots"
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL","llama3.2:1b")
OLLAMA_URL=os.getenv("OLLAMA_URL","http://127.0.0.1:11434/api/chat")
