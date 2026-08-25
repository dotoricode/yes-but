import unittest

from scripts.validate_korean_ui import validate, validate_message


class KoreanUiValidationTests(unittest.TestCase):
    def test_allows_natural_korean_message(self):
        result = validate({"messages": [{"text": "근거가 부족하므로 추가 확인이 필요합니다."}]})
        self.assertEqual(result["violations"], [])

    def test_reports_each_forbidden_display_item(self):
        text = "Facilitator: C01은 accepted입니다. task_started 뒤 gpt-4o가 changed_ids를 보냈습니다."
        categories = {item["category"] for item in validate_message(text)}
        self.assertTrue({"영어 역할명", "영어 상태명", "내부 식별자", "시스템 이벤트", "모델명", "내부 데이터 필드"} <= categories)

    def test_reports_unexplained_english_and_allows_only_explicit_original(self):
        self.assertTrue(validate_message("다음 sprint를 시작합니다."))
        self.assertEqual(validate_message("사용자가 OpenAI API 사용을 요청했습니다.", ["OpenAI API"]), [])

    def test_rejects_invalid_message_shape(self):
        with self.assertRaisesRegex(ValueError, "string"):
            validate({"messages": [{"text": None}]})
        with self.assertRaisesRegex(ValueError, "allowed_originals"):
            validate({"messages": [{"text": "문장", "allowed_originals": "제품명"}]})


if __name__ == "__main__":
    unittest.main()
