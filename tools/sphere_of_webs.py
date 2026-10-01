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
ARCH_SCHEMA = "redogit/sphere-architecture-expansion/v1"

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



ARCH_REQUIRED_RULES = {
    "SPHERE != CENTER",
    "CONNECTION != AUTHORITY_TRANSFER",
    "REFERENCE != EVIDENCE_TRANSFER",
    "CURRENTNESS != CHRONOLOGY",
    "DISCOVERY != ADMISSION",
    "DUPLICATE_OCCURRENCE != INDEPENDENT_EVIDENCE",
    "FRONTIER_REFERENCE != INGESTION",
    "TARGET_LOCAL_IMPLEMENTATION != COPIED_IMPLEMENTATION",
    "SEMANTIC_CYCLE != CHRONOLOGY_CYCLE",
    "HOMEWARD_REQUIRES_PINNED_SOURCE",
}

ARCH_CONNECTION_STATES = {
    "CONNECTED_PINNED_REFERENCE",
    "FRONTIER_ADAPTER_REQUIRED",
}

ARCH_ADAPTER_STATES = {
    "DIRECT_PINNED_REFERENCE",
    "ADAPTER_REQUIRED_DO_NOT_INGEST",
}


def _validate_pinned_source(source: dict[str, Any], where: str) -> None:
    _exact_keys(source, {"repository", "path", "ref", "blob_sha", "role"}, where)
    _require_string(source["repository"], f"{where}.repository")
    _require_string(source["path"], f"{where}.path")
    if not isinstance(source["ref"], str) or not SHA40.fullmatch(source["ref"]):
        raise SphereError(f"{where}.ref must be a lowercase 40-hex commit")
    if not isinstance(source["blob_sha"], str) or not SHA40.fullmatch(source["blob_sha"]):
        raise SphereError(f"{where}.blob_sha must be a lowercase 40-hex Git blob")
    _require_string(source["role"], f"{where}.role")


