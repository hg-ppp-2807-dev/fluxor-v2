import csv
import math
import os
import signal
import subprocess
import time

running = True
samples = []

def stop(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

containers = ["backend-1", "backend-2", "backend-3"]

print("[MONITOR] Backend CPU monitor started.")
print("[MONITOR] Sampling backend-1, backend-2, backend-3 every 1 second.")
print("[MONITOR] Press Ctrl+C to stop and save results.")

while running:
    try:
        proc = subprocess.run(
            [
                "docker", "stats", "--no-stream",
                "--format", "{{.Name}}|{{.CPUPerc}}",
                *containers
            ],
            capture_output=True,
            text=True,
            timeout=3
        )

        if proc.returncode == 0:
            cpu = {}

            for line in proc.stdout.strip().splitlines():
                parts = line.split("|")
                if len(parts) == 2:
                    name = parts[0]
                    value = parts[1].replace("%", "").strip()

                    try:
                        cpu[name] = float(value)
                    except ValueError:
                        pass

            if all(c in cpu for c in containers):
                values = [cpu[c] for c in containers]

                mean = sum(values) / len(values)
                variance = sum((x - mean) ** 2 for x in values) / len(values)
                stddev = math.sqrt(variance)

                sample = {
                    "timestamp": time.time(),
                    "backend_1_cpu_pct": cpu["backend-1"],
                    "backend_2_cpu_pct": cpu["backend-2"],
                    "backend_3_cpu_pct": cpu["backend-3"],
                    "mean_cpu_pct": mean,
                    "cpu_stddev_pct": stddev
                }

                samples.append(sample)

                print(
                    f"[CPU] B1={values[0]:6.2f}% "
                    f"B2={values[1]:6.2f}% "
                    f"B3={values[2]:6.2f}% "
                    f"STD={stddev:6.2f}%",
                    flush=True
                )

    except Exception as e:
        print(f"[MONITOR] error: {e}", flush=True)

    time.sleep(1)

os.makedirs("scripts/results/cpu", exist_ok=True)

timestamp = time.strftime("%Y%m%d_%H%M%S")
csv_path = f"scripts/results/cpu/backend_cpu_{timestamp}.csv"

with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "timestamp",
            "backend_1_cpu_pct",
            "backend_2_cpu_pct",
            "backend_3_cpu_pct",
            "mean_cpu_pct",
            "cpu_stddev_pct"
        ]
    )
    writer.writeheader()
    writer.writerows(samples)

if samples:
    stddevs = [s["cpu_stddev_pct"] for s in samples]
    means = [s["mean_cpu_pct"] for s in samples]

    print("\n" + "=" * 60)
    print("BACKEND CPU MONITOR SUMMARY")
    print("=" * 60)
    print(f"Samples:             {len(samples)}")
    print(f"Average CPU:         {sum(means)/len(means):.2f}%")
    print(f"Average CPU STDDEV:  {sum(stddevs)/len(stddevs):.2f}%")
    print(f"Peak CPU STDDEV:     {max(stddevs):.2f}%")
    print(f"Saved:               {csv_path}")
    print("=" * 60)
else:
    print("[MONITOR] No samples collected.")
