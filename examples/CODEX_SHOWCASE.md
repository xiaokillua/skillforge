# Codex Showcase

This example validates a SkillForge-generated Codex skill with a real public repository.

## Example repo

- Source repo: `D4Vinci/Scrapling`
- Generated skill name: `skillforge-scrapling-codex`

## Build command

```bash
skillforge build D4Vinci/Scrapling --target codex --name skillforge-scrapling-codex --output ./dist --verify
```

## Run with Codex

Run Codex in the generated workspace and ask for information that should come from the skill:

```bash
codex exec --skip-git-repo-check -C ./dist --dangerously-bypass-approvals-and-sandbox \
  "Use the available skill in this workspace and answer with exactly three lines: first reference file, strongest install command, upstream existing skill file if any."
```

## Validated output

The real validation run returned:

```text
references/OVERVIEW.md
pip install "scrapling[all]"
agent-skill/Scrapling-Skill/SKILL.md
```

## What this validates

- Codex loads the generated layout at `.agents/skills/<name>`
- `build --verify` passes for the Codex target
- Codex can answer from generated references and metadata
- Existing upstream skill files remain discoverable through the generated bundle
