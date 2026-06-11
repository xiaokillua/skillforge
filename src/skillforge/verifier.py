from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath


VERIFY_TARGETS = {"auto", "portable", "claude", "codex", "copilot", "openclaw", "hermes"}

REQUIRED_FILES = (
    "SKILL.md",
    "analysis.json",
    "references/OVERVIEW.md",
    "references/INSTALL.md",
    "references/COMMANDS.md",
    "references/SECURITY-AUDIT.md",
    "references/REPO-METADATA.md",
    "assets/MANIFEST.txt",
)


@dataclass(slots=True)
class VerificationFinding:
    severity: str
    path: str
    message: str


@dataclass(slots=True)
class VerificationReport:
    target: str
    skill_name: str
    path: str
    archive: bool = False
    findings: list[VerificationFinding] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(item.severity == "error" for item in self.findings)

    @property
    def status(self) -> str:
        return "failed" if self.has_errors else "ok"

    def to_dict(self) -> dict[str, object]:
        return {
            "target": self.target,
            "skill_name": self.skill_name,
            "path": self.path,
            "archive": self.archive,
            "status": self.status,
            "findings": [
                {"severity": item.severity, "path": item.path, "message": item.message}
                for item in self.findings
            ],
        }


def verify_skill(path: Path, target: str = "auto", name: str | None = None) -> VerificationReport:
    normalized = target.lower()
    if normalized not in VERIFY_TARGETS:
        raise ValueError(f"Unknown verification target: {target}")

    candidate = path.expanduser().resolve()
    if candidate.is_file():
        if candidate.suffix != ".skill":
            raise FileNotFoundError(f"Unsupported file type for verification: {candidate}")
        if normalized not in {"auto", "claude"}:
            raise ValueError("Only the Claude target currently supports archive verification.")
        return _verify_archive(candidate)

    if not candidate.exists():
        raise FileNotFoundError(f"Skill path does not exist: {candidate}")
    if not candidate.is_dir():
        raise FileNotFoundError(f"Skill path is not a directory: {candidate}")

    skill_root, detected_target = _locate_skill_root(candidate, normalized, name)
    return _verify_directory(skill_root, detected_target)


def _locate_skill_root(base: Path, target: str, name: str | None) -> tuple[Path, str]:
    if (base / "SKILL.md").exists():
        detected = _detect_target_from_skill_dir(base, target)
        return base, detected

    if target == "auto":
        auto_candidates = (
            (base / ".claude" / "skills", "claude"),
            (base / ".agents" / "skills", "codex"),
            (base / ".github" / "skills", "copilot"),
            (base / "skills", "auto"),
        )
        for layout_dir, detected in auto_candidates:
            if layout_dir.exists():
                root = _pick_skill_dir(layout_dir, name)
                return root, _detect_target_from_skill_dir(root, detected)

        portable_root = _pick_portable_skill_dir(base, name)
        if portable_root:
            return portable_root, "portable"
        raise FileNotFoundError(f"Could not locate a generated skill under: {base}")

    if target == "portable":
        root = _pick_portable_skill_dir(base, name)
        if not root:
            raise FileNotFoundError(f"Could not locate a portable skill under: {base}")
        return root, "portable"

    if target == "claude":
        return _pick_skill_dir(base / ".claude" / "skills", name), "claude"
    if target == "codex":
        return _pick_skill_dir(base / ".agents" / "skills", name), "codex"
    if target == "copilot":
        return _pick_skill_dir(base / ".github" / "skills", name), "copilot"
    if target in {"openclaw", "hermes"}:
        return _pick_skill_dir(base / "skills", name), target
    raise ValueError(f"Unknown verification target: {target}")


def _pick_portable_skill_dir(base: Path, name: str | None) -> Path | None:
    if name:
        named = base / name
        if (named / "SKILL.md").exists():
            return named
        return None
    children = _skill_children(base)
    if len(children) == 1:
        return children[0]
    return None


def _pick_skill_dir(layout_dir: Path, name: str | None) -> Path:
    if not layout_dir.exists():
        raise FileNotFoundError(f"Expected skill directory does not exist: {layout_dir}")
    if name:
        named = layout_dir / name
        if not (named / "SKILL.md").exists():
            raise FileNotFoundError(f"Expected skill '{name}' was not found under: {layout_dir}")
        return named

    children = _skill_children(layout_dir)
    if not children:
        raise FileNotFoundError(f"No skill directories were found under: {layout_dir}")
    if len(children) > 1:
        raise FileNotFoundError(
            f"Multiple skills were found under {layout_dir}. Re-run verify with --name to select one."
        )
    return children[0]


def _skill_children(layout_dir: Path) -> list[Path]:
    return sorted(
        child
        for child in layout_dir.iterdir()
        if child.is_dir() and (child / "SKILL.md").exists()
    )


def _detect_target_from_skill_dir(skill_root: Path, requested: str) -> str:
    if requested != "auto":
        return requested

    skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    if skill_root.parent.name == "skills" and skill_root.parent.parent.name == ".claude":
        return "claude"
    if skill_root.parent.name == "skills" and skill_root.parent.parent.name == ".agents":
        return "codex"
    if skill_root.parent.name == "skills" and skill_root.parent.parent.name == ".github":
        return "copilot"
    if skill_root.parent.name == "skills":
        if re.search(r"(?m)^  openclaw:\s*$", skill_text):
            return "openclaw"
        if re.search(r"(?m)^  hermes:\s*$", skill_text):
            return "hermes"
    return "portable"


