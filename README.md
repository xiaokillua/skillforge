# SkillForge

[![CI](https://github.com/xiaokillua/skillforge/actions/workflows/ci.yml/badge.svg)](https://github.com/xiaokillua/skillforge/actions/workflows/ci.yml)

[中文说明](README.zh-CN.md) | [Tutorial](docs/TUTORIAL.md) | [Project skill](skills/skillforge-repo-to-skill/SKILL.md)

SkillForge turns a GitHub repository into an audited, portable agent skill that works across Claude, Codex, GitHub Copilot, OpenClaw, Hermes, and other Agent Skills compatible runtimes.

It is built for one job: take a public repo, extract the useful setup and usage knowledge, run a lightweight safety audit, then package the result into target-specific skill layouts without requiring an API key.

## Why It Exists

Open-source repos are full of workflows that agents should know how to use, but most of that knowledge is trapped inside long READMEs, examples, install scripts, and repo-specific docs.

SkillForge bridges that gap:

- accepts a GitHub URL, `owner/repo`, or local checkout
- shallow-clones the repo and extracts install and usage commands
- detects ecosystems and entrypoints
- runs a lightweight audit for risky setup patterns
- emits a standard `SKILL.md` bundle plus target-specific packaging

## Supported Targets

- `portable`: raw Agent Skills directory
- `claude`: raw skill folder plus `.skill` archive
- `codex`: `.agents/skills/<name>`
- `copilot`: `.github/skills/<name>`
- `openclaw`: `skills/<name>`
- `hermes`: `skills/<name>`
- `all`: generate every layout in one run

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
```

## Quick Start

Inspect a repo:

```bash
skillforge inspect openai/openai-python
```

Build every target:

```bash
skillforge build openai/openai-python --output ./dist --target all
```

Build only a Codex-compatible layout:

```bash
skillforge build openai/openai-python --target codex --output ./dist
```

Build from a local checkout:

```bash
skillforge build ~/code/my-tool --target portable --output ./dist
```

If the audit finds a high-risk pattern, SkillForge stops by default:

```bash
skillforge build owner/risky-repo --output ./dist
```

Override only after review:

```bash
skillforge build owner/risky-repo --output ./dist --allow-risky
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

## Security Model

SkillForge is intentionally conservative.

- It audits upstream docs and execution-oriented files for risky patterns such as `curl` piped into a shell, inline PowerShell execution, suspicious base64 pipelines, and upstream AI instruction files.
- It stops packaging when the highest severity is `high`, unless you explicitly pass `--allow-risky`.
- It keeps the generated `SKILL.md` concise and pushes detail into `references/`.

This is not a full malware scanner. It is a fast first pass that helps you avoid blindly trusting upstream automation.

## CLI Reference

```bash
skillforge inspect SOURCE [--json] [--name NAME]
skillforge build SOURCE [--target TARGET] [--output DIR] [--name NAME] [--allow-risky]
skillforge version
```

`SOURCE` can be:

- `https://github.com/owner/repo`
- `owner/repo`
- `/local/path/to/repo`

## Development

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
```

## Roadmap

- optional LLM-assisted summarization mode
- better monorepo package selection
- richer ecosystem adapters for Go, Rust, and Docker services
- publish helpers for Hermes taps and Claude upload bundles
- comparison mode for with-skill vs baseline agent performance

## License

MIT
