from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from . import __version__


CommandRunner = Callable[[list[str]], str]
WhichLookup = Callable[[str], str | None]


@dataclass(slots=True)
class RuntimeDoctorEntry:
    runtime: str
    target: str
    status: str
    cli_path: str | None
    version: str | None
    install_paths: list[str]
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "runtime": self.runtime,
            "target": self.target,
            "status": self.status,
            "cli_path": self.cli_path,
            "version": self.version,
            "install_paths": self.install_paths,
            "notes": self.notes,
        }


@dataclass(slots=True)
class DoctorReport:
    skillforge_version: str
    workspace: str
    home: str
    entries: list[RuntimeDoctorEntry]

    def to_dict(self) -> dict[str, object]:
        return {
            "skillforge_version": self.skillforge_version,
            "workspace": self.workspace,
            "home": self.home,
            "entries": [item.to_dict() for item in self.entries],
        }


def inspect_local_runtimes(
    workspace: Path,
    home: Path | None = None,
    which_lookup: WhichLookup | None = None,
    command_runner: CommandRunner | None = None,
) -> DoctorReport:
    resolved_workspace = workspace.resolve()
    resolved_home = (home or Path.home()).expanduser().resolve()
    which = which_lookup or shutil.which
    runner = command_runner or _run_command

    entries = [
        _codex_entry(resolved_workspace, which, runner),
        _claude_entry(resolved_workspace, resolved_home, which, runner),
        _copilot_entry(resolved_workspace, which, runner),
        _openclaw_entry(resolved_home, which, runner),
        _hermes_entry(resolved_home, which, runner),
    ]
    return DoctorReport(
        skillforge_version=__version__,
        workspace=str(resolved_workspace),
        home=str(resolved_home),
        entries=entries,
    )


def _codex_entry(workspace: Path, which: WhichLookup, runner: CommandRunner) -> RuntimeDoctorEntry:
    cli_path = which("codex")
    install_path = str(workspace / ".agents" / "skills" / "<name>")
    if not cli_path:
        return RuntimeDoctorEntry(
            runtime="Codex",
            target="codex",
            status="missing",
            cli_path=None,
            version=None,
            install_paths=[install_path],
            notes=["Codex CLI was not found on PATH."],
        )
    return RuntimeDoctorEntry(
        runtime="Codex",
        target="codex",
        status="ready",
        cli_path=cli_path,
        version=_safe_version(runner, ["codex", "--version"]),
        install_paths=[install_path],
        notes=["Project-local Codex skills live under .agents/skills/<name>."],
    )


def _claude_entry(workspace: Path, home: Path, which: WhichLookup, runner: CommandRunner) -> RuntimeDoctorEntry:
    cli_path = which("claude")
    install_paths = [
        str(workspace / ".claude" / "skills" / "<name>"),
        str(home / ".claude" / "skills" / "<name>"),
    ]
    if not cli_path:
        return RuntimeDoctorEntry(
            runtime="Claude Code",
            target="claude",
            status="missing",
            cli_path=None,
            version=None,
            install_paths=install_paths,
            notes=["Claude CLI was not found on PATH."],
        )
    return RuntimeDoctorEntry(
        runtime="Claude Code",
        target="claude",
        status="ready",
        cli_path=cli_path,
        version=_safe_version(runner, ["claude", "--version"]),
        install_paths=install_paths,
        notes=[
            "Project-local Claude skills live under .claude/skills/<name>.",
            "Personal Claude skills live under ~/.claude/skills/<name>.",
        ],
    )


def _copilot_entry(workspace: Path, which: WhichLookup, runner: CommandRunner) -> RuntimeDoctorEntry:
    cli_path = which("code")
    install_path = str(workspace / ".github" / "skills" / "<name>")
    if not cli_path:
        return RuntimeDoctorEntry(
            runtime="GitHub Copilot",
            target="copilot",
            status="missing",
            cli_path=None,
            version=None,
            install_paths=[install_path],
            notes=[
                "VS Code CLI was not found on PATH.",
                "SkillForge can still generate Copilot layouts, but local runtime readiness was not detected.",
            ],
        )
    return RuntimeDoctorEntry(
        runtime="GitHub Copilot",
        target="copilot",
        status="partial",
        cli_path=cli_path,
        version=_safe_version(runner, ["code", "--version"]),
        install_paths=[install_path],
        notes=[
            "VS Code CLI is available, but the Copilot extension and login are not verified automatically.",
            "Project-local Copilot skills live under .github/skills/<name>.",
        ],
    )


def _openclaw_entry(home: Path, which: WhichLookup, runner: CommandRunner) -> RuntimeDoctorEntry:
    cli_path = which("openclaw")
    install_path = str(home / ".openclaw" / "workspace" / "skills" / "<name>")
    if not cli_path:
        return RuntimeDoctorEntry(
            runtime="OpenClaw",
            target="openclaw",
            status="missing",
            cli_path=None,
            version=None,
            install_paths=[install_path],
            notes=["OpenClaw CLI was not found on PATH."],
        )
    return RuntimeDoctorEntry(
        runtime="OpenClaw",
        target="openclaw",
        status="ready",
        cli_path=cli_path,
        version=_safe_version(runner, ["openclaw", "--version"]),
        install_paths=[install_path],
        notes=["Default OpenClaw workspace skills path is ~/.openclaw/workspace/skills/<name>."],
    )


def _hermes_entry(home: Path, which: WhichLookup, runner: CommandRunner) -> RuntimeDoctorEntry:
    cli_path = which("hermes")
    install_path = str(home / ".hermes" / "skills" / "<name>")
    if not cli_path:
        return RuntimeDoctorEntry(
            runtime="Hermes",
            target="hermes",
            status="missing",
            cli_path=None,
            version=None,
            install_paths=[install_path],
            notes=["Hermes CLI was not found on PATH."],
        )
    return RuntimeDoctorEntry(
        runtime="Hermes",
        target="hermes",
        status="ready",
        cli_path=cli_path,
        version=_safe_version(runner, ["hermes", "--version"]),
        install_paths=[install_path],
        notes=["Default Hermes skills path is ~/.hermes/skills/<name>."],
    )


def _safe_version(runner: CommandRunner, command: list[str]) -> str | None:
    try:
        return runner(command)
    except Exception:
        return None


def _run_command(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    output = (completed.stdout or completed.stderr).strip()
    if not output:
        return ""
    return output.splitlines()[0].strip()
