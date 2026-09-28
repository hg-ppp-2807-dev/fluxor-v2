#!/bin/bash
set -e

cd ~/fluxor-clean
mkdir -p scripts/results/cpu scripts/results/trials

# ============================================================
# RL
# ============================================================
echo "=== Starting RL Benchmarks ==="
curl -s -X POST http://localhost:8080/admin/algorithm \
  -H 'Content-Type: application/json' \
  -d '{"algorithm":"RL"}'
echo ""

# RL NORMAL
echo "--- RL Normal Trial 1 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rl_normal_cpu_trial1.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=normal scripts/loadtest.js | tee scripts/results/trials/rl_normal_cpu_trial1.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- RL Normal Trial 2 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rl_normal_cpu_trial2.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=normal scripts/loadtest.js | tee scripts/results/trials/rl_normal_cpu_trial2.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- RL Normal Trial 3 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rl_normal_cpu_trial3.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=normal scripts/loadtest.js | tee scripts/results/trials/rl_normal_cpu_trial3.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true


# RL SPIKE
echo "--- RL Spike Trial 1 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rl_spike_cpu_trial1.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=spike scripts/loadtest.js | tee scripts/results/trials/rl_spike_cpu_trial1.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- RL Spike Trial 2 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rl_spike_cpu_trial2.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=spike scripts/loadtest.js | tee scripts/results/trials/rl_spike_cpu_trial2.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- RL Spike Trial 3 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rl_spike_cpu_trial3.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=spike scripts/loadtest.js | tee scripts/results/trials/rl_spike_cpu_trial3.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true


# RL FAILURE
echo "--- RL Failure Trial 1 ---"
(sleep 30; docker compose stop backend-2; sleep 30; docker compose start backend-2) &
FAIL_PID=$!
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rl_failure_cpu_trial1.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=failure scripts/loadtest.js | tee scripts/results/trials/rl_failure_cpu_trial1.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true
wait $FAIL_PID || true

docker compose ps backend-2

echo "--- RL Failure Trial 2 ---"
(sleep 30; docker compose stop backend-2; sleep 30; docker compose start backend-2) &
FAIL_PID=$!
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rl_failure_cpu_trial2.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=failure scripts/loadtest.js | tee scripts/results/trials/rl_failure_cpu_trial2.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true
wait $FAIL_PID || true

docker compose ps backend-2

echo "--- RL Failure Trial 3 ---"
(sleep 30; docker compose stop backend-2; sleep 30; docker compose start backend-2) &
FAIL_PID=$!
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rl_failure_cpu_trial3.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=failure scripts/loadtest.js | tee scripts/results/trials/rl_failure_cpu_trial3.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true
wait $FAIL_PID || true

docker compose ps backend-2


# ============================================================
# RR
# ============================================================
echo "=== Starting RR Benchmarks ==="
curl -s -X POST http://localhost:8080/admin/algorithm \
  -H 'Content-Type: application/json' \
  -d '{"algorithm":"RR"}'
echo ""

# RR NORMAL
echo "--- RR Normal Trial 1 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rr_normal_cpu_trial1.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=normal scripts/loadtest.js | tee scripts/results/trials/rr_normal_cpu_trial1.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- RR Normal Trial 2 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rr_normal_cpu_trial2.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=normal scripts/loadtest.js | tee scripts/results/trials/rr_normal_cpu_trial2.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- RR Normal Trial 3 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rr_normal_cpu_trial3.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=normal scripts/loadtest.js | tee scripts/results/trials/rr_normal_cpu_trial3.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true


# RR SPIKE
echo "--- RR Spike Trial 1 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rr_spike_cpu_trial1.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=spike scripts/loadtest.js | tee scripts/results/trials/rr_spike_cpu_trial1.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- RR Spike Trial 2 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rr_spike_cpu_trial2.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=spike scripts/loadtest.js | tee scripts/results/trials/rr_spike_cpu_trial2.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- RR Spike Trial 3 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rr_spike_cpu_trial3.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=spike scripts/loadtest.js | tee scripts/results/trials/rr_spike_cpu_trial3.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true


