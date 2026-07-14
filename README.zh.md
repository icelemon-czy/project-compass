# Compass（罗盘）

> [English](README.md) · [变更记录](CHANGELOG.md) · [版本](VERSION)

一套可以直接复制到项目中的 AI 辅助开发工具包，支持 **Codex**、**Claude Code** 和 **OpenCode**。

只有 [`compass/`](compass/) 会被复制到目标项目。它包含项目规则基线、L1–L5 上下文、9 个 Skill、内置只读 SDD Reviewer、可选 Explorer 角色和平台安装器；研发文档仅留在本仓库供维护者使用。

Compass 只暴露目标型入口。一次正常的 `develop` 会在内部完成规划、TDD、审查、上下文同步和归档，用户不需要串联 Workflow 命令。

尚未定型的 idea 可以先交给 `brainstorm`：它会结合 `ask-codebase` 获取现状证据，收敛方向后在用户要求实施时直接进入 `develop`。

普通 code review 仍是 Agent 的基础能力，用户直接提出 review 即可。只有需要专项判断测试覆盖与可信度时，才使用 `audit-tests`。

需要创建或调整 project-local Skill 时使用 `skill-creator`；它不会默认安装 third-party Skill 或修改 global environment。

## 安装到项目

对于新的 Project A，只复制安装包目录本身。若 Project A 已有 `.compass/`，不要直接执行此命令。

```bash
cp -R /path/to/project-compass/compass /path/to/projectA/.compass
```

然后对正在 Project A 中工作的 Agent 说：

> 请阅读 `.compass/INSTALL.md`，并按照说明为当前项目安装 Compass。

Agent 会把规则基线合并到项目已有规则中，直接填写已经复制的 L1–L5 上下文，并把平台专用工作交给各个平台的 `INSTALL.md`；不会创建第二个 context 目录或复制 Skill。每个已选平台会得到只读 `sdd-reviewer`，Main Agent 仍是唯一 writer。

## 可复制安装包

```text
compass/
├── AGENTS.md       合并到目标项目根 AGENTS.md 的规则基线
├── INSTALL.md      Agent 可执行的安装与迁移契约
├── context/        L1–L5 空白上下文，在每个项目中原地填写
├── skills/         9 个权威 Skill（7 个核心入口 + 可选 ralph-loop、skill-creator）
├── subagents/      内置 sdd-reviewer + 可选 codebase-explorer
└── platforms/      Codex、Claude Code、OpenCode 的安装器与模板
    ├── codex/INSTALL.md
    ├── claude-code/INSTALL.md
    └── opencode/INSTALL.md
```

`docs/` 是源仓库维护材料，刻意不包含在复制给目标项目的安装包中。

## License

MIT License
