#!/usr/bin/env python3
"""Apply deterministic, kind-specific decisions to meeting claims."""

import json
import sys
from typing import Any


CRITERIA = {
    "fact": ("direct", "current", "corroborated"),
    "proposal": ("feasible", "beneficial", "preferable"),
    "risk": ("likely", "severe", "manageable"),
}
RISK_EXISTENCE_CRITERIA = ("likely", "severe")
RISK_RESPONSE_STATUSES = {
    True: "대응 가능",
    False: "차단 위험",
    None: "대응 확인 필요",
}


def decide_claim(claim: dict[str, Any]) -> dict[str, Any]:
    """Return a Korean decision code and the criteria used for one claim."""
    kind = claim.get("kind")
    if kind not in CRITERIA:
        raise ValueError("kind must be fact, proposal, or risk")
    assessment = claim.get("assessment")
    if not isinstance(assessment, dict):
        raise ValueError("assessment must be an object")
    criteria = CRITERIA[kind]
    missing = [name for name in criteria if name not in assessment]
    if missing:
        raise ValueError("missing assessment criteria: " + ", ".join(missing))
    values = [assessment[name] for name in criteria]
    if any(value not in (True, False, None) for value in values):
        raise ValueError("assessment criteria must be true, false, or null")

    decision_criteria = RISK_EXISTENCE_CRITERIA if kind == "risk" else criteria
    decision_values = [assessment[name] for name in decision_criteria]
    if claim.get("conflicting_evidence", False):
        decision = "이견 유지"
    elif all(value is True for value in decision_values):
        decision = "채택"
    elif any(value is False for value in decision_values):
        decision = "기각"
    else:
        decision = "추가 확인 필요"
    result = {"id": claim.get("id"), "kind": kind, "decision": decision, "criteria": list(criteria)}
    if kind == "risk":
        result["response_status"] = RISK_RESPONSE_STATUSES[assessment["manageable"]]
    return result


def decide(state: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Decide all claims, or only changed_ids, without changing input order."""
    claims = state.get("claims")
    if not isinstance(claims, list):
        raise ValueError("claims must be an array")
    changed_ids = state.get("changed_ids")
    if changed_ids is not None and (not isinstance(changed_ids, list) or not all(isinstance(item, str) for item in changed_ids)):
        raise ValueError("changed_ids must be an array of strings")
    ids = [claim.get("id") for claim in claims if isinstance(claim, dict)]
    if len(ids) != len(claims) or any(not isinstance(item, str) or not item for item in ids):
        raise ValueError("every claim needs a non-empty string id")
    if len(set(ids)) != len(ids):
        raise ValueError("claim ids must be unique")
    selected = set(changed_ids) if changed_ids is not None else None
    if selected is not None:
        unknown = selected - set(ids)
        if unknown:
            raise ValueError("changed_ids contains unknown id: " + sorted(unknown)[0])
    return {"decisions": [decide_claim(claim) for claim in claims if selected is None or claim["id"] in selected]}


def main() -> int:
    try:
        state = json.load(sys.stdin)
        if not isinstance(state, dict):
            raise ValueError("input must be an object")
        json.dump(decide(state), sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except (json.JSONDecodeError, ValueError) as error:
        print(f"invalid meeting state: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
