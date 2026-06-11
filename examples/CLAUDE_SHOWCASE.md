# Claude Showcase

This example shows how to generate a Claude Code-ready skill layout from a real public repository.

## Example repo

- Source repo: `D4Vinci/Scrapling`
- Generated skill name: `skillforge-scrapling-claude`

## Build command

```bash
skillforge build D4Vinci/Scrapling --target claude --name skillforge-scrapling-claude --output ./dist
```

## Install into Claude Code

For a project-local skill, copy the generated `.claude` directory into your repository:

```bash
cp -R ./dist/.claude /path/to/your/project/
```

For a personal skill available across projects, copy just the generated skill directory:

```bash
cp -R ./dist/.claude/skills/skillforge-scrapling-claude ~/.claude/skills/
```

Then start Claude Code inside the project and invoke the skill directly:

```bash
claude
/skillforge-scrapling-claude
```

SkillForge also emits `./dist/skillforge-scrapling-claude.skill` as an optional archive for sharing or backup.

## What this validates

- SkillForge writes the official Claude Code skill layout at `.claude/skills/<name>/SKILL.md`
- The generated skill keeps the same `references/` bundle as the portable target
- The optional `.skill` archive remains available when you want a single-file artifact
