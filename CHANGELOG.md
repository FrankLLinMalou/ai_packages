# Changelog

All notable changes are documented here. Versions follow semantic versioning intent for workflow compatibility.

## [3.0.0] - 2026-09-15

### Added

- Pinned, maximally redistributable working-tree snapshots of Matt Pocock Skills, Ponytail, and Nature Skills.
- Progressive module adapters for 37 Matt skills, 6 Ponytail skills, and 20 Nature skill packages.
- Per-snapshot SHA-256 manifests, a machine-readable upstream lock file, and a zero-dependency manifest verifier.
- Embedded scripts, templates, examples, assets, runtime adapters, and project documentation supplied by the upstream snapshots.

### Changed

- Replaced the three selected-excerpt references from 2.2.0 with full modular snapshots and leaf-level routing.
- External setup is now limited to runtime dependencies, host registration, external services, or explicitly requested upstream updates; duplicate upstream skill installation is unnecessary.
- Release packaging now includes the complete redistributable module tree deterministically while preserving executable file modes.
- Nature's unlicensed `figures4papers` payloads are intentionally excluded while their upstream notice and safe fallback routing are retained.

### Removed

- The 2.2.0 `bundled-grilling`, `bundled-minimal-code`, and `bundled-research-guardrails` excerpt files.

## [2.2.0] - 2026-09-15

### Added

- Selected upstream Grill Me clarification, Ponytail minimum-code, and Nature Skills research-quality instructions as locally bundled, conditionally loaded modules.
- Complete upstream MIT and Apache-2.0 license copies plus pinned revisions, source hashes, attribution, and modification notices.

### Changed

- Prefer bundled capabilities for planning, coding, and scientific work; external installation is now only an explicitly authorized extension path.
- Clarified mixed-license redistribution boundaries while retaining MIT for project-authored content.

## [2.1.0] - 2026-09-15

### Added

- GitHub-ready repository documentation and community health files.
- Zero-dependency repository validator and continuous integration workflow.
- Architecture documentation, issue forms, pull request template, and release metadata.
- Explicit Agent Skills version, language, and MIT license metadata.
- Deterministic source-and-install release archive with an exact file allowlist.

### Changed

- Packaged the existing v2 workflow as a repository-root Agent Skill.
- Separated `intake_policy` from `execution_mode` and made activation explicitly opt-in.

## [2.0.0] - 2026-09-15

### Added

- English internal orchestration with Chinese user-facing communication.
- Adaptive `economy` intake and optional `strict` intake.
- Structured requirement compilation, resource budgets, multiple persistence backends, and behavioral regression cases.
- Safe smoke-test pre-authorization and evidence-grounded command rules.

## [1.0.0] - 2026-09-15

### Added

- Initial Chinese complex-project workflow with planning, resource allocation, validation, smoke authorization, and independent acceptance.
