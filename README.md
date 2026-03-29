# Project Compass

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
- **可验证 > 抽象** — "Domain 层禁止 import Infrastructure 层"比"采用 Clean Architecture"有用

## 四层架构

```
.ai/
├── L1-codebase-map/          ← 代码导航层（稳定，低频更新）
│   ├── overview.md           ← 项目导航首页（功能→代码映射 + 数据流 + 雷区）
│   ├── module-map.md         ← 模块合约与耦合地图（公开 API + 变更联动）
│   └── key-files.md          ← 任务食谱与变更影响索引
│
├── L2-rules/                 ← 规则层（稳定，按领域分片）
│   ├── global.md             ← 全局规则（具体可执行规则 + 反模式清单）
│   ├── _module-template.md   ← 模块规则模板（合约 + 陷阱 + 边界）
│   └── [module-name].md      ← 按项目实际模块创建
│
├── L3-tasks/                 ← 任务层（中频变化）
│   ├── current-plan.md       ← 当前计划（具体到文件 + 验证命令 + 风险标注）
│   ├── decision-log.md       ← 技术决策记录（ADR）
│   └── backlog.md            ← 待办事项池
│
├── L4-session/               ← 会话层（高频变化，每次对话维护）
│   └── active-session.md     ← 当前会话状态（含测试状态 + 下一步动作）
│
├── prompt-template.md        ← AI 提示词组装模板
├── clineprompt-L1.md         ← Cline 自动生成 L1 导航文档的 Prompt
├── clineprompt-L2.md         ← Cline 自动生成 L2 编码规则的 Prompt
└── README.md                 ← 本文件
```

## 快速开始

1. 将本模板复制到你的项目根目录，重命名为 `.ai/`
2. 填写 `.ai/L1-codebase-map/overview.md` — **最重要的一步**
   - 重点填写：功能→代码映射表、核心数据流、雷区清单
   - 或使用 `clineprompt-L1.md` 中的 prompt 让 Cline 辅助填写
3. 填写 `.ai/L2-rules/global.md` — 写下具体的编码规则和反模式
4. 复制 `.ai/L2-rules/_module-template.md`，按项目模块创建对应的规则文件
5. 在项目根目录创建入口文件（`CLAUDE.md` / `.cursorrules`），指向 `.ai/` 下的文档
6. 每次和 AI 对话时，按下方"加载策略"组装上下文

## 加载策略

### 每次对话必加载（Prompt 前置）
- `L1-codebase-map/overview.md` — 项目导航首页（功能→代码映射）
- `L4-session/active-session.md` — 当前会话状态（含下一步动作）
- `L2-rules/global.md` — 全局规则（含反模式清单）

### 按任务按需加载
- `L1-codebase-map/key-files.md` — 做常见开发任务时（加端点、加表、修 bug）
- `L1-codebase-map/module-map.md` — 跨模块修改时（查变更联动表）
- `L2-rules/[module-name].md` — 处理特定模块任务时（查合约和陷阱）
- `L3-tasks/current-plan.md` — 当前活跃计划

### 偶尔参考
- `L3-tasks/decision-log.md` — 遇到"为什么这样做"的问题时
- `L3-tasks/backlog.md` — 规划下一步时

## 每个文档该写什么（填写指南）

| 文档 | ✅ 该写 | ❌ 不该写（AI 自己能推导） |
|------|---------|--------------------------|
| overview.md | 功能→文件映射、数据流路径、雷区、构建命令 | 目录结构、技术栈列表、"某模块负责某功能" |
| module-map.md | 公开 API 清单、变更联动表、依赖禁止规则 | 模块职责描述、代码行数统计 |
| key-files.md | 任务食谱（改哪些文件+顺序）、调查起点、变更影响 | 文件列表（`tree` 的搬运） |
| global.md | 具体可执行规则、反模式清单、错误处理模式代码 | "架构模式: Clean Architecture"（太抽象） |
| 模块规则 | 对外合约（函数签名）、已知陷阱、测试策略 | 模块职责（从文件名就能猜到） |
| current-plan.md | 文件级步骤 + 验证命令 + 风险标注 | "重构某模块"（太模糊） |
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

### 方式一：Project Instructions（推荐）
在项目根目录创建 AI 工具的入口文件，指向 `.ai/` 下的文档：
- GitHub Copilot → `.github/copilot-instructions.md`
- Cursor → `.cursorrules`
- Claude → `CLAUDE.md`
- Cline → `.clinerules`
- 其他 → 参考对应工具的文档

入口文件示例：
```markdown
请阅读以下文件（按顺序）：
1. .ai/L1-codebase-map/overview.md — 项目导航（功能→代码映射）
2. .ai/L2-rules/global.md — 编码规则与反模式
3. .ai/L4-session/active-session.md — 当前进度与下一步

按需加载：
- .ai/L1-codebase-map/key-files.md — 常见任务食谱
- .ai/L1-codebase-map/module-map.md — 跨模块变更联动
- .ai/L2-rules/[模块名].md — 模块合约与陷阱
- .ai/L3-tasks/current-plan.md — 当前计划
```

### 方式二：手动粘贴
每次对话开始时，按加载策略粘贴相关文档内容。

### 方式三：自动化脚本
编写脚本根据当前 git diff / 修改文件，自动组装需要加载的上下文。
