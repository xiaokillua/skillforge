# SkillForge

[![CI](https://github.com/xiaokillua/skillforge/actions/workflows/ci.yml/badge.svg)](https://github.com/xiaokillua/skillforge/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/xiaokillua/skillforge)](https://github.com/xiaokillua/skillforge/releases)
[![License](https://img.shields.io/github/license/xiaokillua/skillforge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)

[中文说明](README.zh-CN.md) | [Tutorial](docs/TUTORIAL.md) | [Compatibility](docs/RUNTIME_COMPATIBILITY.md) | [Sample Report](examples/SCRAPLING_REPORT.md) | [Sample JSON](examples/SCRAPLING_REPORT.json) | [Contributing](CONTRIBUTING.md) | [Security](SECURITY.md) | [Project skill](skills/skillforge-repo-to-skill/SKILL.md)

SkillForge compiles a GitHub repository into an audited, portable agent skill that works across Claude, Codex, GitHub Copilot, OpenClaw, Hermes, and other Agent Skills compatible runtimes.

It is built for one job: take a public repo, extract the setup and usage knowledge an agent actually needs, run a lightweight safety audit, then package the result into target-specific skill layouts without requiring an API key.

Validated runtime paths already exist for `Codex`, `Hermes`, and `OpenClaw`, while `Claude` and `Copilot` are packaging-verified and ready for local install.

## Why SkillForge

| Capability | README summarizer | One-target exporter | SkillForge |
| --- | --- | --- | --- |
| Extract install and usage commands | partial | yes | yes |
| Run an upstream safety pass | no | rare | yes |
| Package for multiple runtimes | no | partial | yes |
| Verify generated layouts | no | rare | yes |
| Report local runtime readiness | no | no | yes |
| Export a shareable markdown or JSON report | no | no | yes |

## How It Works

```mermaid
flowchart LR
    A["GitHub repo or local checkout"] --> B["Inspect README, docs, and entrypoints"]
    B --> C["Audit install paths and instruction files"]
    C --> D["Generate portable skill bundle"]
    D --> E["Package for Claude, Codex, Copilot, OpenClaw, and Hermes"]
    E --> F["Verify layouts and export report artifacts"]
```

## Why It Exists

Open-source repos are full of workflows that agents should know how to use, but most of that knowledge is trapped inside long READMEs, examples, install scripts, and repo-specific docs.

SkillForge bridges that gap:

- accepts a GitHub URL, `owner/repo`, or local checkout
- shallow-clones the repo and extracts install and usage commands
- detects ecosystems and entrypoints
- detects upstream `SKILL.md` bundles when the repo already ships agent skills
- runs a lightweight audit for risky setup patterns
- emits a standard `SKILL.md` bundle plus target-specific packaging
- verifies the generated layout before you install it into an agent runtime

## Supported Targets

- `portable`: raw Agent Skills directory
- `claude`: `.claude/skills/<name>` plus an optional `.skill` archive
- `codex`: `.agents/skills/<name>`
- `copilot`: `.github/skills/<name>`
- `openclaw`: `skills/<name>`
- `hermes`: `skills/<name>`
- `all`: generate every layout in one run

## Compatibility Snapshot

Validated on `2026-06-12` with SkillForge `v0.3.0`.

| Runtime | Status | Validation |
| --- | --- | --- |
| Codex | Supported | Runtime validated |
| Claude Code | Supported | Packaging validated |
| GitHub Copilot | Supported | Layout validated |
| OpenClaw | Supported | Runtime validated |
| Hermes | Supported | Runtime validated |

See the full matrix in [Runtime Compatibility](docs/RUNTIME_COMPATIBILITY.md).

## Launch Assets

- [Codex Showcase](examples/CODEX_SHOWCASE.md)
- [Scrapling Showcase](examples/SCRAPLING_SHOWCASE.md)
- [Claude Showcase](examples/CLAUDE_SHOWCASE.md)
- [Hermes Showcase](examples/HERMES_SHOWCASE.md)
- [OpenClaw Showcase](examples/OPENCLAW_SHOWCASE.md)
- [Sample markdown report](examples/SCRAPLING_REPORT.md)
- [Sample JSON report](examples/SCRAPLING_REPORT.json)

## Install

From a clone:

```bash
git clone https://github.com/xiaokillua/skillforge.git
cd skillforge
python3 -m pip install -e .
```

Check it:

```bash
skillforge version
skillforge doctor
```

Install without cloning:

```bash
python3 -m pip install "git+https://github.com/xiaokillua/skillforge.git"
```

For an isolated CLI install:

```bash
pipx install "git+https://github.com/xiaokillua/skillforge.git"
```

## Quick Start

Check which targets are usable on your machine:

```bash
skillforge doctor
skillforge doctor --markdown
```

Inspect a repo:

```bash
skillforge inspect openai/openai-python
```

Build every target:

```bash
skillforge build openai/openai-python --output ./dist --target all --verify
```

Build only a Codex-compatible layout:

```bash
skillforge build openai/openai-python --target codex --output ./dist --verify
```

Build from a local checkout:

```bash
skillforge build ~/code/my-tool --target portable --output ./dist --verify
```

Build a Hermes-ready layout:

```bash
skillforge build D4Vinci/Scrapling --target hermes --name skillforge-scrapling-hermes --output ./dist --verify
```

Build an OpenClaw-ready layout:

```bash
skillforge build D4Vinci/Scrapling --target openclaw --name skillforge-scrapling-openclaw --output ./dist --verify
```

Build a Claude Code-ready layout:

```bash
skillforge build D4Vinci/Scrapling --target claude --name skillforge-scrapling-claude --output ./dist --verify
```

Verify a generated target after the fact:

```bash
skillforge verify ./dist --target codex
```

Verify a Claude archive:

```bash
skillforge verify ./dist/skillforge-scrapling-claude.skill
```

Generate a shareable report:

```bash
skillforge report openai/openai-python --target all --artifacts ./dist --output ./skillforge-report.md
```

Generate the same report as structured JSON:

```bash
skillforge report openai/openai-python --target all --artifacts ./dist --json --output ./skillforge-report.json
```

See a real report generated from `D4Vinci/Scrapling`:

- [Markdown sample](examples/SCRAPLING_REPORT.md)
- [JSON sample](examples/SCRAPLING_REPORT.json)

Regenerate those sample artifacts locally:

```bash
python3 scripts/generate_example_reports.py
```

If the audit finds a high-risk pattern, SkillForge stops by default:

```bash
skillforge build owner/risky-repo --output ./dist
```

Override only after review:

```bash
skillforge build owner/risky-repo --output ./dist --allow-risky --verify
```

## Output Layout

A generated skill includes:

```text
my-skill/
  SKILL.md
  analysis.json
  references/
    OVERVIEW.md
    INSTALL.md
    COMMANDS.md
    SECURITY-AUDIT.md
    REPO-METADATA.md
  assets/
    MANIFEST.txt
```

Target-specific packaging wraps that same content in each runtime's preferred directory structure. For Claude Code, SkillForge now writes `.claude/skills/<name>/SKILL.md` and also emits a `<name>.skill` archive as a convenience artifact for sharing.

## Security Model

SkillForge is intentionally conservative.

- It audits upstream docs and execution-oriented files for risky patterns such as `curl` piped into a shell, inline PowerShell execution, suspicious base64 pipelines, and upstream AI instruction files.
- It stops packaging when the highest severity is `high`, unless you explicitly pass `--allow-risky`.
- It keeps the generated `SKILL.md` concise and pushes detail into `references/`.

This is not a full malware scanner. It is a fast first pass that helps you avoid blindly trusting upstream automation.

## CLI Reference

```bash
skillforge inspect SOURCE [--json] [--name NAME]
skillforge build SOURCE [--target TARGET] [--output DIR] [--name NAME] [--allow-risky] [--verify]
skillforge verify PATH [--target TARGET] [--name NAME] [--json]
skillforge doctor [--workspace DIR] [--json | --markdown]
skillforge report SOURCE [--target TARGET] [--artifacts DIR] [--workspace DIR] [--name NAME] [--allow-risky] [--json] [--output FILE]
skillforge version
```

`SOURCE` can be:

- `https://github.com/owner/repo`
- `owner/repo`
- `/local/path/to/repo`

## Development

```bash
python3 -m pip install -e ".[dev]"
python3 -m unittest discover -s tests
python3 -m build
```

## Release Flow

- CI now tests Python `3.11`, `3.12`, and `3.13`
- CI also builds `sdist` and `wheel`, then runs `twine check`
- Release artifacts are attached automatically to GitHub Releases
- PyPI publishing is supported through Trusted Publishing when you configure a PyPI publisher and set the repository variable `PYPI_PUBLISH=true`

## Community

- [Contributing guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Code of conduct](CODE_OF_CONDUCT.md)

## Roadmap

- optional LLM-assisted summarization mode
- better monorepo package selection
- richer ecosystem adapters for Go, Rust, and Docker services
- publish helpers for Hermes taps and skill catalogs
- comparison mode for with-skill vs baseline agent performance

## License

MIT
