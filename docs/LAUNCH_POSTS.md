# Launch Posts

Use these as copy-ready starting points for launch week.

## X / Twitter

### Post 1

SkillForge is out.

It turns a GitHub repo into an audited, portable agent skill for Claude, Codex, Copilot, OpenClaw, and Hermes.

No API key required for the core flow.

```bash
skillforge build D4Vinci/Scrapling --target all --verify
```

Repo: https://github.com/xiaokillua/skillforge

### Post 2

Most repo-to-skill experiments stop at markdown.

SkillForge goes further:
- extracts install and usage commands
- audits risky setup patterns
- packages for multiple runtimes
- verifies the output
- emits markdown and JSON reports

https://github.com/xiaokillua/skillforge

## Hacker News

### Title Options

- Show HN: SkillForge – compile GitHub repos into portable agent skills
- Show HN: SkillForge turns GitHub repos into audited agent skills
- Show HN: SkillForge – repo-to-skill packaging for Claude, Codex, Hermes, and OpenClaw

### First Comment

I built SkillForge because repo-to-skill workflows usually stop at "generate a markdown summary." That is useful, but it leaves out the parts that matter when you want agents to use real open-source tools safely and repeatedly: extracting concrete install and usage commands, auditing risky upstream setup patterns, packaging for multiple runtimes, validating the generated layout, and exporting a report artifact you can review or share.

The current release has runtime validation for Codex, Hermes, and OpenClaw, plus packaging validation for Claude and Copilot.

Repo: https://github.com/xiaokillua/skillforge

## Reddit

### r/ClaudeAI or agent tooling communities

I built an open-source tool called SkillForge that turns a GitHub repo into an audited, portable agent skill.

What it does:
- inspects README/docs and extracts install + usage commands
- flags risky setup patterns before you trust them
- packages the result for Claude, Codex, Copilot, OpenClaw, Hermes, or a portable Agent Skills layout
- verifies generated layouts
- emits a shareable markdown or JSON report

Example:

```bash
skillforge report D4Vinci/Scrapling --target all --json --output ./skillforge-report.json
```

Repo: https://github.com/xiaokillua/skillforge

If you try it on another repo, I would love to know which runtime you use.

## Discord / Slack Short Version

Built a new OSS tool: SkillForge.

It compiles GitHub repos into audited, portable agent skills for Claude, Codex, Copilot, OpenClaw, and Hermes.

It also verifies outputs and generates markdown/JSON reports.

Repo: https://github.com/xiaokillua/skillforge
