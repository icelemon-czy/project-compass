# Project Compass

> **[English Version](README.md)**

> 通用 AI 上下文模板 — 适用于任意语言、任意框架、任意规模的项目
> 将本模板复制到你的项目根目录（重命名为 `.ai/`），按 `[填写]` 提示填入具体内容即可

## 核心理念

AI 的上下文窗口是有限的。对于任何有一定规模的代码库，都不可能把所有代码塞进上下文。
因此需要一套 **分层、按需加载** 的上下文管理体系，让 AI 每次对话都能：

1. **精准定位** — 收到任务时，知道该看哪些文件（功能→代码映射）
2. **遵守规则** — 知道该怎么写，不该怎么写（规则 + 反模式）
3. **理解目标** — 知道当前在做什么（任务层）
4. **延续进度** — 知道上一步做到哪了、下一步做什么（会话层）

### 设计原则

- **只写 AI 推导不出来的东西** — 目录结构、技术栈、模块职责这些 AI 能 `tree` + `grep` 推导，不值得写
- **面向任务的索引** — 文档的目标是帮 AI 定位"该看哪些代码"，而不是描述"代码长什么样"
- **关系 > 描述** — 文件间的耦合关系、变更联动比文件列表有用 100 倍
- **渐进式披露** — AI 每次只加载当前任务所需的最小上下文，而非一次性塞满窗口
- **可验证 > 抽象** — "Domain 层禁止 import Infrastructure 层"比"采用 Clean Architecture"有用

### L1 导航模型

AI 每次对话**只读 `overview.md`**（< 60 行），然后根据任务类型选择路径：

```
收到任务
 ├─ 匹配到具体功能 → features/[功能名]/README.md → 按需深入层文件
 ├─ 做常见开发任务 → key-files.md（通用任务食谱）
 ├─ 修改涉及多个模块 → module-map.md（变更联动表）
 └─ 改底层基础设施 → infrastructure/README.md
```

路径可组合 — 例如跨功能修改会同时加载 feature README + module-map。
每个目标文件都有**双向链接**（来源 / 相关文件），防止 AI 迷路。

## 四层架构

```
.ai/
├── L1-codebase-map/          ← 代码导航层（稳定，低频更新）
│   ├── overview.md           ← 唯一入口（< 60 行，功能索引 + 按需加载导航决策树）
│   ├── module-map.md         ← 模块合约与耦合地图（跨模块修改时加载）
│   ├── key-files.md          ← 通用任务食谱与调查起点（常见开发任务时加载）
│   ├── infrastructure/       ← 基础设施文档（框架/中间件/通用工具，与 features 平级）
│   │   └── README.md         ← 分层导航 + 架构全景 + 变更影响
│   └── features/             ← 按功能拆分的详细上下文（渐进式披露）
│       ├── _feature-template/   ← 功能文档模板（单文件，复制来创建新功能）
│       │   └── README.md        ← 概览 + 分层导航 + 数据流 + 层文件格式参考
│       └── [feature-name]/      ← 每个功能一个文件夹
│           ├── README.md        ← 功能概览（必读）
│           └── [层名].md        ← 层文件（按项目概念动态命名，按需加载）
│
├── L2-rules/                 ← 规则层（稳定，按领域分片）
│   ├── global.md             ← 全局规则（具体可执行规则 + 反模式清单）
│   ├── templates.md          ← 新建文件的代码模板（创建新文件时加载）
│   ├── _module-template.md   ← 模块规则模板（合约 + 陷阱 + 边界）
│   └── [module-name].md      ← 按项目实际模块创建
│
├── L3-tasks/                 ← 任务层（中频变化）
│   ├── board.md              ← 任务看板（所有任务状态索引）
│   ├── _task-template.md     ← 任务模板（复制来创建新任务）
│   ├── TASK-xxx.md           ← 各任务详情（输入→计划→测试用例）
│   ├── decision-log.md       ← 技术决策记录（ADR）
│   └── review/               ← 人工审核区（AI 产出先放这，人工确认后合入）
│
├── L4-session/               ← 会话层（高频变化，每次对话维护）
│   └── active-session.md     ← 当前会话状态（含测试状态 + 下一步动作）
│
├── builders/                  ← 自动生成文档的 Prompt 集合（按工具分目录）
│   ├── cline/               ← Cline 专用（subagent 只读，输出文本由主 agent 写入文件）
│   │   ├── prompt-L1a.md     ← 生成 L1 文档 Phase 1-3（扫描 + overview）
│   │   ├── prompt-L1b.md     ← 生成 L1 文档 Phase 4-5（subagents 深入分析）
│   │   ├── prompt-L2.md      ← 生成 L2 编码规则
│   │   └── prompt-L3.md      ← 创建与规划 L3 任务
│   └── claude/              ← Claude Code 专用（subagent 可读写，直接创建文件）
│       ├── prompt-L1a.md
│       ├── prompt-L1b.md
│       ├── prompt-L2.md
│       └── prompt-L3.md
├── entrypoints/              ← AI 工具入口文件模板
│   ├── clinerules.md         ← Cline 入口模板（→ .clinerules）
│   ├── claude.md             ← Claude Code 入口模板（→ CLAUDE.md）
│   ├── cursorrules.md        ← Cursor 入口模板（→ .cursorrules）
│   └── copilot-instructions.md ← GitHub Copilot 入口模板
├── roadmap/                  ← 路线图与调研
│   ├── requirements-integration-research.md ← 需求衔接方案调研
│   └── multi-agent-collaboration-research.md ← 多 Agent 并行协作调研
└── README.md                 ← 本文件
```

