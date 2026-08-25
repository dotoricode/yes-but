# yes-but

`yes-but` is a skill for reaching a clear answer through a short Korean meeting. It opens a meeting only when a request has competing options, meaningful risk, or facts that could change the conclusion.

The skill selects only the needed roles, keeps independent review parallel, and shows the user only natural Korean statements that affect the decision. Internal identifiers, statuses, logs, and model names stay out of the visible conversation.

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

Replace `/path/to/yes-but` with the absolute path of this repository. Each command creates an independent directory containing real files at the target path.

## How it runs

The skill first narrows the goal, constraints, and decision points. It then gathers only the required proposals, objections, and fact checks. Claims are assessed by type, important disagreements may be revisited up to twice, and the final response states the recommendation, reason, rejected alternative, remaining uncertainty, and next action.

Solo mode is the default and uses the current session's active agent, model, and reasoning settings. Mix mode requires explicit `independent_workers` capability as well as an available provider; missing capabilities are unavailable. `parallel` controls `can_run_concurrently`, so a valid mix review may run sequentially. Assignments rotate by review round so no provider permanently owns a role. If capability is missing, the skill continues solo unless both providers are required.

Exact model versions are not pinned. The portable skill uses only `standard` and `deep` review intent; host adapters map those intents to supported runtime settings. It does not include a Codex or Claude launcher, so cross-provider end-to-end execution is host-dependent and unverified.

`scripts/decide.py` keeps evidence state (`confirmed`, `refuted`, `unknown`, `conflicting`) separate from decision state. Weak, indirect, stale, or uncorroborated evidence stays `unknown`; only an explicit `evidence_state: "refuted"` is refuted. Proposal feasibility and risk existence are decided by their own criteria, while risk mitigation and blocking impact remain independent. With `changed_ids`, it reassesses each changed claim and all transitive dependents in input order, rejecting unknown dependencies and cycles. The Korean UI validator permits URLs and backtick code while requiring explicit preservation entries for product and API names.

## Test

```sh
python3 -m unittest discover -s tests -v
```
