# Research: AI 上下文管理生态对比

> 调研日期：2026-03-31
> 目的：了解当前 AI 编码助手的上下文管理方案，评估 Project Compass 的定位与改进方向

---

## 1. 行业背景

AI 编码助手（Cursor、Cline、GitHub Copilot、Claude Code 等）的上下文窗口是有限的。随着项目规模增长，"如何让 AI 精准理解项目"成为核心问题。

当前主流方案可分为三类：

| 类型 | 代表 | 策略 |
|------|------|------|
| **文件规则型** | AGENTS.md、.cursorrules、.clinerules | 在仓库中放置指令文件，AI 启动时读取 |
| **规格驱动型** | OpenSpec、Spec Kit | 先写需求规格，再让 AI 按规格实现 |
| **平台集成型** | GitHub Copilot Agent HQ、Linear Agent | 从 issue/ticket 自动分配给 AI agent |

Project Compass 属于**文件规则型 + 任务管理混合型**，同时覆盖代码导航、编码规则、任务管理和会话续传。

---

## 2. 主要方案详解

### 2.1 AGENTS.md（19.6k ⭐）

- **仓库**: https://github.com/agentsmd/agents.md
- **定位**: AI agent 的通用指令格式（类似 README，但面向 AI）

**核心特点**:
- 纯 Markdown，无特殊格式要求
- 支持嵌套：子目录下的 AGENTS.md 就近生效
- 60k+ GitHub 项目已采用
- 被 20+ 工具原生支持：Cursor、Codex、Windsurf、Zed、RooCode、Kilo Code 等

**典型内容**:
- 开发环境配置
- 构建/测试命令
- 代码风格指南
- PR 提交规范
- 安全/部署注意事项

**与 Project Compass 的关系**:
- AGENTS.md 是单文件、扁平结构，适合简单项目
- Project Compass 是多层分文件结构，适合有规模的项目
- 两者可兼容：生成一个 AGENTS.md 作为入口，指向 `.ai/` 下的详细文档

---

### 2.2 OpenSpec（35.6k ⭐）

- **仓库**: https://github.com/Fission-AI/OpenSpec
- **官网**: https://openspec.dev
- **定位**: Spec-Driven Development (SDD) 框架

**核心理念**: 在"想法"和"写代码"之间加一层正式的需求规格，先就"做什么"达成一致，再写代码。

**工作流**:
```
/opsx:propose "add dark mode"
  → 生成 openspec/changes/add-dark-mode/
      ├── proposal.md    ← 为什么做、改什么
      ├── specs/         ← GIVEN/WHEN/THEN 场景
      ├── design.md      ← 技术方案
      └── tasks.md       ← 实现清单

/opsx:apply
  → AI 按 spec 逐步实现

/opsx:archive
  → 归档到 openspec/changes/archive/
```

**关键特征**:
- 每个变更有独立文件夹，包含 proposal + spec + design + tasks
- Spec 用 GIVEN/WHEN/THEN 格式（类 BDD）
- 支持 review spec diff（需求变更可视化）
- 支持 20+ AI 工具（通过 slash commands）
- 有归档机制

**设计哲学**:
- fluid not rigid（灵活不僵硬）
- iterative not waterfall（迭代不瀑布）
- built for brownfield not just greenfield（适合已有项目）

---

### 2.3 Cursor Rules

- **文档**: https://cursor.com/docs/rules
- **定位**: Cursor IDE 的项目级 AI 指令系统

**四层规则体系**:

| 层级 | 位置 | 作用域 |
|------|------|--------|
| User Rules | Cursor 设置 | 跨所有项目 |
| Team Rules | Dashboard | 组织级强制 |
| Project Rules | `.cursor/rules/*.md` | 项目级 |
| AGENTS.md | 项目根目录 | 项目级（简化版） |

**Project Rules 特色**:
- 支持 YAML frontmatter（`description`、`globs`、`alwaysApply`）
- 4 种应用模式：Always / Intelligently / Specific Files / Manual @mention
- 支持 glob 模式匹配特定文件

---

### 2.4 Cline（59.7k ⭐）

- **仓库**: https://github.com/cline/cline
- **定位**: VSCode 中的自主 AI 编码 agent

**上下文管理**:
- `.clinerules/` 目录结构（模块化规则文件）
- `CLAUDE.md` 作为入口引用文件
- MCP 工具扩展
- `@mentions` 手动添加上下文（`@url`、`@file`、`@folder`、`@problems`）

**Tribal Knowledge 理念**: `.clinerules/general.md` 专门记录"需要人工干预的模式"——与 Project Compass"只写 AI 推导不出来的东西"高度一致。

---

### 2.5 GitHub Copilot Agent HQ

- **文档**: https://github.com/features/copilot/agents
- **定位**: 多 agent 任务中心

**Pipeline**:
```
Issue (GitHub / Linear / Jira / Slack)
  → Assign to Copilot
  → 拉取完整上下文
  → 选择 agent（Copilot / Claude / Codex）
  → Agent HQ 统一管控
  → 生成 PR
```

**特色**:
- 原生集成 GitHub Issues + 第三方 issue tracker
- Agent memory：记住项目知识供未来使用
- 多 agent 选择
- `copilot-instructions.md` 作为项目指令文件

