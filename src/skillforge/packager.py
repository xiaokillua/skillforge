from __future__ import annotations

import json
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

from .generator import PACKAGE_TARGETS, TARGETS, skill_files
from .models import RepoProfile, SEVERITY_ORDER
from .utils import ensure_parent, write_json, write_text


@dataclass(slots=True)
class BuildResult:
    profile: RepoProfile
    outputs: list[Path]


def build_packages(
    profile: RepoProfile,
    output_dir: Path,
    target: str,
    allow_risky: bool = False,
) -> BuildResult:
    normalized = target.lower()
    if normalized not in TARGETS:
        raise ValueError(f"Unknown target: {target}")
    if profile.audit.max_severity == "high" and not allow_risky:
        raise RuntimeError("Audit found high-risk patterns. Re-run with --allow-risky after review.")

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    if normalized == "all":
        for item in PACKAGE_TARGETS:
            outputs.extend(_build_one(profile, output_dir / item, item))
    else:
        outputs.extend(_build_one(profile, output_dir, normalized))

    return BuildResult(profile=profile, outputs=outputs)


def _build_one(profile: RepoProfile, base_output: Path, target: str) -> list[Path]:
    layout_root = _layout_root(base_output, target, profile.slug)
    file_map = skill_files(profile, target)
    created: list[Path] = []
    for relative, content in file_map.items():
        destination = layout_root / relative
        write_text(destination, content)
        created.append(destination)

    manifest = layout_root / "analysis.json"
    write_json(manifest, profile.to_dict())
    created.append(manifest)

    if target == "claude":
        archive = base_output / f"{profile.slug}.skill"
        _zip_skill(layout_root, archive)
        created.append(archive)
    return created


def _layout_root(base_output: Path, target: str, slug: str) -> Path:
    if target == "portable":
        return base_output / slug
    if target == "codex":
        return base_output / ".agents" / "skills" / slug
    if target == "copilot":
        return base_output / ".github" / "skills" / slug
    if target in {"openclaw", "hermes"}:
        return base_output / "skills" / slug
    if target == "claude":
        return base_output / ".claude" / "skills" / slug
    raise ValueError(f"Unknown target: {target}")


def _zip_skill(skill_root: Path, archive_path: Path) -> None:
    ensure_parent(archive_path)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in skill_root.rglob("*"):
            if not path.is_file():
                continue
            arcname = Path(skill_root.name) / path.relative_to(skill_root)
            bundle.write(path, arcname.as_posix())
