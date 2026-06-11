# Hermes 示例

这个示例演示如何用 SkillForge 生成一个真正能给 Hermes 使用的 skill。

## 示例仓库

- 源仓库：`D4Vinci/Scrapling`
- 生成后的 skill 名称：`skillforge-scrapling-hermes`

## 生成命令

```bash
skillforge build D4Vinci/Scrapling --target hermes --name skillforge-scrapling-hermes --output ./dist
```

## 安装到 Hermes

把生成后的目录复制到 Hermes 的本地 skills 目录：

```bash
cp -R ./dist/skills/skillforge-scrapling-hermes ~/.hermes/skills/
```

然后启动一个新的 Hermes 会话，并预加载这个 skill：

```bash
hermes --skills skillforge-scrapling-hermes -z "Use the preloaded skill and summarize the install path."
```

## 这个例子验证了什么

- Hermes 能接受 SkillForge 生成出来的 skill 结构
- Hermes 能在新会话里加载这个 skill
- Hermes 能读取生成出来的 `references/OVERVIEW.md` 等参考文件
- 即使像 Scrapling 这种 README 很重 HTML，SkillForge 也能生成可用结果
