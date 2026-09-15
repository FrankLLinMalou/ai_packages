# Workflow, budgets, and persistence

Keep internal records in concise English. Render all user-facing content in Chinese.

## Contents

- State machine and minimum plan
- Resource budget and agent briefs
- Project state backends
- Structural review
- Independent acceptance and completion view

## State machine

`INTAKE -> DISCOVER -> CLARIFY? -> PLAN -> AWAIT_PLAN_APPROVAL -> EXECUTE -> STRUCTURAL_REVIEW -> AWAIT_OR_USE_SMOKE_APPROVAL -> SMOKE? -> INDEPENDENT_ACCEPTANCE -> COMPLETE`

Do not cross an approval gate. A material scope change returns to `INTAKE`, then `PLAN`.

## Minimum plan

Include:

- goal and user value;
- deliverables;
- scope and non-goals;
- known inputs and constraints;
- phases, dependencies, and milestones;
- observable acceptance criteria;
- validation strategy and exact proposed smoke test;
- resource budget;
- persistence backend, if needed;
- risks, assumptions, and unresolved decisions.

Ask in Chinese whether the user approves implementation. Separately ask whether approval also pre-authorizes the exact smoke test. A generic “run tests” statement is not pre-authorization. Offer pre-authorization only for a non-destructive test with no irreversible or external side effects, and only after the real command or procedure, target environment, fixtures/data, cost, risk, and success criteria are known. Before that, state a test objective without fabricating operational details.

## Resource budget

Every plan selects a tier and briefly records:

```text
intake_policy: economy | strict
execution_mode: economy | fast
tier: light | standard | heavy
execution_agents: 0 | justified count
max_parallelism: justified count
embedded_modules: none | exact adapter names
embedded_leaf_skills: none | exact upstream leaf paths
external_extensions: none | exact runtimes, services, registrations, or updates
high_cost_calls: none | bounded calls
state_backend: none | local | persistent
escalation_condition: observable trigger
stop_condition: observable trigger
```

| Tier | Fit | Default |
| --- | --- | --- |
| Light | One deliverable or tightly coupled work | Coordinator only, plus required intake/audit agents |
| Standard | Multiple stages within one manageable context | Serial coordinator; selected embedded leaves if useful; no execution agent |
| Heavy | Large corpus, multiple specialties, long builds, or independent workstreams under fast mode | A small dependency-based set of bounded execution agents |

Do not invent precise token counts when the runtime cannot measure them. Prefer relative budgets, bounded calls, and explicit escalation/stop conditions. Do not create agents merely to play roles. Keep work serial when context-transfer cost exceeds parallel benefit.

Each execution-agent brief contains one objective, allowed read/write scope, preserved constraints, expected output, acceptance criteria, forbidden side effects, and a stop/escalation condition.

## Project state backends

Persist state only when reconstruction cost is material and the approved plan includes it.

1. **Repository or stable project root:** `.codex/zh-complex-project-state.md`.
2. **Non-code project with an available persistent file workspace:** a clearly named project state file in that workspace; use Library only when available and permitted by the host.
3. **No persistent backend:** provide a compact Chinese checkpoint to the user and state that cross-thread recovery is not guaranteed.

Store only:

```text
skill: zh-complex-project-orchestrator
status:
goal:
requirements_fingerprint:
plan_version:
approved_plan:
decisions:
pending_user_decisions:
source_documents:
deliverables:
artifact_versions:
intake_policy: economy | strict
execution_mode: economy | fast
resource_budget:
validation:
smoke_test: not_requested | awaiting_approval | preauthorized | approved | passed | failed | declined
acceptance: pending | passed | partial | failed
next_step:
updated_at:
```

Use hashes or stable version identifiers only when cheaply available. Never store secrets, credentials, unnecessary personal data, or long conversation transcripts. On recovery, verify the state against current artifacts, then summarize the goal and next step in Chinese. If state is missing, conflicting, or stale, ask instead of guessing.

## Structural review

Before smoke testing, check:

- every approved deliverable exists;
- interfaces and component relationships agree;
- assumptions remain plausible and internally consistent;
- every acceptance criterion has evidence or is marked unverified;
- no obvious regression, unsafe shortcut, or scope leak is present.
- every proposed command, path, fixture, environment, and capability is grounded in inspected project evidence rather than invented for completeness.

## Independent acceptance brief

```text
Act as an independent read-only acceptance reviewer. Compare final artifacts only with the original requirements, approved plan and acceptance criteria, and user-provided source documents. Follow pointers and read only the material needed for each criterion. Do not trust the implementing agent's conclusions. For each criterion return PASS, PARTIAL, FAIL, or NOT_VERIFIABLE with concise evidence. Then list structural/common-sense issues, remaining risks, and prioritized change recommendations. Do not modify files or perform side-effecting actions.
```

The coordinator may deduplicate and translate the review into Chinese but must not hide failures or change verdicts. Blocking defects require a user decision before repair. Revalidate affected criteria after repair and repeat independent acceptance when the change is material.

## Chinese completion view

Show:

1. deliverables and locations;
2. structural/common-sense review;
3. smoke authorization, result, and evidence;
4. independent acceptance verdict;
5. recommendations by blocking/high/medium/low priority, including “无” when empty;
6. unresolved risks and next decision.
