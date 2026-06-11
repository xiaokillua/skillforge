from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from skillforge.reporting import generate_report, render_report_markdown


def make_repo(tmp_path: Path) -> Path:
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
    return repo


class ReportingTests(unittest.TestCase):
    def test_generate_report_and_render_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = make_repo(tmp_path)
            report = generate_report(
                source=str(repo),
                target="portable",
                artifacts_dir=tmp_path / "dist",
                workspace=tmp_path / "workspace",
            )
            markdown = render_report_markdown(report)
            self.assertEqual(report.profile.slug, "demo-tool")
            self.assertEqual(report.target, "portable")
            self.assertIn("# SkillForge Report", markdown)
            self.assertIn("## Repository Summary", markdown)
            self.assertIn("## Build and Verification", markdown)
            self.assertIn("## Local Runtime Readiness", markdown)


if __name__ == "__main__":
    unittest.main()
