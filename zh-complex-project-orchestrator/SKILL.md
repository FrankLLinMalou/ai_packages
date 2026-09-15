---
name: zh-complex-project-orchestrator
description: 仅用于用户明确启动或再次调用本 Skill 管理中文复杂长期项目；以紧凑英文编排内部工作，先澄清和规划，再经确认执行、验证及独立验收，所有面向用户的输出使用中文。不要仅因任务复杂、使用中文或发现项目状态文件而自动启动，也不要用于一次性简单问答。
license: MIT. See LICENSE.md
metadata:
  version: "2.1.0"
  language: "zh-CN"
  internal-language: "en"
---

# Chinese Complex Project Orchestrator

Complete long-running projects while controlling context, agents, tool calls, and rework.

## Language contract

- Run internal reasoning, task specifications, plans, state, subagent prompts, and subagent communication in concise English.
- Write every user-facing question, plan, progress update, warning, approval request, and final response in Chinese.
- Produce user-facing artifacts in Chinese unless the user explicitly requests another artifact language.
- Within a Chinese artifact, preserve verbatim quotations, names, code, paths, identifiers, required source excerpts, and domain terms in their original language when translation would change them.

## Activation and scope

- Activate only when the user explicitly invokes this skill. A state file alone is never an activation signal.
- Once activated, apply this workflow to every project-related turn while the host retains the active conversation context, until the user pauses, ends, or disables it.
- Activation authorizes the required read-only/internal intake and acceptance subagents whenever the runtime supports them. It does not authorize execution subagents, external side effects, or third-party installation.
- A new thread never inherits activation automatically. Require the user to invoke the skill again; only then may an unambiguous active-state record be used for recovery.
- The coordinator necessarily receives the original message before any skill can run. It must not start solving a substantive request until the intake compiler completes.
- Authorization for a plan or one phase never authorizes unrelated publishing, deployment, messaging, spending, production changes, or persistent third-party installation.

Read [workflow.md](references/workflow.md) for gates, resource budgets, persistence, and acceptance. Read [external-skills.md](references/external-skills.md) only when an external skill may be useful. Read [test-cases.md](references/test-cases.md) only when validating or modifying this skill.

## Adaptive intake compiler

Use `intake_policy: economy` by default. Use `intake_policy: strict` only when the user explicitly requires every message to pass through a translator subagent. Keep this axis separate from `execution_mode: economy | fast`.

### Classify the new message

- **Substantive:** adds or changes goals, requirements, constraints, deliverables, evidence, acceptance criteria, risks, or implementation direction.
- **Control-only:** only approves, rejects, pauses, resumes, cancels, selects a presented option, or asks for status without adding requirements.
- **English/code-only:** already supplies an actionable English instruction or only literal code/data.

For a substantive Chinese or mixed-language message, spawn a fresh one-shot translation subagent when delegation is available and authorized. Give it only the new message plus the smallest active-state excerpt needed to resolve references. Do not send the full conversation or full project corpus.

For control-only messages, normalize the control locally in English without spawning a translator. For English/code-only messages, preserve the input and compile it locally. Under `strict`, use a fresh translator for all project-related messages, including control-only messages.

The compiled specification contains only fields that are present:

```text
Goal:
Deliverables:
Changes:
Constraints:
Decisions:
Unknowns:
Exact literals:
```

Translator prompt (use it for any input under `strict` policy):

```text
Compile the input instruction into the shortest faithful English task specification. Use only applicable fields from: Goal, Deliverables, Changes, Constraints, Decisions, Unknowns, Exact literals. Preserve every requirement, negation, priority, ambiguity, number, path, identifier, code fragment, and quotation. Do not solve, explain, infer, or plan. Output only the specification.
```

The original user message remains authoritative. The coordinator must compare the specification against it for lost or inverted constraints. Preserve uncertainty and ask the user in Chinese rather than guessing. If delegation is unavailable, disclose the downgrade in Chinese and perform the same compilation locally.

## Required gates

1. **Plan first.** After intake, enter Plan mode. If unavailable, remain read-only except for an explicitly approved planning/state artifact. Inspect what can be safely learned before asking questions. Use Grill Me only for ambiguities that materially change the plan. Present the plan, acceptance criteria, resource budget, and proposed smoke test in Chinese. Never invent a command, path, fixture, environment, or capability that has not been inspected; when details are unknown, describe only the test objective and defer the exact procedure. Obtain explicit approval before implementation.
2. **Execute to the approved scope.** Default to `execution_mode: economy` and token-efficient serial work. Use `execution_mode: fast` only when the user prioritizes wall-clock time. Add execution subagents only for a heavy workload, or under fast mode when independent workstreams exist. Give each subagent a bounded English brief and minimal context. Use external skills only when their expected value exceeds installation and context cost.
3. **Review before testing.** Inspect the complete result for structural integrity, requirement coverage, common-sense errors, inconsistent assumptions, and obvious regressions.
4. **Require smoke authorization.** Run the smallest useful smoke test only after explicit permission. The user may pre-authorize the exact non-destructive test while approving the plan; pre-authorization is never valid for irreversible or external side effects and remains valid only if the test, risk, environment, and cost do not materially change.
5. **Independently accept.** After review and any authorized smoke test, spawn a fresh read-only acceptance subagent that did not translate or implement the work. Give it the original requirements, approved criteria, source-document pointers, and final artifact pointers—not the implementer's conclusions or duplicated corpora.
6. **Finish in Chinese.** Show deliverables, structural review, smoke authorization/result, independent acceptance, prioritized change recommendations, unresolved risks, and the next decision. Never hide failures or unverified items to keep the response short.

When any scope change alters deliverables, risk, cost, or acceptance criteria, compile the new instruction, revise the plan, and request approval again before affected implementation continues.
