#!/usr/bin/env python3
"""Validate the compact, host-independent idea-evolution handoff."""

import json
import re
import sys
from typing import Any


IDEA_KINDS = {"original", "evolved", "hybrid", "mutation"}
OUTPUT_KINDS = {"best_evolved_original", "hybrid", "mutation"}


def _error(message: str) -> None:
    raise ValueError(message)


def validate(payload: dict[str, Any]) -> dict[str, bool]:
    """Enforce cross-development, lineage, and the three required outputs."""
    if not isinstance(payload, dict):
        _error("idea evolution payload must be an object")
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
        idea_id, kind, text = idea.get("id"), idea.get("kind"), idea.get("text")
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
        if kind == "evolved" and len(parents) != 1:
            _error("evolved ideas need exactly one parent")
        if kind in {"hybrid", "mutation"} and len(parents) < 2:
            _error(f"{kind} ideas need at least two parents")
        if kind == "mutation" and not idea.get("novelty"):
            _error("mutation ideas require a novelty statement")
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
        reviewed.add(review["idea_id"])
    originals = {idea_id for idea_id, idea in by_id.items() if idea["kind"] == "original"}
    if len(originals) < 2:
        _error("idea evolution requires at least two original ideas")
    if not originals <= reviewed:
        _error("each original idea requires keep, but, and build cross-development")
    if len(reviews) != len(originals) or reviewed != originals:
        _error("each original idea requires exactly one cross-development review")

    evolved_roots = {
        idea["parents"][0]
        for idea in ideas
        if idea["kind"] == "evolved" and idea["parents"][0] in originals
    }
    if evolved_roots != originals:
        _error("each original idea requires an evolved descendant")

    selected: dict[str, str] = {}
    for output in outputs:
        if not isinstance(output, dict) or output.get("kind") not in OUTPUT_KINDS:
            _error("outputs must use required output kinds")
        kind, idea_id = output["kind"], output.get("idea_id")
        if kind in selected or idea_id not in by_id:
            _error("each required output kind must select one existing idea")
        selected[kind] = idea_id
    if set(selected) != OUTPUT_KINDS:
        _error("outputs require best_evolved_original, hybrid, and mutation")
    if by_id[selected["best_evolved_original"]]["kind"] != "evolved":
        _error("best_evolved_original must select an evolved idea")
    hybrid = by_id[selected["hybrid"]]
    mutation = by_id[selected["mutation"]]
    hybrid_roots = ancestors(selected["hybrid"]) & originals
    if hybrid["kind"] != "hybrid" or len(hybrid_roots) < 2:
        _error("hybrid output must combine at least two distinct ideas")
    if (
        mutation["kind"] != "mutation"
        or not isinstance(mutation.get("novelty"), str)
        or not mutation["novelty"].strip()
    ):
        _error("mutation output must be a novel third option")
    if selected["mutation"] in {selected["best_evolved_original"], selected["hybrid"]}:
        _error("mutation must be a distinct third option")
    normalize = lambda text: re.sub(r"[\W_]+", "", text, flags=re.UNICODE).casefold()
    mutation_text = normalize(mutation["text"])
    if any(
        idea_id != selected["mutation"] and normalize(idea["text"]) == mutation_text
        for idea_id, idea in by_id.items()
    ):
        _error("mutation must not restate an existing idea")

    output_idea_ids = set(selected.values())
    for check in reality_checks:
        if not isinstance(check, dict) or set(check) != {"idea_id"}:
            _error("each reality check must contain only an idea_id")
        if check["idea_id"] not in output_idea_ids:
            _error("reality checks can only follow the required evolution outputs")
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
