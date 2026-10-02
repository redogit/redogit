#!/usr/bin/env python3
"""Audit GitHub Pages configuration for every public redogit repository.

Uses the documented REST endpoint:
GET /repos/{owner}/{repo}/pages
API version: 2026-03-10

A 200 response means a Pages site is configured.
A 404 response means no Pages site is currently configured (for these public repos).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

OWNER = "redogit"
REPOSITORIES = [
    "orbit",
    "MauiBrickBreak",
    "redogit",
    "DnD",
    "FirstNeuralNetwork",
    "conscience64",
    "Dream-To-Action",
    "Other-Projects-",
    "RMAL",
    "pnp-dean",
    "hodge",
    "conscience64-platform",
    "games",
    "language-carriers",
    "archives-knowledge",
    "portfolio",
]
API_VERSION = "2026-03-10"


def request_pages(repo: str) -> dict:
    url = f"https://api.github.com/repos/{OWNER}/{repo}/pages"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "redogit-pages-audit",
    }
    token = os.environ.get("GITHUB_API_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = json.load(response)
            return {
                "repository": f"{OWNER}/{repo}",
                "configured": True,
                "http_status": response.status,
                "html_url": payload.get("html_url"),
                "status": payload.get("status"),
                "build_type": payload.get("build_type"),
                "source": payload.get("source"),
                "https_enforced": payload.get("https_enforced"),
            }
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {
                "repository": f"{OWNER}/{repo}",
                "configured": False,
                "http_status": 404,
                "reason": "pages_site_not_configured_or_not_visible",
            }
        body = exc.read().decode("utf-8", "replace")
        return {
            "repository": f"{OWNER}/{repo}",
            "configured": None,
            "http_status": exc.code,
            "error": body[:1000],
        }
    except Exception as exc:
        return {
            "repository": f"{OWNER}/{repo}",
            "configured": None,
            "http_status": None,
            "error": repr(exc),
        }


def main() -> int:
    results = [request_pages(repo) for repo in REPOSITORIES]
    summary = {
        "schema": "redogit/github-pages-audit/v1",
        "api_version": API_VERSION,
        "endpoint": "GET /repos/{owner}/{repo}/pages",
        "owner": OWNER,
        "repositories": results,
        "counts": {
            "configured": sum(r["configured"] is True for r in results),
            "missing": sum(r["configured"] is False for r in results),
            "errors": sum(r["configured"] is None for r in results),
            "total": len(results),
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if summary["counts"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
