---
name: skillforge-repo-to-skill
description: Use this skill when the task is to turn a GitHub repository or local codebase into a portable agent skill for Claude, Codex, GitHub Copilot, OpenClaw, Hermes, or other Agent Skills compatible runtimes.
license: MIT
compatibility: Requires git, Python 3.11+, and shell access.
metadata:
  author: xiaokillua
  project: skillforge
---

# SkillForge Repo to Skill

Use this skill when the user wants to package a repository as an agent skill instead of manually writing `SKILL.md`.

## Workflow

1. Run `skillforge inspect SOURCE` to understand the repo first.
2. Run `skillforge doctor` if the user needs to know which local runtimes are ready.
3. Review the extracted install commands, usage commands, and audit severity.
4. Run `skillforge build SOURCE --target TARGET --output DIR --verify` as the default path.
5. If you need a second pass later, run `skillforge verify PATH --target TARGET` against the generated result.
6. Open the generated `references/SECURITY-AUDIT.md` before trusting upstream scripts.
7. Deliver the target-specific folder, and use the `.skill` archive only as an optional sharing artifact.

## Common Commands

Inspect:

```bash
skillforge inspect owner/repo
```

Check local runtime readiness:

```bash
skillforge doctor
```

Build everything:

```bash
skillforge build owner/repo --target all --output ./dist --verify
```

Build a Codex-ready layout:

```bash
skillforge build owner/repo --target codex --output ./dist --verify
```

Build a Claude Code-ready layout:

```bash
skillforge build owner/repo --target claude --output ./dist --verify
```

Verify the generated bundle:

```bash
skillforge verify ./dist --target claude
```

## Safety Notes

- Do not ignore `high` audit findings without human review.
- Keep the generated skill concise and point to `references/` for detail.
- If the repo is a monorepo, verify that the extracted commands match the correct package or service.
