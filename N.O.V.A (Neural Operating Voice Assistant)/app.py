import threading
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from tts_engine import speak
from speech_io import listen_once
from clap_detector import wait_for_clap_wake
from commands import handle_command
from config import ASSISTANT_NAME

app = Flask(__name__)
CORS(app)

STATE = {
    "assistant": ASSISTANT_NAME,
    "status": "online",
    "last_user": "",
    "last_reply": "System online. Clap twice or press Listen.",
    "listening": False,
    "history": [
        {"role": "assistant", "text": "System online. Clap twice or press Listen."}
    ]
}

def add_history(role, text):
    STATE["history"].append({"role": role, "text": text})
    STATE["history"] = STATE["history"][-50:]

def process_text(text: str):
    text = text.strip()
    STATE["last_user"] = text
    add_history("user", text)

    reply = handle_command(text)

    if reply == "__EXIT__":
        reply = "Shutting down assistant. Close the terminal window to stop the server."
        STATE["status"] = "shutdown requested"

    STATE["last_reply"] = reply
    add_history("assistant", reply)
    speak(reply)
    return reply

def wake_and_listen():
    if STATE["listening"]:
        return

    STATE["listening"] = True
    STATE["status"] = "listening"
    speak("Yes, I am listening.")
    try:
        text = listen_once()
        if text:
            process_text(text)
        else:
            reply = "I did not catch that."
            STATE["last_reply"] = reply
            add_history("assistant", reply)
            speak(reply)
    except Exception as e:
        reply = "Voice error: " + str(e)
        STATE["last_reply"] = reply
        add_history("assistant", reply)
    finally:
        STATE["listening"] = False
        STATE["status"] = "online"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/state")
def api_state():
    return jsonify(STATE)

@app.route("/api/command", methods=["POST"])
def api_command():
    data = request.get_json(force=True)
    text = data.get("text", "")
    reply = process_text(text)
    return jsonify({"reply": reply, "history": STATE["history"]})

@app.route("/api/listen", methods=["POST"])
def api_listen():
    threading.Thread(target=wake_and_listen, daemon=True).start()
    return jsonify({"status": "listening"})

def start_clap_thread():
    t = threading.Thread(target=wait_for_clap_wake, args=(wake_and_listen,), daemon=True)
    t.start()

if __name__ == "__main__":
    print(f"{ASSISTANT_NAME} starting...")
    start_clap_thread()
    speak(f"{ASSISTANT_NAME} is online.")
    app.run(host="127.0.0.1", port=5000, debug=False)
