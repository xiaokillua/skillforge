from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from skillforge.analyzer import analyze_repository, inspect_source
from skillforge.models import SourceSnapshot


class AnalyzerTests(unittest.TestCase):
    def test_local_repo_analysis_extracts_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
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
            profile = analyze_repository(snapshot)
            self.assertEqual(profile.slug, "demo-tool")
            self.assertIn("python", profile.ecosystems)
            self.assertIn("demo-tool", profile.entrypoints)
            self.assertIn("python3 -m pip install -e .", profile.install_commands)
            self.assertIn("demo-tool scan ./repo", profile.usage_commands)


    def test_inspect_source_supports_local_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = tmp_path / "sample"
            repo.mkdir()
            (repo / "README.md").write_text("# Sample\n\nA small sample.\n", encoding="utf-8")
            profile = inspect_source(str(repo))
            self.assertEqual(profile.title, "Sample")

    def test_html_hero_readme_falls_back_to_repo_name_and_detects_skill_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = tmp_path / "scrap-demo"
            repo.mkdir()
            (repo / "README.md").write_text(
                """<!-- hidden -->
<h1 align="center">
  <img alt="Scrap Demo Poster" src="cover.png">
</h1>

Scrap Demo is an adaptive scraping toolkit for dynamic sites.

It ships with a CLI and browser-assisted workflows.

# Platinum Sponsors
""",
                encoding="utf-8",
            )
            skill_dir = repo / "agent-skill" / "Scrap-Demo"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: scrap-demo\ndescription: Demo skill.\n---\n",
                encoding="utf-8",
            )
            profile = inspect_source(str(repo))
            self.assertEqual(profile.title, "Scrap Demo")
            self.assertIn("adaptive scraping toolkit", profile.summary.lower())
            self.assertIn("agent-skill/Scrap-Demo/SKILL.md", profile.existing_skill_files)


if __name__ == "__main__":
    unittest.main()
