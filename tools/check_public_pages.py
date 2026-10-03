#!/usr/bin/env python3
"""Verify the live redogit Pages hub and child-page graph."""
from __future__ import annotations

import time
import urllib.error
import urllib.request

HUB = "https://redogit.github.io/redogit/"
CHILDREN = [
    ("orbit", "https://redogit.github.io/orbit/", True),
    ("MauiBrickBreak", "https://redogit.github.io/MauiBrickBreak/", True),
    ("DnD", "https://redogit.github.io/DnD/", True),
    ("FirstNeuralNetwork", "https://redogit.github.io/FirstNeuralNetwork/", True),
    ("Conscience64", "https://redogit.github.io/conscience64/", True),
    ("Dream-To-Action", "https://redogit.github.io/Dream-To-Action/", True),
    ("Other-Projects-", "https://redogit.github.io/Other-Projects-/", True),
    ("RMAL", "https://redogit.github.io/RMAL/", True),
    ("pnp-dean", "https://redogit.github.io/pnp-dean/", True),
    ("hodge", "https://redogit.github.io/hodge/", True),
    ("conscience64-platform", "https://redogit.github.io/conscience64-platform/", True),
    ("games", "https://redogit.github.io/games/", True),
    ("language-carriers", "https://redogit.github.io/language-carriers/", True),
    ("archives-knowledge", "https://redogit.github.io/archives-knowledge/", True),
    ("portfolio", "https://redogit.github.io/portfolio/", True),
]
EXTRA = [
    ("Dream operational app", "https://redogit.github.io/conscience64/dream-to-action/"),
]

def fetch(url: str, attempts: int = 6) -> tuple[int, str]:
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "redogit-pages-integrity/1"},
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
    status, hub = fetch(HUB)
    require(status == 200, f"main hub returned HTTP {status}")
    require("redogit" in hub.lower(), "main hub missing redogit marker")

    failures: list[str] = []
    for name, url, require_backlink in CHILDREN:
        try:
            code, body = fetch(url)
            require(code == 200, f"HTTP {code}")
            require(url in hub, f"main hub does not link to {url}")
            if require_backlink:
                require(HUB in body, f"child page lacks backlink to {HUB}")
            print(f"PASS {name}: {url}")
        except Exception as exc:
            failures.append(f"{name}: {exc}")

    for name, url in EXTRA:
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

    print(f"PASS: main hub + {len(CHILDREN)} child Pages + {len(EXTRA)} extra public route(s)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
