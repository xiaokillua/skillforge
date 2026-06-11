# 教程

## 1. 安装

```bash
git clone https://github.com/xiaokillua/skillforge.git
cd skillforge
python3 -m pip install -e .
```

也可以直接从 GitHub 安装：

```bash
python3 -m pip install "git+https://github.com/xiaokillua/skillforge.git"
```

如果你想把它当成独立 CLI 工具装起来：

```bash
pipx install "git+https://github.com/xiaokillua/skillforge.git"
```

## 2. 先检查，再生成

你也可以先看一下本机运行时是否就绪：

```bash
skillforge doctor
```

先看 SkillForge 识别出了什么：

```bash
skillforge inspect openai/openai-python
```

如果你想看 JSON：

```bash
skillforge inspect openai/openai-python --json
```

你应该先确认：

- 识别出的项目生态是否正确
- 抽取出来的安装命令是否靠谱
- 审计结果里有没有风险提示

## 3. 生成通用 Skill

```bash
skillforge build openai/openai-python --target portable --output ./dist --verify
```

这个结果是标准 Agent Skills 目录，很多环境都能直接用。

## 4. 生成指定平台结构

Codex：

```bash
skillforge build openai/openai-python --target codex --output ./dist --verify
```

Copilot：

```bash
skillforge build openai/openai-python --target copilot --output ./dist --verify
```

Claude：

```bash
skillforge build openai/openai-python --target claude --output ./dist --verify
```

OpenClaw：

```bash
skillforge build openai/openai-python --target openclaw --output ./dist --verify
```

Hermes：

```bash
skillforge build openai/openai-python --target hermes --output ./dist --verify
```

全部一起导出：

```bash
skillforge build openai/openai-python --target all --output ./dist --verify
```

## 5. 先验证生成结果

如果你已经用了 `build --verify`，这些检查 SkillForge 已经顺手帮你跑过一次了。

生成后先验证目标平台结构：

```bash
skillforge verify ./dist --target codex
```

也可以让 SkillForge 自动识别结构：

```bash
skillforge verify ./dist/codex
```

如果是 Claude 的分享压缩包，也可以直接检查：

```bash
skillforge verify ./dist/my-skill.skill
```

## 6. 看审计报告

至少要打开这几个文件：

- `references/SECURITY-AUDIT.md`
- `references/INSTALL.md`
- `references/COMMANDS.md`

如果审计等级是 `high`，SkillForge 默认不会继续打包，除非你手动加 `--allow-risky`。

## 7. 安装生成好的 Skill

常见位置：

- Codex：放到 `.agents/skills/<name>`
- GitHub Copilot：放到 `.github/skills/<name>`
- OpenClaw：把生成出来的目录复制到 `~/.openclaw/workspace/skills/<name>`，或者你自己配置的 `skills.load.extraDirs`
- Hermes：把生成出来的目录复制到 `~/.hermes/skills/<name>`，然后开一个新的 Hermes 会话
- Claude Code 项目级 skill：把 `.claude/skills/<name>` 放进你的仓库
- Claude Code 个人 skill：把生成出来的 skill 目录复制到 `~/.claude/skills/<name>`
- Claude Code 分发包：如果你只是想分享或归档，可以直接使用生成的 `<name>.skill` 压缩包

## 8. 推荐做法

- 保持生成的 skill 短、小、可验证
- 不要把上游 AI 指令文件直接当可信内容
- 优先让 agent 读 skill，不要整段粘贴超长 README
- 上游仓库更新后，重新生成一次
