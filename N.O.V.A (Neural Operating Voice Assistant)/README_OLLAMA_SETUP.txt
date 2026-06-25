NOVA OLLAMA SETUP

1. Install Ollama for Windows from the official Ollama website.

2. Open CMD and run:
   ollama pull llama3.2:1b

3. Test it:
   ollama run llama3.2:1b

4. Rename .env.example to .env

5. Run NOVA:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py

6. Open:
   http://127.0.0.1:5000

If NOVA cannot connect to Ollama, open another CMD and run:
   ollama serve

Then restart:
   python app.py