## L1 与 L2 的区别

> **一句话：L1 = 地图（在哪儿、怎么走），L2 = 规矩（怎么写、什么能做什么不能做）**

用一个比喻来说：
- **L1** = 城市地图 → "医院在这，学校在那，从家到医院走这条路"
- **L2** = 交通规则 → "靠右行驶，红灯停绿灯行，限速 60"

### 具体对比

| 问题 | L1 回答 | L2 回答 |
|------|---------|---------|
| "登录功能代码在哪？" | ✅ `src/auth/` 目录，入口在 `routes/auth.ts` | — |
| "改了 User 表会影响什么？" | ✅ 要同步改 JWTPayload 类型 | — |
| "请求的完整数据流是什么？" | ✅ route → controller → service → repo → 响应 | — |
| "命名应该用什么风格？" | — | ✅ 文件 kebab-case，函数 camelCase |
| "新建一个 Service 文件该长啥样？" | — | ✅ 有标准代码模板 |
| "错误处理该怎么做？" | — | ✅ Service 层 throw AppError，Controller 不 try-catch |
| "这个模块的 API 哪些能改？" | — | ✅ `authenticate()` 是 STABLE，`validatePassword()` 是 INTERNAL |
| "这个功能有什么坑？" | ✅ 异步回调有竞态条件 | — |

### 文件对应

```
L1 features/user-auth/              L2 rules/
├── README.md    → 数据流 + 变更影响     ├── global.md     → 全局编码规范
├── routes.md    → 端点在哪、参数结构     ├── templates.md  → 新建文件的代码模板
├── services.md  → 业务规则、状态流转     └── auth.md       → auth 模块的合约 + 编码约束
└── models.md    → 表结构、查询、迁移
     ↑                                      ↑
     地图：代码在哪、数据怎么流                规矩：代码怎么写、合约是什么
```

> 注：层文件名（如 routes.md、services.md）不是固定的，由 subagent 根据实际代码结构动态命名。

### 当信息同时跟两边有关时

| 信息类型 | 放哪 | 判断依据 |
|----------|------|----------|
| "登录时 token 刷新有竞态条件" | L1 | 跟该功能的数据流相关 |
| "`authenticate()` 是稳定 API，不能改签名" | L2 | 跟模块合约/编码约束相关 |
| "改了 User model 要同步改 DTO" | L1 | 是变更影响（改 A 要改 B） |
| "所有数据库操作必须使用事务" | L2 | 是编码规则（怎么写） |
| "支付回调是异步的" | L1 | 是数据流特性 |
| "新认证方式必须实现 AuthStrategy 接口" | L2 | 是编码约束（必须遵循的模式） |

## 快速开始

1. 将本模板复制到你的项目根目录，重命名为 `.ai/`
2. 填写 `.ai/L1-codebase-map/overview.md` — **最重要的一步**
   - 重点填写：功能→代码映射表、核心数据流、雷区清单
   - 或使用 `builders/cline/prompt-L1a.md`（Cline）或 `builders/claude/prompt-L1a.md`（Claude Code）中的 prompt 让 AI 辅助填写
3. 填写 `.ai/L2-rules/global.md` — 写下具体的编码规则和反模式
4. 复制 `.ai/L2-rules/_module-template.md`，按项目模块创建对应的规则文件
5. 在项目根目录创建入口文件（`CLAUDE.md` / `.cursorrules`），指向 `.ai/` 下的文档
6. 每次和 AI 对话时，按下方"加载策略"组装上下文

## 加载策略

### 每次对话必加载（Prompt 前置）
- `L1-codebase-map/overview.md` — 轻量索引（< 60 行，功能目录 + 雷区）
- `L4-session/active-session.md` — 当前会话状态（含下一步动作）
- `L2-rules/global.md` — 全局规则（含反模式清单）

### 收到任务后按需加载（渐进式披露）
- `L1-codebase-map/features/[功能名]/README.md` — **从 overview.md 索引表匹配到功能后加载，按需深入各层文件**
- `L1-codebase-map/key-files.md` — 做通用开发任务时（加端点、加表、修 bug）
- `L1-codebase-map/module-map.md` — 跨模块修改时（查变更联动表）
- `L2-rules/[module-name].md` — 处理特定模块任务时（查合约和陷阱）
- `L2-rules/templates.md` — 创建新文件时（查标准代码模板）
- `L3-tasks/board.md` — 查看任务全局状态
- `L3-tasks/TASK-xxx.md` — 当前进行中的任务详情

