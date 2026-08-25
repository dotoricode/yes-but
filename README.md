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

## Test

```sh
python3 -m unittest discover -s tests -v
```

