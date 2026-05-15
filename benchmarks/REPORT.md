# Benchmark Report (Initial Smoke Run)

Date: 2026-05-15

This is an initial local smoke benchmark to validate the benchmark harness and provide first-pass numbers.

## Command

```bash
python benchmarks/run_benchmark.py --base-url http://127.0.0.1:8000 --clients 5 --messages 5 --payload-size 64 --transport both --output benchmarks/results/smoke.json
```

## Results (from `benchmarks/results/smoke.json`)

- WebSocket:
  - throughput: 420.37 msg/s
  - latency: p50 0.643 ms, p95 0.984 ms, p99 0.989 ms, mean 0.691 ms
- HTTP polling:
  - throughput: 154.84 msg/s
  - latency: p50 8.358 ms, p95 21.26 ms, p99 24.001 ms, mean 11.155 ms

## Notes

- These numbers are from a small local run and are not statistically stable enough for final conclusions.
- Next step: run matrix in `benchmarks/PLAN.md` (10/100/500 clients, multiple payload sizes, repeated runs) and aggregate means/stddev.
