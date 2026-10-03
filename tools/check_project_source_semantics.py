#!/usr/bin/env python3
"""Cross-check project-page semantics against current repository sources.

This is deliberately narrower than general link checking. It asserts the
source hierarchy and the concrete distinctions that were found to matter
during the 2026-10-02 project-page reconciliation.
"""
from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()


def get(repository: str, path: str, ref: str = "main") -> str:
    quoted = urllib.parse.quote(path, safe="/")
    url = f"{API}/repos/{repository}/contents/{quoted}?ref={urllib.parse.quote(ref, safe='')}"
    headers = {
        "Accept": "application/vnd.github.raw+json",
        "User-Agent": "redogit-project-source-semantics/1",
        "X-GitHub-Api-Version": "2026-03-10",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"{repository}:{path} returned HTTP {response.status}")
        return response.read().decode("utf-8")


def need(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        raise AssertionError(f"{label}: missing {fragment!r}")


def forbid(text: str, fragment: str, label: str) -> None:
    if fragment in text:
        raise AssertionError(f"{label}: stale/forbidden fragment still present: {fragment!r}")


def main() -> int:
    checks = []

    c64 = get("redogit/conscience64", "README.md")
    need(c64, "only explicitly owner-authorized curated routes", "Conscience64 publication scope")
    need(c64, "MMO World Beta", "Conscience64 source-only project list")
    need(c64, "not routes in the current `gh-pages` projection", "Conscience64 source-only boundary")
    checks.append("Conscience64 root publication boundary")

    play = get("redogit/conscience64", "play/README.md")
    need(play, "Current publication state — 2026-09-29", "Play publication state")
    need(play, "For source-only rows below", "Play source-only link rule")
    for stale in (
        "https://redogit.github.io/conscience64/play/explorer-world/",
        "https://redogit.github.io/conscience64/play/mmo-world/",
        "https://redogit.github.io/conscience64/play/orbit/",
        "https://redogit.github.io/conscience64/play/weave/",
        "https://redogit.github.io/conscience64/play/garden/",
        "https://redogit.github.io/conscience64/play/steps/",
        "https://redogit.github.io/conscience64/play/compare/",
        "https://redogit.github.io/conscience64/play/computational-chorus/",
    ):
        forbid(play, stale, "Play source-only routes")
    checks.append("Play curated-vs-source-only boundary")

    about = get("redogit/conscience64", "about/README.md")
    need(about, "Historical snapshot status", "Conscience64 About time scope")
    need(about, "That count is historical", "Conscience64 historical repository count")
    checks.append("Historical About snapshot")

    analytics = get("redogit/conscience64", "analytics/README.md")
    need(analytics, "does **not** include `analytics/`", "Analytics publication boundary")
    checks.append("Research Analytics source-only boundary")

    coordinate = get("redogit/conscience64", "coordinate-space/README.md")
    need(coordinate, "not** in the current curated Conscience64 GitHub Pages projection", "Coordinate Space publication boundary")
    checks.append("Coordinate Space source-only boundary")

    explorer = get("redogit/conscience64", "play/explorer-world/README.md")
    need(explorer, "not** in the current curated Conscience64 GitHub Pages projection", "Explorer World publication boundary")
    checks.append("Explorer World source-only boundary")

    mmo_world = get("redogit/conscience64", "play/mmo-world/README.md")
    need(mmo_world, "not** in the current curated Conscience64 GitHub Pages projection", "MMO World publication boundary")
    need(mmo_world, "Current public Pages advertising surface:** no", "MMO World advertising boundary")
    checks.append("MMO World predecessor/source-only boundary")

    public_updates = get("redogit/conscience64", "research/projects/public-updates/README.md")
    need(public_updates, "does **not** publish `research/**`", "Public research updates boundary")
    checks.append("Research updates source-only boundary")

    versions = json.loads(get("redogit/conscience64", "history/versions.json"))
    if len(versions.get("repositories", [])) != 16:
        raise AssertionError(f"History repository catalog: expected 16, got {len(versions.get('repositories', []))}")
    need(json.dumps(versions), "CURRENT_PUBLIC_ACCOUNT_REPOSITORY_HISTORY_LINKS", "History repository scope")
    checks.append("History current public repository catalog = 16")

    simple_core = get("redogit/conscience64", "play/mmo/simple/core.mjs")
    activity_block = re.search(
        r"export const ACTIVITIES\s*=\s*Object\.freeze\(\[(.*?)\]\);",
        simple_core,
        flags=re.S,
    )
    if not activity_block:
        raise AssertionError("Simple Core: ACTIVITIES block not found")
    activity_ids = re.findall(r"\{id:'([^']+)'", activity_block.group(1))
    if len(activity_ids) != 12:
        raise AssertionError(f"Simple Core: expected 12 activities, found {len(activity_ids)}: {activity_ids}")

    mmo_current = get("redogit/conscience64", "play/mmo/CURRENT.md")
    need(mmo_current, "full **12-activity** bounded mix", "MMO current-state activity count")
    need(mmo_current, "`Sidewalk Slalom`", "MMO current-state movement repair")
    need(mmo_current, "`Parcel Relay`", "MMO current-state movement repair")
    forbid(mmo_current, "remaining category gap is **two additional movement/reaction activities**", "MMO stale 10→12 gap")
    checks.append("Simple Core implementation = 12 activities and CURRENT.md agrees")

    fuzz = get("redogit/conscience64", "play/fuzzball-hidden/README.md")
    need(fuzz, "unlisted", "Fuzzball distribution boundary")
    checks.append("Fuzzball remains intentionally unlisted")

    projects_current = json.loads(get("redogit/conscience64", "research/projects/CURRENT.json"))
    if projects_current.get("currentHumanReadableProjectCount") != 9:
        raise AssertionError("Research project current manifest: expected 9 human-readable records")
    if projects_current.get("browserApiProjection", {}).get("projectCount") != 7:
        raise AssertionError("Research project current manifest: expected preserved browser API count 7")
    checks.append("Research portfolio 7 preserved + 2 successor = 9")

    hodge = get("redogit/conscience64", "research/hodge/README.md")
    need(hodge, "The Hodge conjecture is not established", "Hodge claim ceiling")
    checks.append("Hodge claim ceiling")

    pnp_current = get("redogit/Other-Projects-", "P versus NP Repair Lab/CURRENT.md")
    need(pnp_current, "A P-versus-NP resolution still requires", "PNP current claim ceiling")
    checks.append("P-vs-NP claim ceiling")

    pnp_page = get(
        "redogit/Other-Projects-",
        "P versus NP Repair Lab/decision_field/discriminators_2026_09_14/index.html",
    )
    need(pnp_page, "Historical bounded checkpoint — September 14, 2026.", "PNP dated page scope")
    checks.append("PNP discriminator historical scope")

    s1_page = get("redogit/Other-Projects-", "S1 Models Lab/index.html")
    need(s1_page, "Preserved Experiment 0 interface.", "S1 dated UI scope")
    checks.append("S′1 Experiment 0 historical/current split")

    w114 = get("redogit/Other-Projects-", "Decision Field Operator Lab/hodge-perturbation-game/README.md")
    for fragment in ("alpha = (1,7,78,79,86,91)", "center = MOT-1", "GAME_SCORE != MATHEMATICAL_EVIDENCE"):
        need(w114, fragment, "W114 mathematical/game boundary")
    checks.append("W114 center and game-evidence boundary")

    rmao = get("redogit/Other-Projects-", "Decision Field MMORPG/README.md")
    need(rmao, "Current executable truth", "Decision Field MMORPG current implementation")
    need(rmao, "2D browser transition prototype", "Decision Field MMORPG 2D/3D boundary")
    checks.append("Decision Field MMORPG target-vs-implementation boundary")

    dream = get("redogit/Dream-To-Action", "README.md")
    need(dream, "This repository remains the canonical source.", "Dream source authority")
    need(dream, "https://redogit.github.io/Dream-To-Action/", "Dream dedicated project page")
    need(dream, "https://redogit.github.io/conscience64/dream-to-action/", "Dream operational route")
    checks.append("Dream source / project page / operational route split")

    dnd = get("redogit/DnD", "spec/RMAL_LANGUAGE_SPEC_3.md", ref="master")
    need(dnd, "Canonical repository:** `redogit/DnD`", "RMAL canonical repository")
    need(dnd, "Implementation language:** ISO C23", "RMAL current implementation language")
    checks.append("RMAL canonical repository and C23 implementation")

    live_design = get("redogit/redogit", "RMAL_PNP_LIVE_DESIGN_2026-09-25.md")
    need(live_design, "HISTORICAL DESIGN SNAPSHOT", "September 25 live-design scope")
    checks.append("September 25 PNP design preserved as snapshot")

    recent = get("redogit/redogit", "docs/recent-work.html")
    need(recent, "RECENT WORK · ARCHIVE SNAPSHOT.", "Recent Work archive scope")
    checks.append("Recent Work archive scope")

    project_pages = json.loads(get("redogit/redogit", "PROJECT_PAGES.json"))
    if len(project_pages.get("pages", [])) < 39:
        raise AssertionError("Project page registry unexpectedly shrank below 39 declared pages")
    checks.append(f"Project-page registry declares {len(project_pages['pages'])} pages")

    print("PASS semantic source contract")
    for item in checks:
        print(" - " + item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
