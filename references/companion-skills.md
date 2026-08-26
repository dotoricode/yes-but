# Companion Skill Routing

Use an installed Matt Pocock skill when it gives the meeting a better feedback loop. Read the selected skill's full `SKILL.md` first and obey its trigger and workflow.

## Invoke when the branch fits

- `research`: a current or external fact could change the recommendation. Prefer primary sources and keep citations.
- `prototype`: a state, logic, or UI question needs a runnable or visible answer.
- `codebase-design` and `domain-modeling`: a software idea depends on module seams or precise project language.
- `diagnosing-bugs`: the meeting is about a hard bug or performance regression.
- `tdd`: the user asks to implement the chosen behavior test-first.
- `code-review`: implemented work needs review against a fixed point and its spec.
- `writing-for-agents`: the output changes a skill, `AGENTS.md`, `CLAUDE.md`, or another agent-facing instruction.

Use no companion when it would add ceremony without changing the evidence or outcome. User-invoked orchestrators such as `ask-matt`, `grill-me`, `grill-with-docs`, `to-spec`, `to-tickets`, and `implement` may be recommended as a next action, but `yes-but` must not invoke them silently.
