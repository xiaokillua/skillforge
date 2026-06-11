# Scrapling Showcase

This example uses SkillForge to turn `D4Vinci/Scrapling` into a Codex-ready skill:

```bash
skillforge build D4Vinci/Scrapling --target codex --output ./dist
```

Generated output:

```text
dist/
  .agents/
    skills/
      scrapling/
        SKILL.md
        analysis.json
        references/
```

Why this repo is a good benchmark:

- the README starts with a rich HTML hero instead of a simple Markdown title
- it has deep CLI examples and multiple docs files
- it already ships an upstream agent skill in `agent-skill/`

What SkillForge should capture well:

- install commands like `pip install "scrapling[all]"`
- CLI workflows such as `scrapling extract fetch ...`
- the presence of upstream `SKILL.md` bundles for agent-specific follow-up review
