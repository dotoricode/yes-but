# Idea Evolution Rules

## Runtime modes

- Solo is the default. The current session performs the facilitator, multiple explorers, synthesizer, and reality reviewer roles.
- Mix mode requires an explicit user request and confirmed `independent_workers` capability. The host may assign available Codex and Claude explorers; rotate provider-to-role assignments each round.
- Run independent work concurrently only when `parallel` is confirmed. Do not infer capabilities, simulate providers, or add a launcher.
- If a provider is unavailable, disclose the lost independence and use the supported fallback. If both are required and unavailable, report that the requested mix cannot run.
- Keep review intent portable: only `standard` or `deep`. Cross-provider execution is host-dependent and unverified.

## Roles

- Facilitator (`진행자`): frames the goal, constraints, and success criteria.
- Explorers (`탐험가`): create three materially distinct originals by default and cross-develop them.
- Synthesizer (`합성자`): selects evolved originals, creates a multi-idea hybrid, and creates a novel mutation.
- Reality reviewer (`현실 검토자`): after synthesis only, checks feasibility, evidence, cost, and risk through the claim/evidence engine.

## Flow

1. Diverge: generate distinct original ideas.
2. Yes-But and Build: every original receives non-empty `keep`, `but`, and `build` fields. Keep a concrete strength; make but an improvement opportunity; make build a constructive extension.
3. Hybridize and Mutate: evolve every original, preserve lineage, combine at least two distinct original roots in the hybrid, and make the mutation a distinct third option with a novelty statement.
4. Reality Check: assess feasibility, evidence, cost, and risk only after the evolution outputs exist. Use `decide.py` as the final routing mechanism.
5. Recommend: retain material disagreement and uncertainty rather than manufacturing consensus.

Stop after two rounds, or earlier when no meaningful idea growth or decision-changing reality evidence remains.
