import os, subprocess, webbrowser
from pathlib import Path
from datetime import datetime
import pyautogui, psutil
from memory import remember, recall
from ai_brain import ask_ai
from config import SCREENSHOT_DIR
SAFE_APPS={"notepad":"notepad.exe","calculator":"calc.exe","chrome":r"C:\Program Files\Google\Chrome\Application\chrome.exe","edge":r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe","vscode":r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe","vs code":r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe","paint":"mspaint.exe","command prompt":"cmd.exe","cmd":"cmd.exe","file explorer":"explorer.exe","explorer":"explorer.exe"}
SAFE_WEBSITES={"youtube":"https://youtube.com","google":"https://google.com","gmail":"https://mail.google.com","github":"https://github.com","chatgpt":"https://chatgpt.com","whatsapp":"https://web.whatsapp.com","instagram":"https://instagram.com","spotify":"https://open.spotify.com"}
def open_app(name):
    for key,path in SAFE_APPS.items():
        if key in name.lower():
            try: subprocess.Popen(os.path.expandvars(path)); return f"Opening {key}."
            except Exception as e: return f"I could not open {key}: {e}"
    return "I do not know that app yet. Add it in SAFE_APPS inside commands.py."
def open_website(name):
    name=name.lower()
    for site,url in SAFE_WEBSITES.items():
        if site in name: webbrowser.open(url); return f"Opening {site}."
    if "." in name and " " not in name: webbrowser.open("https://"+name.replace("https://","").replace("http://","")); return f"Opening {name}."
    return None
def system_status():
    cpu=psutil.cpu_percent(interval=1); ram=psutil.virtual_memory().percent; batt=psutil.sensors_battery()
    b="Battery info not available" if not batt else f"Battery is at {batt.percent}%"
    return f"CPU usage is {cpu} percent. RAM usage is {ram} percent. {b}."
def take_screenshot():
    Path(SCREENSHOT_DIR).mkdir(exist_ok=True); fn=Path(SCREENSHOT_DIR)/f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"; pyautogui.screenshot().save(fn); return f"Screenshot saved as {fn}."
def handle_command(text):
    text=text.lower().strip()
    if not text: return "I could not hear that clearly."
    if "shutdown assistant" in text or "exit assistant" in text: return "__EXIT__"
    if text.startswith("open "):
        target=text.replace("open ","",1).strip(); wr=open_website(target); return wr if wr else open_app(target)
    if text.startswith("go to "):
        wr=open_website(text.replace("go to ","",1).strip());
        if wr: return wr
    if "search google for" in text:
        q=text.split("search google for",1)[1].strip(); webbrowser.open("https://www.google.com/search?q="+q.replace(" ","+")); return f"Searching Google for {q}."
    if "search youtube for" in text:
        q=text.split("search youtube for",1)[1].strip(); webbrowser.open("https://www.youtube.com/results?search_query="+q.replace(" ","+")); return f"Searching YouTube for {q}."
    if text.startswith("youtube "):
        q=text.replace("youtube ","",1); webbrowser.open("https://www.youtube.com/results?search_query="+q.replace(" ","+")); return f"Searching YouTube for {q}."
    if text.startswith("google "):
        q=text.replace("google ","",1); webbrowser.open("https://www.google.com/search?q="+q.replace(" ","+")); return f"Searching Google for {q}."
    if "screenshot" in text: return take_screenshot()
    if any(x in text for x in ["system status","cpu","battery","ram"]): return system_status()
    if "increase volume" in text or "volume up" in text: pyautogui.press("volumeup",presses=5); return "Increasing volume."
    if "decrease volume" in text or "volume down" in text: pyautogui.press("volumedown",presses=5); return "Decreasing volume."
    if "mute" in text: pyautogui.press("volumemute"); return "Toggling mute."
    if text.startswith("type "): pyautogui.write(text.replace("type ","",1),interval=0.01); return "Typed it."
    if text.startswith("remember "): return remember(text.replace("remember ","",1).strip())
    if "what do you remember" in text or "recall memory" in text: return recall()
    if "time" in text: return "The time is "+datetime.now().strftime("%I:%M %p")
    if "what can you do" in text or text=="help": return "I can answer questions, open apps/websites, search Google/YouTube, take screenshots, control volume, remember notes, type text, and show system status. For safety, I only run commands listed in commands.py."
    return ask_ai(text)
