# Third-Party Notices

This repository contains pinned, locally embedded snapshots of the projects
below. Project-authored adapter and orchestration files remain under this
repository's MIT License. Upstream files remain under their upstream licenses.

Each snapshot preserves the included file contents of the named Git working
tree at the pinned revision. All `.git` directories are excluded; one explicitly
unlicensed third-party payload is also excluded as documented below. For
portable ZIP extraction, symlinks are materialized as regular files with their
target bytes. `modules/LOCK.json` records the machine-readable source lock.
Each `MANIFEST.sha256` records every embedded upstream file and detects
omissions or changes.

## mattpocock/skills

- Source: <https://github.com/mattpocock/skills>
- Pinned revision: `3cca18b368ae95cdbdebbff572ccafa662551015`
- Embedded path: `modules/mattpocock-skills/upstream/`
- Scope: complete working tree except `.git`
- Integrity manifest: `modules/mattpocock-skills/MANIFEST.sha256`
- Local adapter: `modules/mattpocock-skills/MODULE.md`
- License: MIT, copyright 2026 Matt Pocock
- License copy: `LICENSES/mattpocock-skills-MIT.txt`
- Upstream license SHA-256: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- Normalization: the upstream `AGENTS.md -> CLAUDE.md` symlink is stored as a
  regular file with the same target bytes; `.git` history is not redistributed

## DietrichGebert/ponytail

- Source: <https://github.com/DietrichGebert/ponytail>
- Pinned revision: `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156`
- Embedded path: `modules/ponytail/upstream/`
- Scope: complete working tree except `.git`
- Integrity manifest: `modules/ponytail/MANIFEST.sha256`
- Local adapter: `modules/ponytail/MODULE.md`
- License: MIT
- License copy: `LICENSES/ponytail-MIT.txt`
- Upstream license SHA-256: `fb1bc6909ac3ef82d5c22106e32ef682b0cff66788fa915fb9b53b15c9d2f3ab`
- Changes to upstream files: none; `.git` history is not redistributed

## Yuan1z0825/nature-skills

- Source: <https://github.com/Yuan1z0825/nature-skills>
- Pinned revision: `9ea7330a17813a15421fe843778a776c258b9001`
- Embedded path: `modules/nature-skills/upstream/`
- Scope: complete working tree except `.git` and the unlicensed
  `skills/nature-figure/assets/figures4papers/` payloads; its
  `THIRD_PARTY_NOTICES.md` is retained
- Integrity manifest: `modules/nature-skills/MANIFEST.sha256`
- Local adapter: `modules/nature-skills/MODULE.md`
- Repository license: Apache License 2.0
- License copy: `LICENSES/nature-skills-Apache-2.0.txt`
- Upstream license SHA-256: `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`
- Changes to included upstream files: none; `.git` history and the unlicensed
  payload described below are not redistributed

The excluded `figures4papers` files originate from
<https://github.com/ChenLiu-1996/figures4papers>. The retained upstream notice
states that the source had no explicit license when checked and grants no right
to copy, modify, redistribute, or publish those payloads. They are therefore not
part of this release. Nature Skills' repository-owned templates and original
implementation paths remain available.

Two embedded Nature Skills components include their own MIT licenses, which
are retained in place and copied to `LICENSES/`:

- `skills/nature-downloader/LICENSE` — MIT, copyright 2026 baihe26;
  SHA-256 `ebb3defbe421c016c1d5f2ae18c53954a44236b51e81f12fa7aaff57905d3f66`;
  copy `LICENSES/nature-downloader-MIT.txt`.
- `skills/nature-image2ppt/LICENSE` — MIT, copyright 2026 Image2PPT
  contributors and ningzimu; SHA-256
  `9dcc2f222bd3717345d4a03f9c4a969779fd6f6812d527714b92a9e4810407d0`;
  copy `LICENSES/nature-image2ppt-MIT.txt`.

## Local integration

The root orchestrator and `modules/*/MODULE.md` adapters are new project-authored
files. They add conditional routing, Chinese user-facing output, resource
budgets, permission gates, embedded path resolution, and runtime safety
boundaries. They do not modify upstream files or imply endorsement,
affiliation, or responsibility by upstream maintainers.

Redistributors must preserve this notice, the embedded upstream license files,
the relevant `LICENSES/` copies, and any notices required by those licenses.
