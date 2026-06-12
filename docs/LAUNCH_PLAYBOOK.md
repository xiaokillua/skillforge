# Launch Playbook

This guide is for the first public push where the goal is not just "ship the repo," but get the repo seen, tried, and starred.

## Core Positioning

Use one sentence consistently:

> SkillForge compiles GitHub repositories into audited, portable agent skills for Claude, Codex, Copilot, OpenClaw, and Hermes.

That sentence works because it answers:

- what it is: a compiler for repo-to-skill workflows
- why it matters: audited and portable
- who it is for: people using agent runtimes today

## What To Lead With

Lead with outcomes, not internal implementation.

Best hooks:

1. Turn any GitHub repo into an agent skill.
2. Export once, use across Claude, Codex, Copilot, OpenClaw, and Hermes.
3. Audit upstream setup steps before your agent trusts them.
4. Generate a shareable markdown or JSON report in one command.

## Best Demo Flow

Use the same public repo every time for consistency:

```bash
skillforge doctor
skillforge build D4Vinci/Scrapling --target all --verify
skillforge report D4Vinci/Scrapling --target all --json --output ./skillforge-report.json
```

Why this works:

- `doctor` proves the tool is runtime-aware
- `build --verify` proves packaging is real
- `report --json` proves there is a concrete artifact at the end

## Best Proof Points

Keep repeating the same few proof points:

- real runtime validation for Codex, Hermes, and OpenClaw
- packaging validation for Claude and Copilot
- bilingual docs and tutorials
- release artifacts available on GitHub
- sample report and JSON artifact checked into the repo

## Posting Order

Use the rollout in this order:

1. GitHub README and release
2. X / Twitter
3. Reddit
4. Hacker News
5. V2EX / Chinese communities
6. targeted Discord or Slack communities for Claude, Codex, Hermes, OpenClaw, and agent tooling

This order helps because the public links and release are already ready before the outside traffic lands.

## What To Post On Each Platform

### X / Twitter

- short hook
- one concrete command
- one screenshot or repo visual
- repo link

### Hacker News

- plain title
- no hype
- first comment explains why repo-to-skill needs auditing and multi-runtime packaging

### Reddit

- emphasize the workflow pain point
- show the exact command sequence
- answer "why not just copy the README?" clearly

### V2EX / Chinese communities

- emphasize cross-agent compatibility
- emphasize that docs are available in Chinese
- show sample report artifact and release link

## Seven-Day Launch Cadence

### Day 1

- publish release
- publish X post
- publish Reddit post
- publish V2EX or Chinese forum post

### Day 2

- reply to comments
- add any missing clarifications to README
- pin one "best example" comment or follow-up post

### Day 3

- post one short Codex-specific example
- post one Hermes or OpenClaw example

### Day 4

- publish "how it compares to repo-to-skill tools that stop at markdown"

### Day 5-7

- turn questions into small README improvements
- surface sample JSON and markdown reports again
- ask first users what runtime they want validated next

## What Success Looks Like

In the first week, watch:

- stars per source post
- clicks to the repo
- release downloads
- issue quality
- whether users understand the core value without asking what the project does

The healthiest early signal is not raw traffic. It is whether people say:

- "I want this for my runtime"
- "I tried this on repo X"
- "This solves the repo-to-skill problem cleanly"

## Fast Responses For Common Questions

### Why not just paste a README into the prompt?

Because READMEs are long, inconsistent, not runtime-shaped, and often contain install steps you should audit before an agent follows them.

### Is this only for Claude?

No. SkillForge exports for Claude, Codex, Copilot, OpenClaw, Hermes, and a portable Agent Skills layout.

### Is this an LLM wrapper?

No. The current flow works without an API key. It inspects repos, extracts commands, audits risky patterns, packages layouts, verifies outputs, and emits reports.

### What is actually validated?

Codex, Hermes, and OpenClaw have runtime validation. Claude and Copilot currently have packaging and layout validation.
