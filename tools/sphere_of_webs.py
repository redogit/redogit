#!/usr/bin/env python3
"""Validate and reconstruct additive sphere-of-webs relation manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "redogit/sphere-of-webs/v1"

POLICY = {
    "chronology": "SEPARATE_IMMUTABLE_ACYCLIC_AXIS",
    "semantic_relations": "EXPLICIT_TYPED_MAY_CYCLE",
    "duplicates": "PRESERVE_OCCURRENCES",
    "source_local_authority": "PRESERVE",
    "authority_transfer": "DENY",
    "evidence_transfer": "DENY",
    "reverse_inference": "DENY",
    "homeward": "REQUIRED",
}

BINDINGS = {
    "thing": "IDENTITY_PROVENANCE_CARRIER_ONLY",
    "orbit_related": "EXACT_DIRECTION_AND_TYPE_ONLY",
    "pairity_check": "FORWARD_AND_REVERSE_CHECKED_SEPARATELY",
    "authority_rule": "RELATION != AUTHORITY_TRANSFER",
    "homeward": "SOURCE_REF_RECONSTRUCTION",
}

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class SphereError(ValueError):
    pass


def _require_object(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SphereError(f"{where} must be an object")
    return value


def _require_list(value: Any, where: str) -> list[Any]:
    if not isinstance(value, list):
        raise SphereError(f"{where} must be a list")
    return value


def _require_string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise SphereError(f"{where} must be a non-empty string")
    return value


def _exact_keys(obj: dict[str, Any], expected: set[str], where: str) -> None:
    actual = set(obj)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise SphereError(f"{where} keys mismatch; missing={missing} extra={extra}")


def _assert_acyclic(nodes: set[str], edges: list[tuple[str, str]]) -> None:
    outgoing = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}
    for before, after in edges:
        if before not in nodes or after not in nodes:
            raise SphereError("chronology precedence references an unknown occurrence")
        outgoing[before].append(after)
        indegree[after] += 1

    queue = [node for node, degree in indegree.items() if degree == 0]
    seen = 0
    while queue:
        node = queue.pop()
        seen += 1
        for after in outgoing[node]:
            indegree[after] -= 1
            if indegree[after] == 0:
                queue.append(after)

    if seen != len(nodes):
        raise SphereError("chronology must be acyclic")


def load_manifest(path: str | Path) -> dict[str, Any]:
    raw = Path(path).read_text(encoding="utf-8")
    data = json.loads(raw)
    return _require_object(data, "manifest")


def validate_manifest(data: dict[str, Any]) -> dict[str, Any]:
    _exact_keys(
        data,
        {
            "schema",
            "id",
            "status",
            "source_refs",
            "bindings",
            "policy",
            "nodes",
            "relations",
            "chronology",
            "round_trip",
        },
        "manifest",
    )

    if data["schema"] != SCHEMA:
        raise SphereError(f"schema must be {SCHEMA}")
    _require_string(data["id"], "manifest.id")
    if data["status"] != "NAVIGATION_ONLY":
        raise SphereError("manifest.status must be NAVIGATION_ONLY")

    bindings = _require_object(data["bindings"], "bindings")
    if bindings != BINDINGS:
        raise SphereError("bindings must preserve the declared Libraries-of-Libraries semantics")

    policy = _require_object(data["policy"], "policy")
    if policy != POLICY:
        raise SphereError("policy must preserve the sphere-of-webs invariants")

    source_refs = _require_object(data["source_refs"], "source_refs")
    if not source_refs:
        raise SphereError("source_refs must not be empty")
    for source_id, source in source_refs.items():
        _require_string(source_id, "source_refs key")
        source = _require_object(source, f"source_refs.{source_id}")
        _exact_keys(
            source,
            {"repository", "pull_request", "head_sha", "path", "section", "authority_effect"},
            f"source_refs.{source_id}",
        )
        _require_string(source["repository"], f"source_refs.{source_id}.repository")
        if not isinstance(source["pull_request"], int) or source["pull_request"] <= 0:
            raise SphereError(f"source_refs.{source_id}.pull_request must be a positive integer")
        if not isinstance(source["head_sha"], str) or not SHA40.fullmatch(source["head_sha"]):
            raise SphereError(f"source_refs.{source_id}.head_sha must be a lowercase 40-hex commit")
        _require_string(source["path"], f"source_refs.{source_id}.path")
        _require_string(source["section"], f"source_refs.{source_id}.section")
        if source["authority_effect"] != "NONE":
            raise SphereError("source references cannot transfer authority")

    nodes = _require_list(data["nodes"], "nodes")
    if not nodes:
        raise SphereError("nodes must not be empty")
    occurrence_ids: list[str] = []
    for index, node in enumerate(nodes):
        node = _require_object(node, f"nodes[{index}]")
        _exact_keys(
            node,
            {
                "occurrence_id",
                "semantic_object_id",
                "label",
                "kind",
                "source_refs",
                "authority_scope",
                "evidence_scope",
                "homeward_ref",
            },
            f"nodes[{index}]",
        )
        occurrence_id = _require_string(node["occurrence_id"], f"nodes[{index}].occurrence_id")
        occurrence_ids.append(occurrence_id)
        _require_string(node["semantic_object_id"], f"nodes[{index}].semantic_object_id")
        _require_string(node["label"], f"nodes[{index}].label")
        if node["kind"] != "TRAIL_OCCURRENCE":
            raise SphereError(f"nodes[{index}].kind must be TRAIL_OCCURRENCE")
        node_sources = _require_list(node["source_refs"], f"nodes[{index}].source_refs")
        if not node_sources:
            raise SphereError(f"nodes[{index}].source_refs must not be empty")
        for source_id in node_sources:
            if source_id not in source_refs:
                raise SphereError(f"nodes[{index}] references unknown source {source_id!r}")
        if node["authority_scope"] != "SOURCE_LOCAL":
            raise SphereError("node authority must remain source-local")
        if node["evidence_scope"] != "SOURCE_LOCAL":
            raise SphereError("node evidence must remain source-local")
        if node["homeward_ref"] not in source_refs:
            raise SphereError(f"nodes[{index}].homeward_ref must reference a declared source")

    if len(set(occurrence_ids)) != len(occurrence_ids):
        raise SphereError("occurrence_id values must be unique")
    occurrence_set = set(occurrence_ids)
    # semantic_object_id is deliberately not required to be unique:
    # duplicate source occurrences must remain representable.

    relations = _require_list(data["relations"], "relations")
    relation_ids: list[str] = []
    for index, relation in enumerate(relations):
        relation = _require_object(relation, f"relations[{index}]")
        _exact_keys(
            relation,
            {
                "relation_id",
                "axis",
                "from_occurrence",
                "to_occurrence",
                "type",
                "source_ref",
                "infer_reverse",
                "authority_transfer",
                "evidence_transfer",
            },
            f"relations[{index}]",
        )
        relation_ids.append(_require_string(relation["relation_id"], f"relations[{index}].relation_id"))
        if relation["axis"] != "semantic_ancestry":
            raise SphereError("relations must live on the semantic_ancestry axis")
        if relation["from_occurrence"] not in occurrence_set or relation["to_occurrence"] not in occurrence_set:
            raise SphereError("relation endpoint must reference a declared occurrence")
        _require_string(relation["type"], f"relations[{index}].type")
        if relation["source_ref"] not in source_refs:
            raise SphereError("relation source_ref must reference a declared source")
        if relation["infer_reverse"] is not False:
            raise SphereError("reverse-edge inference is forbidden")
        if relation["authority_transfer"] is not False:
            raise SphereError("relation cannot transfer authority")
        if relation["evidence_transfer"] is not False:
            raise SphereError("relation cannot transfer evidence")
    if len(set(relation_ids)) != len(relation_ids):
        raise SphereError("relation_id values must be unique")

    chronology = _require_object(data["chronology"], "chronology")
    _exact_keys(chronology, {"immutable", "entries", "precedence"}, "chronology")
    if chronology["immutable"] is not True:
        raise SphereError("chronology must be immutable")
    entries = _require_list(chronology["entries"], "chronology.entries")
    if len(entries) != len(nodes):
        raise SphereError("chronology must contain every occurrence exactly once")

    ordered_occurrences: list[str] = []
    for index, entry in enumerate(entries):
        entry = _require_object(entry, f"chronology.entries[{index}]")
        _exact_keys(entry, {"ordinal", "occurrence_id"}, f"chronology.entries[{index}]")
        if entry["ordinal"] != index:
            raise SphereError("chronology ordinals must be contiguous and immutable")
        occurrence_id = entry["occurrence_id"]
        if occurrence_id not in occurrence_set:
            raise SphereError("chronology entry references an unknown occurrence")
        ordered_occurrences.append(occurrence_id)

    if len(set(ordered_occurrences)) != len(ordered_occurrences):
        raise SphereError("chronology cannot collapse or duplicate occurrence identities")
    if set(ordered_occurrences) != occurrence_set:
        raise SphereError("chronology occurrence set must exactly match nodes")

    precedence_raw = _require_list(chronology["precedence"], "chronology.precedence")
    precedence: list[tuple[str, str]] = []
    for index, edge in enumerate(precedence_raw):
        edge = _require_object(edge, f"chronology.precedence[{index}]")
        _exact_keys(edge, {"before", "after"}, f"chronology.precedence[{index}]")
        before = _require_string(edge["before"], f"chronology.precedence[{index}].before")
        after = _require_string(edge["after"], f"chronology.precedence[{index}].after")
        precedence.append((before, after))

    _assert_acyclic(occurrence_set, precedence)
    expected_precedence = list(zip(ordered_occurrences, ordered_occurrences[1:]))
    if precedence != expected_precedence:
        raise SphereError("chronology precedence must equal the exact adjacent immutable order")

    round_trip = _require_object(data["round_trip"], "round_trip")
    _exact_keys(
        round_trip,
        {"source_ref", "format", "separator", "trailing_newline", "sha256"},
        "round_trip",
    )
    if round_trip["source_ref"] not in source_refs:
        raise SphereError("round_trip.source_ref must reference a declared source")
    if round_trip["format"] != "trail-lines/v1":
        raise SphereError("round_trip.format must be trail-lines/v1")
    if round_trip["separator"] != "\n-> ":
        raise SphereError(r"round_trip.separator must be '\n-> '")
    if round_trip["trailing_newline"] is not True:
        raise SphereError("round_trip requires a trailing newline")
    if not isinstance(round_trip["sha256"], str) or not SHA256.fullmatch(round_trip["sha256"]):
        raise SphereError("round_trip.sha256 must be lowercase 64-hex")

    restored = restore_trail(data)
    restored_sha = hashlib.sha256(restored.encode("utf-8")).hexdigest()
    if restored_sha != round_trip["sha256"]:
        raise SphereError("round-trip reconstruction digest mismatch")

    return data


def restore_trail(data: dict[str, Any]) -> str:
    nodes = {node["occurrence_id"]: node for node in data["nodes"]}
    ordered = [entry["occurrence_id"] for entry in data["chronology"]["entries"]]
    labels = [nodes[occurrence_id]["label"] for occurrence_id in ordered]
    text = data["round_trip"]["separator"].join(labels)
    if data["round_trip"]["trailing_newline"]:
        text += "\n"
    return text


def has_relation(
    data: dict[str, Any],
    from_occurrence: str,
    to_occurrence: str,
    relation_type: str,
) -> bool:
    """Return only an exact declared relation; never infer reverse edges."""
    return any(
        relation["from_occurrence"] == from_occurrence
        and relation["to_occurrence"] == to_occurrence
        and relation["type"] == relation_type
        for relation in data["relations"]
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate a sphere manifest")
    validate.add_argument("manifest")

    restore = sub.add_parser("restore", help="reconstruct the exact declared trail")
    restore.add_argument("manifest")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        data = load_manifest(args.manifest)
        validate_manifest(data)
        if args.command == "validate":
            print(
                f"PASS {data['id']}: "
                f"{len(data['nodes'])} occurrences, "
                f"{len(data['relations'])} typed relations"
            )
        elif args.command == "restore":
            sys.stdout.write(restore_trail(data))
        return 0
    except (OSError, json.JSONDecodeError, SphereError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
