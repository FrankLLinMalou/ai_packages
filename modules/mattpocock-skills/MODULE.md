# Matt Pocock Skills module

Pinned upstream revision: `3cca18b368ae95cdbdebbff572ccafa662551015`.
The complete upstream working tree is preserved under `upstream/`, excluding
only `.git`. For portable ZIP extraction, the upstream `AGENTS.md` symlink is
materialized as a regular copy of its `CLAUDE.md` target; file contents are
unchanged. This adapter controls local routing and precedence.

Read one leaf skill at a time. If it invokes another named skill, resolve that
skill inside `upstream/skills/` instead of installing it.

## Primary routes

| Need | Leaf skill |
| --- | --- |
| Relentless decision clarification | [grill-me](upstream/skills/productivity/grill-me/SKILL.md), then [grilling](upstream/skills/productivity/grilling/SKILL.md) |
| Clarification plus glossary/ADR work | [grill-with-docs](upstream/skills/engineering/grill-with-docs/SKILL.md) |
| Large multi-session decision map | [wayfinder](upstream/skills/engineering/wayfinder/SKILL.md) |
| Synthesize a specification | [to-spec](upstream/skills/engineering/to-spec/SKILL.md) |
| Decompose work into dependent tickets | [to-tickets](upstream/skills/engineering/to-tickets/SKILL.md) |
| Ask a stakeholder asynchronously | [to-questionnaire](upstream/skills/productivity/to-questionnaire/SKILL.md) |
| Implement from an approved spec | [implement](upstream/skills/engineering/implement/SKILL.md) |
| Test-driven work | [tdd](upstream/skills/engineering/tdd/SKILL.md) |
| Diagnose a difficult bug | [diagnosing-bugs](upstream/skills/engineering/diagnosing-bugs/SKILL.md) |
| Standards/spec code review | [code-review](upstream/skills/engineering/code-review/SKILL.md) |
| Deep-module design | [codebase-design](upstream/skills/engineering/codebase-design/SKILL.md) |
| Survey architectural deepening opportunities | [improve-codebase-architecture](upstream/skills/engineering/improve-codebase-architecture/SKILL.md) |
| Domain vocabulary and ADRs | [domain-modeling](upstream/skills/engineering/domain-modeling/SKILL.md) |
| Resolve merge/rebase conflicts | [resolving-merge-conflicts](upstream/skills/engineering/resolving-merge-conflicts/SKILL.md) |
| Throwaway design prototype | [prototype](upstream/skills/engineering/prototype/SKILL.md) |
| Primary-source engineering research | [research](upstream/skills/engineering/research/SKILL.md) |
| Human-operated setup wizard | [wizard](upstream/skills/engineering/wizard/SKILL.md) |
| Issue/PR triage | [triage](upstream/skills/engineering/triage/SKILL.md) |
| Compact project handoff | [handoff](upstream/skills/productivity/handoff/SKILL.md) |
| Multi-session teaching | [teach](upstream/skills/productivity/teach/SKILL.md) |
| Re-explain a message that did not land | [wait-what](upstream/skills/productivity/wait-what/SKILL.md) |
| Write agent-facing instructions | [writing-for-agents](upstream/skills/productivity/writing-for-agents/SKILL.md) |

Use [ask-matt](upstream/skills/engineering/ask-matt/SKILL.md) only as a fallback
router when the table does not resolve the need. `setup-matt-pocock-skills`
may describe useful repository conventions, but do not run setup or configure
an issue tracker without explicit scope and authorization.

## Additional bundled routes

The full `misc/` and `in-progress/` trees are included for completeness. Load
them only when the user explicitly requests the named capability or an approved
plan clearly requires it. Treat `in-progress/` as experimental and review it
more strictly before following it. `deprecated/` is reference-only.

## Local overrides

- Ask all questions and present all results in Chinese.
- Respect the root plan and smoke-test gates even if a leaf suggests immediate
  implementation, tests, commits, ticket publication, or document writes.
- Do not auto-create subagents. Use the root resource budget.
- Do not assume a configured issue tracker, domain-document layout, browser,
  or external account; inspect or ask.
