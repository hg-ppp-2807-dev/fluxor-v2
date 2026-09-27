import re

logs = ["task-24.log", "task-61.log", "task-85.log"]
path = "/Users/pritampriyabratapalai/.gemini/antigravity-ide/brain/8ac70b77-f98f-457c-83be-e695bcf3338d/.system_generated/tasks/"

for l in logs:
    with open(path + l, "r") as f:
        content = f.read()
    
    vus_m = re.search(r"vus_max\.*:\s*(\d+)", content)
    if vus_m:
        print(f"{l}: Max VUs={vus_m.group(1)}")
