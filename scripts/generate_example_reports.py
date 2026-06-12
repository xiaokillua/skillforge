from __future__ import annotations

import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

import sys

sys.path.insert(0, str(SRC))

from skillforge.reporting import generate_report, render_report_markdown
from skillforge.utils import write_text


EXAMPLE_SOURCE = "D4Vinci/Scrapling"
WORKSPACE_PLACEHOLDER = "/workspace/skillforge"
HOME_PLACEHOLDER = "/Users/demo"
TMP_PLACEHOLDER = "/tmp/skillforge-report-sample"


def main() -> int:
    examples_dir = ROOT / "examples"
    report_name = "SCRAPLING_REPORT"

    with tempfile.TemporaryDirectory(prefix="skillforge-report-sample-") as tmp:
        temp_root = Path(tmp)
        artifacts_dir = temp_root / "dist"
        report = generate_report(
            source=EXAMPLE_SOURCE,
            target="all",
            artifacts_dir=artifacts_dir,
            workspace=ROOT,
        )

        markdown = sanitize_text(
            render_report_markdown(report),
            temp_root=temp_root,
        )
        payload = sanitize_payload(
            report.to_dict(),
            temp_root=temp_root,
        )

        write_text(examples_dir / f"{report_name}.md", markdown)
        write_text(
            examples_dir / f"{report_name}.json",
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        )
    return 0


def sanitize_payload(payload: object, temp_root: Path) -> object:
    if isinstance(payload, dict):
        return {key: sanitize_payload(value, temp_root) for key, value in payload.items()}
    if isinstance(payload, list):
        return [sanitize_payload(value, temp_root) for value in payload]
    if isinstance(payload, str):
        return sanitize_text(payload, temp_root=temp_root)
    return payload


def sanitize_text(value: str, temp_root: Path) -> str:
    replacements = {
        str(ROOT): WORKSPACE_PLACEHOLDER,
        str(temp_root): TMP_PLACEHOLDER,
        str(Path.home()): HOME_PLACEHOLDER,
    }
    sanitized = value
    for original, replacement in replacements.items():
        sanitized = sanitized.replace(original, replacement)
    sanitized = sanitized.replace("/private/tmp/skillforge-report-sample", TMP_PLACEHOLDER)
    sanitized = sanitized.replace("/private/tmp", "/tmp")
    return sanitized


if __name__ == "__main__":
    raise SystemExit(main())
