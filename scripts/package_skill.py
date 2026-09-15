#!/usr/bin/env python3
"""Build and verify a deterministic source-and-install release archive."""

from __future__ import annotations

import argparse
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME = ROOT.name
EXCLUDED_PARTS = {".git", "dist", "__pycache__", ".pytest_cache", ".mypy_cache"}
EXCLUDED_NAMES = {".DS_Store", "Thumbs.db", "zh-complex-project-state.md"}


def selected_files() -> list[Path]:
    files: list[Path] = []
    root_resolved = ROOT.resolve()
    for source in ROOT.rglob("*"):
        relative = source.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if source.is_symlink():
            raise ValueError(f"Release cannot contain a symlink: {relative}")
        if not source.is_file():
            continue
        if source.name in EXCLUDED_NAMES:
            continue
        if root_resolved not in source.resolve().parents:
            raise ValueError(f"Release file escapes repository root: {relative}")
        files.append(source)
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def archive_mode(source: Path) -> int:
    return 0o755 if source.stat().st_mode & 0o111 else 0o644


def verify_archive(output: Path, files: list[Path]) -> None:
    expected = [f"{NAME}/{source.relative_to(ROOT).as_posix()}" for source in files]
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        if names != expected:
            raise ValueError("Archive entries differ from selected repository files")
        if archive.testzip() is not None:
            raise ValueError("Archive CRC verification failed")
        for source, member in zip(files, expected):
            if archive.read(member) != source.read_bytes():
                raise ValueError(f"Archive content differs from source: {member}")
            stored_mode = (archive.getinfo(member).external_attr >> 16) & 0o777
            if stored_mode != archive_mode(source):
                raise ValueError(f"Archive mode differs from source: {member}")


def write_archive(output: Path) -> None:
    files = selected_files()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for source in files:
            relative = source.relative_to(ROOT)
            info = zipfile.ZipInfo(
                f"{NAME}/{relative.as_posix()}", date_time=(2026, 1, 1, 0, 0, 0)
            )
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | archive_mode(source)) << 16
            archive.writestr(info, source.read_bytes())
    verify_archive(output, files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT
        / "dist"
        / f"{NAME}-{(ROOT / 'VERSION').read_text(encoding='utf-8').strip()}.zip",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    write_archive(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
