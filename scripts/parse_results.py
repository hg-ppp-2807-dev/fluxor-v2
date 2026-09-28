import re
import sys
import os

scenarios = {
    'RR Normal': ('scripts/results/rr_normal_k6.log', 'scripts/results/rr_normal_cpu.log'),
    'RR Failure': ('scripts/results/rr_failure_k6.log', 'scripts/results/rr_failure_cpu.log'),
    'LC Normal': ('scripts/results/lc_normal_k6.log', 'scripts/results/lc_normal_cpu.log'),
    'LC Failure': ('scripts/results/lc_failure_k6.log', 'scripts/results/lc_failure_cpu.log'),
}

print(f"{'Algorithm | Scenario':<25} | {'Requests':<8} | {'Throughput':<15} | {'Avg Latency':<12} | {'Median':<10} | {'P90':<10} | {'P95':<10} | {'Max':<10} | {'Error Rate':<12} | {'CPU STD':<10}")
print("-" * 145)

for name, (k6_file, cpu_file) in scenarios.items():
    if not os.path.exists(k6_file) or not os.path.exists(cpu_file):
        print(f"Missing logs for {name}")
        continue
        
    k6_data = open(k6_file, 'r').read()
    cpu_data = open(cpu_file, 'r').read()
    
    # Extract k6 metrics
    # http_req_duration..............: avg=60.11ms  min=24.91ms  med=59.82ms  max=170.65ms p(90)=79.88ms  p(95)=84.38ms 
    dur_match = re.search(r'http_req_duration\.*:\s*avg=([^\s]+)\s+min=[^\s]+\s+med=([^\s]+)\s+max=([^\s]+)\s+p\(90\)=([^\s]+)\s+p\(95\)=([^\s]+)', k6_data)
    
    # http_reqs......................: 70208  875.830614/s
    reqs_match = re.search(r'http_reqs\.*:\s*(\d+)\s+([^\s]+)/s', k6_data)
    
    # http_req_failed................: 1.62%  450 out of 27699
    # http_req_failed................: 0.00%  0 out of 18564
    fail_match = re.search(r'http_req_failed\.*:\s*([^\s]+)', k6_data)
    
    # Extract CPU metrics
    std_values = re.findall(r'STD:\s+([0-9\.]+)%', cpu_data)
    if std_values:
        avg_std = sum(float(x) for x in std_values) / len(std_values)
        cpu_str = f"{avg_std:.2f}%"
    else:
        cpu_str = "N/A"
        
    if dur_match and reqs_match and fail_match:
        avg, med, mx, p90, p95 = dur_match.groups()
        reqs, tput = reqs_match.groups()
        err = fail_match.group(1)
        
        tput_fmt = f"{float(tput):.2f} req/s"
        
        algo, scen = name.split(' ', 1)
        
        print(f"{name:<25} | {reqs:<8} | {tput_fmt:<15} | {avg:<12} | {med:<10} | {p90:<10} | {p95:<10} | {mx:<10} | {err:<12} | {cpu_str:<10}")
    else:
        print(f"Could not parse metrics for {name}")
