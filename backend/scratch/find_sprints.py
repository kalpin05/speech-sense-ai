import json
import sys

# Ensure stdout encodes to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

logfile = r"C:\Users\anujn\.gemini\antigravity\brain\92ed4b46-f6d1-4446-9ae3-d041efc01c7b\.system_generated\logs\transcript.jsonl"

with open(logfile, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        content = data.get("content", "")
        if "ROADMAP" in content or "Sprint" in content:
            # Print steps with mentions of Sprint or ROADMAP
            print(f"--- Step {data.get('step_index')} ({data.get('source')}) ---")
            lines = content.split("\n")
            for l in lines:
                if any(k in l for k in ["ROADMAP", "Sprint 1", "Sprint 2", "Sprint 3", "Sprint 4", "Sprint 5", "Sprint 6", "Sprint 7"]):
                    print(l)
