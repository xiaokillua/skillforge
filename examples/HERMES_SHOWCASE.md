# Hermes Showcase

This example validates a SkillForge-generated Hermes skill with a real public repository.

## Example repo

- Source repo: `D4Vinci/Scrapling`
- Generated skill name: `skillforge-scrapling-hermes`

## Build command

```bash
skillforge build D4Vinci/Scrapling --target hermes --name skillforge-scrapling-hermes --output ./dist
```

## Install into Hermes

Copy the generated directory into your Hermes profile:

```bash
cp -R ./dist/skills/skillforge-scrapling-hermes ~/.hermes/skills/
```

Start a new Hermes session, then preload the skill:

```bash
hermes --skills skillforge-scrapling-hermes -z "Use the preloaded skill and summarize the install path."
```

## What this validates

- Hermes accepts the generated skill structure
- Hermes can load the generated skill in a fresh session
- Hermes can answer from generated references such as `references/OVERVIEW.md`
- HTML-heavy READMEs like Scrapling still produce a usable title, summary, and command set
