import json
import statistics
import time
import urllib.request

URL = "http://localhost:8080/admin/status"
samples = []

print("Monitoring CPU... Press Ctrl+C after the load test finishes.")

try:
    while True:
        try:
            with urllib.request.urlopen(URL, timeout=2) as response:
                data = json.load(response)

            cpus = [server["cpu"] for server in data["servers"]]

            if len(cpus) == 3:
                cpu_std = statistics.pstdev(cpus)

                samples.append({
                    "timestamp": time.time(),
                    "cpu_1": cpus[0],
                    "cpu_2": cpus[1],
                    "cpu_3": cpus[2],
                    "cpu_std": cpu_std
                })

                print(
                    f"CPU: {cpus[0]:6.2f}% | "
                    f"{cpus[1]:6.2f}% | "
                    f"{cpus[2]:6.2f}% | "
                    f"STD: {cpu_std:6.2f}%"
                )

        except Exception as e:
            print(f"Monitoring error: {e}")

        time.sleep(1)

except KeyboardInterrupt:
    pass

if samples:
    output = "scripts/results/cpu_samples.json"

    with open(output, "w") as f:
        json.dump(samples, f, indent=2)

    avg_std = statistics.mean(sample["cpu_std"] for sample in samples)

    print("\nMonitoring stopped.")
    print(f"Samples: {len(samples)}")
    print(f"Average CPU STD: {avg_std:.2f}%")
    print(f"Saved: {output}")
else:
    print("\nNo CPU samples collected.")
