# WebSocket vs HTTP Benchmark Plan

This document defines a reproducible benchmark plan for comparing WebSocket and HTTP in practical scenarios. The goal is to quantify where WebSocket is a clear win and where it can be overkill.

## 1) Objective

Measure tradeoffs across transport options for latency, throughput, resource usage, and network overhead:

- WebSocket (bidirectional, persistent)
- HTTP polling (request/response, periodic)
- Optional: SSE (server-to-client stream baseline)

## 2) Core Questions

1. At what update frequency does WebSocket materially beat HTTP polling?
2. How much overhead does polling add at different concurrency levels?
3. For one-way notification workloads, is WebSocket worth the operational complexity?
4. What are the p95/p99 latency and CPU costs per transport?

## 3) Scenarios

### Scenario A: Low-frequency notifications
- Pattern: server pushes/serves updates ~1 every 30 seconds per client.
- Real-world analog: product alerts, occasional status updates.
- Hypothesis: polling or SSE is often enough; WebSocket may be overkill.

### Scenario B: Medium interactivity
- Pattern: ~1-2 updates per second.
- Real-world analog: dashboard counters, lightweight collaboration.
- Hypothesis: mixed outcome depending on concurrency and latency target.

### Scenario C: High-frequency realtime
- Pattern: 10-50 updates per second.
- Real-world analog: multiplayer events, telemetry streams.
- Hypothesis: WebSocket should outperform polling in latency and overhead.

### Scenario D: Bidirectional chat/collab
- Pattern: clients send + receive events continuously.
- Real-world analog: chat rooms, collaborative text/cursors.
- Hypothesis: WebSocket is preferred due to full duplex behavior.

## 4) Test Matrix

### Concurrency levels
- 10 clients
- 100 clients
- 500 clients (or highest stable level in local environment)

### Payload sizes
- 64 bytes
- 1 KB
- 8 KB

### Transport variants
- HTTP polling: intervals of 1s, 5s, 30s
- WebSocket
- Optional SSE in one-way scenarios

## 5) Metrics

For each run, collect:

1. **Latency**
   - p50, p95, p99 end-to-end latency (ms)
2. **Throughput**
   - successful messages per second
3. **CPU**
   - average and peak CPU% of server process
4. **Memory**
   - average and peak RSS memory
5. **Network overhead**
   - total bytes transferred / useful payload bytes
6. **Connection behavior**
   - connection setup time
   - reconnect count
7. **Reliability**
   - timeouts
   - failed/dropped messages

## 6) Methodology

- Run all tests on the same machine/environment.
- Warm-up: 30-60 seconds per case.
- Measurement window: 3-5 minutes per case.
- Repeat each case 3 times.
- Report mean, standard deviation, min, max.
- Persist raw run outputs as CSV/JSON under `protocols/websocket/protocols/websocket/benchmarks/results/`.

## 7) Suggested Output Artifacts

- `protocols/websocket/protocols/websocket/benchmarks/results/*.csv` raw measurements
- `protocols/websocket/protocols/websocket/benchmarks/results/*.json` metadata and summary stats
- `protocols/websocket/protocols/websocket/benchmarks/plots/*.png` generated charts
- `protocols/websocket/protocols/websocket/benchmarks/REPORT.md` benchmark findings + interpretation

## 8) Visualizations

Create these charts for blog/tutorial readability:

1. Latency CDF by transport and scenario
2. p95 latency bar chart by concurrency
3. CPU usage vs message rate
4. Network overhead ratio by transport
5. Decision heatmap (best transport by workload profile)

## 9) Decision Rules (to derive from data)

After benchmarks are run, document explicit guidance such as:

- Low-frequency, one-way updates: prefer HTTP polling or SSE.
- Medium-frequency workloads: choose based on p95 latency target and infra complexity.
- High-frequency or bidirectional workloads: prefer WebSocket.

Do not hardcode final recommendations before collecting real results.

## 10) Implementation Roadmap

1. Add benchmark endpoints with equivalent payload semantics:
   - `GET /poll`
   - `WS /ws`
   - optional `GET /sse`
2. Add load generator scripts:
   - polling clients
   - websocket clients
3. Add metrics collection + result serialization.
4. Add plot generation script.
5. Publish report with reproducible command list.
