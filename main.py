import sys
import subprocess
import time
import urllib.request
from core.agent import Agent

def is_ollama_running():
    try:
        urllib.request.urlopen("http://localhost:11434/", timeout=1)
        return True
    except Exception:
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: ai <command>")
        return

    prompt = " ".join(sys.argv[1:])

    # 1. Instant Stop
    if prompt.strip().lower() == "stop":
        print("🛑 Stopping Ollama background service...")
        subprocess.run("pkill -f 'ollama serve'", shell=True)
        subprocess.run("sudo systemctl stop ollama 2>/dev/null", shell=True)
        print("✅ Ollama is completely stopped.")
        return

    # 2. Auto-Start
    if not is_ollama_running():
        print("🚀 Waking up Ollama in the background...")
        subprocess.Popen("OLLAMA_MODELS='/usr/share/ollama/.ollama/models' ollama serve > /dev/null 2>&1 &", shell=True)
        time.sleep(2)

    # 3. Run the Smart Agent
    agent = Agent()
    result = agent.chat(prompt)

    if result:
        print(result)

if __name__ == "__main__":
    main()
