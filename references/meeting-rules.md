# Idea Evolution Rules

## Runtime modes

- Single-provider mode is the default. The current session facilitates and synthesizes; the host creates three independent explorers from that session's provider.
- Mix mode requires an explicit user request, confirmed `independent_workers` capability, and both Codex and Claude. Rotate provider assignments each round.
- The facilitator mediates communication: explorers receive the same goal without peer outputs, return originals, then receive another explorer's original for cross-development.
- Run independent work concurrently only when `parallel` is confirmed. Sequential workers remain independent when their contexts are isolated.
- If the required independent workers are unavailable, report that the meeting cannot run. Never replace them with multiple personas in the current session.
- Use host-native agent tools. Do not simulate providers or shell out to provider command-line tools.
- Keep review intent portable: only `standard` or `deep`. Cross-provider execution is host-dependent and unverified.

## Roles

- Facilitator (`진행자`): frames the goal, constraints, and success criteria.
- Explorers (`탐험가`): create three materially distinct originals by default and cross-develop them.
- Synthesizer (`합성자`): selects evolved originals, creates a multi-idea hybrid, and creates a novel mutation.
- Reality reviewer (`현실 검토자`): after synthesis only, checks feasibility, evidence, cost, and risk through the claim/evidence engine.

## Flow

1. Diverge: independent explorers generate distinct original ideas without seeing peer outputs.
2. Yes-But and Build: every original receives non-empty `keep`, `but`, and `build` fields. Keep a concrete strength; make but an improvement opportunity; make build a constructive extension.
3. Hybridize and Mutate: evolve every original, preserve lineage, combine at least two distinct original roots in the hybrid, and make the mutation a distinct third option with a novelty statement.
4. Reality Check: assess feasibility, evidence, cost, and risk only after the evolution outputs exist. Use `decide.py` as the final routing mechanism.
5. Recommend: retain material disagreement and uncertainty rather than manufacturing consensus.

Stop after two rounds, or earlier when no meaningful idea growth or decision-changing reality evidence remains.
