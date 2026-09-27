import json

log_path = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/logs/transcript.jsonl"

with open(log_path, "r") as f:
    for line in f:
        data = json.loads(line)
        if "tool_calls" in data:
            for tc in data["tool_calls"]:
                name = tc.get("name") or tc.get("toolName")
                if name == "run_command":
                    args = tc.get("args") or tc.get("Arguments")
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except:
                            pass
                    if isinstance(args, dict):
                        cmd = args.get("CommandLine", "")
                        action = args.get("toolAction", "")
                        if "admin/algorithm" in cmd:
                            print(f"ALGO CHANGE: {action} | Cmd: {cmd}")
