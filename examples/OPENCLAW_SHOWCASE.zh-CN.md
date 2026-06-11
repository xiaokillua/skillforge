# OpenClaw 示例

这个示例演示如何用 SkillForge 生成一个真正能给 OpenClaw 使用的 skill。

## 示例仓库

- 源仓库：`D4Vinci/Scrapling`
- 生成后的 skill 名称：`skillforge-scrapling-openclaw`

## 生成命令

```bash
skillforge build D4Vinci/Scrapling --target openclaw --name skillforge-scrapling-openclaw --output ./dist
```

## 安装到 OpenClaw

把生成后的目录复制到 OpenClaw 工作区的 skills 目录：

```bash
cp -R ./dist/skills/skillforge-scrapling-openclaw ~/.openclaw/workspace/skills/
```

先确认 OpenClaw 能识别它：

```bash
openclaw skills info skillforge-scrapling-openclaw --json
```

然后运行一次本地 one-shot：

```bash
openclaw agent --local --session-id skillforge-openclaw-showcase --message "Use the Scrapling skill available in the workspace and summarize it." --json
```

## 这个例子验证了什么

- OpenClaw 会把生成后的 skill 识别为 eligible
- OpenClaw 会把这个 skill 加进 agent prompt
- agent 能读取生成出来的 `references/OVERVIEW.md` 等参考文件
- 上游已有的 skill，例如 `agent-skill/Scrapling-Skill/SKILL.md`，也会被保留在生成结果里
