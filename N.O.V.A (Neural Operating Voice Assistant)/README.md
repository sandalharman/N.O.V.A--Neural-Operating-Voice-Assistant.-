# NOVA Desktop App - Ollama Jarvis Version

This is a real Windows desktop app, not a webpage.

## Setup
1. Install Ollama for Windows.
2. Run: `ollama pull llama3.2:1b`
3. Rename `.env.example` to `.env`
4. Run:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python nova_desktop.py
```

## Commands
open youtube, open chrome, open notepad, open file explorer, google python projects, youtube relaxing music, take screenshot, system status, increase volume, decrease volume, mute, remember my project is nova, what do you remember, type hello world

## Make EXE
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile nova_desktop.py
```
Your app will be in the `dist` folder.
