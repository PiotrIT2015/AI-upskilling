import subprocess
import time
import ollama
import re
import platform

# --- CONFIGURATION ---
MODEL = "phi3"

# Detect OS and choose proper log source
if platform.system() == "Windows":
    # Windows Security Log monitoring
    LOG_COMMAND = [
        "powershell",
        "-Command",
        """
        Get-WinEvent -LogName Security |
        Select-Object -First 20 |
        ForEach-Object { $_.Message }
        """
    ]
else:
    # Linux systemd SSH logs
    LOG_COMMAND = ["journalctl", "-u", "ssh", "-n", "0", "-f"]

# Patterns that trigger an AI review
SUSPICIOUS_PATTERNS = [
    r"Failed password",
    r"Invalid user",
    r"Connection closed by authenticating user",
    r"Did not receive identification string",
    r"failure",
    r"failed",
    r"logon failure",
    r"unknown user"
]

def ask_ai_about_anomaly(log_buffer):
    """Sends the captured log burst to the local AI for judgment."""
    
    context = "\n".join(log_buffer)

    prompt = f"""
SYSTEM: You are an automated SSH intrusion detection assistant.

TASK:
Analyze the following logs and determine whether this looks like:
- brute force attack
- suspicious login activity
- credential stuffing
- or normal behavior

LOG DATA:
{context}

QUESTIONS:
1. Is this an attack? (Yes/No)
2. What is the source IP if visible?
3. Risk score 1-10
4. One-sentence explanation

Respond concisely.
"""

    try:
        response = ollama.generate(
            model=MODEL,
            prompt=prompt
        )

        return response["response"]

    except Exception as e:
        return f"AI Error: {e}"

def main():

    print(f"--- SSH Anomaly Detector Started (Model: {MODEL}) ---")
    print(f"--- Platform Detected: {platform.system()} ---")

    try:
        proc = subprocess.Popen(
            LOG_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    except FileNotFoundError as e:
        print(f"[ERROR] Cannot start log monitor: {e}")
        return

    buffer = []
    last_trigger_time = time.time()

    try:

        for line in proc.stdout:

            line = line.strip()

            if not line:
                continue

            print(f"[LOG] {line}")

            # Check suspicious patterns
            if any(re.search(pattern, line, re.IGNORECASE)
                   for pattern in SUSPICIOUS_PATTERNS):

                print(f"[!] Suspicious Activity Detected")

                buffer.append(line)
                last_trigger_time = time.time()

            # Analyze burst after inactivity
            if len(buffer) > 0 and (time.time() - last_trigger_time > 5):

                print("\n[AI ANALYZING BURST...]")

                analysis = ask_ai_about_anomaly(buffer)

                print("\n--- AI REPORT ---")
                print(analysis)
                print("-----------------\n")

                buffer = []

    except KeyboardInterrupt:

        print("\nStopping detector...")
        proc.terminate()

    except Exception as e:

        print(f"[ERROR] Runtime error: {e}")

if __name__ == "__main__":
    main()