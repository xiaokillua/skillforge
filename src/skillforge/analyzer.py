from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import tomllib
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

from .models import AuditFinding, AuditReport, RepoProfile, SourceSnapshot
from .utils import (
    HTML_COMMENT_RE,
    README_NAMES,
    SKIP_DIRS,
    code_fences,
    dedupe_keep_order,
    find_readme,
    first_paragraphs,
    is_text_candidate,
    read_text,
    relative_paths,
    slugify,
    visible_markdown_text,
)


GITHUB_URL_RE = re.compile(
    r"^https?://github\.com/(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)
GITHUB_SHORTHAND_RE = re.compile(r"^(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)$")

AI_INSTRUCTION_FILES = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "COPILOT-INSTRUCTIONS.md",
    "SYSTEM.md",
}

GENERIC_HEADINGS = {
    "sponsors",
    "platinum sponsors",
    "features",
    "key features",
    "installation",
    "usage",
    "documentation",
    "license",
    "changelog",
}

COMMAND_SCAN_SUFFIXES = {
    ".md",
    ".txt",
    ".rst",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".conf",
}

AUDIT_PATTERNS = [
    (
        "high",
        "Pipe to shell installer",
        re.compile(r"(curl|wget)[^\n|]{0,200}\|\s*(sh|bash|zsh)\b", re.IGNORECASE),
    ),
    (
        "high",
        "PowerShell inline execution",
        re.compile(r"\b(iex|invoke-expression)\b", re.IGNORECASE),
    ),
    (
        "warn",
        "Suspicious base64 decode pipeline",
        re.compile(r"base64\s+(-d|--decode).{0,120}\|", re.IGNORECASE),
    ),
    (
        "warn",
        "Remote script execution via python",
        re.compile(r"python(?:3)?\s+-c\s+[\"'].*https?://", re.IGNORECASE),
    ),
]