# RR FAILURE
echo "--- RR Failure Trial 1 ---"
(sleep 30; docker compose stop backend-2; sleep 30; docker compose start backend-2) &
FAIL_PID=$!
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rr_failure_cpu_trial1.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=failure scripts/loadtest.js | tee scripts/results/trials/rr_failure_cpu_trial1.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true
wait $FAIL_PID || true

docker compose ps backend-2

echo "--- RR Failure Trial 2 ---"
(sleep 30; docker compose stop backend-2; sleep 30; docker compose start backend-2) &
FAIL_PID=$!
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rr_failure_cpu_trial2.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=failure scripts/loadtest.js | tee scripts/results/trials/rr_failure_cpu_trial2.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true
wait $FAIL_PID || true

docker compose ps backend-2

echo "--- RR Failure Trial 3 ---"
(sleep 30; docker compose stop backend-2; sleep 30; docker compose start backend-2) &
FAIL_PID=$!
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/rr_failure_cpu_trial3.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=failure scripts/loadtest.js | tee scripts/results/trials/rr_failure_cpu_trial3.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true
wait $FAIL_PID || true

docker compose ps backend-2


# ============================================================
# LC
# ============================================================
echo "=== Starting LC Benchmarks ==="
curl -s -X POST http://localhost:8080/admin/algorithm \
  -H 'Content-Type: application/json' \
  -d '{"algorithm":"LC"}'
echo ""

# LC NORMAL
echo "--- LC Normal Trial 1 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/lc_normal_cpu_trial1.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=normal scripts/loadtest.js | tee scripts/results/trials/lc_normal_cpu_trial1.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- LC Normal Trial 2 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/lc_normal_cpu_trial2.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=normal scripts/loadtest.js | tee scripts/results/trials/lc_normal_cpu_trial2.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- LC Normal Trial 3 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/lc_normal_cpu_trial3.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=normal scripts/loadtest.js | tee scripts/results/trials/lc_normal_cpu_trial3.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true


# LC SPIKE
echo "--- LC Spike Trial 1 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/lc_spike_cpu_trial1.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=spike scripts/loadtest.js | tee scripts/results/trials/lc_spike_cpu_trial1.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- LC Spike Trial 2 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/lc_spike_cpu_trial2.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=spike scripts/loadtest.js | tee scripts/results/trials/lc_spike_cpu_trial2.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true

echo "--- LC Spike Trial 3 ---"
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/lc_spike_cpu_trial3.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=spike scripts/loadtest.js | tee scripts/results/trials/lc_spike_cpu_trial3.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true


# LC FAILURE
echo "--- LC Failure Trial 1 ---"
(sleep 30; docker compose stop backend-2; sleep 30; docker compose start backend-2) &
FAIL_PID=$!
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/lc_failure_cpu_trial1.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=failure scripts/loadtest.js | tee scripts/results/trials/lc_failure_cpu_trial1.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true
wait $FAIL_PID || true

docker compose ps backend-2

echo "--- LC Failure Trial 2 ---"
(sleep 30; docker compose stop backend-2; sleep 30; docker compose start backend-2) &
FAIL_PID=$!
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/lc_failure_cpu_trial2.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=failure scripts/loadtest.js | tee scripts/results/trials/lc_failure_cpu_trial2.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true
wait $FAIL_PID || true

docker compose ps backend-2

echo "--- LC Failure Trial 3 ---"
(sleep 30; docker compose stop backend-2; sleep 30; docker compose start backend-2) &
FAIL_PID=$!
python3 scripts/monitor_backend_cpu.py > scripts/results/cpu/lc_failure_cpu_trial3.log 2>&1 &
MON_PID=$!
k6 run -e SCENARIO=failure scripts/loadtest.js | tee scripts/results/trials/lc_failure_cpu_trial3.txt
kill -INT $MON_PID; wait $MON_PID 2>/dev/null || true
wait $FAIL_PID || true


# ============================================================
# FINAL HEALTH CHECK
# ============================================================
echo "=== Final Health Check ==="
docker compose ps

echo ""
echo "=============================================="
echo "ALL 27 CPU BENCHMARKS COMPLETED"
echo "=============================================="

find scripts/results/cpu -type f | sort
