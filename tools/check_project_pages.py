#!/usr/bin/env python3
"""Verify source-aware project pages declared in PROJECT_PAGES.json."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "PROJECT_PAGES.json"


def fetch(url: str, attempts: int = 5, accept: str | None = None) -> tuple[int, str]:
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            headers = {"User-Agent": "redogit-project-page-audit/2"}
            if accept:
                headers["Accept"] = accept
            req = urllib.request.Request(
                url,
                headers=headers,
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.status, response.read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = exc
            if attempt < attempts:
                time.sleep(2)
    raise RuntimeError(f"{url} unavailable after {attempts} attempts: {last!r}")


def source_api_url(repository: str, branch: str, path: str) -> str:
    quoted_path = urllib.parse.quote(path, safe="/")
    quoted_branch = urllib.parse.quote(branch, safe="")
    return f"https://api.github.com/repos/{repository}/contents/{quoted_path}?ref={quoted_branch}"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    require(registry.get("schema") == "redogit/project-pages/v1", "unexpected registry schema")
    hub = registry["main_url"]

    failures: list[str] = []
    for page in registry["pages"]:
        page_id = page["id"]
        try:
            source_status, source_body = fetch(
                source_api_url(page["repository"], page["branch"], page["path"]),
                accept="application/vnd.github.raw+json",
            )
            require(source_status == 200, f"source returned HTTP {source_status}")

            if page.get("backlink_required", True):
                require(hub in source_body, "source page lacks canonical main-hub link")

            if page.get("authority") != "canonical-source-separate-projection":
                source_url = page.get("source_url")
                if source_url:
                    require(source_url in source_body, f"source page does not expose current source link {source_url}")

            for material in page.get("materials", []):
                require(material in source_body, f"declared current material missing from page: {material}")

            public_url = page.get("public_url")
            if public_url:
                public_status, public_body = fetch(public_url)
                require(public_status == 200, f"live route returned HTTP {public_status}")
                if page.get("backlink_required", True) and page.get("kind") != "redirect":
                    require(hub in public_body, "live page lacks canonical main-hub link")

            print(f"PASS {page_id}")
        except Exception as exc:
            failures.append(f"{page_id}: {exc}")

    if failures:
        print("FAILURES:")
        for failure in failures:
            print(" - " + failure)
        return 1

    print(f"PASS: {len(registry['pages'])} declared project pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
