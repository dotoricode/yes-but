#!/usr/bin/env python3
"""Apply deterministic evidence and decision states to meeting claims."""

import json
import sys
from typing import Any


CRITERIA = {
    "fact": ("direct", "current", "corroborated"),
    "proposal": ("feasible", "beneficial", "preferable"),
    "risk": ("likely", "severe", "manageable"),
}
RISK_EXISTENCE_CRITERIA = ("likely", "severe")
MITIGATION_FROM_MANAGEABLE = {True: "대응 가능", False: "대응 어려움", None: "대응 확인 필요"}


EVIDENCE_STATES = ("confirmed", "refuted", "unknown", "conflicting")


def _evidence_state(claim: dict[str, Any], values: list[bool | None]) -> str:
    """Derive evidence conservatively unless an explicit state is supplied."""
    explicit = claim.get("evidence_state")
    if explicit is not None:
        if explicit not in EVIDENCE_STATES:
            raise ValueError("invalid evidence_state")
        return explicit
    if claim.get("conflicting_evidence", False):
        return "conflicting"
    # A failed quality check means the available evidence is weak, indirect, or
    # stale. It is not itself evidence that the claim is false.
    return "confirmed" if all(value is True for value in values) else "unknown"


def _decision_state(evidence_state: str) -> str:
    return {
        "confirmed": "selected",
        "refuted": "excluded",
        "unknown": "pending",
        "conflicting": "disagreement",
    }[evidence_state]


def _assessment_decision(values: list[bool | None]) -> str:
    """Make a kind-specific choice from its assessment without changing evidence."""
    if any(value is False for value in values):
        return "excluded"
    if all(value is True for value in values):
        return "selected"
    return "pending"


def _decision_for(kind: str, evidence_state: str, assessment: dict[str, bool | None]) -> str:
    if kind == "fact":
        return _decision_state(evidence_state)

    criteria = RISK_EXISTENCE_CRITERIA if kind == "risk" else CRITERIA[kind]
    assessment_decision = _assessment_decision([assessment[name] for name in criteria])
    if assessment_decision == "excluded" or evidence_state == "refuted":
        return "excluded"
    if evidence_state == "conflicting":
        return "disagreement"
    if assessment_decision == "pending" or evidence_state == "unknown":
        return "pending"
    return "selected"


def _korean_decision(decision_state: str) -> str:
    return {
        "selected": "채택",
        "excluded": "기각",
        "pending": "추가 확인 필요",
        "disagreement": "이견 유지",
    }[decision_state]


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

    evidence_values = [assessment[name] for name in (RISK_EXISTENCE_CRITERIA if kind == "risk" else criteria)]
    evidence_state = _evidence_state(claim, evidence_values)
    decision_state = _decision_for(kind, evidence_state, assessment)
    result = {
        "id": claim.get("id"),
        "kind": kind,
        "evidence_state": evidence_state,
        "decision_state": decision_state,
        "decision": _korean_decision(decision_state),
        "criteria": list(criteria),
    }
    if kind == "risk":
        mitigation = claim.get("mitigation_state", MITIGATION_FROM_MANAGEABLE[assessment["manageable"]])
        if mitigation not in ("대응 검증됨", "대응 가능", "대응 확인 필요", "대응 어려움"):
            raise ValueError("invalid mitigation_state")
        blocking = claim.get("blocking", False)
        if not isinstance(blocking, bool):
            raise ValueError("blocking must be a boolean")
        result["risk_existence"] = evidence_state
        result["mitigation_state"] = mitigation
        result["blocking"] = blocking
    return result


def _affected_ids(claims: list[dict[str, Any]], changed_ids: list[str] | None) -> set[str] | None:
    ids = {claim["id"] for claim in claims}
    dependents: dict[str, list[str]] = {claim_id: [] for claim_id in ids}
    for claim in claims:
        dependencies = claim.get("depends_on", [])
        if not isinstance(dependencies, list) or not all(isinstance(item, str) and item for item in dependencies):
            raise ValueError("depends_on must be an array of non-empty strings")
        for dependency in dependencies:
            if dependency not in ids:
                raise ValueError("depends_on contains unknown id: " + dependency)
            dependents[dependency].append(claim["id"])

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(claim_id: str) -> None:
        if claim_id in visiting:
            raise ValueError("depends_on contains a cycle")
        if claim_id in visited:
            return
        visiting.add(claim_id)
        for dependent in dependents[claim_id]:
            visit(dependent)
        visiting.remove(claim_id)
        visited.add(claim_id)

    for claim_id in ids:
        visit(claim_id)

    if changed_ids is None:
        return None

    affected = set(changed_ids)
    queue = list(changed_ids)
    while queue:
        current = queue.pop(0)
        for dependent in dependents[current]:
            if dependent not in affected:
                affected.add(dependent)
                queue.append(dependent)
    return affected


def decide(state: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Decide all claims, or a changed claim and all of its dependents in input order."""
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
    if changed_ids is not None:
        unknown = set(changed_ids) - set(ids)
        if unknown:
            raise ValueError("changed_ids contains unknown id: " + sorted(unknown)[0])
    selected = _affected_ids(claims, changed_ids)
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
