# Claude 示例

这个示例演示如何把一个真实公开仓库生成成适合 Claude Code 使用的 skill 结构。

## 示例仓库

- 源仓库：`D4Vinci/Scrapling`
- 生成后的 skill 名称：`skillforge-scrapling-claude`

## 生成命令

```bash
skillforge build D4Vinci/Scrapling --target claude --name skillforge-scrapling-claude --output ./dist
```

## 安装到 Claude Code

如果你想把它作为项目级 skill，就把生成出来的 `.claude` 目录复制到你的项目里：

```bash
cp -R ./dist/.claude /path/to/your/project/
```

如果你想把它作为个人 skill，在多个项目里复用，就只复制生成出来的 skill 目录：

```bash
cp -R ./dist/.claude/skills/skillforge-scrapling-claude ~/.claude/skills/
```

然后在项目目录里启动 Claude Code，并直接调用这个 skill：

```bash
claude
/skillforge-scrapling-claude
```

SkillForge 也会额外生成 `./dist/skillforge-scrapling-claude.skill`，方便你做分享或备份。

## 这个例子验证了什么

- SkillForge 会按照 Claude Code 官方习惯输出 `.claude/skills/<name>/SKILL.md`
- 生成后的 skill 会保留和 portable 目标一样的 `references/` 参考文件
- 如果你需要单文件分发，仍然可以使用额外生成的 `.skill` 压缩包
