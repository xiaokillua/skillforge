# SkillForge Report

- Generated on: `2026-06-12`
- SkillForge version: `0.3.0`
- Source: `https://github.com/D4Vinci/Scrapling.git`
- Target: `all`
- Skill name: `scrapling`
- Artifacts directory: `/tmp/skillforge-report-sample/dist`
- Workspace: `/workspace/skillforge`

## Repository Summary

- Title: `Scrapling`
- Ecosystems: python, docker
- Entrypoints: scrapling
- License: `LICENSE`
- Existing upstream skill files: `1`

Scrapling is an adaptive Web Scraping framework that handles everything from a single request to a full-scale crawl. Its parser learns from website changes and automatically relocates your elements when pages update. Its fetchers bypass anti-bot systems like Cloudflare Turnstile out of the box. And its spider framework lets you scale up to concurrent, multi-session crawls with pause/resume and automatic proxy rotation - all in a few lines of Python. One library, zero compromises.

## Audit Summary

- Max severity: `none`
- Files scanned: `202`

No audit findings were detected by the lightweight scan.

## Build and Verification

- Generated files: `49`

| Target | Artifact | Status | Path |
| --- | --- | --- | --- |
| `portable` | `layout` | `ok` | `/tmp/skillforge-report-sample/dist/portable/scrapling` |
| `claude` | `layout` | `ok` | `/tmp/skillforge-report-sample/dist/claude/.claude/skills/scrapling` |
| `claude` | `archive` | `ok` | `/tmp/skillforge-report-sample/dist/claude/scrapling.skill` |
| `codex` | `layout` | `ok` | `/tmp/skillforge-report-sample/dist/codex/.agents/skills/scrapling` |
| `copilot` | `layout` | `ok` | `/tmp/skillforge-report-sample/dist/copilot/.github/skills/scrapling` |
| `openclaw` | `layout` | `ok` | `/tmp/skillforge-report-sample/dist/openclaw/skills/scrapling` |
| `hermes` | `layout` | `ok` | `/tmp/skillforge-report-sample/dist/hermes/skills/scrapling` |

## Key Commands

### Install

- `pip install scrapling`
- `pip install "scrapling[fetchers]"`
- `pip install "scrapling[ai]"`
- `pip install "scrapling[shell]"`
- `pip install "scrapling[all]"`

### Usage

- `scrapling shell`
- `scrapling extract get 'https://example.com' content.md`
- `scrapling extract get 'https://example.com' content.txt --css-selector '#fromSkipToProducts' --impersonate 'chrome'  # All elements matching the CSS selector '#fromSkipToProducts'`
- `scrapling extract fetch 'https://example.com' content.md --css-selector '#fromSkipToProducts' --no-headless`
- `scrapling extract stealthy-fetch 'https://nopecha.com/demo/cloudflare' captchas.html --css-selector '#padded_content a' --solve-cloudflare`

## Existing Upstream Skills

- `agent-skill/Scrapling-Skill/SKILL.md`

## Local Runtime Readiness

| Runtime | Target | Status | CLI | Install Path |
| --- | --- | --- | --- | --- |
| Codex | `codex` | `ready` | `/Users/demo/.local/bin/codex` | `/workspace/skillforge/.agents/skills/<name>` |
| Claude Code | `claude` | `missing` | not found | `/workspace/skillforge/.claude/skills/<name>`<br>`/Users/demo/.claude/skills/<name>` |
| GitHub Copilot | `copilot` | `missing` | not found | `/workspace/skillforge/.github/skills/<name>` |
| OpenClaw | `openclaw` | `ready` | `/opt/homebrew/bin/openclaw` | `/Users/demo/.openclaw/workspace/skills/<name>` |
| Hermes | `hermes` | `ready` | `/Users/demo/.local/bin/hermes` | `/Users/demo/.hermes/skills/<name>` |

## Recommended Next Steps

1. Review `references/SECURITY-AUDIT.md` before trusting upstream install steps.
2. Install the generated layout into a runtime marked `ready` on this machine.
3. Share this report or rerun `skillforge doctor --markdown` if you need to post environment context.
