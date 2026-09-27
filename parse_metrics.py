import os
import re

tasks = [
    ("RL Spike 2", "task-24"),
    ("RL Spike 3", "task-61"),
    ("LC Normal 1", "task-85"),
    ("LC Normal 2", "task-102"),
    ("LC Normal 3", "task-118"),
    ("LC Spike 1", "task-137"),
    ("LC Spike 2", "task-154"),
    ("LC Spike 3", "task-170"),
    ("LC Failure 1", "task-196"),
    ("LC Failure 2", "task-218"),
    ("LC Failure 3", "task-240"),
    ("RR Normal 1", "task-266"),
    ("RR Normal 2", "task-280"),
    ("RR Normal 3", "task-294"),
    ("RR Spike 1", "task-309"),
    ("RR Spike 2", "task-323"),
    ("RR Spike 3", "task-337"),
    ("RR Failure 1", "task-352"),
    ("RR Failure 2", "task-377"),
    ("RR Failure 3", "task-399"),
    ("RL Failure 1", "task-422"),
    ("RL Failure 2", "task-444"),
    ("RL Failure 3", "task-466")
]

cpus = [
    "task-18", "task-55", "task-82", "task-99", "task-115",
    "task-134", "task-151", "task-167", "task-193", "task-217",
    "task-239", "task-265", "task-279", "task-293", "task-308",
    "task-322", "task-336", "task-351", "task-376", "task-398",
    "task-421", "task-443", "task-465"
]

path = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/tasks/"

for i, (trial_name, k6_task) in enumerate(tasks):
    cpu_task = cpus[i]
    
    with open(path + k6_task + ".log", "r") as f:
        content = f.read()
    
    reqs_m = re.search(r"http_reqs\.*:\s*(\d+)\s+([\d.]+)/s", content)
    lat_m = re.search(r"http_req_duration\.*:\s*avg=([\d.]+)ms.*p\(95\)=([\d.]+)ms", content)
    if not lat_m:
         lat_m = re.search(r"http_req_duration\.*:\s*avg=([\d.]+)s.*p\(95\)=([\d.]+)s", content)
    err_m = re.search(r"http_req_failed\.*:\s*([\d.]+)%", content)
    
    reqs = reqs_m.group(1) if reqs_m else "0"
    tput = reqs_m.group(2) if reqs_m else "0"
    lat_avg = lat_m.group(1) if lat_m else "0"
    lat_p95 = lat_m.group(2) if lat_m else "0"
    err = err_m.group(1) if err_m else "0"
    
    with open(path + cpu_task + ".log", "r") as f:
        cpu_content = f.read()
    
    cpu_m = re.search(r"Average CPU STD:\s*([\d.]+)%", cpu_content)
    cpu = cpu_m.group(1) if cpu_m else "0"
    
    alg, scen, tr = trial_name.split(" ")
    vus = 200 if scen == "Spike" else 50
    print(f"{alg},{scen},{tr},{vus},{reqs},{tput},{lat_avg},{lat_p95},{err},{cpu}")