def _verify_directory(skill_root: Path, target: str) -> VerificationReport:
    report = VerificationReport(target=target, skill_name=skill_root.name, path=str(skill_root))
    for relative in REQUIRED_FILES:
        if not (skill_root / relative).exists():
            report.findings.append(VerificationFinding("error", relative, "Required file is missing."))

    skill_md = skill_root / "SKILL.md"
    frontmatter = ""
    if skill_md.exists():
        skill_text = skill_md.read_text(encoding="utf-8")
        frontmatter = _extract_frontmatter(skill_text)
        if not frontmatter:
            report.findings.append(VerificationFinding("error", "SKILL.md", "Missing YAML frontmatter block."))
        elif not _has_frontmatter_key(frontmatter, "description"):
            report.findings.append(
                VerificationFinding("warn", "SKILL.md", "Frontmatter should include a description for discovery.")
            )

    analysis_path = skill_root / "analysis.json"
    if analysis_path.exists():
        try:
            analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.findings.append(VerificationFinding("error", "analysis.json", f"Invalid JSON: {exc.msg}"))
        else:
            slug = analysis.get("slug")
            if isinstance(slug, str) and slug and slug != skill_root.name:
                report.findings.append(
                    VerificationFinding("warn", "analysis.json", f"Slug '{slug}' does not match directory name.")
                )

    _check_target_layout(report, skill_root, frontmatter)
    return report


def _verify_archive(archive_path: Path) -> VerificationReport:
    report = VerificationReport(
        target="claude",
        skill_name=archive_path.stem,
        path=str(archive_path),
        archive=True,
    )
    with zipfile.ZipFile(archive_path) as bundle:
        names = [
            item
            for item in bundle.namelist()
            if item and not item.endswith("/") and not item.startswith("__MACOSX/")
        ]
        if not names:
            report.findings.append(VerificationFinding("error", archive_path.name, "Archive is empty."))
            return report
        roots = {PurePosixPath(name).parts[0] for name in names}
        if len(roots) != 1:
            report.findings.append(
                VerificationFinding("error", archive_path.name, "Archive should contain exactly one top-level skill directory.")
            )
            return report

        root = next(iter(roots))
        archive_paths = set(names)
        for relative in REQUIRED_FILES:
            expected = f"{root}/{relative}"
            if expected not in archive_paths:
                report.findings.append(VerificationFinding("error", expected, "Required file is missing from archive."))

        skill_path = f"{root}/SKILL.md"
        if skill_path in archive_paths:
            skill_text = bundle.read(skill_path).decode("utf-8", errors="replace")
            frontmatter = _extract_frontmatter(skill_text)
            if not frontmatter:
                report.findings.append(
                    VerificationFinding("error", skill_path, "Missing YAML frontmatter block.")
                )
            elif not _has_frontmatter_key(frontmatter, "description"):
                report.findings.append(
                    VerificationFinding("warn", skill_path, "Frontmatter should include a description for discovery.")
                )
        report.skill_name = root
    return report


def _check_target_layout(report: VerificationReport, skill_root: Path, frontmatter: str) -> None:
    parent = skill_root.parent
    grandparent = parent.parent

    if report.target == "claude":
        if not (parent.name == "skills" and grandparent.name == ".claude"):
            report.findings.append(
                VerificationFinding("error", str(skill_root), "Claude skills should live under .claude/skills/<name>.")
            )
        return

    if report.target == "codex":
        if not (parent.name == "skills" and grandparent.name == ".agents"):
            report.findings.append(
                VerificationFinding("error", str(skill_root), "Codex skills should live under .agents/skills/<name>.")
            )
        return

    if report.target == "copilot":
        if not (parent.name == "skills" and grandparent.name == ".github"):
            report.findings.append(
                VerificationFinding("error", str(skill_root), "Copilot skills should live under .github/skills/<name>.")
            )
        return

    if report.target == "openclaw":
        if parent.name != "skills":
            report.findings.append(
                VerificationFinding("error", str(skill_root), "OpenClaw skills should live under skills/<name>.")
            )
        if frontmatter and not re.search(r"(?m)^  openclaw:\s*$", frontmatter):
            report.findings.append(
                VerificationFinding("warn", "SKILL.md", "OpenClaw metadata block was not found in frontmatter.")
            )
        return

    if report.target == "hermes":
        if parent.name != "skills":
            report.findings.append(
                VerificationFinding("error", str(skill_root), "Hermes skills should live under skills/<name>.")
            )
        if frontmatter and not _has_frontmatter_key(frontmatter, "platforms"):
            report.findings.append(
                VerificationFinding("warn", "SKILL.md", "Hermes skills usually include a platforms field.")
            )
        if frontmatter and not re.search(r"(?m)^  hermes:\s*$", frontmatter):
            report.findings.append(
                VerificationFinding("warn", "SKILL.md", "Hermes metadata block was not found in frontmatter.")
            )


def _extract_frontmatter(skill_text: str) -> str:
    lines = skill_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]).strip()
    return ""


def _has_frontmatter_key(frontmatter: str, key: str) -> bool:
    return bool(re.search(rf"(?m)^{re.escape(key)}:\s*.+$", frontmatter))