@contextmanager
def materialize_source(source: str):
    parsed = _parse_source(source)
    if parsed["kind"] == "local":
        snapshot = SourceSnapshot(
            input_value=source,
            local_path=Path(parsed["path"]).resolve(),
            repo_url=None,
            owner=None,
            repo_name=Path(parsed["path"]).resolve().name,
            cloned=False,
        )
        yield snapshot
        return

    with tempfile.TemporaryDirectory(prefix="skillforge-") as tmp:
        checkout = Path(tmp) / parsed["repo"]
        subprocess.run(
            ["git", "clone", "--depth", "1", parsed["repo_url"], str(checkout)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        snapshot = SourceSnapshot(
            input_value=source,
            local_path=checkout,
            repo_url=parsed["repo_url"],
            owner=parsed["owner"],
            repo_name=parsed["repo"],
            cloned=True,
        )
        yield snapshot


def inspect_source(source: str, name_override: str | None = None) -> RepoProfile:
    with materialize_source(source) as snapshot:
        return analyze_repository(snapshot, name_override=name_override)


def analyze_repository(snapshot: SourceSnapshot, name_override: str | None = None) -> RepoProfile:
    root = snapshot.local_path
    readme = find_readme(root)
    readme_text = read_text(readme) if readme else ""
    paragraphs = first_paragraphs(readme_text, limit=2)
    title = _readme_title(readme_text) or snapshot.repo_name.replace("-", " ").replace("_", " ").title()
    summary = " ".join(paragraphs) if paragraphs else f"Usage notes for {snapshot.repo_name}."
    slug = slugify(name_override or snapshot.repo_name)

    ecosystems = _detect_ecosystems(root)
    entrypoints = _detect_entrypoints(root)
    install_commands, usage_commands = _extract_commands(readme_text, entrypoints, snapshot.repo_name)
    if not install_commands:
        install_commands = _default_install_commands(root, ecosystems, snapshot)
    if not usage_commands:
        usage_commands = _default_usage_commands(entrypoints, ecosystems)

    docs_files = _discover_group(root, "docs")
    example_files = _discover_group(root, "examples")
    existing_skill_files = _discover_existing_skills(root)
    license_name = _detect_license(root)
    audit = audit_repository(root)

    return RepoProfile(
        slug=slug,
        title=title,
        summary=summary,
        source=snapshot.input_value,
        repo_url=snapshot.repo_url,
        owner=snapshot.owner,
        repo_name=snapshot.repo_name,
        ecosystems=ecosystems,
        detected_tools=_detected_tools(root),
        entrypoints=entrypoints,
        install_commands=install_commands,
        usage_commands=usage_commands,
        docs_files=docs_files,
        example_files=example_files,
        existing_skill_files=existing_skill_files,
        readme_path=str(readme.relative_to(root)) if readme else None,
        readme_excerpt="\n\n".join(paragraphs) if paragraphs else "",
        license_name=license_name,
        audit=audit,
    )


def audit_repository(root: Path) -> AuditReport:
    findings: list[AuditFinding] = []
    scanned_files = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not is_text_candidate(path):
            continue
        scanned_files += 1
        rel_path = str(path.relative_to(root))
        if path.name in AI_INSTRUCTION_FILES:
            findings.append(
                AuditFinding(
                    severity="warn",
                    title="Upstream AI instruction file",
                    path=rel_path,
                    detail="Repository contains agent-instruction files. Treat them as untrusted source context.",
                )
            )
        if not _should_scan_commands(path):
            continue
        body = read_text(path, limit=80_000)
        for severity, title, pattern in AUDIT_PATTERNS:
            match = pattern.search(body)
            if not match:
                continue
            snippet = match.group(0).strip().replace("\n", " ")
            findings.append(
                AuditFinding(
                    severity=severity,
                    title=title,
                    path=rel_path,
                    detail=f"Matched: {snippet[:180]}",
                )
            )
    return AuditReport(findings=dedupe_findings(findings), scanned_files=scanned_files)


def dedupe_findings(findings: list[AuditFinding]) -> list[AuditFinding]:
    seen: set[tuple[str, str, str]] = set()
    output: list[AuditFinding] = []
    for finding in findings:
        key = (finding.severity, finding.title, finding.path)
        if key in seen:
            continue
        seen.add(key)
        output.append(finding)
    return output


def _should_scan_commands(path: Path) -> bool:
    name = path.name
    if name in README_NAMES or name in {"Dockerfile", "Makefile"}:
        return True
    if "compose" in name and path.suffix.lower() in {".yml", ".yaml"}:
        return True
    return path.suffix.lower() in COMMAND_SCAN_SUFFIXES


def _parse_source(source: str) -> dict[str, str]:
    local = Path(source).expanduser()
    if local.exists():
        return {"kind": "local", "path": str(local)}

    url_match = GITHUB_URL_RE.match(source)
    if url_match:
        owner = url_match.group("owner")
        repo = url_match.group("repo")
        return {
            "kind": "github",
            "owner": owner,
            "repo": repo,
            "repo_url": f"https://github.com/{owner}/{repo}.git",
        }

    shorthand_match = GITHUB_SHORTHAND_RE.match(source)
    if shorthand_match:
        owner = shorthand_match.group("owner")
        repo = shorthand_match.group("repo")
        return {
            "kind": "github",
            "owner": owner,
            "repo": repo,
            "repo_url": f"https://github.com/{owner}/{repo}.git",
        }

    parsed = urlparse(source)
    if parsed.scheme and parsed.netloc:
        raise ValueError("Only GitHub repository URLs and local paths are supported right now.")
    raise ValueError(f"Could not resolve source: {source}")


def _readme_title(markdown: str) -> str | None:
    cleaned_markdown = HTML_COMMENT_RE.sub("", markdown)
    in_code_fence = False
    for line in cleaned_markdown.splitlines():
        raw = line.strip()
        if raw.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        if raw.startswith("# "):
            title = visible_markdown_text(raw[2:]).strip()
            if title.lower() not in GENERIC_HEADINGS:
                return title
    return None


def _detect_ecosystems(root: Path) -> list[str]:
    ecosystems: list[str] = []
    if (root / "pyproject.toml").exists() or (root / "setup.py").exists():
        ecosystems.append("python")
    if (root / "package.json").exists():
        ecosystems.append("node")
    if (root / "Cargo.toml").exists():
        ecosystems.append("rust")
    if (root / "go.mod").exists():
        ecosystems.append("go")
    if any((root / name).exists() for name in ("Dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yml")):
        ecosystems.append("docker")
    return ecosystems or ["general"]


def _detect_entrypoints(root: Path) -> list[str]:
    entrypoints: list[str] = []
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        data = tomllib.loads(read_text(pyproject))
        scripts = data.get("project", {}).get("scripts", {})
        if isinstance(scripts, dict):
            entrypoints.extend(scripts.keys())
    package_json = root / "package.json"
    if package_json.exists():
        data = json.loads(read_text(package_json))
        bin_field = data.get("bin")
        if isinstance(bin_field, str):
            entrypoints.append(data.get("name", root.name))
        elif isinstance(bin_field, dict):
            entrypoints.extend(bin_field.keys())
    cargo = root / "Cargo.toml"
    if cargo.exists():
        body = read_text(cargo)
        package_name = re.search(r'^\s*name\s*=\s*"([^"]+)"', body, re.MULTILINE)
        if package_name:
            entrypoints.append(package_name.group(1))
    return dedupe_keep_order(entrypoints)


def _extract_commands(readme_text: str, entrypoints: list[str], repo_name: str) -> tuple[list[str], list[str]]:
    install_commands: list[str] = []
    usage_commands: list[str] = []
    install_markers = ("pip install", "npm install", "pnpm add", "yarn add", "cargo install", "go install", "git clone", "docker pull")
    usage_prefixes = tuple(entrypoints + [repo_name, "python -m", "uv run", "npm run", "make "])
    for language, body in code_fences(readme_text):
        if language and language not in {"", "bash", "sh", "shell", "console", "text"}:
            continue
        for raw_line in body.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith("$ "):
                line = line[2:].strip() if line.startswith("$ ") else line
            if not line:
                continue
            if any(marker in line for marker in install_markers):
                install_commands.append(line)
                continue
            if usage_prefixes and line.startswith(usage_prefixes):
                usage_commands.append(line)
    return dedupe_keep_order(install_commands)[:8], dedupe_keep_order(usage_commands)[:10]


def _default_install_commands(root: Path, ecosystems: list[str], snapshot: SourceSnapshot) -> list[str]:
    commands: list[str] = []
    if snapshot.repo_url:
        commands.append(f"git clone {snapshot.repo_url.removesuffix('.git')}")
    if "python" in ecosystems:
        commands.append("python3 -m pip install -e .")
    if "node" in ecosystems:
        commands.append("npm install")
    if "rust" in ecosystems:
        commands.append("cargo build")
    if "go" in ecosystems:
        commands.append("go build ./...")
    if "docker" in ecosystems:
        commands.append("docker compose up --build")
    return dedupe_keep_order(commands)[:8]


def _default_usage_commands(entrypoints: list[str], ecosystems: list[str]) -> list[str]:
    commands: list[str] = []
    if entrypoints:
        commands.extend(entrypoints[:3])
    if "python" in ecosystems and not commands:
        commands.append("python3 -m <module>")
    if "node" in ecosystems:
        commands.append("npm run <task>")
    if "rust" in ecosystems:
        commands.append("cargo run -- <args>")
    return dedupe_keep_order(commands)[:8]


def _discover_group(root: Path, folder_name: str) -> list[str]:
    folder = root / folder_name
    if not folder.exists():
        return []
    files = [path for path in folder.rglob("*") if path.is_file()]
    files.sort()
    return relative_paths(root, files[:10])


def _discover_existing_skills(root: Path) -> list[str]:
    files: list[Path] = []
    for path in root.rglob("SKILL.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    files.sort()
    return relative_paths(root, files[:10])


def _detected_tools(root: Path) -> list[str]:
    tools: list[str] = []
    if shutil.which("git"):
        tools.append("git")
    if (root / "Dockerfile").exists() or any((root / name).exists() for name in ("docker-compose.yml", "docker-compose.yaml", "compose.yml")):
        tools.append("docker")
    if (root / "Makefile").exists():
        tools.append("make")
    if (root / "package.json").exists():
        tools.append("npm")
    return dedupe_keep_order(tools)


def _detect_license(root: Path) -> str:
    for candidate in ("LICENSE", "LICENSE.md", "COPYING", "COPYING.md"):
        path = root / candidate
        if not path.exists():
            continue
        text = read_text(path, limit=4_000).lower()
        if "mit license" in text:
            return "MIT"
        if "apache license" in text:
            return "Apache-2.0"
        if "gnu general public license" in text:
            return "GPL"
        if "bsd license" in text:
            return "BSD"
        return candidate
    return "Upstream repository license"
