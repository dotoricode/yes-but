---
name: yes-but
description: Generate new options by sending ideas through distinct invention lenses, constructive cross-development, collision, and late reality checks. Use for creative meetings, alternative generation, or idea evolution. Show the user only natural Korean meeting dialogue.
---

# yes-but

Open an idea-evolution session only when a request benefits from alternatives, creative development, or a decision-changing reality check. Answer simple requests directly.

Use single-provider mode by default. Keep the current session as facilitator and synthesizer, then create isolated workers from the current provider. Enter mix mode only when the user explicitly asks for it. If independent workers are unavailable, disclose that the meeting cannot run instead of simulating participants in one session.

Before the meeting, route to an installed companion skill when it can supply primary-source research, a runnable experiment, precise architecture language, or implementation feedback. Read that skill's current `SKILL.md` before using it; names and catalog summaries are not proof of behavior. Follow [companion skill routing](references/companion-skills.md), and never silently invoke a user-invoked skill.

1. Frame the goal, constraints, success criteria, and dominant frame: what the obvious approaches keep observing or assuming.
2. Read the [idea warehouse](references/idea-warehouse.md). Select three thinking operators for a light meeting, four for a normal meeting, or five for a complex meeting. Maximize cognitive distance; never select synonymous operators. Give each selected operator a natural Korean character name and one-line focus.
3. Introduce only the selected participants. Each isolated worker then brainwrites one original without peer outputs, pushing only its assigned operator.
4. Swap lenses. Pass every original to a worker with a different operator and require `keep`, `but`, and `build`. A `but` identifies limited potential and must lead to a constructive build.
5. Collide the two most distant evolved ideas. Create a hybrid that preserves both strengths, then classify further outputs as a variant or a new idea using the novelty gates in the meeting rules.
6. If the pool has plateaued, summon one previously absent operator, introduce that participant at the moment they join, and run one mutation round. Never expose unused candidates.
7. Convert unresolved concepts into knowledge questions instead of rejecting them. Only after evolution, reality-check feasibility, evidence, cost, causality, control boundaries, risk, and falsification. Recommend the strongest surviving outcome while preserving material uncertainty.

Show only meaningful idea growth in concise, natural Korean. Introduce the actual participants and their focus before they speak; show a late participant only from the moment they join. Never show the candidate roster, method names, A/B/C identifiers, provider names, internal state, or work logs.

Use [meeting rules](references/meeting-rules.md) for modes and flow, [Korean UI rules](references/korean-ui.md) for visible output, and [decision rules](references/decision-rules.md) for the final reality check. Validate a completed evolution record and its visible transcript together with `scripts/validate_meeting.py`; this binding prevents invented UI participants from passing as actual workers.