---

### 2.6 Linear Agent

- **官网**: https://linear.app
- **定位**: 为 AI-人类协作而生的项目管理工具

**工作流示例**:
```
Slack 对话发现问题 → @Linear 创建 issue → @Cursor 处理
→ Agent 读 issue + AGENTS.md → 自动 In Progress → 生成 PR → 完成
```

**特色**: 从一开始就为 agent 协作设计，issue 状态与 agent 执行实时同步。

---

## 3. 对比矩阵

| 能力 | Project Compass | OpenSpec | AGENTS.md | Cursor Rules | Copilot Agent |
|------|----------------|----------|-----------|--------------|---------------|
| **代码导航（L1）** | ✅ 多文件分层 | ❌ | ❌ | ❌ | ❌ |
| **编码规则（L2）** | ✅ 全局+模块 | ❌ | ⚠️ 单文件 | ✅ 多文件+glob | ⚠️ 单文件 |
| **需求规格** | ❌ 缺失 | ✅ 核心功能 | ❌ | ❌ | ❌ |
| **任务管理** | ✅ 看板+模板 | ✅ tasks.md | ❌ | ❌ | ✅ issue 驱动 |
| **会话续传（L4）** | ✅ 独有 | ❌ | ❌ | ❌ | ⚠️ agent memory |
| **归档** | ❌ 只删除 | ✅ 有 archive | ❌ | ❌ | ✅ issue 关闭 |
| **工具兼容** | ⚠️ 手动适配 | ✅ 20+ 工具 | ✅ 20+ 工具 | ❌ Cursor only | ❌ GitHub only |
| **自动化生成** | ✅ builders/cline/ | ✅ CLI 命令 | ❌ | ❌ | ❌ |
| **Issue 集成** | ❌ | ❌ | ❌ | ⚠️ GitHub | ✅ 多源 |

---

## 4. Project Compass 的独特价值

Project Compass 在以下方面是**独有的或领先的**：

1. **四层分离架构** — 没有其他方案同时覆盖导航、规则、任务、会话四层
2. **渐进式披露** — overview.md → features/[name]/ 的按需加载设计
3. **会话续传（L4）** — 几乎没有其他方案关注"跨对话进度接续"
4. **"只写 AI 推导不出来的东西"** — 与 Cline 的 tribal knowledge 理念一致，但更系统化
5. **关系 > 描述** — 强调变更联动、数据流路径，不是文件列表

---

## 5. 改进方向建议

### 优先级 1：需求规格层

**问题**: 当前 TASK 文件中，"任务输入"是纯自然语言，缺少结构化的需求规格。AI 需要从模糊描述中推测需求边界。

**方案 A — 内置 spec 区块**: 在 `_task-template.md` 中加入 `## 需求规格`，用 GIVEN/WHEN/THEN 格式，由 AI 根据验收问题的答案自动生成。

**方案 B — 与 OpenSpec 并行**: 用 OpenSpec 管需求规格（spec），用 Compass 管上下文（L1-L2）+ 会话（L4）。两者互补不冲突。

**建议**: 方案 A 更轻量，适合 Project Compass 的"够用就好"哲学。

### 优先级 2：AGENTS.md 兼容入口

**问题**: AGENTS.md 已成为事实标准（60k+ 项目），但 Project Compass 没有生成 AGENTS.md 的支持。

**方案**: 添加一个自动生成 `AGENTS.md` 的脚本或 prompt，从 `.ai/` 下的文档提取关键信息，生成一个符合 AGENTS.md 格式的入口文件。

### 优先级 3：Issue Tracker 衔接

**问题**: 需求来自 GitHub Issues / Linear / 脑子里，但没有"从 issue 创建 TASK"的标准流程。

**方案**: 在 builders/cline/prompt-L3.md 中增加“从 Issue 创建任务”的变体 prompt，让 AI 读取 issue 内容自动填充 TASK 文件。

### 优先级 4：归档工作流

**问题**: 任务完成后只是删除文件，没有历史记录。

**方案**: 添加 `L3-tasks/archive/` 目录，完成的任务移入而非删除；或在 decision-log.md 追加完成摘要。

---

## 6. 定位总结

```
                    需求规格            上下文管理           执行追踪
                   ┌────────┐        ┌────────────┐      ┌─────────┐
                   │OpenSpec│        │  Project   │      │ Copilot │
                   │        │        │  Compass   │      │Agent HQ │
                   │proposal│        │ L1 导航    │      │  Issue   │
                   │ specs  │◄──────►│ L2 规则    │◄────►│ tracking│
                   │ design │        │ L3 任务    │      │   PR    │
                   │ tasks  │        │ L4 会话    │      │ review  │
                   └────────┘        └────────────┘      └─────────┘
                        ↑                  ↑                  ↑
                   "做什么"           "怎么做+在哪"        "谁在做"
```

**Project Compass 的最佳定位**: 不是要替代 OpenSpec 或 issue tracker，而是做**中间层的上下文基础设施** — 无论需求从哪来、用什么工具执行，项目的代码导航、编码规则、会话续传始终需要 Project Compass 提供的四层上下文。
