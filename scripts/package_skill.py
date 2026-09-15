#!/usr/bin/env python3
"""Build and verify a deterministic source-and-install release archive."""

from __future__ import annotations

import argparse
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME = ROOT.name
SOURCE_FILES = (
    ".editorconfig",
    ".gitattributes",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    ".github/workflows/validate.yml",
    ".gitignore",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE.md",
    "Makefile",
    "README.en.md",
    "README.md",
    "SECURITY.md",
    "SKILL.md",
    "SUPPORT.md",
    "VERSION",
    "agents/openai.yaml",
    "docs/architecture.md",
    "docs/publishing.md",
    "references/external-skills.md",
    "references/test-cases.md",
    "references/workflow.md",
    "scripts/package_skill.py",
    "scripts/validate_repo.py",
)


def selected_files() -> list[Path]:
    files: list[Path] = []
    root_resolved = ROOT.resolve()
    for relative in SOURCE_FILES:
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(f"Missing release file: {relative}")
        if root_resolved not in source.resolve().parents:
            raise ValueError(f"Release file escapes repository root: {relative}")
        files.append(source)
    return files


def verify_archive(output: Path, files: list[Path]) -> None:
    expected = [f"{NAME}/{source.relative_to(ROOT).as_posix()}" for source in files]
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        if names != expected:
            raise ValueError("Archive entries differ from the release allowlist")
        if archive.testzip() is not None:
            raise ValueError("Archive CRC verification failed")
        for source, member in zip(files, expected):
            if archive.read(member) != source.read_bytes():
                raise ValueError(f"Archive content differs from source: {member}")


def write_archive(output: Path) -> None:
    files = selected_files()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in files:
            relative = source.relative_to(ROOT)
            info = zipfile.ZipInfo(f"{NAME}/{relative.as_posix()}", date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, source.read_bytes())
    verify_archive(output, files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist" / f"{NAME}-{(ROOT / 'VERSION').read_text(encoding='utf-8').strip()}.zip",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    write_archive(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
