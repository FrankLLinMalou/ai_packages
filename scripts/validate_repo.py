#!/usr/bin/env python3
"""Validate the repository without third-party Python dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


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
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".py", ".txt"}
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def scalar(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    return match.group(1).strip().strip('"\'')


def quoted_yaml_value(text: str, field: str, indent: int = 2) -> str | None:
    prefix = " " * indent
    match = re.search(rf'(?m)^{prefix}{re.escape(field)}:\s*"([^"]+)"\s*$', text)
    return match.group(1) if match else None


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_markdown_links(errors: list[str]) -> None:
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for document in ROOT.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(("#", "/")):
                continue
            relative = unquote(parsed.path)
            if relative and not (document.parent / relative).resolve().exists():
                fail(errors, f"Broken relative link in {document.relative_to(ROOT)}: {target}")


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            fail(errors, f"Missing required file: {relative}")

    forbidden_state = ROOT / ".codex/zh-complex-project-state.md"
    if forbidden_state.exists():
        fail(errors, "Project state must not be committed: .codex/zh-complex-project-state.md")

    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            try:
                path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                fail(errors, f"File is not valid UTF-8: {path.relative_to(ROOT)}")

    version_file = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").is_file() else None
    if not version_file or not SEMVER.fullmatch(version_file):
        fail(errors, "VERSION must be a SemVer core version such as 2.1.0")

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
            version_match = re.search(r'(?m)^  version:\s*["\']([^"\']+)["\']\s*$', frontmatter)

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
        if not re.search(rf"(?m)^## \[{escaped_version}\](?:\s|$)", changelog.read_text(encoding="utf-8")):
            fail(errors, f"CHANGELOG.md has no section for VERSION {version_file}")

    unresolved = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\[TODO", re.IGNORECASE)
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".yml", ".yaml"}:
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
        if not re.search(r"(?m)^policy:\s*$\n  allow_implicit_invocation:\s*false\s*$", ui):
            fail(errors, "agents/openai.yaml must set policy.allow_implicit_invocation to false")

    gitignore = ROOT / ".gitignore"
    if gitignore.is_file() and ".codex/zh-complex-project-state.md" not in gitignore.read_text(encoding="utf-8").splitlines():
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
