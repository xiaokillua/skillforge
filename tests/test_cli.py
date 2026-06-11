from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from skillforge.cli import main


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


class CliTests(unittest.TestCase):
    def test_build_with_verify_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = make_repo(tmp_path)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "build",
                        str(repo),
                        "--target",
                        "claude",
                        "--output",
                        str(tmp_path / "dist"),
                        "--verify",
                    ]
                )

            output = stdout.getvalue()
            self.assertEqual(code, 0, stderr.getvalue())
            self.assertIn("Built skill 'demo-tool'", output)
            self.assertIn("Verification:", output)
            self.assertIn("[OK] claude:", output)
            self.assertIn("[OK] claude archive:", output)

    def test_doctor_json_succeeds(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(["doctor", "--workspace", ".", "--json"])

        output = stdout.getvalue()
        self.assertEqual(code, 0, stderr.getvalue())
        self.assertIn('"skillforge_version"', output)
        self.assertIn('"entries"', output)

    def test_doctor_markdown_succeeds(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(["doctor", "--workspace", ".", "--markdown"])

        output = stdout.getvalue()
        self.assertEqual(code, 0, stderr.getvalue())
        self.assertIn("# SkillForge Doctor Report", output)
        self.assertIn("| Runtime | Target | Status | CLI | Version | Install Path |", output)

    def test_report_writes_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = make_repo(tmp_path)
            stdout = io.StringIO()
            stderr = io.StringIO()
            report_path = tmp_path / "skillforge-report.md"

            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "report",
                        str(repo),
                        "--target",
                        "portable",
                        "--artifacts",
                        str(tmp_path / "dist"),
                        "--workspace",
                        str(tmp_path / "workspace"),
                        "--output",
                        str(report_path),
                    ]
                )

            self.assertEqual(code, 0, stderr.getvalue())
            self.assertTrue(report_path.exists())
            content = report_path.read_text(encoding="utf-8")
            self.assertIn("# SkillForge Report", content)
            self.assertIn("## Build and Verification", content)

    def test_report_writes_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            repo = make_repo(tmp_path)
            stdout = io.StringIO()
            stderr = io.StringIO()
            report_path = tmp_path / "skillforge-report.json"

            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    [
                        "report",
                        str(repo),
                        "--target",
                        "portable",
                        "--artifacts",
                        str(tmp_path / "dist"),
                        "--workspace",
                        str(tmp_path / "workspace"),
                        "--json",
                        "--output",
                        str(report_path),
                    ]
                )

            self.assertEqual(code, 0, stderr.getvalue())
            self.assertTrue(report_path.exists())
            payload = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["target"], "portable")
            self.assertIn("doctor_report", payload)
            self.assertTrue(payload["verification_reports"])


if __name__ == "__main__":
    unittest.main()
