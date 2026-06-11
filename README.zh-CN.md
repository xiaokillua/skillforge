# SkillForge

[![CI](https://github.com/xiaokillua/skillforge/actions/workflows/ci.yml/badge.svg)](https://github.com/xiaokillua/skillforge/actions/workflows/ci.yml)

[English README](README.md) | [中文教程](docs/TUTORIAL.zh-CN.md) | [Scrapling 示例](examples/SCRAPLING_SHOWCASE.zh-CN.md) | [Claude 示例](examples/CLAUDE_SHOWCASE.zh-CN.md) | [Hermes 示例](examples/HERMES_SHOWCASE.zh-CN.md) | [OpenClaw 示例](examples/OPENCLAW_SHOWCASE.zh-CN.md) | [项目 Skill](skills/skillforge-repo-to-skill/SKILL.md)

SkillForge 可以把一个 GitHub 仓库整理成可移植的 agent skill，并导出成适合 Claude、Codex、GitHub Copilot、OpenClaw、Hermes 等环境使用的结构。

它解决的是一个很实际的问题：很多开源项目已经有很强的能力，但 agent 不知道应该怎么安装、怎么运行、哪些命令最常用、哪些脚本有风险。SkillForge 会把这些信息抽出来，再打包成标准 skill。

## 这个项目做什么

SkillForge 会：

- 接受 GitHub URL、`owner/repo` 简写，或者本地仓库路径
- 浅克隆仓库并提取安装命令、常用命令、入口命令
- 识别项目生态，例如 Python、Node、Rust、Go、Docker
- 如果上游仓库已经自带 `SKILL.md`，也会识别出来，方便继续人工复核
- 对上游文本文件做一个轻量安全审计
- 生成标准 `SKILL.md` + `references/`
- 再按目标平台导出不同目录结构
- 在安装前再检查生成结果是否符合目标平台的布局要求

## 支持的导出目标

- `portable`：通用 Agent Skills 目录
- `claude`：`.claude/skills/<name>` 目录 + 可选的 `.skill` 压缩包
- `codex`：`.agents/skills/<name>`
- `copilot`：`.github/skills/<name>`
- `openclaw`：`skills/<name>`
- `hermes`：`skills/<name>`
- `all`：一次导出全部

## 安装

```bash
git clone https://github.com/xiaokillua/skillforge.git
cd skillforge
python3 -m pip install -e .
```

检查版本：

```bash
skillforge version
```

如果你不想先 clone，也可以直接安装：

```bash
python3 -m pip install "git+https://github.com/xiaokillua/skillforge.git"
```

如果你想把它作为隔离的命令行工具安装：

```bash
pipx install "git+https://github.com/xiaokillua/skillforge.git"
```

## 快速开始

先检查一个仓库：

```bash
skillforge inspect openai/openai-python
```

导出全部目标：

```bash
skillforge build openai/openai-python --output ./dist --target all
```

只导出 Codex：

```bash
skillforge build openai/openai-python --target codex --output ./dist
```

从本地仓库生成：

```bash
skillforge build ~/code/my-tool --target portable --output ./dist
```

生成适合 Hermes 的结构：

```bash
skillforge build D4Vinci/Scrapling --target hermes --name skillforge-scrapling-hermes --output ./dist
```

生成适合 OpenClaw 的结构：

```bash
skillforge build D4Vinci/Scrapling --target openclaw --name skillforge-scrapling-openclaw --output ./dist
```

生成适合 Claude Code 的结构：

```bash
skillforge build D4Vinci/Scrapling --target claude --name skillforge-scrapling-claude --output ./dist
```

验证一个生成结果：

```bash
skillforge verify ./dist --target codex
```

验证一个 Claude `.skill` 压缩包：

```bash
skillforge verify ./dist/skillforge-scrapling-claude.skill
```

## 输出结构

生成后的 skill 默认会包含：

```text
my-skill/
  SKILL.md
  analysis.json
  references/
    OVERVIEW.md
    INSTALL.md
    COMMANDS.md
    SECURITY-AUDIT.md
    REPO-METADATA.md
  assets/
    MANIFEST.txt
```

不同平台会再把这套内容包进各自习惯的目录结构。对于 Claude Code，SkillForge 现在会输出 `.claude/skills/<name>/SKILL.md`，同时额外生成一个 `<name>.skill` 压缩包，方便分发和存档。

## 安全设计

SkillForge 默认比较保守：

- 会检查把 `curl` 输出直接管道给 shell 的安装方式
- 会检查 PowerShell 内联执行
- 会检查可疑 base64 管道
- 会提示上游仓库里的 AI instruction 文件
- 如果最高风险是 `high`，默认直接停止打包

如果你已经人工确认过，可以再加：

```bash
skillforge build owner/risky-repo --output ./dist --allow-risky
```

这不是完整的恶意代码扫描器，但它能挡住一批最常见、最不该被直接信任的上游安装方式。

## 命令参考

```bash
skillforge inspect SOURCE [--json] [--name NAME]
skillforge build SOURCE [--target TARGET] [--output DIR] [--name NAME] [--allow-risky]
skillforge verify PATH [--target TARGET] [--name NAME] [--json]
skillforge version
```

`SOURCE` 可以是：

- `https://github.com/owner/repo`
- `owner/repo`
- 本地仓库路径

## 开发

```bash
python3 -m pip install -e ".[dev]"
python3 -m unittest discover -s tests
python3 -m build
```

## 发布流程

- CI 现在会测试 Python `3.11`、`3.12`、`3.13`
- CI 也会构建 `sdist` 和 `wheel`，并执行 `twine check`
- 发布 GitHub Release 时，会自动附加打包产物
- 如果你在 PyPI 配好 Trusted Publisher，并设置仓库变量 `PYPI_PUBLISH=true`，就可以自动发布到 PyPI

## 后续计划

- 可选 LLM 总结模式
- 更好的 monorepo 识别
- 更完整的 Go / Rust / Docker 生态提取
- Hermes tap 和 skill catalog 辅助功能
- 自动做 with-skill / baseline 效果对比

## License

MIT
