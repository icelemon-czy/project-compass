# Compass Harness TODO

> 当前状态：可复制安装包与源仓库维护材料已于 2026-07-12 分离。
>
> 产品目标：用户仅复制 `harness/` 为目标项目的 `.compass-harness/`，然后让 Agent 阅读其中的 `INSTALL.md` 完成非破坏安装。

## 最终用户流程

对于新的 Project A：

```bash
cp -R /path/to/project-compass/harness /path/to/projectA/.compass-harness
```

然后对 Agent 说：

```text
请阅读 .compass-harness/INSTALL.md，并按照说明为当前项目安装 Compass Harness。
```

不要求用户运行安装脚本，不进行全局安装，也不要求用户手工维护平台适配文件。已有 `.compass-harness/` 时不得用复制命令覆盖；由 Agent 先检查并报告合并选择。

## 产品边界

- `harness/` 是唯一可复制安装包；`docs/` 只服务源仓库维护。
- `harness/skills/` 是 13 个内置 Skill 的唯一权威源，不维护复制版本。
- `harness/context/` 直接保存 L1–L5 空白上下文；复制后在原地填写，不再创建 `context-template/` 或第二个 `context/`。
- `harness/subagents/` 只保存四个具体、可选的委派角色定义；默认不生成任何真实 Subagent 配置。
- `harness/AGENTS.md` 是要合并到目标项目根 `AGENTS.md` 的规则基线。
- `harness/platforms/` 只保存 Claude Code、Codex 和 OpenCode 必需的格式差异。
- 根 README 只介绍项目和复制 `harness/` 的方法；全部安装、迁移、验证和移除规则放在 `harness/INSTALL.md`。
- 当前阶段不引入 Bash 安装器、全局插件、manifest、lock file 或自动升级系统。

## 最终仓库结构

```text
project-compass/
├── README.md                         # 源仓库说明
├── README.zh.md
├── CHANGELOG.md
├── VERSION
├── harness/                          # 唯一可复制安装包
│   ├── AGENTS.md
│   ├── INSTALL.md
│   ├── context/                      # L1–L5，复制后直接填写
│   ├── skills/                       # 13 个真实 Skill，唯一权威源
│   ├── subagents/                    # 四个具体可选角色，不生成实例
│   └── platforms/                    # 三平台最小格式
└── docs/                             # 维护者的设计、路线图与 TODO
```

目标项目只接收 `harness/` 的内容：

```text
projectA/
├── AGENTS.md                         # 与 Harness 标记区块合并后的项目规则
└── .compass-harness/
    ├── INSTALL.md
    ├── AGENTS.md
    ├── context/
    ├── skills/
    ├── subagents/
    └── platforms/
```

仓库和目标项目都不保留 Skill 软链接；唯一内容始终位于 `harness/skills/` 或复制后的 `.compass-harness/skills/`。

## INSTALL.md 契约

安装说明必须要求 Agent：

1. 确认目标项目根目录是 `.compass-harness/` 的父目录。
2. 确认 `.compass-harness/` 内没有嵌套 `.git/`。
3. 检查并保留已有 `AGENTS.md`、`CLAUDE.md` 和平台配置。
4. 直接在 `.compass-harness/context/` 中填写或迁移 L1–L5；禁止创建第二个 context 目录。
5. 将 `.compass-harness/AGENTS.md` 与目标项目根 `AGENTS.md` 进行语义合并，禁止直接覆盖。
6. 根 `AGENTS.md` 直接导航到 `.compass-harness/skills`，Agent 按需读取对应 `SKILL.md`。
7. 默认不安装 Subagent；仅在四个角色的 `Delegate only when` 条件成立且用户明确要求时，才结合对应平台格式讨论使用方式。
8. 发现旧 `.ai/` 时先迁移并验证，再由用户决定是否删除旧目录。
9. 完成后报告新增、合并、复用、跳过和仍需确认的内容。

## 当前重构任务

- [x] 将 `.agents/skills/` 的 13 个 Skill 移到唯一权威目录，且不保留软链接。
- [x] 将原有 L1–L5 上下文收口为 `harness/context/`，复制后直接原地填写。
- [x] 将四个具体 Subagent 角色和三平台 formats 收口到 `harness/`。
- [x] 将唯一 AGENTS 规则基线收口为 `harness/AGENTS.md`。
- [x] 创建 `harness/INSTALL.md`，覆盖安装、旧结构迁移、验证和移除。
- [x] 精简中英文 README，只保留介绍、复制 `harness/` 的方法和安装入口。
- [x] 删除已放弃的 manifest、installed manifest、config、旧 Bash CLI、通用 Skill 脚手架和系统 `.DS_Store` 残留。
- [x] 将 TODO、工作流分析和 roadmap 保留在根 `docs/`，不复制给目标项目。
- [x] 删除没有产品价值的仓库静态测试与仅服务于它的 GitHub Actions CI。
- [x] 更新 13 个 Skill 和当前文档中的旧目录引用。
- [x] 验证仓库只有一份 Skill 内容、没有软链接，并且不存在真实 Subagent 实例。

## 后续能力

- [ ] 在真实需求出现后，再评估自动升级和版本迁移工具。
- [ ] 在真实跨平台限制出现后，再评估是否需要原生 Skill 自动发现。
- [ ] 只有用户明确需要时，才设计项目自定义 Skill 或 Subagent 安装机制。
