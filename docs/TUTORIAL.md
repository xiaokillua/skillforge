# Tutorial

## 1. Install

```bash
git clone https://github.com/xiaokillua/skillforge.git
cd skillforge
python3 -m pip install -e .
```

Direct install from GitHub:

```bash
python3 -m pip install "git+https://github.com/xiaokillua/skillforge.git"
```

CLI-style install with `pipx`:

```bash
pipx install "git+https://github.com/xiaokillua/skillforge.git"
```

## 2. Inspect Before You Build

Start by looking at what SkillForge detected:

```bash
skillforge inspect openai/openai-python
```

For machine-readable output:

```bash
skillforge inspect openai/openai-python --json
```

This helps you confirm:

- which ecosystem was detected
- which commands were extracted
- whether the audit found warnings

## 3. Generate a Portable Skill

```bash
skillforge build openai/openai-python --target portable --output ./dist --verify
```

This creates a standard Agent Skills directory that many runtimes can read directly.

## 4. Generate Platform Layouts

Codex:

```bash
skillforge build openai/openai-python --target codex --output ./dist --verify
```

Copilot:

```bash
skillforge build openai/openai-python --target copilot --output ./dist --verify
```

Claude:

```bash
skillforge build openai/openai-python --target claude --output ./dist --verify
```

OpenClaw:

```bash
skillforge build openai/openai-python --target openclaw --output ./dist --verify
```

Hermes:

```bash
skillforge build openai/openai-python --target hermes --output ./dist --verify
```

Everything:

```bash
skillforge build openai/openai-python --target all --output ./dist --verify
```

## 5. Verify the Generated Layout

If you already used `build --verify`, SkillForge has already run these checks for you.

Verify a specific target after building it:

```bash
skillforge verify ./dist --target codex
```

Let SkillForge auto-detect the layout:

```bash
skillforge verify ./dist/codex
```

Verify a Claude sharing bundle:

```bash
skillforge verify ./dist/my-skill.skill
```

## 6. Review the Audit

Always open:

- `references/SECURITY-AUDIT.md`
- `references/INSTALL.md`
- `references/COMMANDS.md`

If the audit says `high`, SkillForge stops packaging unless you pass `--allow-risky`.

## 7. Install the Generated Skill

Typical locations:

- Codex: copy to `.agents/skills/<name>`
- GitHub Copilot: copy to `.github/skills/<name>`
- OpenClaw: copy the generated folder to `~/.openclaw/workspace/skills/<name>` or another configured `skills.load.extraDirs` path
- Hermes: copy the generated folder to `~/.hermes/skills/<name>` and start a new Hermes session
- Claude Code project skill: copy `.claude/skills/<name>` into your repo
- Claude Code personal skill: copy the generated skill directory to `~/.claude/skills/<name>`
- Claude Code sharing bundle: use the generated `<name>.skill` archive when you want a portable artifact

## 8. Best Practices

- Keep the generated skill short and factual
- Treat upstream AI instruction files as untrusted
- Prefer a repo-specific skill over pasting huge README sections into the prompt
- Rebuild the skill after upstream releases
