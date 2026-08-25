---
name: yes-but
description: Evolve competing ideas through constructive cross-development, then reality-check the strongest results. Show the user only natural Korean meeting dialogue.
---

# yes-but

Open an idea-evolution session only when a request benefits from alternatives, creative development, or a decision-changing reality check. Answer simple requests directly.

Use single-provider mode by default. Keep the current session as facilitator and synthesizer, then use the host-native agent mechanism to create three independent explorers from the current provider: Codex explorers in a Codex session, Claude explorers in a Claude session. Enter mix mode only when the user explicitly asks for it; assign available Codex and Claude explorers across the round. If independent workers are unavailable, disclose that the meeting cannot run instead of simulating multiple people in one session.

1. The facilitator states the goal, constraints, and success criteria.
2. Diverge with three materially distinct original ideas by default.
3. After independent divergence, the facilitator passes each original to another explorer. Cross-develop every original with `keep`, `but`, and `build`: preserve its strength, name the improvement opportunity, and extend it constructively. A `but` must never be a bare rejection.
4. Evolve every original, then select the strongest evolution, create a hybrid that traces to at least two distinct originals, and create a novel mutation/third option that is neither selection nor restatement.
5. Only after evolution, let the reality reviewer check feasibility, evidence, cost, and risk with the existing claim/evidence decision engine.
6. Recommend the strongest evolved outcome while preserving material uncertainty.

Show only meaningful idea growth in concise, natural Korean. Use the Korean labels `진행자`, `탐험가`, `합성자`, and `현실 검토자`; never show A/B/C identifiers, provider names, internal state, or work logs.

Use [meeting rules](references/meeting-rules.md) for modes and flow, [Korean UI rules](references/korean-ui.md) for visible output, and [decision rules](references/decision-rules.md) for the final reality check. Validate structured evolution handoffs with `scripts/validate_idea_evolution.py`.
