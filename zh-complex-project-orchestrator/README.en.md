# Chinese Complex Project Orchestrator

[简体中文](README.md)

An Agent Skill for long-running projects led by Chinese-speaking users. It uses concise English for internal orchestration and subagent communication while keeping all user-facing questions, plans, progress, approvals, warnings, and final deliverables in Chinese by default.

## What it enforces

- Substantive Chinese or mixed-language instructions are compiled into a compact, faithful English task specification by a fresh intake agent.
- The original user instruction remains authoritative.
- Planning and explicit approval precede implementation.
- Token-efficient serial execution is the default; execution agents require a heavy workload or explicitly requested speed with independent workstreams.
- Smoke tests require exact authorization and must be grounded in inspected project evidence.
- A fresh read-only agent performs final acceptance against the original requirements and approved criteria.

## Install

Clone or copy the complete repository to the host's Agent Skills directory. For Codex, the conventional location is:

```text
~/.codex/skills/zh-complex-project-orchestrator/
```

On Windows it is commonly:

```text
%USERPROFILE%\.codex\skills\zh-complex-project-orchestrator\
```

Restart the client or start a new thread. Keep the repository directory name unchanged and do not copy only `SKILL.md`; its referenced files are required.

## Invoke

```text
Use $zh-complex-project-orchestrator to manage this project. Run internally in English and keep every user-facing output in Chinese.
```

The two controls are independent. `intake_policy` defaults to `economy`; use `intake_policy: strict` to route every project message through a fresh intake agent. `execution_mode` defaults to `economy`; use `execution_mode: fast` to prioritize wall-clock time where independent workstreams exist.

Activation is explicit-only. A state file does not activate the skill by itself, and a new thread requires the user to invoke the skill again before state recovery.

## Validate

```bash
python3 scripts/validate_repo.py
skills-ref validate .
```

The first command has no third-party dependencies. The second uses the reference validator recommended by the Agent Skills specification.

See [the Chinese README](README.md) for the complete usage guide and [docs/architecture.md](docs/architecture.md) for design boundaries.

## License

This project is licensed under the [MIT License](LICENSE.md).
