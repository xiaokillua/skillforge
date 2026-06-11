# Runtime Compatibility

This matrix summarizes what SkillForge has actually validated so far, not just what it can theoretically export.

Validated with SkillForge `v0.2.0` on `2026-06-12`.

## Snapshot

| Runtime | Status | Validation level | Notes | Evidence |
| --- | --- | --- | --- | --- |
| Codex | Supported | Runtime validated | Generated Codex skill loaded in a real `codex exec` session and answered from the generated files. | [Codex Showcase](../examples/CODEX_SHOWCASE.md) |
| Claude Code | Supported | Packaging validated | `.claude/skills/<name>` layout and `.skill` archive are generated and verified. Local Claude CLI was not available for a live runtime session. | [Claude Showcase](../examples/CLAUDE_SHOWCASE.md) |
| GitHub Copilot | Supported | Layout validated | `.github/skills/<name>` target is generated and verified. A local Copilot runtime session has not been recorded yet. | [Tutorial](TUTORIAL.md) |
| OpenClaw | Supported | Runtime validated | Generated OpenClaw skill was marked eligible and used in a real local OpenClaw agent run. | [OpenClaw Showcase](../examples/OPENCLAW_SHOWCASE.md) |
| Hermes | Supported | Runtime validated | Generated Hermes skill was installed locally and used in a real Hermes one-shot session. | [Hermes Showcase](../examples/HERMES_SHOWCASE.md) |
| Portable Agent Skills | Supported | Layout validated | Portable bundles are generated and validated by `skillforge verify`. Runtime behavior depends on the host agent. | [Tutorial](TUTORIAL.md) |

## Runtime Notes

### Codex

- Local runtime present: `codex-cli 0.133.0`
- Verified behavior:
  - generated layout at `.agents/skills/<name>`
  - `build --verify` passes
  - a real `codex exec` run read the generated skill and returned:
    - `references/OVERVIEW.md`
    - `pip install "scrapling[all]"`
    - `agent-skill/Scrapling-Skill/SKILL.md`

### Claude Code

- Local Claude CLI was not installed during validation
- Verified behavior:
  - generated layout at `.claude/skills/<name>`
  - generated `.skill` archive
  - `skillforge verify` passes for both directory and archive

### GitHub Copilot

- Local VS Code / Copilot runtime session was not available during validation
- Verified behavior:
  - generated layout at `.github/skills/<name>`
  - included in `build --verify --target all`

### OpenClaw

- Local runtime present: `OpenClaw 2026.4.22 (00bd2cf)`
- Verified behavior:
  - generated layout at `skills/<name>`
  - `openclaw skills info` reported the skill as eligible
  - a local agent run answered from generated references and metadata

### Hermes

- Local runtime present: `Hermes Agent v0.16.0 (2026.6.5)`
- Verified behavior:
  - generated layout at `skills/<name>`
  - skill installed under `~/.hermes/skills/<name>`
  - a one-shot Hermes run answered from generated references and metadata

## Recommended Reading Order

If you are evaluating SkillForge for a specific runtime, use this order:

1. Run `skillforge doctor` on your machine.
2. Start with this matrix.
3. Open the runtime-specific showcase linked above.
4. Reproduce it with `skillforge build ... --verify`.
5. Only then install the generated skill into your agent environment.
