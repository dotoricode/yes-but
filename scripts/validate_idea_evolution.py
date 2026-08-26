#!/usr/bin/env python3
"""Validate the compact, host-independent idea-evolution handoff."""

import json
import re
import sys
from typing import Any


IDEA_KINDS = {"original", "evolved", "hybrid", "mutation"}
BASE_OUTPUT_KINDS = {"best_evolved_original", "hybrid"}
NOVELTY_FIELDS = {
    "observation_axis",
    "relationship",
    "causal_model",
    "control_boundary",
    "falsifier",
    "irreducibility",
}


def _error(message: str) -> None:
    raise ValueError(message)


def validate(payload: dict[str, Any]) -> dict[str, bool]:
    """Enforce cross-development, lineage, and the three required outputs."""
    if not isinstance(payload, dict):
        _error("idea evolution payload must be an object")
    dominant_frame = payload.get("dominant_frame")
    if not isinstance(dominant_frame, str) or not dominant_frame.strip():
        _error("dominant_frame must be a non-empty string")
    participants = payload.get("participants")
    if not isinstance(participants, list) or not 3 <= len(participants) <= 6:
        _error("participants must contain three to five initial workers and at most one late worker")
    participant_by_name: dict[str, dict[str, str]] = {}
    for participant in participants:
        if (
            not isinstance(participant, dict)
            or set(participant) != {"name", "operator", "joined"}
            or participant.get("joined") not in {"initial", "plateau"}
            or not all(isinstance(participant.get(field), str) and participant[field].strip() for field in ("name", "operator"))
        ):
            _error("each participant needs a name, operator, and valid join stage")
        if participant["name"] in participant_by_name:
            _error("participant names must be unique")
        participant_by_name[participant["name"]] = participant
    if len({participant["operator"] for participant in participants}) != len(participants):
        _error("participant operators must be distinct")
    initial_participants = {name for name, participant in participant_by_name.items() if participant["joined"] == "initial"}
    plateau_participants = {name for name, participant in participant_by_name.items() if participant["joined"] == "plateau"}
    if not 3 <= len(initial_participants) <= 5 or len(plateau_participants) > 1:
        _error("meetings need three to five initial workers and at most one plateau worker")

    ideas = payload.get("ideas")
    reviews = payload.get("reviews")
    outputs = payload.get("outputs")
    reality_checks = payload.get("reality_checks")
    if not all(isinstance(value, list) for value in (ideas, reviews, outputs, reality_checks)):
        _error("ideas, reviews, outputs, and reality_checks must be arrays")

    by_id: dict[str, dict[str, Any]] = {}
    for idea in ideas:
        if not isinstance(idea, dict):
            _error("each idea must be an object")
        idea_id, kind, text, producer = idea.get("id"), idea.get("kind"), idea.get("text"), idea.get("producer")
        if not isinstance(idea_id, str) or not idea_id or idea_id in by_id:
            _error("idea ids must be unique non-empty strings")
        if kind not in IDEA_KINDS or not isinstance(text, str) or not text.strip():
            _error("each idea needs a supported kind and non-empty text")
        parents = idea.get("parents", [])
        if not isinstance(parents, list) or any(not isinstance(parent, str) or not parent for parent in parents):
            _error("idea parents must be non-empty string ids")
        if len(parents) != len(set(parents)):
            _error("idea parents must be distinct")
        if kind == "original" and parents:
            _error("original ideas cannot have parents")
        operator = idea.get("operator")
        if not isinstance(operator, str) or not operator.strip():
            _error("each idea requires the thinking operator that produced it")
        if not isinstance(producer, str) or not producer.strip():
            _error("each idea requires its actual producer")
        if kind in {"original", "evolved", "mutation"}:
            if producer not in participant_by_name or participant_by_name[producer]["operator"] != operator:
                _error("worker-produced ideas must match an actual participant and operator")
            if kind in {"original", "evolved"} and producer not in initial_participants:
                _error("late participants cannot contribute before the plateau")
            if kind == "mutation" and producer not in plateau_participants:
                _error("mutation ideas must come from the late participant")
        elif producer != "facilitator":
            _error("hybrid ideas must be produced by the facilitator")
        if kind == "evolved" and len(parents) != 1:
            _error("evolved ideas need exactly one parent")
        if kind in {"hybrid", "mutation"} and len(parents) < 2:
            _error(f"{kind} ideas need at least two parents")
        classification = idea.get("classification")
        if kind == "original" and classification is not None:
            _error("original ideas are not classified before development")
        if kind == "evolved" and classification != "variant":
            _error("evolved ideas must be classified as variants")
        if kind in {"hybrid", "mutation"} and classification not in {"variant", "new_idea"}:
            _error("hybrid and mutation ideas require a novelty classification")
        if kind == "mutation" and classification != "new_idea":
            _error("mutation ideas must be classified as new ideas")
        if kind == "hybrid" and not isinstance(idea.get("collision_reason"), str):
            _error("hybrid ideas require a collision reason")
        if kind == "hybrid" and not idea["collision_reason"].strip():
            _error("hybrid ideas require a non-empty collision reason")
        if classification == "new_idea":
            novelty = idea.get("novelty")
            if not isinstance(novelty, dict) or set(novelty) != NOVELTY_FIELDS:
                _error("new ideas require all six novelty checks")
            if not all(isinstance(value, str) and value.strip() for value in novelty.values()):
                _error("novelty checks must be non-empty strings")
        by_id[idea_id] = idea

    def ancestors(idea_id: str, trail: set[str] | None = None) -> set[str]:
        if idea_id not in by_id:
            _error(f"unknown idea parent: {idea_id}")
        trail = trail or set()
        if idea_id in trail:
            _error("idea lineage contains a cycle")
        next_trail = trail | {idea_id}
        parents = by_id[idea_id].get("parents", [])
        return {idea_id} | set().union(*(ancestors(parent, next_trail) for parent in parents)) if parents else {idea_id}

    for idea_id in by_id:
        ancestors(idea_id)

    reviewed: set[str] = set()
    for review in reviews:
        if not isinstance(review, dict) or review.get("idea_id") not in by_id:
            _error("each review must name an existing idea")
        if not all(isinstance(review.get(field), str) and review[field].strip() for field in ("keep", "but", "build")):
            _error("each review requires non-empty keep, but, and build")
        if not all(
            isinstance(review.get(field), str) and review[field].strip()
            for field in ("from_operator", "to_operator")
        ):
            _error("each review requires source and destination operators")
        if review["from_operator"] == review["to_operator"]:
            _error("cross-development must swap to a different operator")
        if by_id[review["idea_id"]]["operator"] != review["from_operator"]:
            _error("review source operator must match the original idea")
        reviewer = review.get("reviewer")
        if reviewer not in participant_by_name or participant_by_name[reviewer]["operator"] != review["to_operator"]:
            _error("reviewer must be an actual participant using the destination operator")
        if reviewer not in initial_participants:
            _error("late participants cannot review ideas before the plateau")
        if reviewer == by_id[review["idea_id"]]["producer"]:
            _error("an original must be cross-developed by another participant")
        reviewed.add(review["idea_id"])
    originals = {idea_id for idea_id, idea in by_id.items() if idea["kind"] == "original"}
    original_producers = {by_id[idea_id]["producer"] for idea_id in originals}
    if original_producers != initial_participants or len(originals) != len(initial_participants):
        _error("each initial participant must produce exactly one original idea")
    if not originals <= reviewed:
        _error("each original idea requires keep, but, and build cross-development")
    if len(reviews) != len(originals) or reviewed != originals:
        _error("each original idea requires exactly one cross-development review")

    review_by_idea = {review["idea_id"]: review for review in reviews}
    for original_id in originals:
        evolved = [idea for idea in ideas if idea["kind"] == "evolved" and idea["parents"] == [original_id]]
        if len(evolved) != 1:
            _error("each original idea requires exactly one direct evolved descendant")
        review = review_by_idea[original_id]
        if evolved[0]["producer"] != review["reviewer"] or evolved[0]["operator"] != review["to_operator"]:
            _error("the recorded reviewer must produce the evolved descendant")

    plateau = payload.get("plateau", {"detected": False})
    if not isinstance(plateau, dict) or not isinstance(plateau.get("detected"), bool):
        _error("plateau must record whether idea development stalled")
    expected_output_kinds = set(BASE_OUTPUT_KINDS)
    if plateau["detected"]:
        if set(plateau) != {"detected", "reason", "summoned_participant"}:
            _error("a detected plateau requires a reason and summoned participant")
        summoned = plateau.get("summoned_participant")
        if summoned not in plateau_participants or not isinstance(plateau.get("reason"), str) or not plateau["reason"].strip():
            _error("plateau must summon the recorded late participant")
        expected_output_kinds.add("mutation")
        mutations = [idea for idea in ideas if idea["kind"] == "mutation"]
        if len(mutations) != 1:
            _error("a detected plateau requires exactly one mutation idea")
    else:
        if set(plateau) != {"detected"} or plateau_participants or any(idea["kind"] == "mutation" for idea in ideas):
            _error("an undetected plateau cannot have a late participant or mutation idea")

    selected: dict[str, str] = {}
    for output in outputs:
        if not isinstance(output, dict) or output.get("kind") not in expected_output_kinds:
            _error("outputs must use required output kinds")
        kind, idea_id = output["kind"], output.get("idea_id")
        if kind in selected or idea_id not in by_id:
            _error("each required output kind must select one existing idea")
        selected[kind] = idea_id
    if set(selected) != expected_output_kinds:
        _error("outputs must match the plateau-dependent required kinds")
    if by_id[selected["best_evolved_original"]]["kind"] != "evolved":
        _error("best_evolved_original must select an evolved idea")
    hybrid = by_id[selected["hybrid"]]
    hybrid_roots = ancestors(selected["hybrid"]) & originals
    if hybrid["kind"] != "hybrid" or len(hybrid_roots) < 2:
        _error("hybrid output must combine at least two distinct ideas")
    if plateau["detected"]:
        mutation = by_id[selected["mutation"]]
        summoned = plateau["summoned_participant"]
        if mutation["kind"] != "mutation" or mutation.get("classification") != "new_idea" or mutation["producer"] != summoned:
            _error("a plateau mutation must be a new idea from the summoned participant")
        normalize = lambda text: re.sub(r"[\W_]+", "", text, flags=re.UNICODE).casefold()
        mutation_text = normalize(mutation["text"])
        if any(
            idea_id != selected["mutation"] and normalize(idea["text"]) == mutation_text
            for idea_id, idea in by_id.items()
        ):
            _error("mutation must not restate an existing idea")

    output_idea_ids = set(selected.values())
    checked_ids: set[str] = set()
    for check in reality_checks:
        if not isinstance(check, dict) or set(check) != {"idea_id"}:
            _error("each reality check must contain only an idea_id")
        if check["idea_id"] not in output_idea_ids:
            _error("reality checks can only follow the required evolution outputs")
        checked_ids.add(check["idea_id"])
    if checked_ids != output_idea_ids or len(reality_checks) != len(output_idea_ids):
        _error("each selected output requires exactly one reality check")
    return {"valid": True}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        print(json.dumps(validate(payload), ensure_ascii=False))
        return 0
    except (json.JSONDecodeError, ValueError) as error:
        print(f"invalid idea evolution payload: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
