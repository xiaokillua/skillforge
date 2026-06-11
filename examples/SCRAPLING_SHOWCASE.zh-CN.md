# Scrapling 示例

这个示例演示如何用 SkillForge 把 `D4Vinci/Scrapling` 生成成适合 Codex 使用的 skill：

```bash
skillforge build D4Vinci/Scrapling --target codex --output ./dist
```

生成后的结构大致如下：

```text
dist/
  .agents/
    skills/
      scrapling/
        SKILL.md
        analysis.json
        references/
```

为什么这个仓库很适合作为样板：

- 它的 README 不是简单的 Markdown 标题，而是复杂的 HTML hero
- 它本身有很多 CLI 例子和多语言文档
- 它已经自带上游 agent skill，在 `agent-skill/` 目录里

SkillForge 在这个例子里应该尽量抓到：

- 安装命令，例如 `pip install "scrapling[all]"`
- 常用命令，例如 `scrapling extract fetch ...`
- 上游现成 `SKILL.md` 的存在，方便后续人工复核
