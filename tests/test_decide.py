import unittest

from scripts.decide import decide, decide_claim


class DecideTests(unittest.TestCase):
    def test_decides_each_kind_by_its_own_criteria(self):
        state = {
            "claims": [
                {"id": "f", "kind": "fact", "assessment": {"direct": True, "current": True, "corroborated": True}},
                {"id": "p", "kind": "proposal", "assessment": {"feasible": True, "beneficial": False, "preferable": True}},
                {"id": "r", "kind": "risk", "assessment": {"likely": None, "severe": True, "manageable": True}},
            ]
        }
        self.assertEqual([item["decision"] for item in decide(state)["decisions"]], ["채택", "기각", "추가 확인 필요"])

    def test_conflicting_evidence_keeps_disagreement(self):
        claim = {"id": "f", "kind": "fact", "conflicting_evidence": True, "assessment": {"direct": True, "current": True, "corroborated": True}}
        self.assertEqual(decide_claim(claim)["decision"], "이견 유지")

    def test_missing_evidence_is_unknown_not_refuted_and_has_a_separate_decision_state(self):
        result = decide_claim({
            "id": "f",
            "kind": "fact",
            "assessment": {"direct": None, "current": True, "corroborated": True},
        })
        self.assertEqual(result["evidence_state"], "unknown")
        self.assertEqual(result["decision_state"], "pending")
        self.assertEqual(result["decision"], "추가 확인 필요")

    def test_indirect_fact_evidence_is_unknown_and_pending_not_refuted(self):
        result = decide_claim({
            "id": "f",
            "kind": "fact",
            "assessment": {"direct": False, "current": True, "corroborated": True},
        })
        self.assertEqual(result["evidence_state"], "unknown")
        self.assertEqual(result["decision_state"], "pending")
        self.assertEqual(result["decision"], "추가 확인 필요")

    def test_explicitly_refuted_fact_is_refuted_and_excluded(self):
        result = decide_claim({
            "id": "f",
            "kind": "fact",
            "evidence_state": "refuted",
            "assessment": {"direct": True, "current": True, "corroborated": True},
        })
        self.assertEqual(result["evidence_state"], "refuted")
        self.assertEqual(result["decision_state"], "excluded")
        self.assertEqual(result["decision"], "기각")

    def test_infeasible_proposal_can_be_excluded_while_evidence_is_unknown(self):
        result = decide_claim({
            "id": "p",
            "kind": "proposal",
            "evidence_state": "unknown",
            "assessment": {"feasible": False, "beneficial": True, "preferable": True},
        })
        self.assertEqual(result["evidence_state"], "unknown")
        self.assertEqual(result["decision_state"], "excluded")

    def test_keeps_risk_existence_mitigation_and_blocking_impact_separate(self):
        claim = {
            "id": "r",
            "kind": "risk",
            "assessment": {"likely": True, "severe": True, "manageable": False},
            "blocking": False,
        }

        result = decide_claim(claim)

        self.assertEqual(result["decision"], "채택")
        self.assertEqual(result["risk_existence"], "confirmed")
        self.assertEqual(result["mitigation_state"], "대응 어려움")
        self.assertFalse(result["blocking"])

    def test_changed_ids_and_transitive_dependents_are_decided_in_input_order(self):
        state = {"changed_ids": ["third", "first"], "claims": [
            {"id": "first", "kind": "fact", "assessment": {"direct": True, "current": True, "corroborated": True}},
            {"id": "second", "kind": "proposal", "depends_on": ["first"], "assessment": {"feasible": True, "beneficial": True, "preferable": True}},
            {"id": "fourth", "kind": "fact", "depends_on": ["second"], "assessment": {"direct": True, "current": True, "corroborated": True}},
            {"id": "third", "kind": "risk", "assessment": {"likely": False, "severe": True, "manageable": True}},
        ]}
        self.assertEqual([item["id"] for item in decide(state)["decisions"]], ["first", "second", "fourth", "third"])

    def test_rejects_unknown_changed_id(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            decide({"changed_ids": ["missing"], "claims": []})

    def test_rejects_unknown_dependency_and_cycles(self):
        claim = {"id": "a", "kind": "fact", "assessment": {"direct": True, "current": True, "corroborated": True}}
        with self.assertRaisesRegex(ValueError, "unknown"):
            decide({"changed_ids": ["a"], "claims": [{**claim, "depends_on": ["missing"]}]})
        with self.assertRaisesRegex(ValueError, "cycle"):
            decide({"claims": [
                {**claim, "depends_on": ["b"]},
                {"id": "b", "kind": "fact", "depends_on": ["a"], "assessment": {"direct": True, "current": True, "corroborated": True}},
            ]})


if __name__ == "__main__":
    unittest.main()
