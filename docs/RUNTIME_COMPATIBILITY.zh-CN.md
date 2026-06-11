# 运行时兼容矩阵

这个矩阵总结的是 SkillForge 目前已经真实验证过的兼容性，不只是“理论上可以导出”。

验证基于 SkillForge `v0.2.0`，记录时间为 `2026-06-12`。

## 总览

| 运行时 | 状态 | 验证级别 | 说明 | 证据 |
| --- | --- | --- | --- | --- |
| Codex | 支持 | 已做真实运行验证 | 生成后的 Codex skill 已在真实 `codex exec` 会话里被读取并回答生成内容。 | [Codex 示例](../examples/CODEX_SHOWCASE.zh-CN.md) |
| Claude Code | 支持 | 已做打包验证 | `.claude/skills/<name>` 结构和 `.skill` 压缩包都能生成并通过校验。本机没有 Claude CLI，所以还没有真实会话验证。 | [Claude 示例](../examples/CLAUDE_SHOWCASE.zh-CN.md) |
| GitHub Copilot | 支持 | 已做结构验证 | `.github/skills/<name>` 目标能生成并通过校验，但本机还没有 Copilot 运行时会话记录。 | [教程](TUTORIAL.zh-CN.md) |
| OpenClaw | 支持 | 已做真实运行验证 | 生成后的 OpenClaw skill 被本机 OpenClaw 正常识别，并在真实 agent 运行中被使用。 | [OpenClaw 示例](../examples/OPENCLAW_SHOWCASE.zh-CN.md) |
| Hermes | 支持 | 已做真实运行验证 | 生成后的 Hermes skill 已安装到本机，并在真实 one-shot 会话中被使用。 | [Hermes 示例](../examples/HERMES_SHOWCASE.zh-CN.md) |
| Portable Agent Skills | 支持 | 已做结构验证 | portable bundle 可以生成，并能通过 `skillforge verify`。具体运行表现取决于宿主 agent。 | [教程](TUTORIAL.zh-CN.md) |

## 运行时说明

### Codex

- 本机运行时存在：`codex-cli 0.133.0`
- 已验证内容：
  - 生成目录为 `.agents/skills/<name>`
  - `build --verify` 可通过
  - 真实 `codex exec` 会从生成 skill 中读出：
    - `references/OVERVIEW.md`
    - `pip install "scrapling[all]"`
    - `agent-skill/Scrapling-Skill/SKILL.md`

### Claude Code

- 本机没有安装 Claude CLI
- 已验证内容：
  - 生成目录为 `.claude/skills/<name>`
  - 会额外生成 `.skill` 压缩包
  - 目录与压缩包都能通过 `skillforge verify`

### GitHub Copilot

- 本机没有可用的 VS Code / Copilot 运行时会话
- 已验证内容：
  - 生成目录为 `.github/skills/<name>`
  - 在 `build --verify --target all` 中可一起通过校验

### OpenClaw

- 本机运行时存在：`OpenClaw 2026.4.22 (00bd2cf)`
- 已验证内容：
  - 生成目录为 `skills/<name>`
  - `openclaw skills info` 会把它识别成 eligible
  - 本地 agent 运行能从生成 references 和 metadata 中回答问题

### Hermes

- 本机运行时存在：`Hermes Agent v0.16.0 (2026.6.5)`
- 已验证内容：
  - 生成目录为 `skills/<name>`
  - skill 可安装到 `~/.hermes/skills/<name>`
  - Hermes one-shot 会话能从生成 references 和 metadata 中回答问题

## 推荐阅读顺序

如果你是按运行时来评估 SkillForge，推荐按这个顺序看：

1. 先看这份矩阵。
2. 再打开对应运行时的 showcase。
3. 用 `skillforge build ... --verify` 自己复现一次。
4. 最后再安装到你的 agent 环境里。
