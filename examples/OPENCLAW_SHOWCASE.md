# OpenClaw Showcase

This example validates a SkillForge-generated OpenClaw skill with a real public repository.

## Example repo

- Source repo: `D4Vinci/Scrapling`
- Generated skill name: `skillforge-scrapling-openclaw`

## Build command

```bash
skillforge build D4Vinci/Scrapling --target openclaw --name skillforge-scrapling-openclaw --output ./dist
```

## Install into OpenClaw

Copy the generated directory into your OpenClaw workspace skills folder:

```bash
cp -R ./dist/skills/skillforge-scrapling-openclaw ~/.openclaw/workspace/skills/
```

Check that OpenClaw sees it:

```bash
openclaw skills info skillforge-scrapling-openclaw --json
```

Run a local one-shot agent turn:

```bash
openclaw agent --local --session-id skillforge-openclaw-showcase --message "Use the Scrapling skill available in the workspace and summarize it." --json
```

## What this validates

- OpenClaw marks the generated skill as eligible
- OpenClaw loads the generated skill into the agent prompt
- The agent can answer from generated references such as `references/OVERVIEW.md`
- Existing upstream skills such as `agent-skill/Scrapling-Skill/SKILL.md` remain discoverable in the generated output
