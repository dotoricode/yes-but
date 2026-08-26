# yes-but

`yes-but` is a multi-lens idea-evolution skill. It sends one problem through different invention operators, cross-develops the results, and deliberately creates options that were absent at the start. The user sees only concise, natural Korean meeting dialogue.

## How it runs

The pipeline is **Frame → Select → Brainwrite → Lens Swap → Collide → Mutate → Reality Check → Recommend**.

The facilitator first extracts the goal, constraints, and dominant frame. It selects three to five semantically distant operators from the hidden idea warehouse and assigns each one to an isolated worker. Workers brainwrite without seeing peer outputs. Every original then passes through a different operator with three required fields: `keep` preserves a concrete strength, `but` identifies limited potential, and `build` supplies the next development. The two most distant evolved ideas collide into a hybrid. If the pool plateaus, one previously absent operator joins for a mutation round.

Only then does the current session check feasibility, evidence, cost, causality, control boundaries, risk, and falsification. `scripts/decide.py` remains the final claim/evidence decision engine. `scripts/validate_idea_evolution.py` enforces the dominant frame, actual workers, operator swaps, lineage, collision rationale, novelty gates, plateau records, and required outputs. `scripts/validate_meeting.py` binds that execution record to the visible transcript so invented attendees cannot pass independently.

Single-provider mode is the default. The current session facilitates and synthesizes while the host creates isolated workers from the same provider: Codex in a Codex session or Claude in a Claude session. Mix mode requires an explicit request, independent-worker support, and both providers. Missing worker support makes the meeting unavailable; the skill never substitutes same-session role-play. Provider execution remains host-dependent.

## Korean UI

Only meaningful idea growth is visible. Character names are derived from the selected operator, such as `뒤집기 대장`, `연결 장인`, or `가설 탐정`; there is no fixed cast. The opening introduces only actual participants. A late participant appears under `추가 참석` immediately before speaking. The candidate pool, method names, A/B/C labels, provider names, identifiers, statuses, and logs never appear in the UI.

For changeable facts, the skill separates published claims, account-visible conditions, and operational results. Repetition of one source does not become corroboration. The skill can also route to installed Matt Pocock model-invoked skills for primary-source research, runnable prototypes, architecture vocabulary, and implementation feedback; user-invoked orchestrators are only suggested, never called silently.

## Install

Install a real copy of the skill files. Do not use a symbolic link.

For Codex, copy this directory to `~/.agents/skills/yes-but`:

```sh
mkdir -p ~/.agents/skills
cp -R /path/to/yes-but ~/.agents/skills/yes-but
```

For Claude Code, copy this directory to `~/.claude/skills/yes-but`:

```sh
mkdir -p ~/.claude/skills
cp -R /path/to/yes-but ~/.claude/skills/yes-but
```

## Test

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_idea_evolution.py < examples/idea-evolution.json
python3 scripts/validate_korean_ui.py < examples/meeting-ui.json
python3 scripts/validate_meeting.py examples/idea-evolution.json examples/meeting-ui.json
```
