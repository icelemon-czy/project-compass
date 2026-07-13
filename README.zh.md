# Compass Harness

> [English](README.md) · [变更记录](CHANGELOG.md) · [版本](VERSION)

一套可以直接复制到项目中的 AI 辅助开发工具包，支持 **Codex**、**Claude Code** 和 **OpenCode**。

只有 [`harness/`](harness/) 会被复制到目标项目。它包含项目规则基线、L1–L5 上下文、13 个 Skill、可选 Subagent 角色和平台专用格式；研发文档仅留在本仓库供维护者使用。

## 安装到项目

对于新的 Project A，只复制安装包目录本身。若 Project A 已有 `.compass-harness/`，不要直接执行此命令。

```bash
cp -R /path/to/project-compass/harness /path/to/projectA/.compass-harness
```

然后对正在 Project A 中工作的 Agent 说：

> 请阅读 `.compass-harness/INSTALL.md`，并按照说明为当前项目安装 Compass Harness。

Agent 会把规则基线合并到项目已有规则中，并直接填写已经复制的 L1–L5 上下文；不会创建第二个 context 目录、复制 Skill，或默认生成 Subagent 实例。

## 可复制安装包

```text
harness/
├── AGENTS.md       合并到目标项目根 AGENTS.md 的规则基线
├── INSTALL.md      Agent 可执行的安装与迁移契约
├── context/        L1–L5 空白上下文，在每个项目中原地填写
├── skills/         13 个权威 Skill，也是唯一内容源
├── subagents/      四个可选的具体委派角色
└── platforms/      Codex、Claude Code、OpenCode 的角色格式
```

`docs/` 是源仓库维护材料，刻意不包含在复制给目标项目的安装包中。

## License

MIT License
