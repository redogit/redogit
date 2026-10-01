from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import sphere_of_webs as sphere  # noqa: E402

MANIFEST = ROOT / "sphere-of-webs" / "pr52-continuity-successor-2026-09-30.json"

EXPECTED_LABELS = [
    "Word Carrier native occurrence",
    "native AnyInvocation export",
    "AnyFunctor / Decision Field",
    "continuity receipt",
    "Orbit Reflow persistence/retrieval",
    "Homeward",
]
EXPECTED_TRAIL = (
    "Word Carrier native occurrence\n"
    "-> native AnyInvocation export\n"
    "-> AnyFunctor / Decision Field\n"
    "-> continuity receipt\n"
    "-> Orbit Reflow persistence/retrieval\n"
    "-> Homeward\n"
)
SEED_HEAD = "eda709f1ea361cd298cda9700f846ada23a9fb6a"


class SphereOfWebsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.canonical = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def fresh(self):
        return copy.deepcopy(self.canonical)

    def update_round_trip_digest(self, data):
        data["round_trip"]["sha256"] = hashlib.sha256(
            sphere.restore_trail(data).encode("utf-8")
        ).hexdigest()

    def test_seed_is_exact_pr52_trail_only(self):
        data = self.fresh()
        sphere.validate_manifest(data)

        labels = [node["label"] for node in data["nodes"]]
        self.assertEqual(labels, EXPECTED_LABELS)
        self.assertEqual(len(data["nodes"]), 6)
        self.assertEqual(len(data["relations"]), 5)
        self.assertEqual(
            data["source_refs"]["pr52-continuity-section-1"]["head_sha"],
            SEED_HEAD,
        )
        self.assertTrue(
            all(
                relation["type"] == "EXECUTED_TRAIL_SUCCESSOR"
                for relation in data["relations"]
            )
        )
        self.assertEqual(
            [
                (relation["from_occurrence"], relation["to_occurrence"])
                for relation in data["relations"]
            ],
            list(
                zip(
                    [node["occurrence_id"] for node in data["nodes"]],
                    [node["occurrence_id"] for node in data["nodes"]][1:],
                )
            ),
        )

    def test_exact_round_trip_reconstructs_original_trail(self):
        data = self.fresh()
        sphere.validate_manifest(data)
        self.assertEqual(sphere.restore_trail(data), EXPECTED_TRAIL)

    def test_reversed_edge_is_not_inferred(self):
        data = self.fresh()
        sphere.validate_manifest(data)
        relation = data["relations"][0]
        self.assertTrue(
            sphere.has_relation(
                data,
                relation["from_occurrence"],
                relation["to_occurrence"],
                relation["type"],
            )
        )
        self.assertFalse(
            sphere.has_relation(
                data,
                relation["to_occurrence"],
                relation["from_occurrence"],
                relation["type"],
            )
        )

    def test_duplicate_semantic_object_occurrences_are_preserved(self):
        data = self.fresh()
        duplicate = copy.deepcopy(data["nodes"][0])
        duplicate["occurrence_id"] = "counterprobe:duplicate-occurrence"
        duplicate["label"] = "Word Carrier native occurrence"
        data["nodes"].append(duplicate)

        last = data["chronology"]["entries"][-1]["occurrence_id"]
        data["chronology"]["entries"].append(
            {"ordinal": len(data["chronology"]["entries"]), "occurrence_id": duplicate["occurrence_id"]}
        )
        data["chronology"]["precedence"].append(
            {"before": last, "after": duplicate["occurrence_id"]}
        )
        data["relations"].append(
            {
                "relation_id": "counterprobe:duplicate-relation",
                "axis": "semantic_ancestry",
                "from_occurrence": last,
                "to_occurrence": duplicate["occurrence_id"],
                "type": "COUNTERPROBE_TRAIL_SUCCESSOR",
                "source_ref": "pr52-continuity-section-1",
                "infer_reverse": False,
                "authority_transfer": False,
                "evidence_transfer": False,
            }
        )
        self.update_round_trip_digest(data)

        sphere.validate_manifest(data)
        same_semantic = [
            node["occurrence_id"]
            for node in data["nodes"]
            if node["semantic_object_id"] == data["nodes"][0]["semantic_object_id"]
        ]
        self.assertEqual(
            same_semantic,
            [
                data["nodes"][0]["occurrence_id"],
                "counterprobe:duplicate-occurrence",
            ],
        )

    def test_forged_authority_transfer_is_rejected(self):
        data = self.fresh()
        data["relations"][0]["authority_transfer"] = True
        with self.assertRaisesRegex(sphere.SphereError, "cannot transfer authority"):
            sphere.validate_manifest(data)

    def test_forged_evidence_transfer_is_rejected(self):
        data = self.fresh()
        data["relations"][0]["evidence_transfer"] = True
        with self.assertRaisesRegex(sphere.SphereError, "cannot transfer evidence"):
            sphere.validate_manifest(data)

    def test_chronology_cycle_injection_is_rejected(self):
        data = self.fresh()
        first = data["chronology"]["entries"][0]["occurrence_id"]
        last = data["chronology"]["entries"][-1]["occurrence_id"]
        data["chronology"]["precedence"].append({"before": last, "after": first})
        with self.assertRaisesRegex(sphere.SphereError, "chronology must be acyclic"):
            sphere.validate_manifest(data)

    def test_semantic_cycle_is_allowed_without_chronology_cycle(self):
        data = self.fresh()
        first = data["chronology"]["entries"][0]["occurrence_id"]
        last = data["chronology"]["entries"][-1]["occurrence_id"]
        data["relations"].append(
            {
                "relation_id": "counterprobe:semantic-cycle",
                "axis": "semantic_ancestry",
                "from_occurrence": last,
                "to_occurrence": first,
                "type": "COUNTERPROBE_HOMEWARD_RELATION",
                "source_ref": "pr52-continuity-section-1",
                "infer_reverse": False,
                "authority_transfer": False,
                "evidence_transfer": False,
            }
        )
        sphere.validate_manifest(data)
        self.assertTrue(
            sphere.has_relation(
                data, last, first, "COUNTERPROBE_HOMEWARD_RELATION"
            )
        )


if __name__ == "__main__":
    unittest.main()
