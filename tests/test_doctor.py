from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from skillforge.doctor import inspect_local_runtimes, render_doctor_markdown


class DoctorTests(unittest.TestCase):
    def test_inspect_local_runtimes_reports_statuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            workspace = tmp_path / "workspace"
            home = tmp_path / "home"
            workspace.mkdir()
            home.mkdir()

            paths = {
                "codex": "/usr/local/bin/codex",
                "code": "/usr/local/bin/code",
                "openclaw": "/usr/local/bin/openclaw",
                "hermes": "/usr/local/bin/hermes",
            }

            versions = {
                ("codex", "--version"): "codex-cli 0.133.0",
                ("code", "--version"): "1.101.0",
                ("openclaw", "--version"): "OpenClaw 2026.4.22 (00bd2cf)",
                ("hermes", "--version"): "Hermes Agent v0.16.0 (2026.6.5)",
            }

            def fake_which(name: str) -> str | None:
                return paths.get(name)

            def fake_runner(command: list[str]) -> str:
                return versions[tuple(command)]

            report = inspect_local_runtimes(
                workspace=workspace,
                home=home,
                which_lookup=fake_which,
                command_runner=fake_runner,
            )

            entries = {entry.target: entry for entry in report.entries}
            self.assertEqual(report.workspace, str(workspace.resolve()))
            self.assertEqual(entries["codex"].status, "ready")
            self.assertEqual(entries["codex"].version, "codex-cli 0.133.0")
            self.assertEqual(entries["claude"].status, "missing")
            self.assertEqual(entries["copilot"].status, "partial")
            self.assertEqual(entries["openclaw"].status, "ready")
            self.assertEqual(entries["hermes"].status, "ready")
            self.assertIn(".agents/skills/<name>", entries["codex"].install_paths[0])
            self.assertIn(".claude/skills/<name>", entries["claude"].install_paths[0])

    def test_render_doctor_markdown_contains_table_and_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            workspace = tmp_path / "workspace"
            home = tmp_path / "home"
            workspace.mkdir()
            home.mkdir()

            def fake_which(name: str) -> str | None:
                return { "codex": "/usr/local/bin/codex" }.get(name)

            def fake_runner(command: list[str]) -> str:
                return "codex-cli 0.133.0"

            report = inspect_local_runtimes(
                workspace=workspace,
                home=home,
                which_lookup=fake_which,
                command_runner=fake_runner,
            )
            markdown = render_doctor_markdown(report)
            self.assertIn("# SkillForge Doctor Report", markdown)
            self.assertIn("| Runtime | Target | Status | CLI | Version | Install Path |", markdown)
            self.assertIn("| Codex | `codex` | `ready` |", markdown)
            self.assertIn("## Notes", markdown)
            self.assertIn("### Codex", markdown)


if __name__ == "__main__":
    unittest.main()
