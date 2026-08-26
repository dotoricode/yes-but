# Decision Rules

A decision is a routing result, not a truth score. Keep evidence state separate from decision state: `confirmed`, `refuted`, `unknown`, or `conflicting` evidence is independent from `selected`, `excluded`, `pending`, or `disagreement`. Weak, indirect, stale, or uncorroborated evidence is `unknown`, never refutation. Only explicit `evidence_state: "refuted"` records refutation.

When `changed_ids` is supplied, reassess each changed claim and every transitive dependent. Emit the selected claims in their original input order. Reject unknown dependencies and dependency cycles.

## Criteria by claim kind

- Fact: source directness, freshness, and corroboration.
- Proposal: feasibility under constraints, expected benefit, and advantage over alternatives. An infeasible proposal can be excluded while its evidence remains unknown.
- Risk: likelihood and severity establish whether it exists. Mitigation state and blocking impact are separate fields; an unmanageable risk is not automatically blocking.

## Changeable external facts

Separate price, free access, and current availability into distinct claims. Specify the exact product, feature, plan, account context, and check time before deciding.

Use three evidence paths without treating them as interchangeable:

- Published: proves only what an official document or marketing page states.
- Account: proves only what the checked account can see or obtain, including paywalls and key issuance.
- Operational: proves only that the checked environment completed the relevant call or action at that time.

Several agents repeating one page are one evidence path. A UI-generation price does not establish MCP pricing. Require account evidence for account-specific price or access claims, and operational evidence only for claims that a capability currently works. A failed or unavailable check does not prove global unavailability. When scopes differ, required evidence is missing, or paths conflict, use `추가 확인 필요` and say `현재 확인 불가` in the visible dialogue.

For decision-changing external facts, set `importance` to `important` and pass `verification` to `decide.py`: identify the claim scope, choose its required path, and record each evidence source with whether its scope matches. Important facts without structured verification remain pending. The engine deduplicates repeated path/source pairs and requires two matching pieces of evidence including the required path.

## Outcomes

- `채택`: evidence is sufficient and supports the current conclusion.
- `기각`: stronger counterevidence excludes the claim from the current choice.
- `추가 확인 필요`: the claim matters but evidence is missing.
- `이견 유지`: both sides retain reasonable support.

Do not resolve a high-impact claim from weak evidence. Reopen work only when a new fact or objection could change the result, and stop work that cannot affect the conclusion.
