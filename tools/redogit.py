#!/usr/bin/env python3
"""Local REDOGIT contract inspector and executor.

Usage:
  python tools/redogit.py status [REPOSITORY_ROOT]
  python tools/redogit.py check  [REPOSITORY_ROOT]
  python tools/redogit.py run    [REPOSITORY_ROOT]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any

ALLOWED_STATUSES = {
    "current",
    "current-with-external-blocker",
    "provenance-boundary",
}

EXPECTED_HISTORY_POLICY = {
    "preserve_predecessors": True,
    "preserve_failures": True,
    "rewrite_history": False,
}


def load_contract(root: Path) -> dict[str, Any]:
    path = root / "redogit.json"
    if not path.is_file():
        raise FileNotFoundError(f"REDOGIT contract not found: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("redogit.json must contain a JSON object")
    return value


def validate_contract(root: Path, contract: dict[str, Any]) -> None:
    if contract.get("schema") != "redogit/v1":
        raise ValueError("schema must be redogit/v1")

    repository = contract.get("repository")
    if not isinstance(repository, str) or not repository:
        raise ValueError("repository is required")

    current = contract.get("current")
    if not isinstance(current, dict):
        raise ValueError("current object is required")
    if not isinstance(current.get("id"), str) or not current["id"]:
        raise ValueError("current.id is required")
    if current.get("status") not in ALLOWED_STATUSES:
        raise ValueError(f"unsupported current.status: {current.get('status')!r}")

    current_path = current.get("path")
    if current_path not in (None, ".") and not (root / str(current_path)).exists():
        raise ValueError(f"current.path does not exist: {current_path}")

    if contract.get("history_policy") != EXPECTED_HISTORY_POLICY:
        raise ValueError("history_policy violates REDOGIT invariants")

    boundary = contract.get("boundary")
    if not isinstance(boundary, dict):
        raise ValueError("boundary object is required")
    if not isinstance(boundary.get("owns"), list):
        raise ValueError("boundary.owns must be a list")
    if not isinstance(boundary.get("does_not_own"), list):
        raise ValueError("boundary.does_not_own must be a list")

    predecessors = contract.get("predecessors", [])
    if not isinstance(predecessors, list):
        raise ValueError("predecessors must be a list")
    for predecessor in predecessors:
        if not isinstance(predecessor, dict) or predecessor.get("retained") is not True:
            raise ValueError("every declared predecessor must be retained")


def print_status(contract: dict[str, Any]) -> None:
    current = contract["current"]
    print(f"repository: {contract['repository']}")
    print(f"current:    {current['id']}")
    print(f"status:     {current['status']}")
    if current.get("path") is not None:
        print(f"path:       {current['path']}")
    if current.get("external_blocker"):
        print(f"blocker:    {current['external_blocker']}")

    predecessors = contract.get("predecessors", [])
    print(f"retained predecessors: {len(predecessors)}")
    for predecessor in predecessors:
        print(f"  - {predecessor['id']}")

    print("owns:")
    for item in contract["boundary"]["owns"]:
        print(f"  - {item}")
    print("does not own:")
    for item in contract["boundary"]["does_not_own"]:
        print(f"  - {item}")


def execute_declared(root: Path, contract: dict[str, Any]) -> None:
    current = contract["current"]
    for phase in ("build", "verify"):
        command = current.get(phase)
        if not command:
            print(f"SKIP {phase}: no command declared")
            continue
        argv = shlex.split(command)
        print(f"RUN {phase}: {command}", flush=True)
        subprocess.run(argv, cwd=root, check=True)
        print(f"PASS {phase}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect or execute a REDOGIT repository contract.")
    parser.add_argument("command", choices=("status", "check", "run"))
    parser.add_argument("root", nargs="?", default=".", help="Repository root; defaults to the current directory.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    try:
        contract = load_contract(root)
        validate_contract(root, contract)

        if args.command == "status":
            print_status(contract)
        elif args.command == "check":
            print(f"PASS contract {contract['repository']} -> {contract['current']['id']} ({contract['current']['status']})")
        else:
            print_status(contract)
            execute_declared(root, contract)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"REDOGIT FAIL: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
