# 首发发布文案

这份文案是给首发周直接复制用的。

## X / Twitter

### 文案 1

SkillForge 发布了。

它可以把 GitHub repo 变成经过审计、可移植的 agent skill，支持 Claude、Codex、Copilot、OpenClaw、Hermes。

核心流程不需要 API key。

```bash
skillforge build D4Vinci/Scrapling --target all --verify
```

Repo: https://github.com/xiaokillua/skillforge

### 文案 2

很多 repo-to-skill 工具最后只停在生成 markdown。

SkillForge 往前多做了几步：
- 提取真实安装命令和使用命令
- 审计高风险 setup pattern
- 打包给多个 agent runtime
- 校验输出结果
- 生成 markdown 和 JSON 报告

https://github.com/xiaokillua/skillforge

## Hacker News

### 标题备选

- Show HN: SkillForge – compile GitHub repos into portable agent skills
- Show HN: SkillForge turns GitHub repos into audited agent skills
- Show HN: SkillForge – repo-to-skill packaging for Claude, Codex, Hermes, and OpenClaw

### 首条评论

我做 SkillForge 的原因，是因为很多 repo-to-skill 尝试最后只停在“生成一份 markdown 摘要”。这一步有帮助，但如果你真的想让 agent 稳定、可重复地使用开源项目，还缺很多关键能力：提取真实安装命令和使用命令、先审计上游 setup 风险、按不同 runtime 打包、验证生成结构是否合规、再输出一份可以复核和分享的报告。

当前版本已经对 Codex、Hermes、OpenClaw 做了真实运行验证，对 Claude 和 Copilot 做了打包验证。

Repo: https://github.com/xiaokillua/skillforge

## Reddit

### 面向 Claude / agent tooling 社区

我做了一个开源工具 SkillForge，可以把 GitHub repo 变成经过审计、可移植的 agent skill。

它会：
- 检查 README / docs 并提取安装命令和使用命令
- 在信任上游 setup 之前先提示常见高风险 pattern
- 打包给 Claude、Codex、Copilot、OpenClaw、Hermes，或者导出 portable Agent Skills 结构
- 校验生成结果
- 输出 markdown 或 JSON 报告

例如：

```bash
skillforge report D4Vinci/Scrapling --target all --json --output ./skillforge-report.json
```

Repo: https://github.com/xiaokillua/skillforge

如果你拿它去跑别的 repo，我也很想知道你主要用的是哪个 runtime。

## Discord / Slack 短文案

刚做了一个新的开源工具：SkillForge。

它可以把 GitHub repo 编译成经过审计、可移植的 agent skill，支持 Claude、Codex、Copilot、OpenClaw、Hermes。

还会顺手校验输出结果，并生成 markdown / JSON 报告。

Repo: https://github.com/xiaokillua/skillforge
