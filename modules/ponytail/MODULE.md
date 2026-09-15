# Ponytail module

Pinned upstream revision: `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156`.
The complete upstream working tree is preserved under `upstream/`, excluding
only `.git`. Files are unmodified.

## Skill routes

| Need | Leaf skill |
| --- | --- |
| Minimum sufficient implementation | [ponytail](upstream/skills/ponytail/SKILL.md) |
| Diff-focused over-engineering review | [ponytail-review](upstream/skills/ponytail-review/SKILL.md) |
| Repository-wide complexity audit | [ponytail-audit](upstream/skills/ponytail-audit/SKILL.md) |
| Inventory deliberate shortcuts | [ponytail-debt](upstream/skills/ponytail-debt/SKILL.md) |
| Explain available modes | [ponytail-help](upstream/skills/ponytail-help/SKILL.md) |
| Show upstream benchmark summary | [ponytail-gain](upstream/skills/ponytail-gain/SKILL.md) |

For ordinary implementation, read `ponytail/SKILL.md` only after tracing the
actual code paths, callers, tests, and constraints. The root workflow remains
responsible for correctness, security, compatibility, documentation requested
by the user, and validation. Minimal code is not permission to weaken an
explicit requirement.

## Runtime compatibility

The snapshot also contains commands, examples, hooks, MCP code, platform
adapters, tests, and package metadata. They are available for inspection and
explicitly approved use, but nesting them here does not register a plugin,
start an MCP server, install npm packages, or activate persistent modes.

Apply the selected skill directly as embedded instructions. Use a runtime
helper only when it adds required capability beyond the instruction file;
inspect it and obtain any required execution or dependency authorization first.
Do not repeat platform-specific copies in context.

## Local overrides

- The root orchestrator controls activation and persistence; Ponytail is not
  silently active outside matching coding phases.
- User-facing output remains Chinese, even when upstream examples use English.
- The approved plan and requested explanation depth override Ponytail's terse
  output defaults.
- Do not present upstream benchmark medians as savings measured on the user's
  repository.

