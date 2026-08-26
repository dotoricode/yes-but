#!/usr/bin/env python3
"""Validate an idea-evolution record and its user-visible meeting together."""

import json
from pathlib import Path
import sys
from typing import Any

try:
    from .validate_idea_evolution import validate as validate_evolution
    from .validate_korean_ui import validate as validate_ui
except ImportError:
    from validate_idea_evolution import validate as validate_evolution
    from validate_korean_ui import validate as validate_ui


def validate(evolution: dict[str, Any], ui: dict[str, Any]) -> dict[str, bool]:
    validate_evolution(evolution)
    ui_result = validate_ui(ui)
    if ui_result["violations"]:
        raise ValueError("user-visible meeting contains Korean UI violations")

    actual = {participant["name"]: participant["joined"] for participant in evolution["participants"]}
    visible = {
        participant["name"]: "initial" if participant["introduced_at"] == 0 else "plateau"
        for participant in ui["participants"]
    }
    if actual != visible:
        raise ValueError("visible participants and join stages must match the actual evolution workers")
    return {"valid": True}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: validate_meeting.py EVOLUTION_JSON UI_JSON", file=sys.stderr)
        return 2
    try:
        evolution = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        ui = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        print(json.dumps(validate(evolution, ui), ensure_ascii=False))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"invalid meeting: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
