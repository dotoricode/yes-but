# Meeting Rules

## Runtime modes

- Solo is the default. The current session performs every selected role and uses its active model and reasoning effort.
- Mix mode requires an explicit user request. Keep the current session as facilitator and decision maker; assign independent specialist reviews across both Codex and Claude when available.
- Run mixed specialist reviews concurrently and keep their conclusions isolated until synthesis. Never simulate a provider or parallel work.
- If either provider is unavailable, disclose that mix mode could not run fully and continue in solo mode unless the user requires both.
- Keep exact model versions unpinned. Use each runtime's configured default model. When per-worker effort is available, use `medium` by default and `high` only for unresolved high-impact claims. User-specified bindings override these defaults.

## Roles

- Facilitator (`진행자`): narrow the goal and decision, then own the final synthesis.
- Proposer (`제안자`): produce materially different approaches and expected benefits.
- Adversarial reviewer (`반대 검토자`): find failure modes, costs, and hidden assumptions.
- Fact checker (`사실 확인자`): verify only facts that could change the decision.
- Decision maker (`판단 담당자`): compare evidence and risk, then recommend an option.

Skip every role the request does not need. A simple request may use only the facilitator or no meeting. Omit the proposer when no alternatives are needed, the adversarial reviewer when risk is negligible, and the fact checker when no changeable fact can affect the result.

## Flow

1. State the goal, constraints, success criteria, and current disputes.
2. Give each role only the goal, constraints, relevant dispute, and new evidence instead of the full transcript.
3. Run independent proposal, challenge, and verification work concurrently. Merge duplicate claims and research requests.
4. Separate claims, evidence, objections, and assumptions, then deduplicate them.
5. Apply the kind-specific decision rules and synthesize the result.

## Reopening and stopping

Reopen only disputes with high decision impact and weak or conflicting evidence. Stop after two rounds, or earlier when no new evidence appears or the result is unlikely to change.

End when material claims have a decision and remaining work cannot change the outcome. Carry unresolved disagreement and uncertainty into the final synthesis.
