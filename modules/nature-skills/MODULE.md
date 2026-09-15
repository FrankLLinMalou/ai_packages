# Nature Skills module

Pinned upstream revision: `9ea7330a17813a15421fe843778a776c258b9001`.
The maximally redistributable upstream working tree is preserved under
`upstream/`, excluding `.git` and the unlicensed payloads below
`skills/nature-figure/assets/figures4papers/`. That directory's upstream
`THIRD_PARTY_NOTICES.md` is retained. The 20 skill directories and their
redistributable scripts, static references, templates, examples, and assets are
otherwise preserved.

Resolve cross-skill references such as `~/.codex/skills/nature-shared` to
`upstream/skills/nature-shared` inside this module. Read only the selected leaf
skill and the files it directly routes to.

## Skill routes

| Need | Leaf skill |
| --- | --- |
| Literature search and citation-impact analysis | [nature-academic-search](upstream/skills/nature-academic-search/SKILL.md) |
| Nature/CNS-family claim-to-citation mapping | [nature-citation](upstream/skills/nature-citation/SKILL.md) |
| Data/code availability and FAIR metadata | [nature-data](upstream/skills/nature-data/SKILL.md) |
| Lawful full-text and supplement retrieval | [nature-downloader](upstream/skills/nature-downloader/SKILL.md) |
| Structured multimodal experiment logs | [nature-experiment-log](upstream/skills/nature-experiment-log/SKILL.md) |
| Scientific figures and graphical abstracts | [nature-figure](upstream/skills/nature-figure/SKILL.md) |
| Reconstruct editable slides from images | [nature-image2ppt](upstream/skills/nature-image2ppt/SKILL.md) |
| Repeatable literature processing | [nature-literature-pipeline](upstream/skills/nature-literature-pipeline/SKILL.md) |
| Structured deep-reading paper card | [nature-paper-card](upstream/skills/nature-paper-card/SKILL.md) |
| Chinese invention patent materials | [nature-paper-to-patent](upstream/skills/nature-paper-to-patent/SKILL.md) |
| Academic presentation from a paper | [nature-paper2ppt](upstream/skills/nature-paper2ppt/SKILL.md) |
| Language polishing, translation, tightening | [nature-polishing](upstream/skills/nature-polishing/SKILL.md) |
| Research proposals and opening reports | [nature-proposal-writer](upstream/skills/nature-proposal-writer/SKILL.md) |
| Source-grounded bilingual paper reading | [nature-reader](upstream/skills/nature-reader/SKILL.md) |
| Verify reference metadata and support | [nature-ref-verifier](upstream/skills/nature-ref-verifier/SKILL.md) |
| Rebuttals and post-decision correspondence | [nature-response](upstream/skills/nature-response/SKILL.md) |
| Mock peer review | [nature-reviewer](upstream/skills/nature-reviewer/SKILL.md) |
| Statistical reporting audit | [nature-statistics](upstream/skills/nature-statistics/SKILL.md) |
| Draft or restructure manuscript arguments | [nature-writing](upstream/skills/nature-writing/SKILL.md) |
| Shared references used by other Nature skills | [nature-shared](upstream/skills/nature-shared/SKILL.md) — never route as a standalone user workflow |

When several scientific deliverables are requested, select the smallest set of
leaf skills and sequence them by evidence dependency. For example, search or
reader work may precede writing; statistics review precedes claims that depend
on it; figure construction follows a verified panel/evidence plan.

## Runtime and evidence boundary

- Bundling makes instruction, script, template, and asset files locally
  available. It does not install Python/R/npm dependencies, provide browsers,
  credentials, subscriptions, journal access, or external APIs.
- Never fabricate findings, sample sizes, statistical tests, references,
  quotations, journal requirements, image provenance, or tool results.
- Inspect a selected script and its requirements before execution. State any
  missing dependency or external service in the plan and obtain authorization.
- Respect lawful-access and source-attribution rules. Never bypass paywalls or
  institutional controls.
- Do not reconstruct or redistribute the excluded `figures4papers` payloads
  without verifying current source terms and obtaining any required permission;
  use the repository-owned patterns and templates routed by `references/demos.md`.
- Use the root smoke-test and user-facing Chinese contracts. Preserve requested
  manuscript or artifact language when the user specifies it.
