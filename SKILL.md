---
name: yes-but
description: Run a short, evidence-aware agent meeting for requests with competing options, material risk, or decision-changing facts. Show the user only natural Korean dialogue.
---

# yes-but

Open a meeting only when options compete, risk or uncertainty is material, or a fact check could change the decision. Answer simple requests directly.

Use solo mode by default: the current session performs every selected role without creating workers. Enter mix mode only when the user explicitly asks for it. In mix mode, keep the current session as facilitator and decision maker, use available Codex and Claude workers for independent specialist reviews, and rotate provider-to-role assignments between review rounds. Do not launch providers yourself; host adapters own that boundary.

Express review intent only as `standard` or `deep`, never provider-specific effort names. If a requested mix provider is unavailable, disclose the limitation and use the supported fallback; do not substitute when the user requires both providers.

1. The facilitator states the goal, decision, constraints, and success criteria.
2. Select the minimum roles: proposer for alternatives, adversarial reviewer for risk, fact checker for changeable facts, and decision maker for comparison or recommendation.
3. Run independent reviews concurrently without sharing another role's conclusion first.
4. Reopen only disputes likely to change the decision, for at most two rounds.
5. Stop when material claims are resolved or more work is unlikely to change the outcome. Preserve meaningful disagreement.

Show the user only decision-relevant content in concise, natural Korean. End with the recommendation, rationale, rejected alternatives, remaining uncertainty, and next action.

Use [meeting rules](references/meeting-rules.md) for modes, roles, and flow, [Korean UI rules](references/korean-ui.md) for visible output, and [decision rules](references/decision-rules.md) for claim handling.
