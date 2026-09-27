import json
import re
import os

log_path = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/logs/transcript.jsonl"

algo = "rl" # Assumed initial
events = []

with open(log_path, "r") as f:
    for line in f:
        data = json.loads(line)
        if "tool_calls" in data:
            for tc in data["tool_calls"]:
                name = tc.get("name") or tc.get("toolName")
                if name == "run_command":
                    args = tc.get("args") or tc.get("Arguments")
                    if isinstance(args, str):
                        try: args = json.loads(args)
                        except: pass
                    if isinstance(args, dict):
                        cmd = args.get("CommandLine", "")
                        action = args.get("toolAction", "")
                        
                        if "admin/algorithm" in cmd:
                            m = re.search(r'"algorithm":"(rl|lc|rr)"', cmd)
                            if m:
                                algo = m.group(1)
                                events.append({"type": "algo", "algo": algo})
        
        elif data.get("type") == "RUN_COMMAND" and data.get("status") == "RUNNING":
            content = data.get("content", "")
            if "k6 run scripts/loadtest.js" in content:
                m = re.search(r"task id:\s*([^\s]+)\n", content)
                if m:
                    task_id = m.group(1).split("/")[-1]
                    events.append({"type": "k6", "task_id": task_id, "algo": algo})

print(f"Total events: {len(events)}")
for e in events:
    if e["type"] == "k6":
        print(f"K6 Task: {e['task_id']}, Algo: {e['algo']}")
    else:
        print(f"ALGO CHANGE: {e['algo']}")

