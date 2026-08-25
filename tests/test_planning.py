import unittest

from scripts.planning import plan_review


class ReviewPlanningTests(unittest.TestCase):
    def test_defaults_to_three_independent_workers_from_current_provider(self):
        result = plan_review({
            "current_provider": "codex",
            "capabilities": {"codex": True, "claude": True, "independent_workers": True, "parallel": True},
        })
        self.assertEqual(result["mode"], "single-provider")
        self.assertEqual(result["synthesizer"], "current-session")
        self.assertEqual([worker["role"] for worker in result["workers"]].count("탐험가"), 3)
        self.assertTrue(all(worker["provider"] == "codex" for worker in result["workers"]))
        self.assertTrue(result["can_run_concurrently"])

    def test_mix_requires_an_explicit_request(self):
        result = plan_review({
            "current_provider": "claude",
            "capabilities": {"codex": True, "claude": True, "independent_workers": True},
        })
        self.assertEqual(result["mode"], "single-provider")
        self.assertTrue(all(worker["provider"] == "claude" for worker in result["workers"]))

    def test_mix_rotates_codex_and_claude(self):
        first = plan_review({"mode": "mix", "rotation": 0, "capabilities": {"codex": True, "claude": True, "independent_workers": True, "parallel": True}})
        next_round = plan_review({"mode": "mix", "rotation": 1, "capabilities": {"codex": True, "claude": True, "independent_workers": True, "parallel": True}})
        self.assertNotEqual(first["workers"][0]["provider"], next_round["workers"][0]["provider"])
        self.assertEqual(first["review_depth"], "standard")
        self.assertTrue(first["can_run_concurrently"])
        self.assertEqual(plan_review({
            "current_provider": "codex",
            "review_depth": "deep",
            "capabilities": {"codex": True, "independent_workers": True},
        })["review_depth"], "deep")

    def test_meeting_does_not_simulate_missing_independent_workers(self):
        same_provider = plan_review({"current_provider": "codex", "capabilities": {"codex": True}})
        mix = plan_review({"mode": "mix", "capabilities": {"codex": True, "claude": True}})
        sequential = plan_review({"mode": "mix", "capabilities": {"codex": True, "claude": True, "independent_workers": True, "parallel": False}})
        self.assertEqual(same_provider["mode"], "unavailable")
        self.assertEqual(same_provider["workers"], [])
        self.assertEqual(mix["mode"], "unavailable")
        self.assertEqual(sequential["mode"], "mix")
        self.assertFalse(sequential["can_run_concurrently"])
        self.assertIn("Parallel execution is unavailable; reviews run sequentially.", sequential["limitations"])

    def test_mix_does_not_silently_substitute_one_provider(self):
        result = plan_review({"mode": "mix", "capabilities": {"codex": True, "claude": False, "independent_workers": True}})
        self.assertEqual(result["mode"], "unavailable")
        self.assertEqual(result["workers"], [])


if __name__ == "__main__":
    unittest.main()
