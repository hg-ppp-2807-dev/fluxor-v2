import json
import re
import csv

log_path = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/logs/transcript_full.jsonl"
text = ""

with open(log_path, "r") as f:
    for line in f:
        data = json.loads(line)
        if data["type"] == "PLANNER_RESPONSE":
            thinking = data.get("thinking", "")
            content = data.get("content", "")
            text += thinking + "\n" + content + "\n"

# Match patterns like:
# Results for LC Normal Trial 3:
# - Requests: 25938
# - Throughput: 287.63 req/s
# - Average latency: 73.16 ms
# - Error rate: 0.47%
# - CPU STD: 2.36%

pattern = re.compile(
    r"(?:Results for|Results:|Trial|For)\s*(RR|LC|RL)\s+(Normal|Spike|Failure)\s*(?:Trial)?\s*(\d+).*?\n"
    r"(?:.*?-\s*Duration.*?s\n)?"
    r".*?-\s*Requests:\s*(\d+)\n"
    r".*?-\s*Throughput:\s*([\d.]+)\s*req/s\n"
    r".*?-\s*Average latency:\s*([\d.]+)\s*ms\n"
    r".*?-\s*P95 latency:\s*([\d.]+)\s*ms\n"
    r".*?-\s*(?:HTTP\s*)?Error rate:\s*([\d.]+)%\n"
    r".*?-\s*CPU STD:\s*([\d.]+)%",
    re.IGNORECASE | re.DOTALL
)

# This pattern is too strict, let's just use regex to find all "Requests: XXX", "CPU STD: YYY" around the keywords "LC Normal Trial 3"

blocks = re.split(r"(RR|LC|RL)\s+(Normal|Spike|Failure)\s+(?:Trial\s+)?(\d+)", text, flags=re.IGNORECASE)

print(f"Split into {len(blocks)} blocks.")
# ... it's too complex to write regex blindly. Let's just find the exact text around "RR Failure" etc.
