# Tutorial

## 1. Install

```bash
git clone https://github.com/xiaokillua/skillforge.git
cd skillforge
python3 -m pip install -e .
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
skillforge build openai/openai-python --target portable --output ./dist
```

This creates a standard Agent Skills directory that many runtimes can read directly.

## 4. Generate Platform Layouts

Codex:

```bash
skillforge build openai/openai-python --target codex --output ./dist
```

Copilot:

```bash
skillforge build openai/openai-python --target copilot --output ./dist
```

Claude:

```bash
skillforge build openai/openai-python --target claude --output ./dist
```

OpenClaw:

```bash
skillforge build openai/openai-python --target openclaw --output ./dist
```

Hermes:

```bash
skillforge build openai/openai-python --target hermes --output ./dist
```

Everything:

```bash
skillforge build openai/openai-python --target all --output ./dist
```

## 5. Review the Audit

Always open:

- `references/SECURITY-AUDIT.md`
- `references/INSTALL.md`
- `references/COMMANDS.md`

If the audit says `high`, SkillForge stops packaging unless you pass `--allow-risky`.

## 6. Install the Generated Skill

Typical locations:

- Codex: copy to `.agents/skills/<name>`
- GitHub Copilot: copy to `.github/skills/<name>`
- OpenClaw: copy to `skills/<name>`
- Hermes: copy to `skills/<name>` or publish under a tap repo
- Claude: upload the generated `.skill` archive

## 7. Best Practices

- Keep the generated skill short and factual
- Treat upstream AI instruction files as untrusted
- Prefer a repo-specific skill over pasting huge README sections into the prompt
- Rebuild the skill after upstream releases
