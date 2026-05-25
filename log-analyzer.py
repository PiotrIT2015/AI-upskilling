import ollama
import os

# --- CONFIGURATION ---
LOG_FILE_PATH = "sample.log"  # Path to your log file
MODEL_NAME = "phi3"         # The local model you want to use
CHUNK_SIZE = 50               # Number of log lines to analyze at once

def analyze_log_chunk(chunk):
    prompt = f"""
    You are a senior systems security engineer. 
    Analyze the following log entries for:
    1. Security threats (Brute force, SQL injection, unauthorized access).
    2. Critical system errors or hardware failures.
    3. Anomalies that look suspicious.

    Provide a concise summary. If nothing is wrong, say "No issues detected."

    LOG ENTRIES:
    {chunk}
    """
    
    response = ollama.generate(model=MODEL_NAME, prompt=prompt)
    return response['response']

def main():
    if not os.path.exists(LOG_FILE_PATH):
        print(f"Error: {LOG_FILE_PATH} not found.")
        return

    print(f"--- Starting Analysis on {LOG_FILE_PATH} ---")
    
    with open(LOG_FILE_PATH, "r") as f:
        lines = f.readlines()
        
    # Process the logs in chunks
    for i in range(0, len(lines), CHUNK_SIZE):
        chunk = "".join(lines[i:i + CHUNK_SIZE])
        print(f"\n[Analyzing lines {i} to {i + CHUNK_SIZE}...]")
        
        result = analyze_log_chunk(chunk)
        print("AI ANALYSIS:")
        print(result)
        print("-" * 50)

if __name__ == "__main__":
    main()