# Multi-Lens Idea Evolution Rules

## Runtime modes

- Single-provider mode is the default. The current session facilitates and synthesizes; the host creates three to five isolated workers from that session's provider.
- Mix mode requires an explicit user request, confirmed `independent_workers` capability, and both Codex and Claude. Rotate provider assignments each round.
- The facilitator mediates communication: workers receive the same goal and dominant frame without peer outputs, return originals, then receive another worker's original and a different operator for cross-development.
- Run independent work concurrently only when `parallel` is confirmed. Sequential workers remain independent when their contexts are isolated.
- If the required independent workers are unavailable, report that the meeting cannot run. Never replace them with multiple personas in the current session.
- Use host-native agent tools. Do not simulate providers or shell out to provider command-line tools.
- Keep review intent portable: only `standard` or `deep`. Cross-provider execution is host-dependent and unverified.

## Selection

Extract the dominant frame before selecting participants. State it positively as the observation axis or assumption that obvious solutions share.

Choose operators by semantic distance, not popularity. Use three workers for a light meeting, four for a normal meeting, and five only when the problem has multiple independent dimensions. More workers are not a substitute for more distinct operators.

Derive a concise Korean character name from each selected operator, such as `모순 박사`, `뒤집기 대장`, `연결 장인`, `조합 셰프`, `가설 탐정`, or `대가 회계사`. These are examples, not a fixed cast. A visible participant must correspond to an actual isolated worker. The current session may speak as `진행자`; do not invent a participant for facilitation or reality review.

## Flow

1. Brainwrite: workers independently generate originals through their assigned operators.
2. Lens Swap: every original receives a different operator and non-empty `keep`, `but`, and `build` fields.
3. Collision: select the two most distant evolved ideas and record why their frames differ before hybridizing them.
4. Novelty Gate: label a variable or implementation swap as `variant`. Label an output `new_idea` only when it states a changed observation axis, new relationship, causal account, control boundary, falsifier, and why it cannot reduce to an earlier idea.
5. Plateau: declare a plateau only when outputs repeat the same frame, introduce no new observation or relationship, or remain blocked by the same limitation. Summon one absent operator and run one mutation round; introduce that worker only when it joins.
6. Concept-Knowledge Expansion: keep unsupported but coherent concepts as knowledge questions. Research only questions capable of changing selection, then revise the concepts.
7. Reality Check: assess feasibility, evidence, cost, causality, control boundaries, risk, and falsification only after evolution. Use `decide.py` for final routing and `decision-rules.md` for changeable facts.
8. Recommend: retain material disagreement and uncertainty rather than manufacturing consensus.

Stop after two rounds, or earlier when no meaningful idea growth or decision-changing reality evidence remains.
