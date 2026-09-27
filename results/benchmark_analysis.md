# FLUXOR Benchmark Analysis

## Experimental Setup

FLUXOR was evaluated using three load-balancing algorithms:

- Round Robin (RR)
- Least Connections (LC)
- Reinforcement Learning (RL)

Three scenarios were evaluated:

- Normal workload
- Spike workload
- Failure workload

Each algorithm-scenario combination was evaluated across three trials.

The measured metrics were:

- Throughput (requests/second)
- Average latency (ms)
- P95 latency (ms)
- HTTP error rate (%)
- CPU utilization standard deviation (%)

## Aggregate Results

| Algorithm | Scenario | Throughput (req/s) | Avg Latency (ms) | P95 Latency (ms) | Error Rate (%) | CPU STD (%) |
|---|---|---:|---:|---:|---:|---:|
| RR | Normal | 284.89 | 74.80 ± 0.61 | 98.79 ± 0.97 | 0.00 | 2.27 ± 0.07 |
| RR | Spike | 813.26 | 72.49 ± 0.21 | 96.00 ± 0.89 | 0.00 | 2.03 ± 0.03 |
| RR | Failure | 286.99 | 73.60 ± 1.55 | 99.01 ± 1.41 | 0.43 | 2.00 ± 0.04 |
| LC | Normal | 285.47 | 74.51 ± 1.59 | 99.21 ± 0.34 | 0.00 | 1.96 ± 0.14 |
| LC | Spike | 813.42 | 72.44 ± 1.67 | 97.33 ± 1.65 | 0.00 | 2.03 ± 0.06 |
| LC | Failure | 288.82 | 72.49 ± 0.64 | 99.79 ± 1.50 | 0.63 | 2.20 ± 0.15 |
| RL | Normal | 288.36 | 72.75 ± 0.62 | 95.29 ± 1.82 | 0.00 | 2.28 ± 0.08 |
| RL | Spike | 420.26 | 235.41 ± 22.77 | 581.32 ± 3.49 | 0.00 | 2.12 ± 0.11 |
| RL | Failure | 292.30 | 70.54 ± 2.49 | 96.21 ± 2.27 | 0.08 | 2.43 ± 0.30 |

## Normal Workload

Under the normal workload, RL achieved:

- 288.36 requests/s throughput
- 72.75 ms average latency
- 95.29 ms P95 latency
- 0.00% HTTP error rate
- 2.28% CPU standard deviation

The corresponding RR measurements were 284.89 requests/s, 74.80 ms average latency, and 98.79 ms P95 latency.

Compared with RR, RL reduced average latency by approximately 2.74% and P95 latency by approximately 3.54%.

RL also achieved slightly higher throughput than RR and LC in the normal workload.

## Spike Workload

The spike workload produced a substantially different result.

RL achieved:

- 420.26 requests/s throughput
- 235.41 ms average latency
- 581.32 ms P95 latency
- 0.00% HTTP error rate
- 2.12% CPU standard deviation

RR and LC both maintained approximately 813 requests/s throughput with average latency near 72 ms.

Therefore, the RL implementation exhibited significantly higher latency and lower throughput during the spike workload.

The three RL spike trials consistently showed this behavior, indicating that the result is not attributable to a single anomalous trial.

This identifies spike handling as the primary performance limitation of the current RL implementation.

## Failure Workload

During the failure workload, RL achieved:

- 292.30 requests/s throughput
- 70.54 ms average latency
- 96.21 ms P95 latency
- 0.08% HTTP error rate
- 2.43% CPU standard deviation

RL had lower average latency and P95 latency than both RR and LC in these trials.

The measured RL error rate was also lower than the corresponding RR and LC measurements.

These results indicate that the current RL policy can continue routing requests under the tested failure workload without a large increase in latency.

## CPU Load Distribution

CPU utilization standard deviation remained close to 2% across the evaluated configurations.

The measurements were:

- RR: approximately 2.00–2.27%
- LC: approximately 1.96–2.20%
- RL: approximately 2.12–2.43%

Therefore, the current experiments do not demonstrate a large load-balancing advantage for RL based solely on CPU standard deviation.

The CPU STD metric should consequently be reported as an observed measurement rather than as evidence of a major improvement.

## Overall Findings

The benchmark results show that the effectiveness of the current RL policy depends on workload characteristics.

For normal traffic, RL produced modest latency improvements and slightly higher throughput.

For the tested failure scenario, RL also maintained comparatively low latency and error rate.

However, under the spike workload, RL performance degraded substantially compared with RR and LC. The high P95 latency indicates that the current policy does not respond effectively enough to rapidly increasing request demand.

The results therefore support further investigation of the RL policy's spike-response behavior, including state representation, action selection, reward behavior, and training dynamics.

## Important Result Interpretation

The benchmark results should not be presented as evidence that RL universally outperforms traditional load-balancing algorithms.

The experiments instead demonstrate workload-dependent behavior:

- RL performs competitively under normal workload.
- RL performs competitively under the tested failure workload.
- RL currently performs poorly under the tested spike workload.
- CPU standard deviation remains similar across the three algorithms.

The spike result is particularly important for future improvements to FLUXOR.

