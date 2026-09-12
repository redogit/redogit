#!/usr/bin/env python3
"""Local REDOGIT contract inspector and executor.

Usage:
  python tools/redogit.py status        [REPOSITORY_ROOT]
  python tools/redogit.py check         [REPOSITORY_ROOT]
  python tools/redogit.py run           [REPOSITORY_ROOT]
  python tools/redogit.py public-status [PROFILE_ROOT]
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


def load_json_object(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def load_contract(root: Path) -> dict[str, Any]:
    path = root / "redogit.json"
    try:
        return load_json_object(path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"REDOGIT contract not found: {path}") from exc


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


def load_public_status(root: Path) -> dict[str, Any]:
    status = load_json_object(root / "PUBLIC_STATUS.json")
    if status.get("schema") != "redogit/public-status/v1":
        raise ValueError("PUBLIC_STATUS.json schema must be redogit/public-status/v1")
    if status.get("scope") != "public repositories only":
        raise ValueError("PUBLIC_STATUS.json must be explicitly public-only")
    if status.get("public_contracts_green") is not True:
        raise ValueError("public REDOGIT contracts are not declared green")
    repositories = status.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        raise ValueError("PUBLIC_STATUS.json repositories must be a non-empty list")
    names: set[str] = set()
    for entry in repositories:
        if not isinstance(entry, dict):
            raise ValueError("every public status entry must be an object")
        name = entry.get("repository")
        if not isinstance(name, str) or not name.startswith("redogit/"):
            raise ValueError(f"invalid public repository name: {name!r}")
        if name in names:
            raise ValueError(f"duplicate public repository: {name}")
        names.add(name)
    return status


def print_public_status(status: dict[str, Any]) -> None:
    print(f"snapshot: {status.get('snapshot_date', 'unknown')}")
    print(f"scope:    {status['scope']}")
    print("public contracts: GREEN")
    for entry in status["repositories"]:
        name = entry["repository"]
        contract_status = entry.get("contract_status", "unknown")
        print(f"  - {name}: {contract_status}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect or execute REDOGIT contracts and public status.")
    parser.add_argument("command", choices=("status", "check", "run", "public-status"))
    parser.add_argument("root", nargs="?", default=".", help="Repository/profile root; defaults to the current directory.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    try:
        if args.command == "public-status":
            print_public_status(load_public_status(root))
            return 0

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
