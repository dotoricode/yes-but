import json
from pathlib import Path
import subprocess
import sys
import unittest

from scripts.validate_meeting import validate as validate_meeting


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class ExampleCommandLineTests(unittest.TestCase):
    def run_script(self, script_name, payload):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script_name)],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )

    def test_example_state_is_decided_from_the_command_line(self):
        state = json.loads((EXAMPLES / "meeting-state.json").read_text(encoding="utf-8"))

        result = self.run_script("decide.py", state)

        self.assertEqual(result.returncode, 0, result.stderr)
        decisions = json.loads(result.stdout)["decisions"]
        self.assertEqual(
            [(item["id"], item["decision"]) for item in decisions],
            [
                ("rollback-confirmed", "채택"),
                ("deploy-today", "채택"),
                ("rollback-risk", "기각"),
            ],
        )

    def test_example_visible_messages_pass_the_command_line_validator(self):
        messages = json.loads((EXAMPLES / "meeting-ui.json").read_text(encoding="utf-8"))

        result = self.run_script("validate_korean_ui.py", messages)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"violations": []})

    def test_example_idea_evolution_passes_the_command_line_validator(self):
        evolution = json.loads((EXAMPLES / "idea-evolution.json").read_text(encoding="utf-8"))

        result = self.run_script("validate_idea_evolution.py", evolution)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"valid": True})

    def test_visible_attendees_match_actual_workers_and_join_stage(self):
        meeting = json.loads((EXAMPLES / "meeting-ui.json").read_text(encoding="utf-8"))
        evolution = json.loads((EXAMPLES / "idea-evolution.json").read_text(encoding="utf-8"))

        visible = {participant["name"]: participant for participant in meeting["participants"]}
        actual = {participant["name"]: participant for participant in evolution["participants"]}

        self.assertEqual(set(visible), set(actual))
        self.assertEqual(validate_meeting(evolution, meeting), {"valid": True})
        for name, participant in actual.items():
            if participant["joined"] == "initial":
                self.assertEqual(visible[name]["introduced_at"], 0)
            else:
                self.assertGreater(visible[name]["introduced_at"], 0)

    def test_integrated_validator_rejects_a_fabricated_visible_roster(self):
        meeting = json.loads((EXAMPLES / "meeting-ui.json").read_text(encoding="utf-8"))
        evolution = json.loads((EXAMPLES / "idea-evolution.json").read_text(encoding="utf-8"))
        meeting["participants"][0]["name"] = "가짜 참석자"
        for message in meeting["messages"]:
            if message.get("role") == "모순 해결사":
                message["role"] = "가짜 참석자"

        with self.assertRaisesRegex(ValueError, "match the actual"):
            validate_meeting(evolution, meeting)

    def test_integrated_validator_command_accepts_the_examples(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_meeting.py"),
                str(EXAMPLES / "idea-evolution.json"),
                str(EXAMPLES / "meeting-ui.json"),
            ],
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"valid": True})


if __name__ == "__main__":
    unittest.main()
