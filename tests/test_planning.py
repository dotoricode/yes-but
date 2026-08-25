import unittest

from scripts.planning import plan_review


class ReviewPlanningTests(unittest.TestCase):
    def test_defaults_to_current_session_solo_without_provider_workers(self):
        result = plan_review({})
        self.assertEqual(result["mode"], "solo")
        self.assertEqual(result["synthesizer"], "current-session")
        self.assertEqual([worker["role"] for worker in result["workers"]].count("탐험가"), 3)
        self.assertTrue(all(worker["provider"] == "current-session" for worker in result["workers"]))

    def test_mix_requires_an_explicit_request(self):
        result = plan_review({"capabilities": {"codex": True, "claude": True}})
        self.assertEqual(result["mode"], "solo")

    def test_mix_falls_back_to_available_provider_and_rotates_roles(self):
        fallback = plan_review({"mode": "mix", "capabilities": {"codex": True, "claude": False, "independent_workers": True, "parallel": True}})
        first = plan_review({"mode": "mix", "rotation": 0, "capabilities": {"codex": True, "claude": True, "independent_workers": True, "parallel": True}})
        next_round = plan_review({"mode": "mix", "rotation": 1, "capabilities": {"codex": True, "claude": True, "independent_workers": True, "parallel": True}})
        self.assertEqual(fallback["mode"], "mix")
        self.assertTrue(all(worker["provider"] == "codex" for worker in fallback["workers"]))
        self.assertNotEqual(first["workers"][0]["provider"], next_round["workers"][0]["provider"])
        self.assertEqual(first["review_depth"], "standard")
        self.assertTrue(first["can_run_concurrently"])
        self.assertEqual(plan_review({"review_depth": "deep"})["review_depth"], "deep")

    def test_mix_does_not_assume_independent_workers_or_parallelism(self):
        fallback = plan_review({"mode": "mix", "capabilities": {"codex": True, "claude": True}})
        sequential = plan_review({"mode": "mix", "capabilities": {"codex": True, "claude": True, "independent_workers": True, "parallel": False}})
        self.assertEqual(fallback["mode"], "solo")
        self.assertFalse(fallback["can_run_concurrently"])
        self.assertEqual(sequential["mode"], "mix")
        self.assertFalse(sequential["can_run_concurrently"])
        self.assertIn("Parallel execution is unavailable; reviews run sequentially.", sequential["limitations"])

    def test_required_both_providers_does_not_silently_substitute(self):
        result = plan_review({"mode": "mix", "require_both": True, "capabilities": {"codex": True, "claude": False, "independent_workers": True}})
        self.assertEqual(result["mode"], "unavailable")
        self.assertEqual(result["workers"], [])


if __name__ == "__main__":
    unittest.main()
