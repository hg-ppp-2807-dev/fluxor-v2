import json
import re

log_path = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/logs/transcript_full.jsonl"

tasks = []

with open(log_path, "r") as f:
    for line in f:
        data = json.loads(line)
        if data["type"] == "PLANNER_RESPONSE" and "tool_calls" in data:
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
                        if "k6 run" in cmd:
                            tasks.append({"action": action})
        elif data["type"] == "RUN_COMMAND" and data["status"] == "RUNNING":
            content = data.get("content", "")
            if "k6 run scripts/loadtest.js" in content:
                m = re.search(r"task id:\s*([^\s]+)\n", content)
                if m:
                    task_id = m.group(1).split("/")[-1]
                    if len(tasks) > 0 and "task_id" not in tasks[-1]:
                        tasks[-1]["task_id"] = task_id

for i, t in enumerate(tasks):
    print(f"{i+1}. Action: {t.get('action')}, Task: {t.get('task_id')}")

