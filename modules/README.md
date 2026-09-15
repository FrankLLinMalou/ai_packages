# Embedded module dispatcher

This directory contains three pinned upstream working-tree snapshots plus local
adapters. The snapshots maximize legally redistributable upstream content, as
documented in `LOCK.json` and `THIRD_PARTY_NOTICES.md`, so users do not need to
install the upstream skills separately. Load them progressively; never place
all three trees into one agent context.

## Precedence

The root `SKILL.md`, the user's current instruction, host permissions, and the
approved project plan take precedence over every embedded upstream file.
Always preserve the root Chinese-interface contract, plan approval gate,
resource budget, smoke-test authorization, and independent acceptance gate.

Upstream prompts may mention English-only output, automatic persistence,
subagents, issue trackers, installers, plugins, hooks, or commands. Treat those
as module-local suggestions. They do not override the root workflow or grant
permission for writes, external actions, dependency installation, or execution.

## Routing

| Need | Read first | Then load |
| --- | --- | --- |
| Clarification, decisions, specifications, engineering workflow, handoff, teaching | [Matt Pocock module](mattpocock-skills/MODULE.md) | Only the selected upstream `SKILL.md` and its directly referenced files |
| Minimum implementation, deletion-first design, complexity review or debt audit | [Ponytail module](ponytail/MODULE.md) | Only the selected Ponytail skill; inspect runtime helpers only if explicitly needed |
| Scientific search, reading, writing, statistics, figures, review, data, patents or slides | [Nature Skills module](nature-skills/MODULE.md) | Only the selected Nature skill and the references/scripts it directly requires |

A mixed task may load more than one matching module. Record every loaded
adapter and leaf skill in the resource budget. Do not load an unrelated module
merely because it is bundled.

## Embedded path resolution

When an upstream file refers to another installed skill by name, resolve it
inside this package first:

- Matt Pocock: `modules/mattpocock-skills/upstream/skills/<name>/`
- Ponytail: `modules/ponytail/upstream/skills/<name>/`
- Nature Skills: `modules/nature-skills/upstream/skills/<name>/`

For category-qualified Matt skills, search within `engineering/`,
`productivity/`, `misc/`, and `in-progress/`. Preserve relative file and script
resolution from the selected upstream skill directory.

## Execution boundary

Instruction files are available immediately. Executable helpers, hooks, MCP
servers, browser automation, package installation, credentials, paid services,
and external publishing are not automatically authorized or activated.

Before running an embedded executable:

1. Verify it belongs to the selected leaf workflow and inspect its inputs,
   writes, network access, dependencies, and platform assumptions.
2. Prefer an already-available host capability when it provides the same
   result safely.
3. Include any dependency or external-service requirement in the plan.
4. Obtain the authorization required by the root workflow and host.
5. Run from the embedded skill's directory when its relative paths require it,
   but direct outputs to the user's approved project workspace.

Never run bundled setup, uninstall, publish, auto-update, hook-registration, or
marketplace scripts solely because they are present.
