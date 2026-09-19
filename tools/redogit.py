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
    "preserve_unresolved_remainder": True,
    "preserve_source_native_identity": True,
    "rewrite_history": False,
}

EXPECTED_CHECKS = ["assumption", "test", "unknown"]
EXPECTED_EVIDENCE_CLASSES = [
    "executed-and-verified",
    "externally-validated",
    "formal-consequence",
    "hypothesis-or-open-question",
]

REQUIRED_RESEARCH_DISTINCTIONS = {
    "UNKNOWN != ABSENT",
    "UNASSIGNED != ABSENT",
    "UNSELECTED != FALSE",
    "INDEX_MISS != ABSENCE",
    "RELATED != SUPPORTS",
    "SEMANTIC_SIMILARITY != IDENTITY",
    "SOURCE != RECONSTRUCTION",
    "BYTE_IDENTITY != SEMANTIC_TRUTH",
    "CURRENT_NAVIGATION != HISTORICAL_SOURCE",
    "OBSERVATION != INTERPRETATION",
    "VIEWPOINT_CHANGE != TASK_CHANGE",
    "SELECTION != GLOBAL_OPTIMALITY",
    "FINITE_VERIFICATION != UNIVERSALITY",
    "LOSS_ACKNOWLEDGED != LOSS_CONCEALED",
    "EVALUATION_COMPLETE != PROMOTION_APPROVED",
    "PERSON != RECORDED_MODEL",
    "USER_GOAL != SYSTEM_GOAL",
    "PREDECESSOR != SUCCESSOR",
    "INTERNAL_CONSISTENCY != EXTERNAL_VALIDATION",
    "CLAIM != EVIDENCE",
    "PUBLIC_REPOSITORY != PRIVATE_FAMILY_CONTEXT",
    "GAME_CHARACTER != PRIVATE_PERSON",
    "SPROUTLING != REAL_CHILD",
}


def is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and len(value) > 0


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


def validate_optional_nonempty_string(value: object, field: str) -> None:
    if value is not None and not is_nonempty_string(value):
        raise ValueError(f"{field} must be null or a non-empty string")


def validate_string_list(value: object, field: str, *, unique: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    if any(not is_nonempty_string(item) for item in value):
        raise ValueError(f"{field} entries must be non-empty strings")
    result = list(value)
    if unique and len(set(result)) != len(result):
        raise ValueError(f"{field} entries must be unique")
    return result


def validate_research_policy(contract: dict[str, Any]) -> None:
    research = contract.get("research_policy")
    if not isinstance(research, dict):
        raise ValueError("research_policy object is required")

    if research.get("surface") != "I/R/P/O":
        raise ValueError("research_policy.surface must be I/R/P/O")
    if research.get("checks") != EXPECTED_CHECKS:
        raise ValueError("research_policy.checks must be assumption/test/unknown")
    if research.get("evidence_classes") != EXPECTED_EVIDENCE_CLASSES:
        raise ValueError("research_policy.evidence_classes must preserve the four evidence classes")

    for field in (
        "claim_policy",
        "selection_policy",
        "promotion",
        "knowledge_decay",
        "historical_checkpoint_policy",
        "privacy_policy",
    ):
        if not is_nonempty_string(research.get(field)):
            raise ValueError(f"research_policy.{field} must be a non-empty string")

    distinctions = validate_string_list(
        research.get("required_distinctions"),
        "research_policy.required_distinctions",
        unique=True,
    )
    missing = sorted(REQUIRED_RESEARCH_DISTINCTIONS.difference(distinctions))
    if missing:
        raise ValueError("research_policy is missing required distinctions: " + ", ".join(missing))

    domain = research.get("domain_distinctions", [])
    validate_string_list(domain, "research_policy.domain_distinctions", unique=True)


def validate_contract(root: Path, contract: dict[str, Any]) -> None:
    if contract.get("schema") != "redogit/v1":
        raise ValueError("schema must be redogit/v1")

    repository = contract.get("repository")
    if not is_nonempty_string(repository):
        raise ValueError("repository is required")

    current = contract.get("current")
    if not isinstance(current, dict):
        raise ValueError("current object is required")
    if not is_nonempty_string(current.get("id")):
        raise ValueError("current.id is required")

    status = current.get("status")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"unsupported current.status: {status!r}")

    current_path = current.get("path")
    validate_optional_nonempty_string(current_path, "current.path")
    if current_path not in (None, ".") and not (root / str(current_path)).exists():
        raise ValueError(f"current.path does not exist: {current_path}")

    validate_optional_nonempty_string(current.get("build"), "current.build")
    validate_optional_nonempty_string(current.get("verify"), "current.verify")

    blocker = current.get("external_blocker")
    if blocker is not None and not is_nonempty_string(blocker):
        raise ValueError("current.external_blocker must be a non-empty string when present")
    if status == "current-with-external-blocker" and not is_nonempty_string(blocker):
        raise ValueError("current-with-external-blocker requires current.external_blocker")

    if contract.get("history_policy") != EXPECTED_HISTORY_POLICY:
        raise ValueError("history_policy violates REDOGIT invariants")

    validate_research_policy(contract)

    boundary = contract.get("boundary")
    if not isinstance(boundary, dict):
        raise ValueError("boundary object is required")
    for field in ("owns", "does_not_own"):
        validate_string_list(boundary.get(field), f"boundary.{field}")

    predecessors = contract.get("predecessors", [])
    if not isinstance(predecessors, list):
        raise ValueError("predecessors must be a list")
    for predecessor in predecessors:
        if not isinstance(predecessor, dict):
            raise ValueError("every predecessor must be an object")
        if not is_nonempty_string(predecessor.get("id")):
            raise ValueError("every predecessor.id must be a non-empty string")
        validate_optional_nonempty_string(predecessor.get("path"), "predecessor.path")
        if predecessor.get("retained") is not True:
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

    research = contract["research_policy"]
    print(f"research surface: {research['surface']}")
    print(f"required distinctions: {len(research['required_distinctions'])}")
    print(f"domain distinctions:   {len(research.get('domain_distinctions', []))}")

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
