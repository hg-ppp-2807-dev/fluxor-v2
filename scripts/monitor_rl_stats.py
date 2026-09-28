import json
import os
import re
import signal
import subprocess
import sys
import time

samples = []
running = True

def handle_sig(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, handle_sig)
signal.signal(signal.SIGTERM, handle_sig)

print("[MONITOR] Starting RL container stats monitor (CPU, MEM, PIDs)...")

while running:
    try:
        proc = subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "{{.CPUPerc}}|{{.MemUsage}}|{{.PIDs}}", "rl-agent"],
            capture_output=True,
            text=True,
            timeout=3
        )
        if proc.returncode == 0:
            out = proc.stdout.strip()
            parts = out.split("|")
            if len(parts) == 3:
                cpu_str = parts[0].replace("%", "").strip()
                mem_str = parts[1].strip()
                pids_str = parts[2].strip()
                try:
                    cpu_val = float(cpu_str)
                    pids_val = int(pids_str)
                    sample = {
                        "timestamp": time.time(),
                        "cpu_pct": cpu_val,
                        "mem": mem_str,
                        "pids": pids_val
                    }
                    samples.append(sample)
                    print(f"[RL-AGENT] CPU: {cpu_val:6.2f}% | MEM: {mem_str} | PIDs: {pids_val}", flush=True)
                except ValueError:
                    pass
    except Exception as e:
        print(f"[MONITOR] error: {e}", flush=True)

    time.sleep(1)

os.makedirs("scripts/results", exist_ok=True)
output_path = "scripts/results/rl_diagnostic_cpu.json"
with open(output_path, "w") as f:
    json.dump(samples, f, indent=2)

if samples:
    cpus = [s["cpu_pct"] for s in samples]
    pids = [s["pids"] for s in samples]
    print("\n" + "="*50)
    print("=== RL AGENT RESOURCE MONITOR SUMMARY ===")
    print(f"Total Samples: {len(samples)}")
    print(f"Average CPU:   {sum(cpus)/len(cpus):.2f}%")
    print(f"Peak CPU:      {max(cpus):.2f}%")
    print(f"Min CPU:       {min(cpus):.2f}%")
    print(f"PIDs (threads): avg={sum(pids)/len(pids):.1f}, min={min(pids)}, max={max(pids)}")
    print("="*50)
else:
    print("\n[MONITOR] No samples collected.")
