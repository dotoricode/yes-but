# yes-but

`yes-but` is an idea-evolution skill. It turns promising but incomplete alternatives into stronger options before asking whether they are feasible, evidenced, affordable, or safe. The user sees only concise, natural Korean meeting dialogue.

## How it runs

The pipeline is **Diverge → Yes-But → Build → Hybridize → Mutate → Reality Check → Recommend**.

The facilitator first frames the goal and constraints. Three explorers produce distinct originals by default. Each original receives constructive cross-development with three required fields: `keep` preserves a concrete strength, `but` identifies how that strength can improve rather than rejecting it, and `build` supplies the next development. A synthesizer must return the strongest evolved original, a hybrid whose lineage reaches at least two distinct originals, and a mutation: a genuinely novel third option, not a selection or restatement.

Only then does the reality reviewer check feasibility, evidence, cost, and risk. `scripts/decide.py` remains the final claim/evidence decision engine. `scripts/validate_idea_evolution.py` uses only the standard library to enforce lineage, cross-development fields, and the required output kinds.

Solo mode is the default and uses the current session for facilitator, explorers, synthesizer, and reality reviewer. Mix mode requires an explicit request plus `independent_workers` and available Codex and/or Claude capabilities. Provider-to-role assignments rotate by round; `parallel` controls whether supported independent work can run concurrently. The skill has no provider launcher, so cross-provider execution remains host-dependent and unverified.

## Korean UI

Only meaningful idea growth is visible. The only speaker labels are `진행자`, `탐험가`, `합성자`, and `현실 검토자`. The UI never exposes A/B/C labels, provider names, internal identifiers, statuses, or logs.

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

## Test

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_idea_evolution.py < examples/idea-evolution.json
```