def validate_architecture_manifest(data: dict[str, Any]) -> dict[str, Any]:
    _exact_keys(
        data,
        {
            "schema",
            "id",
            "status",
            "seed",
            "architecture",
            "fragments",
            "connections",
            "rules",
            "claim_ceiling",
        },
        "architecture manifest",
    )
    if data["schema"] != ARCH_SCHEMA:
        raise SphereError(f"architecture schema must be {ARCH_SCHEMA}")
    _require_string(data["id"], "architecture.id")
    if data["status"] != "NAVIGATION_AND_RECONSTRUCTION_ONLY":
        raise SphereError("architecture.status must be NAVIGATION_AND_RECONSTRUCTION_ONLY")
    if data["claim_ceiling"] != "PINNED_NAVIGATION_RELATIONS_AND_ARCHITECTURE_BINDINGS_ONLY":
        raise SphereError("architecture claim ceiling widened")

    seed = _require_object(data["seed"], "architecture.seed")
    _exact_keys(
        seed,
        {
            "schema",
            "id",
            "path",
            "predecessor_head",
            "authority_transfer",
            "evidence_transfer",
        },
        "architecture.seed",
    )
    if seed["schema"] != SCHEMA:
        raise SphereError("architecture seed must bind the sphere-of-webs v1 schema")
    _require_string(seed["id"], "architecture.seed.id")
    _require_string(seed["path"], "architecture.seed.path")
    if not isinstance(seed["predecessor_head"], str) or not SHA40.fullmatch(seed["predecessor_head"]):
        raise SphereError("architecture seed predecessor_head must be a lowercase 40-hex commit")
    if seed["authority_transfer"] is not False or seed["evidence_transfer"] is not False:
        raise SphereError("architecture seed cannot transfer authority or evidence")

    architecture = _require_object(data["architecture"], "architecture")
    _exact_keys(
        architecture,
        {"predecessor_head", "local_authority", "root", "bindings", "axes"},
        "architecture",
    )
    if architecture["predecessor_head"] != seed["predecessor_head"]:
        raise SphereError("architecture predecessor must match the bound sphere seed")
    _require_string(architecture["local_authority"], "architecture.local_authority")
    if architecture["root"] != "NONE":
        raise SphereError("sphere architecture must not establish a root authority")

    bindings = _require_list(architecture["bindings"], "architecture.bindings")
    binding_ids = []
    for index, binding in enumerate(bindings):
        binding = _require_object(binding, f"architecture.bindings[{index}]")
        _exact_keys(binding, {"binding_id", "construct", "role", "source"}, f"architecture.bindings[{index}]")
        binding_ids.append(_require_string(binding["binding_id"], f"architecture.bindings[{index}].binding_id"))
        _require_string(binding["construct"], f"architecture.bindings[{index}].construct")
        _require_string(binding["role"], f"architecture.bindings[{index}].role")
        _validate_pinned_source(
            _require_object(binding["source"], f"architecture.bindings[{index}].source"),
            f"architecture.bindings[{index}].source",
        )
    if len(binding_ids) != len(set(binding_ids)):
        raise SphereError("architecture binding ids must be unique")

    axes = _require_list(architecture["axes"], "architecture.axes")
    axis_ids = []
    chronology_count = 0
    for index, axis in enumerate(axes):
        axis = _require_object(axis, f"architecture.axes[{index}]")
        _exact_keys(
            axis,
            {"id", "purpose", "cycle_policy", "field_directions", "chronology_effect"},
            f"architecture.axes[{index}]",
        )
        axis_id = _require_string(axis["id"], f"architecture.axes[{index}].id")
        axis_ids.append(axis_id)
        _require_string(axis["purpose"], f"architecture.axes[{index}].purpose")
        directions = _require_list(axis["field_directions"], f"architecture.axes[{index}].field_directions")
        if not directions or not all(direction in {"VERTICAL", "LATERAL", "TEMPORAL", "AMBIENT"} for direction in directions):
            raise SphereError("architecture axis has an invalid all-directional mapping")
        if axis_id == "chronology":
            chronology_count += 1
            if axis["cycle_policy"] != "ACYCLIC_REQUIRED":
                raise SphereError("chronology axis must require acyclicity")
            if axis["chronology_effect"] != "IMMUTABLE_ORDERING":
                raise SphereError("chronology axis must remain immutable ordering")
        else:
            if axis["cycle_policy"] != "CYCLES_ALLOWED_NOT_IMPLIED":
                raise SphereError("non-chronology axes must not inherit chronology acyclicity")
            if axis["chronology_effect"] != "NONE":
                raise SphereError("non-chronology axis cannot mutate chronology")
    if chronology_count != 1:
        raise SphereError("architecture must define exactly one chronology axis")
    if len(axis_ids) != len(set(axis_ids)):
        raise SphereError("architecture axis ids must be unique")
    axis_set = set(axis_ids)

    fragments = _require_list(data["fragments"], "fragments")
    fragment_ids = []
    for index, fragment in enumerate(fragments):
        fragment = _require_object(fragment, f"fragments[{index}]")
        _exact_keys(
            fragment,
            {
                "fragment_id",
                "label",
                "axis",
                "relation",
                "connection_state",
                "source_authority",
                "sources",
                "authority_policy",
                "evidence_policy",
                "duplicate_policy",
                "adapter_state",
                "copy_target_local_implementation",
                "infer_reverse",
                "homeward",
                "notes",
            },
            f"fragments[{index}]",
        )
        fragment_id = _require_string(fragment["fragment_id"], f"fragments[{index}].fragment_id")
        fragment_ids.append(fragment_id)
        _require_string(fragment["label"], f"fragments[{index}].label")
        if fragment["axis"] not in axis_set or fragment["axis"] == "chronology":
            raise SphereError("expansion fragments cannot write the chronology axis")
        _require_string(fragment["relation"], f"fragments[{index}].relation")
        if fragment["connection_state"] not in ARCH_CONNECTION_STATES:
            raise SphereError("unsupported architecture fragment connection state")
        _require_string(fragment["source_authority"], f"fragments[{index}].source_authority")
        if fragment["authority_policy"] != "PRESERVE_EACH_SOURCE":
            raise SphereError("fragment must preserve source-local authority")
        _require_string(fragment["evidence_policy"], f"fragments[{index}].evidence_policy")
        _require_string(fragment["duplicate_policy"], f"fragments[{index}].duplicate_policy")
        if fragment["adapter_state"] not in ARCH_ADAPTER_STATES:
            raise SphereError("unsupported architecture fragment adapter state")
        if fragment["copy_target_local_implementation"] is not False:
            raise SphereError("architecture expansion cannot copy target-local implementation")
        if fragment["infer_reverse"] is not False:
            raise SphereError("architecture expansion cannot infer reverse edges")
        _require_string(fragment["notes"], f"fragments[{index}].notes")

        sources = _require_list(fragment["sources"], f"fragments[{index}].sources")
        if not sources:
            raise SphereError("architecture fragment must have at least one pinned source")
        source_paths = set()
        for source_index, pinned in enumerate(sources):
            pinned = _require_object(pinned, f"fragments[{index}].sources[{source_index}]")
            _validate_pinned_source(pinned, f"fragments[{index}].sources[{source_index}]")
            source_paths.add(pinned["path"])

        homeward = _require_object(fragment["homeward"], f"fragments[{index}].homeward")
        _exact_keys(homeward, {"mode", "source_paths"}, f"fragments[{index}].homeward")
        if homeward["mode"] != "PINNED_SOURCE_SET":
            raise SphereError("architecture Homeward must use pinned source sets")
        homeward_paths = _require_list(homeward["source_paths"], f"fragments[{index}].homeward.source_paths")
        if not homeward_paths or set(homeward_paths) != source_paths:
            raise SphereError("architecture Homeward source set must exactly cover fragment sources")

        if fragment["connection_state"] == "FRONTIER_ADAPTER_REQUIRED":
            if fragment["adapter_state"] != "ADAPTER_REQUIRED_DO_NOT_INGEST":
                raise SphereError("frontier fragments must remain adapter-gated")
        elif fragment["adapter_state"] == "ADAPTER_REQUIRED_DO_NOT_INGEST":
            raise SphereError("adapter-gated fragment cannot be active")

    if len(fragment_ids) != len(set(fragment_ids)):
        raise SphereError("architecture fragment ids must be unique")
    fragment_set = set(fragment_ids)

    connections = _require_list(data["connections"], "connections")
    if len(connections) != len(fragments):
        raise SphereError("architecture requires one connection record per fragment")
    connection_ids = []
    connected_targets = set()
    for index, connection in enumerate(connections):
        connection = _require_object(connection, f"connections[{index}]")
        _exact_keys(
            connection,
            {
                "connection_id",
                "from",
                "to",
                "axis",
                "type",
                "active",
                "removable",
                "infer_reverse",
                "authority_transfer",
                "evidence_transfer",
            },
            f"connections[{index}]",
        )
        connection_ids.append(_require_string(connection["connection_id"], f"connections[{index}].connection_id"))
        if connection["from"] != f"sphere:{seed['id']}":
            raise SphereError("architecture connection must originate at the bound sphere seed")
        if connection["to"] not in fragment_set:
            raise SphereError("architecture connection targets unknown fragment")
        connected_targets.add(connection["to"])
        if connection["axis"] not in axis_set or connection["axis"] == "chronology":
            raise SphereError("architecture connection cannot occupy chronology axis")
        _require_string(connection["type"], f"connections[{index}].type")
        if connection["removable"] is not True:
            raise SphereError("architecture connections must be removable")
        if connection["infer_reverse"] is not False:
            raise SphereError("architecture connections cannot infer reverse edges")
        if connection["authority_transfer"] is not False:
            raise SphereError("architecture connections cannot transfer authority")
        if connection["evidence_transfer"] is not False:
            raise SphereError("architecture connections cannot transfer evidence")

        fragment = next(item for item in fragments if item["fragment_id"] == connection["to"])
        if connection["axis"] != fragment["axis"] or connection["type"] != fragment["relation"]:
            raise SphereError("architecture connection must preserve fragment axis and relation type")
        expected_active = fragment["connection_state"] == "CONNECTED_PINNED_REFERENCE"
        if connection["active"] is not expected_active:
            raise SphereError("architecture frontier/active state mismatch")

    if len(connection_ids) != len(set(connection_ids)):
        raise SphereError("architecture connection ids must be unique")
    if connected_targets != fragment_set:
        raise SphereError("architecture connections must cover every fragment exactly once")

    rules = _require_list(data["rules"], "rules")
    if not all(isinstance(rule, str) and rule for rule in rules):
        raise SphereError("architecture rules must be non-empty strings")
    missing_rules = sorted(ARCH_REQUIRED_RULES.difference(rules))
    if missing_rules:
        raise SphereError("architecture rules missing: " + ", ".join(missing_rules))

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

    validate_arch = sub.add_parser("validate-architecture", help="validate a sphere architecture expansion")
    validate_arch.add_argument("manifest")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        data = load_manifest(args.manifest)
        if args.command == "validate-architecture":
            validate_architecture_manifest(data)
            active = sum(1 for connection in data["connections"] if connection["active"])
            frontier = len(data["connections"]) - active
            print(
                f"PASS {data['id']}: "
                f"{active} active pinned fragments, "
                f"{frontier} adapter-gated frontier"
            )
            return 0

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
