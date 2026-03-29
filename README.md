# Project Compass

> 通用 AI 上下文模板 — 适用于任意语言、任意框架、任意规模的项目
> 将本模板复制到你的项目根目录（重命名为 `.ai/`），按 `[填写]` 提示填入具体内容即可

## 核心理念

AI 的上下文窗口是有限的。对于任何有一定规模的代码库，都不可能把所有代码塞进上下文。
因此需要一套 **分层、按需加载** 的上下文管理体系，让 AI 每次对话都能：

1. **快速定位** — 知道代码库长什么样（代码地图）
2. **遵守规则** — 知道该怎么写（规则层）
3. **理解目标** — 知道当前在做什么（任务层）
4. **延续进度** — 知道上一步做到哪了（会话层）

## 四层架构

```
.ai/
├── L1-codebase-map/          ← 代码地图层（稳定，低频更新）
│   ├── overview.md           ← 项目全局概览（必读）
│   ├── module-map.md         ← 模块结构 + 依赖关系
│   └── key-files.md          ← 关键文件索引
│
├── L2-rules/                 ← 规则层（稳定，按领域分片）
│   ├── global.md             ← 全局规则（语言/通用规范）
│   ├── _module-template.md   ← 模块规则模板（复制此文件来新建模块规则）
│   └── [module-name].md      ← 按项目实际模块创建（如 api.md、ui.md、data.md…）
│
├── L3-tasks/                 ← 任务层（中频变化）
│   ├── current-plan.md       ← 当前活跃的开发/重构计划
│   ├── decision-log.md       ← 技术决策记录（ADR）
│   └── backlog.md            ← 待办事项池
│
├── L4-session/               ← 会话层（高频变化，每次对话维护）
│   └── active-session.md     ← 当前会话状态
│
├── prompt-template.md        ← AI 提示词组装模板
└── README.md                 ← 本文件
```

## 快速开始

1. 将本模板复制到你的项目根目录，重命名为 `.ai/`
2. 填写 `.ai/L1-codebase-map/overview.md` — 这是最重要的一步
3. 填写 `.ai/L2-rules/global.md` — 写下你的编码规范
4. 复制 `.ai/L2-rules/_module-template.md`，按项目模块创建对应的规则文件
5. 在项目根目录创建入口文件（`CLAUDE.md` / `.cursorrules`），指向 `.ai/` 下的文档
6. 每次和 AI 对话时，按下方"加载策略"组装上下文

## 加载策略

### 每次对话必加载（Prompt 前置）
- `L1-codebase-map/overview.md` — 项目全局概览
- `L4-session/active-session.md` — 当前会话状态
- `L2-rules/global.md` — 全局规则

### 按任务按需加载
- `L2-rules/[module-name].md` — 根据当前任务涉及的模块加载对应规则
- `L3-tasks/current-plan.md` — 当前活跃计划
- `L1-codebase-map/module-map.md` — 需要跨模块理解时加载

### 偶尔参考
- `L3-tasks/decision-log.md` — 遇到"为什么这样做"的问题时
- `L3-tasks/backlog.md` — 规划下一步时
- `L1-codebase-map/key-files.md` — 需要精确定位文件时

## 维护节奏

| 文档 | 谁维护 | 频率 |
|------|--------|------|
| L1 代码地图 | 人 + AI辅助 | 架构变更时 |
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
1. .ai/L1-codebase-map/overview.md — 项目全貌
2. .ai/L2-rules/global.md — 编码规范
3. .ai/L4-session/active-session.md — 当前进度

按需加载：
- .ai/L2-rules/[模块名].md — 模块特定规则
- .ai/L3-tasks/current-plan.md — 当前计划
```

### 方式二：手动粘贴
每次对话开始时，按加载策略粘贴相关文档内容。

### 方式三：自动化脚本
编写脚本根据当前 git diff / 修改文件，自动组装需要加载的上下文。
