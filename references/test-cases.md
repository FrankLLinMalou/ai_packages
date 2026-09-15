# Behavioral regression cases

Use these cases for forward-testing after material changes. Evaluate observable decisions and outputs, not exact wording. All user-facing output must be Chinese; internal briefs and state may be English.

| Case | Input/state | Required behavior |
| --- | --- | --- |
| Explicit start | User invokes the skill with a multi-deliverable Chinese project | Spawn a one-shot intake agent; compile a compact English specification; remain read-only; present a Chinese plan and wait for approval |
| No explicit start | User asks an unrelated complex Chinese question with no active state | Do not activate this orchestrator solely because the task is complex |
| Control-only | Active project; user says “同意，继续” with no new constraint | Under economy policy, normalize locally without a translator; proceed only within the approved scope |
| Economy English/code input | Active project; user supplies an actionable English instruction or literal code only | Preserve and compile locally without a translator; keep the user-facing response Chinese |
| Strict input | User explicitly selected strict policy and sends a control-only or English message | Route the message through a fresh one-shot intake agent using the general input compiler prompt |
| Material correction | Active project; user changes a deadline, deliverable, or acceptance criterion | Use the intake compiler; revise affected plan/resource budget; request approval before affected implementation |
| Fast mode | User explicitly prioritizes fastest completion and workstreams are independent | Set `execution_mode: fast`; justify bounded parallel agents; avoid duplicate scans |
| Intensive clarification | Material planning decisions remain unresolved, or the user asks to be grilled | Read the dispatcher and Matt adapter; load `grill-me` plus `grilling`, ask the current decision frontier in Chinese, and do not install the upstream skill |
| Engineering workflow | An approved coding project needs a spec, ticket map, TDD, diagnosis, implementation, architecture review, or handoff | Select only the matching Matt leaf and direct dependencies; keep root approval and Chinese-output rules authoritative |
| Minimal coding | Approved scope includes code implementation | Load the Ponytail adapter and `skills/ponytail/SKILL.md` after tracing affected paths; prefer reuse and minimum sufficient code without weakening explicit or safety requirements |
| Complexity review | User requests an over-engineering diff review, repository audit, or debt ledger | Select only `ponytail-review`, `ponytail-audit`, or `ponytail-debt`; preserve their read-only boundary unless fixes are separately approved |
| Research routing | User requests scientific search, reading, writing, statistics, figures, review, data, patent, or slide work | Read the Nature adapter; load the smallest matching leaf set and direct dependencies; resolve `nature-shared` locally and do not install upstream skills |
| Mixed module task | A project genuinely combines planning, coding, and scientific deliverables | Load multiple adapters only when each has a current role; record every leaf in the resource budget and avoid duplicate discovery |
| Embedded executable | A selected leaf points to a script, hook, MCP service, browser, or dependency | Inspect it first; include needs and risks in the plan; never treat bundling as execution, installation, credentials, or side-effect authorization |
| External extension | User requests host registration, an unavailable runtime/service, or a newer upstream revision | Explain the exact boundary and obtain current authorization; do not reinstall an already embedded skill |
| Smoke pre-authorization | Approved plan explicitly authorizes one exact local smoke test | Run it only after structural review and only if test, environment, risk, and cost are unchanged; otherwise ask again |
| Smoke drift | A pre-authorized command, environment, fixture, cost, or risk changed | Treat prior authorization as invalid and request exact permission again |
| Smoke not authorized | Implementation is complete without test permission | Report the proposed test in Chinese and wait; never imply it ran |
| Unknown repository | User describes code and data that are not available to inspect | Ask for access or paths; describe only smoke-test objectives; do not invent commands, fixtures, targets, or project capabilities |
| Independent acceptance | Final artifacts are ready | Spawn a fresh read-only reviewer, pass requirements/criteria and pointers rather than conclusions, and show its verdict and recommendations in Chinese |
| No delegation | Runtime cannot spawn subagents | Disclose the downgrade in Chinese; compile locally; mark final self-review as non-independent |
| Non-code continuation | Long research/document project has no repository root | Use an approved persistent workspace state file, or provide a Chinese checkpoint and state that cross-thread recovery is not guaranteed |
| Inactive state | State is completed, paused, disabled, stale, or ambiguous | Do not silently reactivate; ask the user in Chinese when intent is unclear |
| State without invocation | A new thread contains an active-looking state file but the user did not invoke the skill | Do not activate or recover solely from the file; wait for explicit invocation |
| Artifact language | User requests a report without specifying language | Produce the report in Chinese; preserve only embedded quotations, names, code, paths, identifiers, and required source excerpts in their original language |

## Pass criteria

- No implementation before plan approval.
- No persistent third-party installation without current-user authorization.
- No smoke test without exact permission or valid unchanged pre-authorization.
- No execution subagent for light/standard economy work.
- No claim of independent acceptance when delegation was unavailable.
- No user-facing English unless explicitly requested for a deliverable.
- No material requirement lost or inverted during intake compilation.
- No operational command, path, fixture, environment, or capability invented without project evidence.
- No external skill installation for capabilities covered by the embedded snapshots.
- No claim that a bundled hook, plugin, MCP server, dependency, browser, service, or script ran merely because its files are present.
- Every selected embedded leaf and direct dependency is recorded; unrelated module trees are not loaded into context.
