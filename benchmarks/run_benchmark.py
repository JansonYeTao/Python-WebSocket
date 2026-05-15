import argparse
import asyncio
import json
import statistics
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import httpx
import websockets


@dataclass
class RunResult:
    transport: str
    clients: int
    messages_per_client: int
    payload_size: int
    total_messages: int
    success_messages: int
    duration_seconds: float
    throughput_mps: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    latency_mean_ms: float


def percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        return 0.0
    index = max(0, min(len(sorted_values) - 1, int((p / 100.0) * (len(sorted_values) - 1))))
    return sorted_values[index]


def summarize(
    transport: str,
    clients: int,
    messages_per_client: int,
    payload_size: int,
    latencies_ms: list[float],
    started_at: float,
) -> RunResult:
    ended_at = time.perf_counter()
    duration = ended_at - started_at
    sorted_lat = sorted(latencies_ms)
    total = clients * messages_per_client
    success = len(latencies_ms)
    throughput = success / duration if duration > 0 else 0.0
    mean = statistics.fmean(sorted_lat) if sorted_lat else 0.0
    return RunResult(
        transport=transport,
        clients=clients,
        messages_per_client=messages_per_client,
        payload_size=payload_size,
        total_messages=total,
        success_messages=success,
        duration_seconds=round(duration, 4),
        throughput_mps=round(throughput, 2),
        latency_p50_ms=round(percentile(sorted_lat, 50), 3),
        latency_p95_ms=round(percentile(sorted_lat, 95), 3),
        latency_p99_ms=round(percentile(sorted_lat, 99), 3),
        latency_mean_ms=round(mean, 3),
    )


async def run_ws_client(ws_url: str, messages: int, payload: str, latencies: list[float]) -> None:
    async with websockets.connect(ws_url) as websocket:
        await websocket.recv()  # hello payload
        for _ in range(messages):
            t0 = time.perf_counter()
            await websocket.send(json.dumps(payload))
            await websocket.recv()
            latencies.append((time.perf_counter() - t0) * 1000)


async def benchmark_ws(base_url: str, clients: int, messages: int, payload_size: int) -> RunResult:
    ws_url = base_url.replace("http://", "ws://").replace("https://", "wss://") + "/ws"
    payload = "x" * payload_size
    latencies: list[float] = []
    started_at = time.perf_counter()
    await asyncio.gather(
        *(run_ws_client(ws_url, messages, payload, latencies) for _ in range(clients))
    )
    return summarize("websocket", clients, messages, payload_size, latencies, started_at)


async def run_poll_client(base_url: str, messages: int, payload: str, latencies: list[float]) -> None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        for _ in range(messages):
            t0 = time.perf_counter()
            resp = await client.get(f"{base_url}/poll", params={"payload": payload})
            resp.raise_for_status()
            _ = resp.json()
            latencies.append((time.perf_counter() - t0) * 1000)


async def benchmark_poll(base_url: str, clients: int, messages: int, payload_size: int) -> RunResult:
    payload = "x" * payload_size
    latencies: list[float] = []
    started_at = time.perf_counter()
    await asyncio.gather(
        *(run_poll_client(base_url, messages, payload, latencies) for _ in range(clients))
    )
    return summarize("http_poll", clients, messages, payload_size, latencies, started_at)


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run simple WebSocket vs HTTP polling benchmark.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--clients", type=int, default=20)
    parser.add_argument("--messages", type=int, default=20)
    parser.add_argument("--payload-size", type=int, default=128)
    parser.add_argument("--transport", choices=["ws", "poll", "both"], default="both")
    parser.add_argument("--output", default="benchmarks/results/latest.json")
    args = parser.parse_args()

    results: list[RunResult] = []
    if args.transport in {"ws", "both"}:
        results.append(await benchmark_ws(args.base_url, args.clients, args.messages, args.payload_size))
    if args.transport in {"poll", "both"}:
        results.append(await benchmark_poll(args.base_url, args.clients, args.messages, args.payload_size))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": int(time.time()),
        "base_url": args.base_url,
        "results": [asdict(r) for r in results],
    }
    output_path.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
