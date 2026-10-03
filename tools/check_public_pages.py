#!/usr/bin/env python3
"""Verify the live public Pages graph declared in PUBLIC_PAGES.json."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "PUBLIC_PAGES.json"


def fetch(url: str, attempts: int = 6) -> tuple[int, str]:
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "redogit-pages-integrity/2"},
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.status, response.read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = exc
            if attempt < attempts:
                time.sleep(3)
    raise RuntimeError(f"{url} unavailable after {attempts} attempts: {last!r}")


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    require(registry.get("schema") == "redogit/public-pages/v1", "unexpected registry schema")

    hub_url = registry["main"]["page_url"]
    status, hub = fetch(hub_url)
    require(status == 200, f"main hub returned HTTP {status}")
    require("redogit" in hub.lower(), "main hub missing redogit marker")

    failures: list[str] = []
    projects = registry.get("projects", [])
    for project in projects:
        name = project["repository"]
        url = project["page_url"]
        source = project["source_url"]
        try:
            code, body = fetch(url)
            require(code == 200, f"HTTP {code}")
            require(url in hub, f"main hub does not link to {url}")
            require(source in hub, f"main hub does not link to source {source}")
            if project.get("backlink_required", False):
                require(hub_url in body, f"child page lacks backlink to {hub_url}")
            print(f"PASS {name}: {url}")
        except Exception as exc:
            failures.append(f"{name}: {exc}")

    for route in registry.get("extra_public_routes", []):
        name = route["id"]
        url = route["url"]
        try:
            code, _ = fetch(url)
            require(code == 200, f"HTTP {code}")
            print(f"PASS {name}: {url}")
        except Exception as exc:
            failures.append(f"{name}: {exc}")

    if failures:
        print("FAILURES:")
        for failure in failures:
            print(" - " + failure)
        return 1

    print(
        f"PASS: main hub + {len(projects)} child Pages + "
        f"{len(registry.get('extra_public_routes', []))} extra public route(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
