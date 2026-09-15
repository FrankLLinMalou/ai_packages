# External skill routing

Third-party repositories can change. Inspect current source, requested permissions, hooks, scripts, and installation scope before use. Never execute repository scripts blindly.

## Grill Me

- Source: <https://github.com/mattpocock/skills/tree/main>
- Use only when ambiguity, scope, acceptance, or a tradeoff can materially change the plan.
- Prefer a model-invoked `grilling` capability when available. If the environment exposes only a user-invoked `grill-me`, ask the user to invoke it or ask equivalent high-information questions directly.
- If missing, obtain explicit current-user installation authorization before using the host's skill installer for only the required capability. Do not block planning when installation is unavailable.

## Ponytail

- Source: <https://github.com/DietrichGebert/ponytail>
- Use for coding only when reuse, standard-library/native features, or a minimum sufficient implementation is likely to reduce code and context more than loading/installing the capability costs.
- Never trade away security, error handling, accessibility, data-loss protection, or necessary verification.

## Nature Skills

- Source: <https://github.com/Yuan1z0825/nature-skills>
- Use only the smallest matching subset for scientific writing, Nature-style expression, scientific figures, or a specialized research workflow.
- Do not load the collection merely because a task mentions research.

## Installation and cost rules

1. Check whether the exact capability is already available.
2. Starting this orchestrator authorizes a suggestion, not installation. Install only after the user explicitly requests it in the current instruction or confirms the source, scope, and persistence impact. Host approval is additional and never substitutes for user authorization.
3. Prefer the host's controlled installer. Review `SKILL.md`, executable scripts, and hooks; reject obfuscated code, secret requests, or unjustified permissions.
4. Pin or record the installed version/commit when practical. Recheck capability names and invocation policy rather than relying on stale examples.
5. Stop after one clear installation failure. Fall back to built-in behavior or report the blocker; do not retry indefinitely.
