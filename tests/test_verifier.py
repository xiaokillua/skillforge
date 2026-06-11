from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from skillforge.analyzer import analyze_repository
from skillforge.models import SourceSnapshot
from skillforge.packager import build_packages
from skillforge.verifier import verify_build_outputs, verify_skill


def make_profile(tmp_path: Path):
    repo = tmp_path / "demo-tool"
    repo.mkdir()
    (repo / "README.md").write_text(
        """# Demo Tool

Demo Tool helps automate boring setup work.

```bash
python3 -m pip install -e .
demo-tool scan ./repo
```
""",
        encoding="utf-8",
    )
    (repo / "pyproject.toml").write_text(
        """
[project]
name = "demo-tool"

[project.scripts]
demo-tool = "demo.cli:main"
""",
        encoding="utf-8",
    )
    snapshot = SourceSnapshot(
        input_value=str(repo),
        local_path=repo,
        repo_url=None,
        owner=None,
        repo_name="demo-tool",
    )
    return analyze_repository(snapshot)


class VerifierTests(unittest.TestCase):
    def test_verify_generated_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            profile = make_profile(tmp_path)
            build_packages(profile, tmp_path / "dist", "all")

            codex_report = verify_skill(tmp_path / "dist" / "codex", target="codex")
            claude_report = verify_skill(tmp_path / "dist" / "claude", target="claude")
            openclaw_report = verify_skill(tmp_path / "dist" / "openclaw", target="openclaw")
            hermes_report = verify_skill(tmp_path / "dist" / "hermes", target="hermes")

            self.assertFalse(codex_report.has_errors)
            self.assertEqual(codex_report.target, "codex")
            self.assertFalse(claude_report.has_errors)
            self.assertEqual(claude_report.target, "claude")
            self.assertFalse(openclaw_report.has_errors)
            self.assertFalse(hermes_report.has_errors)

    def test_verify_claude_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            profile = make_profile(tmp_path)
            build_packages(profile, tmp_path / "dist", "claude")

            report = verify_skill(tmp_path / "dist" / "demo-tool.skill")
            self.assertFalse(report.has_errors)
            self.assertTrue(report.archive)
            self.assertEqual(report.target, "claude")

    def test_verify_build_outputs_for_all_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            profile = make_profile(tmp_path)
            build_packages(profile, tmp_path / "dist", "all")

            reports = verify_build_outputs(tmp_path / "dist", "all", name=profile.slug)
            labels = {(report.target, report.archive) for report in reports}
            self.assertIn(("portable", False), labels)
            self.assertIn(("claude", False), labels)
            self.assertIn(("claude", True), labels)
            self.assertIn(("codex", False), labels)
            self.assertIn(("copilot", False), labels)
            self.assertIn(("openclaw", False), labels)
            self.assertIn(("hermes", False), labels)
            self.assertTrue(all(not report.has_errors for report in reports))

    def test_verify_missing_required_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            profile = make_profile(tmp_path)
            build_packages(profile, tmp_path / "dist", "portable")
            skill_root = tmp_path / "dist" / "demo-tool"
            (skill_root / "references" / "INSTALL.md").unlink()

            report = verify_skill(skill_root, target="portable")
            self.assertTrue(report.has_errors)
            messages = json.dumps(report.to_dict())
            self.assertIn("references/INSTALL.md", messages)


if __name__ == "__main__":
    unittest.main()
