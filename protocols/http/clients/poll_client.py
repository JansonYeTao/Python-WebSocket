import argparse
import time

import httpx


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple HTTP polling client")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--payload", default="hello-http")
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()

    with httpx.Client(timeout=10.0) as client:
        for idx in range(args.count):
            response = client.get(f"{args.base_url}/poll", params={"payload": args.payload})
            response.raise_for_status()
            print(f"[{idx + 1}/{args.count}] {response.json()}")
            if idx < args.count - 1:
                time.sleep(args.interval)


if __name__ == "__main__":
    main()
