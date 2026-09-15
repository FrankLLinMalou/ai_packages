#!/usr/bin/env python3
"""Create or verify SHA-256 manifests for embedded upstream snapshots."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
MODULES = ("mattpocock-skills", "ponytail", "nature-skills")


def snapshot_files(module: str) -> list[Path]:
    upstream = ROOT / "modules" / module / "upstream"
    if not upstream.is_dir():
        raise ValueError(f"Missing upstream snapshot: {module}")
    files = []
    for path in upstream.rglob("*"):
        if path.is_file():
            relative = path.relative_to(upstream)
            if ".git" in relative.parts:
                raise ValueError(f"Forbidden VCS path in {module}: {relative}")
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(upstream).as_posix())


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def expected_lines(module: str) -> list[str]:
    upstream = ROOT / "modules" / module / "upstream"
    return [
        f"{digest(path)}  {path.relative_to(upstream).as_posix()}"
        for path in snapshot_files(module)
    ]


def write(module: str) -> None:
    manifest = ROOT / "modules" / module / "MANIFEST.sha256"
    manifest.write_text("\n".join(expected_lines(module)) + "\n", encoding="utf-8")


def verify(module: str) -> list[str]:
    errors: list[str] = []
    manifest = ROOT / "modules" / module / "MANIFEST.sha256"
    if not manifest.is_file():
        return [f"Missing manifest: {manifest.relative_to(ROOT)}"]

    actual_lines = manifest.read_text(encoding="utf-8").splitlines()
    seen: set[str] = set()
    for line_number, line in enumerate(actual_lines, 1):
        if "  " not in line:
            errors.append(f"Malformed manifest line {module}:{line_number}")
            continue
        hash_value, relative_text = line.split("  ", 1)
        relative = PurePosixPath(relative_text)
        if (
            len(hash_value) != 64
            or any(character not in "0123456789abcdef" for character in hash_value)
            or relative.is_absolute()
            or ".." in relative.parts
            or ".git" in relative.parts
        ):
            errors.append(f"Unsafe manifest line {module}:{line_number}")
        if relative_text in seen:
            errors.append(f"Duplicate manifest path {module}:{relative_text}")
        seen.add(relative_text)

    expected = expected_lines(module)
    if actual_lines != expected:
        errors.append(f"Snapshot differs from manifest: {module}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("write", "verify"))
    parser.add_argument("modules", nargs="*", choices=MODULES)
    args = parser.parse_args()
    selected = tuple(args.modules) or MODULES

    if args.action == "write":
        for module in selected:
            write(module)
            print(ROOT / "modules" / module / "MANIFEST.sha256")
        return 0

    errors = [error for module in selected for error in verify(module)]
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Verified {len(selected)} embedded module snapshots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