### 偶尔参考
- `L3-tasks/decision-log.md` — 遇到"为什么这样做"的问题时
- `L3-tasks/board.md` — 规划下一步时（查看 open 任务）

## 实际工作流程（模式 B：AI 自主导航）

> 推荐用法：在项目根目录放一个入口文件，AI 每次对话自动读取 `.ai/` 下的文档，全程自主导航。

```
┌─────────────────────────────────────────────────────────┐
│  Step 0（一次性配置）                                      │
│  复制 entrypoints/ 下对应模板 → 项目根目录入口文件          │
│  （.clinerules / CLAUDE.md / .cursorrules 等）            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 1-2（每次对话自动）                                  │
│  AI 读取入口文件 → 自动加载：                               │
│    • overview.md      — 项目功能索引                       │
│    • global.md        — 全局编码规则                       │
│    • active-session.md — 上次进度 + 下一步                  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3  用户给出任务                                      │
│  "修复用户登录的 token 刷新 bug"                            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 4  AI 按索引定位功能                                  │
│  overview.md 功能索引 → 匹配"用户认证"                      │
│  → 读取 features/user-auth/README.md                     │
│  → 根据分层导航表按需深入各层文件                 │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 5  AI 读取模块规则                                   │
│  → 读取 L2-rules/auth.md（合约 + 编码约束 + 陷阱）          │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 6  AI 管理任务                                       │
│  → 查 board.md 看现有任务 / 创建新 TASK-xxx.md              │
│  → 写执行计划 + 验收问题 → 等人类确认                        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 7  AI 执行编码                                       │
│  遵守 global.md + 模块规则，参考 templates.md               │
│  跨模块修改前查 module-map.md 变更联动表                      │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 8  AI 更新会话状态                                    │
│  → 更新 active-session.md                                 │
│    • 完成了什么、涉及哪些文件                                │
│    • 测试结果、下一步具体动作                                │
└─────────────────────────────────────────────────────────┘
```

**关键点：** 人只需要做 Step 0（一次）+ Step 3（给任务），其余全部由 AI 自主完成。

## 每个文档该写什么（填写指南）

| 文档 | ✅ 该写 | ❌ 不该写（AI 自己能推导） |
|------|---------|--------------------------|
| overview.md | **功能索引表**（名称+指针）、雷区、构建命令 | 数据流详情、涉及文件列表（放到 features/[name]/ 下） |
| module-map.md | 公开 API 清单、变更联动表、依赖禁止规则 | 模块职责描述、代码行数统计 |
| key-files.md | 通用任务食谱、调查起点、全局变更影响 | 功能相关的食谱（放到 features/[name]/ 下） |
| features/[name]/ | 单个功能的完整上下文，按层拆分：README（概览+数据流）、controller/service/data（各层细节） | 跨功能的通用信息 |
| global.md | 具体可执行规则、反模式清单、错误处理模式 | "架构模式: Clean Architecture"（太抽象） |
| templates.md | 新建文件的代码模板（Service、Test 等） | 应从实际代码中提取，不是编造 |
| 模块规则 | 对外合约（函数签名+稳定性）、模块内编码约束、边界规则、测试策略 | 数据流、文件列表、变更影响（放 L1） |
| board.md | 任务状态索引（ID + 标题 + 状态） | 任务详情（放在 TASK-xxx.md） |
| TASK-xxx.md | 任务输入 + AI 计划 + 测试用例 + 执行步骤 | "重构某模块"（太模糊） |
| active-session.md | 下一步具体动作、测试状态、涉及文件状态 | "正在做某功能"（太模糊） |

## 维护节奏

| 文档 | 谁维护 | 频率 |
|------|--------|------|
| L1 代码导航 | 人 + AI辅助 | 架构变更时 |
| L2 规则 | 人 | 规范变更时 |
| L3 任务计划 | 人 + AI | 每个任务周期 |
| L3 决策日志 | 人 + AI | 每次重要决策后 |
| L4 会话状态 | AI（人审核） | 每次对话结束时 |

## 集成方式

### 方式一：入口文件（推荐 — AI 自主导航）

从 `entrypoints/` 目录复制对应模板到项目根目录：

| AI 工具 | 模板文件 | 放置位置 |
|---------|----------|----------|
| Cline | `entrypoints/clinerules.md` | 项目根目录 `.clinerules` |
| Claude Code | `entrypoints/claude.md` | 项目根目录 `CLAUDE.md` |
| Cursor | `entrypoints/cursorrules.md` | 项目根目录 `.cursorrules`（或 `.cursor/rules/`）|
| GitHub Copilot | `entrypoints/copilot-instructions.md` | `.github/copilot-instructions.md` |

入口文件包含完整的导航指令，AI 会自动读取 `.ai/` 下的文档并按需导航。
详见上方「实际工作流程（模式 B）」。
