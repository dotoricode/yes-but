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

    def test_adopts_unmanageable_severe_likely_risk_as_blocking_risk(self):
        claim = {
            "id": "r",
            "kind": "risk",
            "assessment": {"likely": True, "severe": True, "manageable": False},
        }

        result = decide_claim(claim)

        self.assertEqual(result["decision"], "채택")
        self.assertEqual(result["response_status"], "차단 위험")

    def test_changed_ids_only_decides_changed_claims_in_input_order(self):
        state = {"changed_ids": ["third", "first"], "claims": [
            {"id": "first", "kind": "fact", "assessment": {"direct": True, "current": True, "corroborated": True}},
            {"id": "second", "kind": "proposal", "assessment": {"feasible": True, "beneficial": True, "preferable": True}},
            {"id": "third", "kind": "risk", "assessment": {"likely": False, "severe": True, "manageable": True}},
        ]}
        self.assertEqual([item["id"] for item in decide(state)["decisions"]], ["first", "third"])

    def test_rejects_unknown_changed_id(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            decide({"changed_ids": ["missing"], "claims": []})


if __name__ == "__main__":
    unittest.main()
