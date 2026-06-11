# 教程

## 1. 安装

```bash
git clone https://github.com/xiaokillua/skillforge.git
cd skillforge
python3 -m pip install -e .
```

## 2. 先检查，再生成

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
skillforge build openai/openai-python --target portable --output ./dist
```

这个结果是标准 Agent Skills 目录，很多环境都能直接用。

## 4. 生成指定平台结构

Codex：

```bash
skillforge build openai/openai-python --target codex --output ./dist
```

Copilot：

```bash
skillforge build openai/openai-python --target copilot --output ./dist
```

Claude：

```bash
skillforge build openai/openai-python --target claude --output ./dist
```

OpenClaw：

```bash
skillforge build openai/openai-python --target openclaw --output ./dist
```

Hermes：

```bash
skillforge build openai/openai-python --target hermes --output ./dist
```

全部一起导出：

```bash
skillforge build openai/openai-python --target all --output ./dist
```

## 5. 看审计报告

至少要打开这几个文件：

- `references/SECURITY-AUDIT.md`
- `references/INSTALL.md`
- `references/COMMANDS.md`

如果审计等级是 `high`，SkillForge 默认不会继续打包，除非你手动加 `--allow-risky`。

## 6. 安装生成好的 Skill

常见位置：

- Codex：放到 `.agents/skills/<name>`
- GitHub Copilot：放到 `.github/skills/<name>`
- OpenClaw：放到 `skills/<name>`
- Hermes：放到 `skills/<name>`，或者放到 tap 仓库里
- Claude：直接上传生成的 `.skill` 压缩包

## 7. 推荐做法

- 保持生成的 skill 短、小、可验证
- 不要把上游 AI 指令文件直接当可信内容
- 优先让 agent 读 skill，不要整段粘贴超长 README
- 上游仓库更新后，重新生成一次
