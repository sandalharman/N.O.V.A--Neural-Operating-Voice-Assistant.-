import json
from pathlib import Path
from config import MEMORY_FILE
def _load():
    p=Path(MEMORY_FILE)
    if not p.exists(): return {"notes":[]}
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {"notes":[]}
def _save(data): Path(MEMORY_FILE).write_text(json.dumps(data,indent=2),encoding="utf-8")
def remember(note:str):
    d=_load(); d.setdefault("notes",[]).append(note); _save(d); return "I will remember that."
def recall():
    notes=_load().get("notes",[])
    return "I do not have anything saved yet." if not notes else "Here is what I remember: "+"; ".join(notes[-10:])
