from __future__ import annotations

import json
import re
from pathlib import Path


README_NAMES = (
    "README.md",
    "README.rst",
    "README.txt",
    "readme.md",
    "readme.rst",
    "readme.txt",
)

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".rst",
    ".py",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".conf",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".html",
    ".css",
    ".sql",
    ".dockerfile",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    ".turbo",
}

HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
HTML_TAG_RE = re.compile(r"<[^>]+>")
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "generated-skill"


def read_text(path: Path, limit: int = 200_000) -> str:
    data = path.read_bytes()[:limit]
    return data.decode("utf-8", errors="replace")


def is_text_candidate(path: Path) -> bool:
    if path.name in README_NAMES or path.name in {"Dockerfile", "Makefile"}:
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def find_readme(root: Path) -> Path | None:
    for name in README_NAMES:
        candidate = root / name
        if candidate.exists():
            return candidate
    return None


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        output.append(normalized)
    return output


def first_paragraphs(markdown: str, limit: int = 2) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    cleaned_markdown = HTML_COMMENT_RE.sub("", markdown)
    in_code_fence = False
    skip_until: str | None = None
    for raw_line in cleaned_markdown.splitlines():
        stripped_raw = raw_line.strip()
        if stripped_raw.startswith("```"):
            in_code_fence = not in_code_fence
            if current:
                paragraph = " ".join(current).strip()
                lowered = paragraph.lower()
                if paragraph and lowered not in {"sponsors", "platinum sponsors"}:
                    paragraphs.append(paragraph)
                current = []
                if len(paragraphs) >= limit:
                    break
            continue
        if in_code_fence:
            continue
        if skip_until:
            if skip_until in stripped_raw:
                skip_until = None
            continue
        if stripped_raw.startswith("<h1"):
            skip_until = "</h1>"
            continue
        if stripped_raw.startswith("<p ") and 'align="center"' in stripped_raw:
            skip_until = "</p>"
            continue
        if stripped_raw.startswith("<table"):
            skip_until = "</table>"
            continue
        if stripped_raw.count("<a ") >= 2:
            continue
        line = visible_markdown_text(raw_line)
        if not line:
            if current:
                paragraph = " ".join(current).strip()
                lowered = paragraph.lower()
                if paragraph and lowered not in {"sponsors", "platinum sponsors"}:
                    paragraphs.append(paragraph)
                current = []
                if len(paragraphs) >= limit:
                    break
            continue
        if line.startswith("#"):
            continue
        current.append(line)
    if current and len(paragraphs) < limit:
        paragraph = " ".join(current).strip()
        if paragraph and paragraph.lower() not in {"sponsors", "platinum sponsors"}:
            paragraphs.append(paragraph)
    return paragraphs[:limit]


def code_fences(markdown: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"```(?P<lang>[^\n`]*)\n(?P<body>.*?)```", re.DOTALL)
    fences: list[tuple[str, str]] = []
    for match in pattern.finditer(markdown):
        fences.append((match.group("lang").strip().lower(), match.group("body").strip()))
    return fences


def relative_paths(root: Path, paths: list[Path]) -> list[str]:
    return [str(path.relative_to(root)) for path in paths]


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def visible_markdown_text(raw_line: str) -> str:
    line = HTML_TAG_RE.sub(" ", raw_line)
    line = MARKDOWN_IMAGE_RE.sub(" ", line)
    line = MARKDOWN_LINK_RE.sub(r"\1", line)
    line = (
        line.replace("&middot;", " ")
        .replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
    )
    line = " ".join(line.split())
    return line.strip()
