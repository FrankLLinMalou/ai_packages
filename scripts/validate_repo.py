#!/usr/bin/env python3
"""Validate the repository and embedded modules without third-party packages."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from module_manifest import MODULES, snapshot_files, verify as verify_module


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REQUIRED_FILES = (
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
    "LICENSES/mattpocock-skills-MIT.txt",
    "LICENSES/nature-downloader-MIT.txt",
    "LICENSES/nature-image2ppt-MIT.txt",
    "LICENSES/nature-skills-Apache-2.0.txt",
    "LICENSES/ponytail-MIT.txt",
    "Makefile",
    "README.en.md",
    "README.md",
    "SECURITY.md",
    "SKILL.md",
    "SUPPORT.md",
    "THIRD_PARTY_NOTICES.md",
    "VERSION",
    "agents/openai.yaml",
    "docs/architecture.md",
    "docs/module-maintenance.md",
    "docs/publishing.md",
    "modules/LOCK.json",
    "modules/README.md",
    "modules/mattpocock-skills/MANIFEST.sha256",
    "modules/mattpocock-skills/MODULE.md",
    "modules/ponytail/MANIFEST.sha256",
    "modules/ponytail/MODULE.md",
    "modules/nature-skills/MANIFEST.sha256",
    "modules/nature-skills/MODULE.md",
    "references/external-skills.md",
    "references/test-cases.md",
    "references/workflow.md",
    "scripts/module_manifest.py",
    "scripts/package_skill.py",
    "scripts/validate_repo.py",
)
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".py", ".txt", ".json"}
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
PINS = {
    "mattpocock-skills": "3cca18b368ae95cdbdebbff572ccafa662551015",
    "ponytail": "e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156",
    "nature-skills": "9ea7330a17813a15421fe843778a776c258b9001",
}
NORMALIZATIONS = {
    "mattpocock-skills": "AGENTS.md symlink materialized as a regular copy of CLAUDE.md for portable ZIP extraction",
    "ponytail": "none",
    "nature-skills": "none",
}
SCOPES = {
    "mattpocock-skills": "complete working tree except .git",
    "ponytail": "complete working tree except .git",
    "nature-skills": "complete working tree except .git and unlicensed figures4papers payloads; retain its notice",
}
MINIMUM_SNAPSHOT_FILES = {
    "mattpocock-skills": 100,
    "ponytail": 100,
    "nature-skills": 700,
}
THIRD_PARTY_LICENSE_HASHES = {
    "LICENSES/mattpocock-skills-MIT.txt": "0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5",
    "LICENSES/ponytail-MIT.txt": "fb1bc6909ac3ef82d5c22106e32ef682b0cff66788fa915fb9b53b15c9d2f3ab",
    "LICENSES/nature-skills-Apache-2.0.txt": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
    "LICENSES/nature-downloader-MIT.txt": "ebb3defbe421c016c1d5f2ae18c53954a44236b51e81f12fa7aaff57905d3f66",
    "LICENSES/nature-image2ppt-MIT.txt": "9dcc2f222bd3717345d4a03f9c4a969779fd6f6812d527714b92a9e4810407d0",
}


def scalar(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    return match.group(1).strip().strip('"\'') if match else None


def quoted_yaml_value(text: str, field: str, indent: int = 2) -> str | None:
    prefix = " " * indent
    match = re.search(rf'(?m)^{prefix}{re.escape(field)}:\s*"([^"]+)"\s*$', text)
    return match.group(1) if match else None


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def is_upstream(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    return len(relative.parts) >= 3 and relative.parts[0] == "modules" and relative.parts[2] == "upstream"


def authored_files() -> list[Path]:
    ignored_parts = {".git", "dist", "__pycache__", ".pytest_cache", ".mypy_cache"}
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not is_upstream(path)
        and not any(part in ignored_parts for part in path.relative_to(ROOT).parts)
    ]


def check_markdown_links(errors: list[str]) -> None:
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for document in authored_files():
        if document.suffix.lower() != ".md":
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(("#", "/")):
                continue
            relative = unquote(parsed.path)
            if relative and not (document.parent / relative).resolve().exists():
                fail(errors, f"Broken relative link in {document.relative_to(ROOT)}: {target}")


def check_lock(errors: list[str]) -> None:
    lock_path = ROOT / "modules/LOCK.json"
    if not lock_path.is_file():
        return
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        fail(errors, f"Invalid modules/LOCK.json: {exc}")
        return
    snapshots = lock.get("snapshots") if isinstance(lock, dict) else None
    if not isinstance(snapshots, list):
        fail(errors, "modules/LOCK.json must contain a snapshots array")
        return
    by_name = {item.get("name"): item for item in snapshots if isinstance(item, dict)}
    if set(by_name) != set(MODULES):
        fail(errors, "modules/LOCK.json snapshot names do not match embedded modules")
        return
    for module, revision in PINS.items():
        item = by_name[module]
        if item.get("revision") != revision:
            fail(errors, f"Pinned revision mismatch: {module}")
        if item.get("scope") != SCOPES[module]:
            fail(errors, f"Unexpected snapshot scope: {module}")
        if item.get("normalization") != NORMALIZATIONS[module]:
            fail(errors, f"Snapshot normalization mismatch: {module}")
        expected_manifest = f"modules/{module}/MANIFEST.sha256"
        if item.get("manifest") != expected_manifest:
            fail(errors, f"Manifest path mismatch: {module}")


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            fail(errors, f"Missing required file: {relative}")

    forbidden_state = ROOT / ".codex/zh-complex-project-state.md"
    if forbidden_state.exists():
        fail(errors, "Project state must not be committed: .codex/zh-complex-project-state.md")

    for old_reference in (
        "references/bundled-grilling.md",
        "references/bundled-minimal-code.md",
        "references/bundled-research-guardrails.md",
    ):
        if (ROOT / old_reference).exists():
            fail(errors, f"Obsolete v2.2 excerpt remains: {old_reference}")

    for path in authored_files():
        if path.suffix.lower() in {".pyc", ".pyo", ".log", ".zip"}:
            fail(errors, f"Generated artifact must not be committed: {path.relative_to(ROOT)}")
        if path.suffix.lower() in TEXT_SUFFIXES:
            try:
                path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                fail(errors, f"Authored file is not valid UTF-8: {path.relative_to(ROOT)}")

    version_file = (
        (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        if (ROOT / "VERSION").is_file()
        else None
    )
    if not version_file or not SEMVER.fullmatch(version_file):
        fail(errors, "VERSION must be a SemVer core version such as 3.0.0")

    if not SKILL.is_file():
        fail(errors, "SKILL.md is unavailable; frontmatter checks skipped")
    else:
        text = SKILL.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            fail(errors, "SKILL.md must start with YAML frontmatter delimited by ---")
        else:
            frontmatter, body = parts[1], parts[2]
            name = scalar(frontmatter, "name")
            description = scalar(frontmatter, "description")
            compatibility = scalar(frontmatter, "compatibility")
            license_value = scalar(frontmatter, "license")
            version_match = re.search(
                r'(?m)^  version:\s*["\']([^"\']+)["\']\s*$', frontmatter
            )

            if not name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                fail(errors, "Skill name must contain lowercase letters, digits, and single hyphens only")
            elif len(name) > 64:
                fail(errors, "Skill name exceeds 64 characters")
            elif ROOT.name != name:
                fail(errors, f"Skill name {name!r} must match directory name {ROOT.name!r}")
            if not description:
                fail(errors, "Frontmatter description is required")
            elif len(description) > 1024:
                fail(errors, "Frontmatter description exceeds 1024 characters")
            if compatibility and len(compatibility) > 500:
                fail(errors, "Frontmatter compatibility exceeds 500 characters")
            if not license_value or "LICENSE.md" not in license_value:
                fail(errors, "Frontmatter license must reference LICENSE.md")
            if not body.strip():
                fail(errors, "SKILL.md body is empty")
            if len(text.splitlines()) > 500:
                fail(errors, "SKILL.md exceeds the recommended 500-line limit")
            if not version_match:
                fail(errors, "metadata.version is required and must be quoted")
            elif version_file != version_match.group(1):
                fail(errors, "VERSION does not match SKILL.md metadata.version")

    changelog = ROOT / "CHANGELOG.md"
    if version_file and changelog.is_file():
        escaped_version = re.escape(version_file)
        if not re.search(
            rf"(?m)^## \[{escaped_version}\](?:\s|$)",
            changelog.read_text(encoding="utf-8"),
        ):
            fail(errors, f"CHANGELOG.md has no section for VERSION {version_file}")

    notices = ROOT / "THIRD_PARTY_NOTICES.md"
    if notices.is_file():
        notice_text = notices.read_text(encoding="utf-8")
        for marker in (*PINS.values(), *THIRD_PARTY_LICENSE_HASHES):
            if marker not in notice_text:
                fail(errors, f"THIRD_PARTY_NOTICES.md is missing required marker: {marker}")

    for relative, expected_hash in THIRD_PARTY_LICENSE_HASHES.items():
        license_path = ROOT / relative
        if license_path.is_file():
            actual_hash = hashlib.sha256(license_path.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                fail(errors, f"Third-party license differs from pinned upstream copy: {relative}")

    check_lock(errors)
    for module in MODULES:
        errors.extend(verify_module(module))
        try:
            count = len(snapshot_files(module))
            if count < MINIMUM_SNAPSHOT_FILES[module]:
                fail(errors, f"Embedded snapshot appears incomplete: {module} has {count} files")
        except ValueError as exc:
            fail(errors, str(exc))

    excluded_notice = (
        ROOT
        / "modules/nature-skills/upstream/skills/nature-figure/assets/figures4papers/THIRD_PARTY_NOTICES.md"
    )
    if excluded_notice.is_file():
        unexpected_payloads = [
            path
            for path in excluded_notice.parent.rglob("*")
            if path.is_file() and path != excluded_notice
        ]
        if unexpected_payloads:
            fail(errors, "Unlicensed figures4papers payloads must not be redistributed")

    unresolved = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\[TODO", re.IGNORECASE)
    for path in authored_files():
        if path.suffix.lower() in {".md", ".yml", ".yaml"}:
            if unresolved.search(path.read_text(encoding="utf-8")):
                fail(errors, f"Unresolved placeholder marker in {path.relative_to(ROOT)}")

    openai_yaml = ROOT / "agents/openai.yaml"
    if openai_yaml.is_file():
        ui = openai_yaml.read_text(encoding="utf-8")
        display_name = quoted_yaml_value(ui, "display_name")
        short_description = quoted_yaml_value(ui, "short_description")
        default_prompt = quoted_yaml_value(ui, "default_prompt")
        if not display_name:
            fail(errors, "agents/openai.yaml is missing quoted interface.display_name")
        if not short_description:
            fail(errors, "agents/openai.yaml is missing quoted interface.short_description")
        elif not 25 <= len(short_description) <= 64:
            fail(errors, "interface.short_description must contain 25 to 64 characters")
        if not default_prompt:
            fail(errors, "agents/openai.yaml is missing quoted interface.default_prompt")
        elif "$zh-complex-project-orchestrator" not in default_prompt:
            fail(errors, "interface.default_prompt must mention $zh-complex-project-orchestrator")
        if not re.search(
            r"(?m)^policy:\s*$\n  allow_implicit_invocation:\s*false\s*$", ui
        ):
            fail(errors, "agents/openai.yaml must set policy.allow_implicit_invocation to false")

    gitignore = ROOT / ".gitignore"
    if gitignore.is_file() and ".codex/zh-complex-project-state.md" not in gitignore.read_text(
        encoding="utf-8"
    ).splitlines():
        fail(errors, ".gitignore must exclude .codex/zh-complex-project-state.md")

    check_markdown_links(errors)

    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Repository is valid: {ROOT.name} {version_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
