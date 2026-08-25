import copy
import json
from pathlib import Path
import unittest

from scripts.validate_idea_evolution import validate


ROOT = Path(__file__).resolve().parents[1]


class IdeaEvolutionValidationTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT / "examples" / "idea-evolution.json").read_text(encoding="utf-8"))

    def test_accepts_lineage_and_required_evolution_outputs(self):
        self.assertEqual(validate(self.payload), {"valid": True})

    def test_requires_constructive_cross_development_for_every_original(self):
        payload = copy.deepcopy(self.payload)
        payload["reviews"].pop()
        with self.assertRaisesRegex(ValueError, "keep, but, and build"):
            validate(payload)

    def test_requires_a_novel_distinct_mutation(self):
        payload = copy.deepcopy(self.payload)
        payload["ideas"][-1].pop("novelty")
        with self.assertRaisesRegex(ValueError, "novelty"):
            validate(payload)

        payload = copy.deepcopy(self.payload)
        payload["ideas"][-1]["text"] = payload["ideas"][0]["text"]
        with self.assertRaisesRegex(ValueError, "must not restate"):
            validate(payload)

        payload = copy.deepcopy(self.payload)
        payload["ideas"][-1]["text"] = "Deploy the requested change today!"
        with self.assertRaisesRegex(ValueError, "must not restate"):
            validate(payload)

    def test_hybrid_requires_two_distinct_original_roots(self):
        payload = copy.deepcopy(self.payload)
        hybrid = next(idea for idea in payload["ideas"] if idea["kind"] == "hybrid")
        hybrid["parents"] = ["direct", "direct-checked"]
        with self.assertRaisesRegex(ValueError, "two distinct ideas"):
            validate(payload)

    def test_every_original_requires_an_evolved_descendant(self):
        payload = copy.deepcopy(self.payload)
        payload["ideas"] = [idea for idea in payload["ideas"] if idea["id"] != "gradual-observed"]
        hybrid = next(idea for idea in payload["ideas"] if idea["kind"] == "hybrid")
        hybrid["parents"] = ["direct-checked", "gradual"]
        with self.assertRaisesRegex(ValueError, "evolved descendant"):
            validate(payload)

    def test_rejects_broken_lineage(self):
        payload = copy.deepcopy(self.payload)
        payload["ideas"][2]["parents"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "unknown idea parent"):
            validate(payload)

    def test_reality_checks_only_target_completed_evolution_outputs(self):
        payload = copy.deepcopy(self.payload)
        payload["reality_checks"] = [{"idea_id": "direct"}]
        with self.assertRaisesRegex(ValueError, "only follow"):
            validate(payload)
