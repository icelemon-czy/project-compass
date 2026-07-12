# Compass Harness

> **[English Version](README.md)** · 版本见 [VERSION](VERSION) · [CHANGELOG](CHANGELOG.md)

一套开放的 AI 工程辅助框架，用于复用项目上下文、Skills、Agent 规则和平台适配模板。

Compass Harness 当前只面向 **Codex**、**Claude Code** 和 **OpenCode**。

## Phase 2 提供什么

Phase 2 将已有真实资产与后来新增的模板能力分开：

- 项目原有的 13 个工作流作为真实 Skill，统一维护在 `.agents/skills/`。
- AGENTS 规则、项目上下文、新 Skill 脚手架、Subagent 角色和平台适配统一放在 `templates/compass-harness/`。
- 安装到其他项目后，所有可编辑 Harness 内容统一放在 `.compass-harness/`，工具原生文件只是生成的发现层。
- Subagent 只提供角色示例；Phase 2 不会在仓库中安装 `.codex/agents/`、`.claude/agents/` 或 `.opencode/agents/`。
- 验证只检查确定性的结构和格式，不声称证明模型行为或跨平台推理质量。

## 仓库结构

```text
project-compass/
├── .agents/skills/                   # 13 个现有 Skill 的权威源
├── templates/compass-harness/
│   ├── manifest.yaml                 # 组件、占位符和安装目标
│   ├── installed-manifest.yaml.template
│   ├── config.yaml                   # 目标项目配置模板
│   ├── agent-rules/                  # 全局和项目 AGENTS 模板
│   ├── context/                      # L1–L5 上下文模板
│   ├── skills/_skill-template/       # 未来新建 Skill 的模板
│   ├── subagents/                    # 通用角色模板和四个示例
│   └── adapters/
│       ├── codex/
│       ├── claude-code/
│       └── opencode/
├── scripts/validate-phase2.rb       # 可重复的静态校验
├── builders/claude/                 # 现有 Claude 上下文构建 prompts
├── roadmap/                         # 产品路线图与历史调研
└── compass                          # CLI 入口；生成能力属于 Phase 3
```

## 目标项目结构

```text
.compass-harness/
├── manifest.yaml                    # 已安装版本和受管路径
├── config.yaml                      # 项目参数与启用平台
├── rules/                           # 跨平台规则与项目导航
├── context/                         # L1–L5 项目上下文
├── skills/                          # 安装后的权威 Skills
└── subagents/                       # 权威角色定义与示例

AGENTS.md / CLAUDE.md                # 生成的薄入口
.agents/skills/                      # Codex/OpenCode 生成镜像
.claude/skills/                      # Claude Code 生成镜像
各工具 agents 目录                  # 仅为明确选择的角色生成
```

目标项目只编辑 `.compass-harness/` 内的 Harness 内容。外部生成文件必须可以重建，也不能保存唯一一份项目知识。

## 上下文模型

可选的 `.compass-harness/context/` 上下文包含五层：

| 层级 | 用途 |
|:-----|:-----|
| L1 Codebase Map | 功能位置、架构、入口和依赖关系 |
| L2 Rules | 编码、测试、模块和新建文件约束 |
| L3 Specs | 系统需求、能力 Spec 和进行中的变更 |
| L4 Session | 项目确实需要时才使用的可恢复会话状态 |
| L5 Validation | 追溯、测试设计和已经检查的证据 |

项目不需要一次填满所有层。只写能够由源码或用户需求支持的最小上下文，其余内容在真正有用时再补充。

## 现有 Skills

模板仓库在 `.agents/skills/` 维护 Skill 原始文件；安装到其他项目后，权威副本位于 `.compass-harness/skills/`：

| 分类 | Skills |
|:-----|:-------|
| 初始化 | `git-init`、`init-project`、`build-ai`、`setup-testing` |
| 开发 | `new-change`、`continue-change` |
| 审查与归档 | `review-tests`、`archive-change`、`check-changes` |
| 修复 | `fix-bug` |
| 查询 | `ask-codebase` |
| 文档与交付 | `update-ai`、`git-commit` |

每个 Skill 的权威 `SKILL.md` frontmatter 只包含 `name` 和 `description`。平台专用元数据由适配层或后续生成结果负责。

## 模板

### AGENTS 规则

- `agent-rules/AGENTS.global.md`：跨项目通用工作原则。
- `agent-rules/AGENTS.project.md`：项目占位符、命令和 `.compass-harness/context/` 导航。

### Skill 模板

`skills/_skill-template/SKILL.md` 只用于以后创建新 Skill，不复制已有的 13 个 Skill。

### Subagent 模板

`subagents/` 包含一个通用角色契约和四个示例：

- Codebase Explorer
- Impact Analyst
- Test Reviewer
- Spec Validator

它们只定义职责、权限、禁止事项和输出契约，不是已经安装或验证过行为的 Agent。

### 平台适配模板

| 平台 | 生成的发现适配层 |
|:-----|:-----------------|
| Codex | `AGENTS.md`、`.agents/skills/`、可选 `.codex/agents/*.toml` |
| Claude Code | `CLAUDE.md`、`.claude/skills/`、可选 `.claude/agents/*.md` |
| OpenCode | `AGENTS.md`、`.agents/skills/`、可选 `opencode.json` 和 `.opencode/agents/*.md` |

所有适配文件都指回 `.compass-harness/`。Phase 2 只提供格式模板；自动安装与重新生成由 Phase 3 CLI 实现。

## 手动使用

在生成器完成之前：

1. 在目标项目创建 `.compass-harness/{rules,context,skills,subagents}`。
2. 将 `installed-manifest.yaml.template` 和 `config.yaml` 渲染到 `.compass-harness/`。
3. 将 AGENTS 规则、上下文模板、13 个 Skill 和 Subagent 角色模板复制到对应权威目录。
4. 渲染所选平台的根入口，并生成该平台的 Skill 发现镜像。
5. 只有项目明确选择某个 Subagent 角色时，才生成平台专用实例。

不要覆盖项目已有规则，应将其与薄适配入口合并；也不要把生成镜像当作权威内容修改。

## 静态校验

运行：

```bash
ruby scripts/validate-phase2.rb
```

校验内容包括：

- 权威 Skill 数量为 13；
- Skill 名称、目录和 frontmatter；
- manifest 能够解析且声明的源文件存在；
- `.compass-harness/` 权威安装契约和生成适配策略正确；
- AGENTS、Skill、Subagent 和适配器模板齐全；
- 占位符已登记、Markdown 相对链接无断链；
- OpenCode JSON 语法正确；
- 仓库根目录没有安装 Agent/Subagent 实例。
- 当前 Skill 和模板不再依赖 `.ai/`。

这些检查只证明仓库结构正确，不证明模型行为。

## 路线图

- Phase 1：Compass Harness 品牌调整和兼容基线。
- Phase 2：迁移权威 Skill，并为三个支持平台建立可复用模板。
- Phase 3：CLI 初始化、渲染、校验和升级。

实施清单见 [doc/todo.md](doc/todo.md)。

## License

MIT License
