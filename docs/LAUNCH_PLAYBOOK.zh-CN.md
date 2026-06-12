# 首发发布手册

这份手册不是教你“把仓库发出去”而已，而是按“第一波就尽量拿到曝光和 star”的思路来用 SkillForge。

## 核心定位

统一使用这句定位：

> SkillForge 可以把 GitHub 仓库编译成经过审计、可移植的 agent skill，并导出给 Claude、Codex、Copilot、OpenClaw、Hermes。

这句话有几个好处：

- 直接说清楚它是什么：repo-to-skill compiler
- 直接说清楚价值：审计、可移植
- 直接说清楚面向谁：正在使用 agent runtime 的人

## 对外先讲什么

先讲结果，不要先讲内部实现。

最适合反复用的几个点：

1. 把任意 GitHub repo 变成 agent skill
2. 一次导出，兼容多个 agent runtime
3. 在 agent 信任上游安装步骤前先做安全初筛
4. 一条命令生成 markdown 或 JSON 报告

## 最适合演示的流程

尽量固定用同一个公开仓库来演示，这样更容易形成记忆：

```bash
skillforge doctor
skillforge build D4Vinci/Scrapling --target all --verify
skillforge report D4Vinci/Scrapling --target all --json --output ./skillforge-report.json
```

这套顺序的好处是：

- `doctor` 先证明它知道你机器上的运行时环境
- `build --verify` 再证明它不是只会生成 markdown
- `report --json` 最后证明它有真正可交付的结果

## 最值得反复强调的证据

建议反复讲同一组证据，不要每次换一套说法：

- `Codex`、`Hermes`、`OpenClaw` 已做真实运行验证
- `Claude`、`Copilot` 已做打包和结构验证
- 中英文文档都齐
- GitHub release 已经可下载
- 仓库里直接放了 markdown 和 JSON 报告样例

## 推荐发布顺序

建议按这个顺序发：

1. GitHub README 和 release 先整理好
2. X / Twitter
3. Reddit
4. Hacker News
5. V2EX / 中文社区
6. 和 Claude、Codex、Hermes、OpenClaw、agent tooling 相关的 Discord / Slack

这样做的原因很简单：外部流量一进来，仓库本身已经是完整状态。

## 每个平台应该怎么发

### X / Twitter

- 一句短 hook
- 一条具体命令
- 一张截图或 README 视觉图
- 一个 repo 链接

### Hacker News

- 标题尽量朴素
- 不要太营销
- 第一条评论重点解释为什么 repo-to-skill 不应该只停在 markdown，而应该包含审计和多运行时打包

### Reddit

- 重点讲痛点
- 给出完整命令链
- 明确回答“为什么不直接复制 README”

### V2EX / 中文社区

- 强调多 agent 兼容
- 强调中文文档现成可用
- 带上报告样例和 release 链接

## 七天发布节奏

### 第一天

- 发 release
- 发 X
- 发 Reddit
- 发 V2EX 或中文社区

### 第二天

- 回评论
- 把高频问题补到 README
- 选一条最有代表性的评论做跟进帖

### 第三天

- 单独发一个 Codex 例子
- 单独发一个 Hermes 或 OpenClaw 例子

### 第四天

- 发一篇“为什么 SkillForge 不只是 repo-to-markdown 工具”的对比内容

### 第五到第七天

- 把用户问题继续沉淀回 README
- 再次强调 sample JSON 和 markdown report
- 收集“下一个最想验证的 runtime”是什么

## 第一周应该看什么指标

优先看：

- 每个平台带来的 star
- release 下载量
- 点击到 repo 的流量
- issue 质量
- 用户是否一打开仓库就能理解这项目在做什么

最健康的早期信号不是单纯的流量，而是有人会说：

- “这个我想拿来接我的 runtime”
- “我已经拿 repo X 跑了一次”
- “这个把 repo-to-skill 这件事做完整了”

## 高频问题的快速回答

### 为什么不直接把 README 粘给 agent？

因为 README 往往很长、很杂、结构不适合 runtime，而且里面的安装步骤不应该在没有审计前就直接让 agent 执行。

### 这是只给 Claude 用的吗？

不是。SkillForge 可以导出给 Claude、Codex、Copilot、OpenClaw、Hermes，以及 portable Agent Skills 结构。

### 这是一个 LLM wrapper 吗？

不是。当前流程不需要 API key，它会检查仓库、提取命令、审计风险、打包结构、校验输出，并生成报告。

### 现在到底哪些是真的验证过的？

`Codex`、`Hermes`、`OpenClaw` 已做真实运行验证；`Claude` 和 `Copilot` 目前完成了打包和结构验证。
