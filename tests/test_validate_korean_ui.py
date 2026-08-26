import unittest

from scripts.validate_korean_ui import validate, validate_message


class KoreanUiValidationTests(unittest.TestCase):
    def payload(self, messages):
        return {
            "participants": [
                {"name": "뒤집기 대장", "focus": "전제 뒤집기", "introduced_at": 0},
                {"name": "연결 장인", "focus": "다른 분야 연결하기", "introduced_at": 0},
                {"name": "가설 탐정", "focus": "원인 추리하기", "introduced_at": 0},
            ],
            "messages": messages,
        }

    def test_allows_natural_korean_message(self):
        result = validate(self.payload([{"text": "근거가 부족하므로 추가 확인이 필요합니다."}]))
        self.assertEqual(result["violations"], [])

    def test_reports_each_forbidden_display_item(self):
        text = "Facilitator: C01은 accepted입니다. task_started 뒤 gpt-4o가 changed_ids를 보냈습니다."
        categories = {item["category"] for item in validate_message(text)}
        self.assertTrue({"영어 역할명", "영어 상태명", "내부 식별자", "시스템 이벤트", "모델명", "내부 데이터 필드"} <= categories)

    def test_reports_unexplained_english_and_allows_only_explicit_original(self):
        self.assertTrue(validate_message("다음 sprint를 시작합니다."))
        self.assertEqual(validate_message("사용자가 OpenAI API 사용을 요청했습니다.", ["OpenAI API"]), [])

    def test_allows_urls_and_backtick_code_but_requires_explicit_product_preservation(self):
        self.assertEqual(validate_message("문서는 https://example.com/API 에 있고 `git status`로 확인합니다."), [])
        self.assertTrue(validate_message("OpenAI API로 확인합니다."))

    def test_rejects_invalid_message_shape(self):
        with self.assertRaisesRegex(ValueError, "string"):
            validate(self.payload([{"text": None}]))
        with self.assertRaisesRegex(ValueError, "allowed_originals"):
            validate(self.payload([{"text": "문장", "allowed_originals": "제품명"}]))

    def test_rejects_unintroduced_role_and_idea_identifiers(self):
        with self.assertRaisesRegex(ValueError, "introduced participant"):
            validate(self.payload([{"role": "제안자", "text": "새 방향을 제안합니다."}]))
        self.assertTrue(validate_message("A안은 더 검토하겠습니다."))
        self.assertTrue(validate_message("A / B / C 중 하나를 고르겠습니다."))

    def test_accepts_dynamic_participants_and_facilitator(self):
        payload = {
            "participants": [
                {"name": "뒤집기 대장", "focus": "당연한 전제를 반대로 뒤집기", "introduced_at": 0},
                {"name": "연결 장인", "focus": "다른 분야의 해결 원리 연결하기", "introduced_at": 0},
                {"name": "가설 탐정", "focus": "관측에서 가능한 원인 추리하기", "introduced_at": 0},
            ],
            "messages": [
                {"role": "진행자", "text": "오늘 함께 생각할 분들을 소개합니다."},
                {"role": "뒤집기 대장", "text": "질문의 전제를 반대로 보겠습니다."},
            ],
        }
        self.assertEqual(validate(payload), {"violations": []})

    def test_rejects_participant_speaking_before_late_introduction(self):
        payload = {
            "participants": [
                {"name": "뒤집기 대장", "focus": "전제 뒤집기", "introduced_at": 0},
                {"name": "연결 장인", "focus": "다른 분야 연결하기", "introduced_at": 0},
                {"name": "대가 회계사", "focus": "숨긴 대가 추적하기", "introduced_at": 2},
            ],
            "messages": [
                {"role": "대가 회계사", "text": "치른 비용을 살펴보겠습니다."},
                {"role": "진행자", "text": "새 관점을 더하겠습니다."},
                {"role": "진행자", "text": "이제 추가 참석자를 소개합니다."},
            ],
        }
        with self.assertRaisesRegex(ValueError, "before being introduced"):
            validate(payload)

    def test_requires_an_actual_participant_roster(self):
        with self.assertRaisesRegex(ValueError, "participants"):
            validate({"messages": [{"role": "진행자", "text": "회의를 시작합니다."}]})

    def test_rejects_internal_role_labels_in_visible_text(self):
        categories = {item["category"] for item in validate_message("탐험가: 새 방향을 제안합니다.")}
        self.assertIn("내부 역할명", categories)


if __name__ == "__main__":
    unittest.main()
