import json

log_path = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/logs/transcript.jsonl"

with open(log_path, "r") as f:
    for line in f:
        data = json.loads(line)
        
        # look for tool calls
        if "tool_calls" in data:
            for tc in data["tool_calls"]:
                name = tc.get("toolName", "")
                action = tc.get("toolAction", "")
                args = tc.get("Arguments", {})
                if name == "run_command":
                    cmd = args.get("CommandLine", "")
                    if "k6 run" in cmd:
                        print(f"K6: {action} | Cmd: {cmd}")
                    elif "admin/algorithm" in cmd:
                        print(f"ALGO: {action} | Cmd: {cmd}")
                    elif "loadtest.js" in cmd and "sed" in cmd:
                        print(f"SCENARIO CHANGE: {action} | Cmd: {cmd}")
                    elif "failureOptions" in action or "failureOptions" in cmd:
                        print(f"SCENARIO CHANGE: {action} | Cmd: {cmd}")

