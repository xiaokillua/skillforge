from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path


SEVERITY_ORDER = {"none": 0, "info": 1, "warn": 2, "high": 3}


@dataclass(slots=True)
class AuditFinding:
    severity: str
    title: str
    path: str
    detail: str


@dataclass(slots=True)
class AuditReport:
    findings: list[AuditFinding] = field(default_factory=list)
    scanned_files: int = 0

    @property
    def max_severity(self) -> str:
        highest = "none"
        for finding in self.findings:
            if SEVERITY_ORDER[finding.severity] > SEVERITY_ORDER[highest]:
                highest = finding.severity
        return highest

    def to_dict(self) -> dict[str, object]:
        return {
            "max_severity": self.max_severity,
            "scanned_files": self.scanned_files,
            "findings": [asdict(item) for item in self.findings],
        }


@dataclass(slots=True)
class SourceSnapshot:
    input_value: str
    local_path: Path
    repo_url: str | None
    owner: str | None
    repo_name: str
    cloned: bool = False


@dataclass(slots=True)
class RepoProfile:
    slug: str
    title: str
    summary: str
    source: str
    repo_url: str | None
    owner: str | None
    repo_name: str
    ecosystems: list[str]
    detected_tools: list[str]
    entrypoints: list[str]
    install_commands: list[str]
    usage_commands: list[str]
    docs_files: list[str]
    example_files: list[str]
    readme_path: str | None
    readme_excerpt: str
    license_name: str
    audit: AuditReport

    def to_dict(self) -> dict[str, object]:
        return {
            "slug": self.slug,
            "title": self.title,
            "summary": self.summary,
            "source": self.source,
            "repo_url": self.repo_url,
            "owner": self.owner,
            "repo_name": self.repo_name,
            "ecosystems": self.ecosystems,
            "detected_tools": self.detected_tools,
            "entrypoints": self.entrypoints,
            "install_commands": self.install_commands,
            "usage_commands": self.usage_commands,
            "docs_files": self.docs_files,
            "example_files": self.example_files,
            "readme_path": self.readme_path,
            "readme_excerpt": self.readme_excerpt,
            "license_name": self.license_name,
            "audit": self.audit.to_dict(),
        }
