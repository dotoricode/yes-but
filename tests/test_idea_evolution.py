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

    def test_requires_a_real_lens_swap(self):
        payload = copy.deepcopy(self.payload)
        payload["reviews"][0]["to_operator"] = payload["reviews"][0]["from_operator"]
        with self.assertRaisesRegex(ValueError, "different operator"):
            validate(payload)

    def test_requires_a_novel_distinct_mutation(self):
        payload = copy.deepcopy(self.payload)
        payload["ideas"][-1].pop("novelty")
        with self.assertRaisesRegex(ValueError, "six novelty"):
            validate(payload)

        payload = copy.deepcopy(self.payload)
        payload["ideas"][-1]["text"] = payload["ideas"][0]["text"]
        with self.assertRaisesRegex(ValueError, "must not restate"):
            validate(payload)

    def test_plateau_mutation_may_honestly_remain_a_variant(self):
        payload = copy.deepcopy(self.payload)
        mutation = next(idea for idea in payload["ideas"] if idea["kind"] == "mutation")
        mutation["classification"] = "variant"
        mutation.pop("novelty")
        self.assertEqual(validate(payload), {"valid": True})

    def test_lens_swap_may_create_a_genuinely_new_idea(self):
        payload = copy.deepcopy(self.payload)
        evolved = next(idea for idea in payload["ideas"] if idea["id"] == "direct-checked")
        evolved["classification"] = "new_idea"
        evolved["novelty"] = copy.deepcopy(next(idea for idea in payload["ideas"] if idea["kind"] == "mutation")["novelty"])
        self.assertEqual(validate(payload), {"valid": True})

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

    def test_hybrid_records_why_distant_ideas_were_collided(self):
        payload = copy.deepcopy(self.payload)
        hybrid = next(idea for idea in payload["ideas"] if idea["kind"] == "hybrid")
        hybrid["collision_reason"] = ""
        with self.assertRaisesRegex(ValueError, "collision reason"):
            validate(payload)

    def test_detected_plateau_requires_a_new_operator(self):
        payload = copy.deepcopy(self.payload)
        payload["plateau"] = {"detected": True}
        with self.assertRaisesRegex(ValueError, "reason and summoned"):
            validate(payload)

    def test_no_plateau_requires_no_late_worker_or_mutation(self):
        payload = copy.deepcopy(self.payload)
        payload["participants"] = [item for item in payload["participants"] if item["joined"] == "initial"]
        payload["ideas"] = [idea for idea in payload["ideas"] if idea["kind"] != "mutation"]
        payload["outputs"] = [output for output in payload["outputs"] if output["kind"] != "mutation"]
        payload["reality_checks"] = [
            check for check in payload["reality_checks"] if check["idea_id"] != "same-path-preview"
        ]
        payload["plateau"] = {"detected": False}
        self.assertEqual(validate(payload), {"valid": True})

    def test_late_worker_cannot_contribute_before_plateau(self):
        payload = copy.deepcopy(self.payload)
        evolved = next(idea for idea in payload["ideas"] if idea["id"] == "direct-checked")
        evolved["producer"] = "대가 회계사"
        evolved["operator"] = "causal-residue"
        with self.assertRaisesRegex(ValueError, "before the plateau"):
            validate(payload)

    def test_each_initial_worker_produces_exactly_one_original(self):
        payload = copy.deepcopy(self.payload)
        duplicate = copy.deepcopy(next(idea for idea in payload["ideas"] if idea["id"] == "direct"))
        duplicate["id"] = "direct-again"
        payload["ideas"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "exactly one original"):
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
        payload["ideas"][3]["parents"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "unknown idea parent"):
            validate(payload)

    def test_reality_checks_only_target_completed_evolution_outputs(self):
        payload = copy.deepcopy(self.payload)
        payload["reality_checks"] = [copy.deepcopy(payload["reality_checks"][0])]
        payload["reality_checks"][0]["idea_id"] = "direct"
        with self.assertRaisesRegex(ValueError, "only follow"):
            validate(payload)

    def test_reality_checks_require_substantive_quality_findings(self):
        payload = copy.deepcopy(self.payload)
        payload["reality_checks"][0]["evidence"] = ""
        with self.assertRaisesRegex(ValueError, "non-empty"):
            validate(payload)
