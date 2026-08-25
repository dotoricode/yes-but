# Meeting Rules

## Runtime modes

- Solo is the default. The current session performs every selected role and keeps its active model and reasoning settings.
- Mix mode requires an explicit user request and confirmed `independent_workers` capability. Keep the current session as facilitator and decision maker; assign independent specialist reviews across available Codex and Claude workers. Rotate provider-to-role assignments between review rounds rather than permanently reserving a role for one provider.
- Run mixed specialist reviews concurrently only when `parallel` capability is confirmed; otherwise plan sequential work and disclose it. Never infer either capability from provider names or simulate a provider or parallel work.
- If one provider is unavailable, use the available provider and disclose the lost cross-provider independence. If neither is available, continue in solo mode unless the user requires both.
- Keep exact model versions unpinned. Express review intent only as `standard` or `deep`; a host adapter may map that intent to its supported settings. User-specified bindings override these defaults.

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

## Host boundary

This skill plans workers but does not launch Codex or Claude. Cross-provider end-to-end execution depends on a host adapter and remains unverified here.

## Reopening and stopping

Reopen only disputes with high decision impact and weak or conflicting evidence. Stop after two rounds, or earlier when no new evidence appears or the result is unlikely to change.

End when material claims have a decision and remaining work cannot change the outcome. Carry unresolved disagreement and uncertainty into the final synthesis.
