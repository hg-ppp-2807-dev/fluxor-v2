import json
import re
import csv

log_path = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/logs/transcript_full.jsonl"

text = ""
with open(log_path, "r") as f:
    for line in f:
        data = json.loads(line)
        if "content" in data and isinstance(data["content"], str):
            text += data["content"] + "\n"

# We want to find blocks like:
# LC Normal Trial 1
# - Duration: 90s
# - Requests: 26343
# - Throughput: ...
#
# But wait, let's just use regex to find all the trial results blocks.
pattern = re.compile(
    r"(?i)(RR|LC|RL)\s+(Normal|Spike|Failure)\s+Trial\s+(\d+).*?"
    r"(?:Duration:\s*(\d+)s|Requests:\s*(\d+)|Throughput:\s*([\d.]+)\s*req/s|Average latency:\s*([\d.]+)\s*ms|P95 latency:\s*([\d.]+)\s*ms|Error rate:\s*([\d.]+)%|HTTP Error rate:\s*([\d.]+)%|CPU STD:\s*([\d.]+)%)",
    re.DOTALL
)

# Actually, it's easier to find the k6 summary logs directly if we have them, or my own summary blocks.
# Let's try matching my own summary blocks.
summary_pattern = re.compile(
    r"(RR|LC|RL)\s+(Normal|Spike|Failure)\s+Trial\s+(\d+)[^\n]*\n"
    r"(?:-\s*Duration:\s*\d+s\n)?"
    r"-\s*Requests:\s*(\d+)\n"
    r"-\s*Throughput:\s*([\d.]+)\s*req/s\n"
    r"-\s*Average latency:\s*([\d.]+)\s*ms\n"
    r"-\s*P95 latency:\s*([\d.]+)\s*ms\n"
    r"-\s*(?:HTTP\s*)?Error rate:\s*([\d.]+)%\n"
    r"-\s*CPU STD:\s*([\d.]+)%",
    re.IGNORECASE
)

matches = summary_pattern.findall(text)
seen = set()
unique_matches = []
for m in matches:
    key = (m[0].upper(), m[1].capitalize(), m[2])
    if key not in seen:
        seen.add(key)
        unique_matches.append(m)

with open("results/benchmark_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Algorithm", "Scenario", "Trial", "VUs", "Requests", "Throughput", "Latency_Avg_ms", "Latency_P95_ms", "Error_Rate", "CPU_STD"])
    
    for m in unique_matches:
        alg = m[0].upper()
        scenario = m[1].capitalize()
        trial = m[2]
        reqs = m[3]
        tput = m[4]
        lat_avg = m[5]
        lat_p95 = m[6]
        err = m[7]
        cpu = m[8]
        # Calculate VUs based on scenario
        if scenario == "Normal":
            vus = 50
        elif scenario == "Spike":
            vus = 200 # Assuming max VUs for spike
        elif scenario == "Failure":
            vus = 50
        else:
            vus = 50
        
        writer.writerow([alg, scenario, trial, vus, reqs, tput, lat_avg, lat_p95, err, cpu])
print(f"Extracted {len(unique_matches)} records.")

