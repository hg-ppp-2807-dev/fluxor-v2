import re

logs = ["task-24.log", "task-61.log", "task-85.log"]
path = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/tasks/"

for l in logs:
    with open(path + l, "r") as f:
        content = f.read()
    
    reqs_m = re.search(r"http_reqs\.*:\s*(\d+)", content)
    vus_m = re.search(r"vus\.*:\s*(\d+)", content)
    dur_m = re.search(r"iteration_duration\.*: avg=([\d.]+)ms", content)
    if reqs_m:
        print(f"{l}: VUs={vus_m.group(1)}, Reqs={reqs_m.group(1)}")
    else:
        print(f"{l}: No reqs found")
