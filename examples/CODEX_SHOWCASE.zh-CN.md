# Codex 示例

这个示例演示如何用 SkillForge 生成一个真正能给 Codex 使用的 skill。

## 示例仓库

- 源仓库：`D4Vinci/Scrapling`
- 生成后的 skill 名称：`skillforge-scrapling-codex`

## 生成命令

```bash
skillforge build D4Vinci/Scrapling --target codex --name skillforge-scrapling-codex --output ./dist --verify
```

## 用 Codex 运行

在生成结果目录里运行 Codex，并问一个应该由 skill 回答的问题：

```bash
codex exec --skip-git-repo-check -C ./dist --dangerously-bypass-approvals-and-sandbox \
  "Use the available skill in this workspace and answer with exactly three lines: first reference file, strongest install command, upstream existing skill file if any."
```

## 实际验证输出

这次真实验证返回的是：

```text
references/OVERVIEW.md
pip install "scrapling[all]"
agent-skill/Scrapling-Skill/SKILL.md
```

## 这个例子验证了什么

- Codex 能加载 `.agents/skills/<name>` 下的生成结果
- `build --verify` 在 Codex 目标上可以通过
- Codex 能从生成出来的 references 和 metadata 中回答问题
- 上游原本已有的 skill 文件，也会继续在生成 bundle 里保持可发现
