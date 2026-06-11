from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import __version__
from .analyzer import inspect_source
from .doctor import DoctorReport, inspect_local_runtimes
from .models import RepoProfile
from .packager import BuildResult, build_packages
from .verifier import VerificationReport, verify_build_outputs


@dataclass(slots=True)
class SkillForgeReport:
    source: str
    target: str
    artifacts_dir: str
    workspace: str
    generated_on: str
    profile: RepoProfile
    build_result: BuildResult
    verification_reports: list[VerificationReport]
    doctor_report: DoctorReport


def generate_report(
    source: str,
    target: str,
    artifacts_dir: Path,
    workspace: Path,
    name_override: str | None = None,
    allow_risky: bool = False,
) -> SkillForgeReport:
    profile = inspect_source(source, name_override=name_override)
    build_result = build_packages(
        profile=profile,
        output_dir=artifacts_dir,
        target=target,
        allow_risky=allow_risky,
    )
    verification_reports = verify_build_outputs(
        output_dir=artifacts_dir,
        target=target,
        name=build_result.profile.slug,
    )
    doctor_report = inspect_local_runtimes(workspace)
    return SkillForgeReport(
        source=source,
        target=target,
        artifacts_dir=str(artifacts_dir.resolve()),
        workspace=str(workspace.resolve()),
        generated_on=str(date.today()),
        profile=profile,
        build_result=build_result,
        verification_reports=verification_reports,
        doctor_report=doctor_report,
    )


def render_report_markdown(report: SkillForgeReport) -> str:
    source_line = report.profile.repo_url or report.profile.source
    lines = [
        "# SkillForge Report",
        "",
        f"- Generated on: `{report.generated_on}`",
        f"- SkillForge version: `{__version__}`",
        f"- Source: `{source_line}`",
        f"- Target: `{report.target}`",
        f"- Skill name: `{report.profile.slug}`",
        f"- Artifacts directory: `{report.artifacts_dir}`",
        f"- Workspace: `{report.workspace}`",
        "",
        "## Repository Summary",
        "",
        f"- Title: `{report.profile.title}`",
        f"- Ecosystems: {', '.join(report.profile.ecosystems)}",
        f"- Entrypoints: {', '.join(report.profile.entrypoints) if report.profile.entrypoints else 'none detected'}",
        f"- License: `{report.profile.license_name}`",
        f"- Existing upstream skill files: `{len(report.profile.existing_skill_files)}`",
        "",
        report.profile.summary,
        "",
        "## Audit Summary",
        "",
        f"- Max severity: `{report.profile.audit.max_severity}`",
        f"- Files scanned: `{report.profile.audit.scanned_files}`",
        "",
    ]

    if report.profile.audit.findings:
        lines.append("### Findings")
        lines.append("")
        for finding in report.profile.audit.findings[:5]:
            lines.append(
                f"- [{finding.severity.upper()}] `{finding.path}`: {finding.title}. {finding.detail}"
            )
        lines.append("")
    else:
        lines.extend(
            [
                "No audit findings were detected by the lightweight scan.",
                "",
            ]
        )

    lines.extend(
        [
            "## Build and Verification",
            "",
            f"- Generated files: `{len(report.build_result.outputs)}`",
            "",
            "| Target | Artifact | Status | Path |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in report.verification_reports:
        artifact = "archive" if item.archive else "layout"
        lines.append(
            f"| `{item.target}` | `{artifact}` | `{item.status}` | `{item.path}` |"
        )
    lines.append("")

    lines.extend(
        [
            "## Key Commands",
            "",
            "### Install",
            "",
        ]
    )
    if report.profile.install_commands:
        for command in report.profile.install_commands[:5]:
            lines.append(f"- `{command}`")
    else:
        lines.append("- No install command was extracted.")
    lines.extend(["", "### Usage", ""])
    if report.profile.usage_commands:
        for command in report.profile.usage_commands[:5]:
            lines.append(f"- `{command}`")
    else:
        lines.append("- No usage command was extracted.")
    lines.append("")

    if report.profile.existing_skill_files:
        lines.extend(["## Existing Upstream Skills", ""])
        for path in report.profile.existing_skill_files[:5]:
            lines.append(f"- `{path}`")
        lines.append("")

    lines.extend(
        [
            "## Local Runtime Readiness",
            "",
            "| Runtime | Target | Status | CLI | Install Path |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for entry in report.doctor_report.entries:
        cli_value = f"`{entry.cli_path}`" if entry.cli_path else "not found"
        install_value = "<br>".join(f"`{path}`" for path in entry.install_paths)
        lines.append(
            f"| {entry.runtime} | `{entry.target}` | `{entry.status}` | {cli_value} | {install_value} |"
        )
    lines.append("")

    lines.extend(
        [
            "## Recommended Next Steps",
            "",
            "1. Review `references/SECURITY-AUDIT.md` before trusting upstream install steps.",
            "2. Install the generated layout into a runtime marked `ready` on this machine.",
            "3. Share this report or rerun `skillforge doctor --markdown` if you need to post environment context.",
            "",
        ]
    )
    return "\n".join(lines)
