# WebSocket vs HTTP Polling: What You Pay (Detailed Tradeoffs)

Date: 2026-05-15

This document focuses on the *cost side* of choosing WebSocket. Benchmarks in this repo show WebSocket can significantly improve latency and throughput, but that performance gain comes with operational and engineering costs.

See benchmark summary data in:
- `benchmarks/REPORT.md`
- `benchmarks/results/*.json`

---

## 1) Connection lifecycle management cost

With HTTP polling, each request is short-lived and independent. With WebSocket, connections stay open and must be actively managed.

You need to design and maintain:
- connection open/close handling
- idle timeout behavior
- heartbeat/ping-pong to detect dead peers
- reconnect handling

**Cost paid:** extra code paths, more state, and more edge-case testing.

---

## 2) Stateful horizontal scaling cost

HTTP is naturally stateless and easy to spread across many instances. WebSocket often requires one (or both):

- sticky sessions at the load balancer, and/or
- shared messaging backplane (Redis/NATS/Kafka) for fan-out across instances

**Cost paid:** added infrastructure, coordination complexity, and failure modes.

---

## 3) Backpressure and memory safety cost

A slow client can cause queued outbound messages to grow. You must define backpressure policy:

- buffer (risking memory growth)
- drop messages (possible data loss)
- disconnect slow consumers (possible UX impact)

**Cost paid:** explicit design tradeoffs and robust safeguards.

---

## 4) Delivery semantics and replay cost

WebSocket transport does not automatically solve app-level reliability semantics.

You may need:
- message IDs
- ack/retry rules
- deduplication logic
- replay on reconnect

**Cost paid:** protocol design work and ongoing compatibility maintenance.

---

## 5) Authentication and authorization lifecycle cost

Long-lived channels complicate auth compared to per-request HTTP checks.

You need to handle:
- token expiry during active sessions
- auth refresh/reconnect behavior
- revocation propagation
- per-message authorization checks (when needed)

**Cost paid:** additional security logic and testing burden.

---

## 6) Observability and on-call cost

HTTP tooling is mature by default. For WebSocket, you should add custom metrics and dashboards such as:

- active connections
- message throughput by type
- send queue depth
- dropped/disconnected slow clients
- reconnect storm rates

**Cost paid:** more instrumentation work and more complex incident debugging.

---

## 7) Infrastructure and failure mode cost

Common operational pitfalls with long-lived sockets include:

- load balancer/proxy idle timeout mismatch
- file descriptor/socket limits
- reconnect spikes after deploy/network blips
- uneven distribution of sticky sessions

**Cost paid:** infra tuning + resilience planning.

---

## 8) Team productivity and maintenance cost

WebSocket systems usually require more specialized operational and protocol knowledge.

Compared to polling, teams often spend more time on:
- protocol evolution
- resilience testing
- production diagnostics
- runbook development

**Cost paid:** higher long-term ownership cost.

---

## 9) How to decide (practical checklist)

Choose WebSocket when most are true:
- strong realtime UX requirement
- bidirectional interaction needed
- high update frequency
- team can own lifecycle/reliability/observability complexity

Prefer polling/SSE when most are true:
- low-frequency updates
- mostly one-way delivery
- simpler ops and faster implementation are priorities
- latency budget is relaxed

---

## 10) Tie-back to this repository’s benchmark runs

In this repo’s local benchmark scenarios, WebSocket outperformed HTTP polling on throughput and latency. That demonstrates the **benefit** side.

This document captures the **cost** side so decisions are made on both dimensions:
- performance gains
- ownership complexity

Use both `benchmarks/REPORT.md` and this file together when deciding architecture.
