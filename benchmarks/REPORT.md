# Benchmark Report

Date: 2026-05-15

## What was tested

Yes — multiple benchmark scenarios were executed across different concurrency and payload settings.

Run matrix executed:

1. `clients=10`, `messages=40`, `payload=64B`
2. `clients=10`, `messages=40`, `payload=1024B`
3. `clients=50`, `messages=20`, `payload=64B`
4. `clients=50`, `messages=20`, `payload=1024B`

Transport compared in each run:
- WebSocket (`/ws`)
- HTTP polling (`/poll`)

## Commands used

```bash
python benchmarks/run_benchmark.py --base-url http://127.0.0.1:8000 --clients 10 --messages 40 --payload-size 64 --transport both --output benchmarks/results/c10_p64.json
python benchmarks/run_benchmark.py --base-url http://127.0.0.1:8000 --clients 10 --messages 40 --payload-size 1024 --transport both --output benchmarks/results/c10_p1024.json
python benchmarks/run_benchmark.py --base-url http://127.0.0.1:8000 --clients 50 --messages 20 --payload-size 64 --transport both --output benchmarks/results/c50_p64.json
python benchmarks/run_benchmark.py --base-url http://127.0.0.1:8000 --clients 50 --messages 20 --payload-size 1024 --transport both --output benchmarks/results/c50_p1024.json
```

## Results summary

| Scenario | Transport | Throughput (msg/s) | p50 (ms) | p95 (ms) | p99 (ms) |
|---|---|---:|---:|---:|---:|
| c10, p64B | WebSocket | 2926.15 | 1.048 | 1.445 | 13.219 |
| c10, p64B | HTTP poll | 523.98 | 15.487 | 19.794 | 42.692 |
| c10, p1024B | WebSocket | 2662.56 | 1.616 | 2.586 | 3.058 |
| c10, p1024B | HTTP poll | 494.80 | 16.395 | 22.733 | 46.906 |
| c50, p64B | WebSocket | 3766.71 | 4.760 | 6.212 | 7.108 |
| c50, p64B | HTTP poll | 510.56 | 77.851 | 130.290 | 234.359 |
| c50, p1024B | WebSocket | 3054.21 | 6.593 | 9.656 | 11.711 |
| c50, p1024B | HTTP poll | 543.07 | 75.663 | 92.384 | 246.003 |

## Initial interpretation

- In these local runs, WebSocket outperformed HTTP polling in both latency and throughput.
- The gap widens as concurrency increases (50 clients showed much larger p95/p99 polling latency).
- These are still single-machine, short-duration runs; they are useful directional data but not final production conclusions.

## Next benchmark steps

- Add larger concurrency tiers (100/500 where feasible).
- Repeat each scenario 3+ times and publish mean/stddev.
- Add CPU and memory capture to align with `benchmarks/PLAN.md`.
- Generate plots for p95 latency, throughput, and overhead trends.
