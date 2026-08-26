#!/usr/bin/env python3
"""Reject internal or unexplained English text in user-visible meeting messages."""

import json
import re
import sys
from typing import Any


FORBIDDEN_PATTERNS = {
    "영어 상태명": r"(?<![A-Za-z0-9_])(?:accepted|rejected|pending|running|completed|failed|needs[_ -]?confirmation)(?![A-Za-z0-9_])",
    "영어 역할명": r"(?<![A-Za-z0-9_])(?:facilitator|proposer|devil'?s advocate|fact checker|decision maker|explorer|synthesizer|reality reviewer)(?![A-Za-z0-9_])",
    "내부 식별자": r"(?<![A-Za-z0-9_])(?:[A-Z]{1,8}[-_]?\d+|[ABC](?:안|[ -]?\d+)|[ABC](?:[ /,]+[ABC]){1,2}|claim[_-]?\d+|[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12})(?![A-Za-z0-9_])",
    "시스템 이벤트": r"(?<![A-Za-z0-9_])(?:task_started|task_completed|tool_call|model_response|state_changed)(?![A-Za-z0-9_])",
    "모델명": r"(?<![A-Za-z0-9_])(?:gpt-[A-Za-z0-9_.-]+|claude[-A-Za-z0-9_.]*|gemini[-A-Za-z0-9_.]*)(?![A-Za-z0-9_])",
    "내부 데이터 필드": r"(?<![A-Za-z0-9_])(?:changed_ids|claim_id|assessment|conflicting_evidence|decision)(?![A-Za-z0-9_])",
    "내부 역할명": r"(?:탐험가|합성자|현실 검토자)\s*:",
}
FACILITATOR = "진행자"
KOREAN_NAME = re.compile(r"^[가-힣][가-힣 ]{0,19}$")
ENGLISH = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z][A-Za-z0-9'_-]*(?![A-Za-z0-9_])")
URL = re.compile(r"https?://[^\s]+", re.IGNORECASE)
CODE = re.compile(r"`[^`]+`")


def _mask_allowed(text: str, allowed_originals: list[str]) -> str:
    masked = text
    for original in allowed_originals:
        if not isinstance(original, str) or not original:
            raise ValueError("allowed_originals must contain non-empty strings")
        masked = masked.replace(original, " " * len(original))
    return masked


def _mask_structured_content(text: str) -> str:
    """Keep URLs and backtick code out of prose-only English validation."""
    return CODE.sub(lambda match: " " * len(match.group(0)), URL.sub(lambda match: " " * len(match.group(0)), text))


def validate_message(text: str, allowed_originals: list[str] | None = None) -> list[dict[str, str]]:
    if not isinstance(text, str):
        raise ValueError("message text must be a string")
    masked = _mask_structured_content(_mask_allowed(text, allowed_originals or []))
    violations: list[dict[str, str]] = []
    for category, pattern in FORBIDDEN_PATTERNS.items():
        for match in re.finditer(pattern, masked, flags=re.IGNORECASE):
            violations.append({"category": category, "text": match.group(0)})
    covered = [(item["text"].lower(), item["category"]) for item in violations]
    for match in ENGLISH.finditer(masked):
        word = match.group(0)
        if not any(word.lower() in matched for matched, _ in covered):
            violations.append({"category": "설명되지 않은 영문", "text": word})
    return violations


def validate(payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    messages = payload.get("messages")
    if not isinstance(messages, list):
        raise ValueError("messages must be an array")
    global_allowed = payload.get("allowed_originals", [])
    if not isinstance(global_allowed, list):
        raise ValueError("allowed_originals must be an array")
    participants = payload.get("participants")
    if not isinstance(participants, list):
        raise ValueError("participants must be an array")
    if not 3 <= len(participants) <= 6:
        raise ValueError("participants must contain three to five initial attendees and at most one late attendee")
    introduced_at: dict[str, int] = {}
    for participant in participants:
        if not isinstance(participant, dict) or set(participant) != {"name", "focus", "introduced_at"}:
            raise ValueError("each participant needs name, focus, and introduced_at")
        name, focus, joined = participant["name"], participant["focus"], participant["introduced_at"]
        if not isinstance(name, str) or not KOREAN_NAME.fullmatch(name) or name == FACILITATOR:
            raise ValueError("participant name must be a natural Korean display name")
        if name in introduced_at:
            raise ValueError("participant names must be unique")
        if not isinstance(joined, int) or isinstance(joined, bool) or not 0 <= joined <= len(messages):
            raise ValueError("introduced_at must be a valid message index")
        focus_violations = validate_message(focus, global_allowed)
        if focus_violations:
            raise ValueError("participant focus must use natural Korean only")
        introduced_at[name] = joined
    violations = []
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            raise ValueError("each message must be an object")
        if "role" in message:
            role = message["role"]
            if role != FACILITATOR and role not in introduced_at:
                raise ValueError("message role must be the facilitator or an introduced participant")
            if role in introduced_at and introduced_at[role] > index:
                raise ValueError("a participant cannot speak before being introduced")
        local_allowed = message.get("allowed_originals", [])
        if not isinstance(local_allowed, list):
            raise ValueError("message allowed_originals must be an array")
        allowed = global_allowed + local_allowed
        found = validate_message(message.get("text"), allowed)
        violations.extend({"index": index, **item} for item in found)
    return {"violations": violations}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError("input must be an object")
        result = validate(payload)
        json.dump(result, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 1 if result["violations"] else 0
    except (json.JSONDecodeError, ValueError) as error:
        print(f"invalid UI payload: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
