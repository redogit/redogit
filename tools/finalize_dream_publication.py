"""Verify the current redogit / Dream public Pages topology.

This validator preserves historical deployment evidence but treats the current
October 2, 2026 Pages state as authoritative for navigation.
"""
from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB_URL = "https://redogit.github.io/redogit/"
PROJECT_URL = "https://redogit.github.io/Dream-To-Action/"
APP_URL = "https://redogit.github.io/conscience64/dream-to-action/"
ORIGINAL_RUN = "https://github.com/redogit/conscience64/actions/runs/36459096995"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require(HUB_URL in readme, "Canonical redogit hub missing from README")
    require(PROJECT_URL in readme, "Dream dedicated project page missing from README")

    publishing = (ROOT / "docs/dream-to-action/PUBLISHING.md").read_text(encoding="utf-8")
    for url in (HUB_URL, PROJECT_URL, APP_URL):
        require(url in publishing, f"Publishing record missing {url}")

    data = json.loads((ROOT / "docs/dream-to-action/SOURCE.json").read_text(encoding="utf-8"))
    require(data["public_url"] == APP_URL, "Operational Dream app route changed")
    require(data["profile_public_url"] == HUB_URL, "Canonical profile URL is not redogit/redogit")
    require(data.get("profile_pages_enabled") is True, "Profile Pages current state not enabled")
    require(data.get("current_project_page") == PROJECT_URL, "Dedicated Dream project page not recorded")
    require(data.get("live_verification", {}).get("url") == ORIGINAL_RUN, "Original app verification evidence changed")
    require(data.get("prior_attempt", {}).get("status") == "NOT DEPLOYED: Pages site Not Found",
            "Historical failed attempt was rewritten")
    print("PASS: current hub/project/app topology and historical failure boundary are consistent.")


def fetch(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "redogit-public-pages-verifier/1"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status, response.read()


def live() -> None:
    check()
    expectations = [
        (HUB_URL, b"redogit"),
        (PROJECT_URL, b"Dream to Action"),
        (APP_URL, b"Dream to Action"),
    ]
    for url, marker in expectations:
        status, body = fetch(url)
        require(status == 200, f"{url} returned HTTP {status}")
        require(marker.lower() in body.lower(), f"{url} missing expected marker")
        print(f"PASS {status} {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--live", action="store_true")
    args = parser.parse_args()

    try:
        if args.check:
            check()
        else:
            live()
    except (OSError, ValueError) as exc:
        raise SystemExit("Publication verification failed: " + str(exc))
