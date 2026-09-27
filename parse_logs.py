import os
import re
import csv

log_dir = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/tasks/"

k6_logs = []
cpu_logs = []

for file in os.listdir(log_dir):
    if not file.endswith(".log"):
        continue
    filepath = os.path.join(log_dir, file)
    mtime = os.path.getmtime(filepath)
    with open(filepath, "r") as f:
        content = f.read()
        
    if "http_reqs" in content and "http_req_duration" in content:
        # It's a k6 log
        reqs_m = re.search(r"http_reqs\.*:\s*(\d+)\s+([\d.]+)/s", content)
        lat_m = re.search(r"http_req_duration\.*:\s*avg=([\d.]+)ms.*p\(95\)=([\d.]+)ms", content)
        if not lat_m:
             lat_m = re.search(r"http_req_duration\.*:\s*avg=([\d.]+)s.*p\(95\)=([\d.]+)s", content) # maybe seconds
        err_m = re.search(r"http_req_failed\.*:\s*([\d.]+)%", content)
        
        reqs = reqs_m.group(1) if reqs_m else "0"
        tput = reqs_m.group(2) if reqs_m else "0"
        lat_avg = lat_m.group(1) if lat_m else "0"
        lat_p95 = lat_m.group(2) if lat_m else "0"
        err = err_m.group(1) if err_m else "0"
        
        k6_logs.append({
            "time": mtime,
            "reqs": reqs,
            "tput": tput,
            "lat_avg": lat_avg,
            "lat_p95": lat_p95,
            "err": err,
            "file": file
        })
    elif "Average CPU STD:" in content:
        # It's a CPU log
        cpu_m = re.search(r"Average CPU STD:\s*([\d.]+)%", content)
        cpu = cpu_m.group(1) if cpu_m else "0"
        cpu_logs.append({
            "time": mtime,
            "cpu": cpu,
            "file": file
        })

k6_logs.sort(key=lambda x: x["time"])
cpu_logs.sort(key=lambda x: x["time"])

print(f"Found {len(k6_logs)} k6 logs and {len(cpu_logs)} cpu logs")

trials_sequence = [
    ("RL", "Normal", 1), ("RL", "Normal", 2), ("RL", "Normal", 3),
    ("RL", "Spike", 1), ("RL", "Spike", 2), ("RL", "Spike", 3),
    ("LC", "Normal", 1), ("LC", "Normal", 2), ("LC", "Normal", 3),
    ("LC", "Spike", 1), ("LC", "Spike", 2), ("LC", "Spike", 3),
    ("LC", "Failure", 1), ("LC", "Failure", 2), ("LC", "Failure", 3),
    ("RR", "Normal", 1), ("RR", "Normal", 2), ("RR", "Normal", 3),
    ("RR", "Spike", 1), ("RR", "Spike", 2), ("RR", "Spike", 3),
    ("RR", "Failure", 1), ("RR", "Failure", 2), ("RR", "Failure", 3),
    ("RL", "Failure", 1), ("RL", "Failure", 2), ("RL", "Failure", 3)
]

with open("results/benchmark_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Algorithm", "Scenario", "Trial", "VUs", "Requests", "Throughput", "Latency_Avg_ms", "Latency_P95_ms", "Error_Rate", "CPU_STD"])
    
    for i in range(min(len(trials_sequence), len(k6_logs), len(cpu_logs))):
        alg, scenario, trial = trials_sequence[i]
        k6 = k6_logs[i]
        cpu = cpu_logs[i]
        
        if scenario == "Normal":
            vus = 50
        elif scenario == "Spike":
            vus = 200
        else:
            vus = 50
            
        writer.writerow([alg, scenario, trial, vus, k6["reqs"], k6["tput"], k6["lat_avg"], k6["lat_p95"], k6["err"], cpu["cpu"]])

print("CSV generated!")
