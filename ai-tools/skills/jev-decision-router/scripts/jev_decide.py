#!/usr/bin/env python3
"""Call TypeSafe System One for a bounded typed decision."""
import json
import os
import sys
import time
import urllib.error
import urllib.request


def main() -> int:
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        print(json.dumps({"error": "TYPESAFE_API_KEY is not set"}), file=sys.stderr)
        return 2
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"invalid JSON input: {exc}"}), file=sys.stderr)
        return 2
    payload.setdefault("model", os.environ.get("JEV_MODEL", "jev-latest"))
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        os.environ.get("TYPESAFE_API_URL", "https://api.typesafe.ai/v1/systemone"),
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
            print(json.dumps(result, ensure_ascii=False))
            return 0
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 529) or attempt == 2:
                detail = exc.read().decode("utf-8", errors="replace")
                print(json.dumps({"error": f"TypeSafe HTTP {exc.code}", "detail": detail}), file=sys.stderr)
                return 1
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == 2:
                print(json.dumps({"error": f"TypeSafe request failed: {exc}"}), file=sys.stderr)
                return 1
        time.sleep(2**attempt)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
