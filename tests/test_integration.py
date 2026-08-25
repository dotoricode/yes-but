import json
from pathlib import Path
import subprocess
import sys
import unittest


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


if __name__ == "__main__":
    unittest.main()
