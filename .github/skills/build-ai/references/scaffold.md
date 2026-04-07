# Phase 0: Scaffold .ai Directory

Create the `.ai/` directory structure in the target project.

## Directory Structure

```
.ai/
├── L1-codebase-map/
│   ├── overview.md              ← Phase 3 creates
│   ├── module-map.md            ← Phase 5 creates
│   ├── key-files.md             ← Phase 5 creates
│   ├── features/
│   │   └── _feature-template/
│   │       └── README.md        ← Scaffold creates (format reference)
│   └── infrastructure/
│       └── _infrastructure-template/
│           └── README.md        ← Scaffold creates (format reference)
├── L2-rules/
│   ├── global.md                ← Phase 6 creates
│   ├── templates.md             ← Phase 6 creates
│   └── _module-template.md      ← Scaffold creates (format reference)
├── L3-tasks/
│   ├── board.md                 ← Scaffold creates (initialized)
│   ├── _task-template.md        ← Scaffold creates (format reference)
│   └── decision-log.md          ← Scaffold creates (initialized)
└── L4-session/
    └── active-session.md        ← Scaffold creates (initialized)
```

## Files to Create Now

Create each file below with the specified content. Files marked "Phase X creates" will be created later during analysis.

---

### `.ai/L1-codebase-map/features/_feature-template/README.md`

```markdown
# [功能名称]

> 本文件夹包含「[功能名称]」的完整上下文，按层拆分。
> **加载时机**：当任务涉及此功能时，从 overview.md 的功能索引跳转到这里。
>
> ⚠️ **本文件夹是内容格式参考，不是结构蓝图。**
> 文件数量和文件名由该功能的实际层次决定（由 subagent 在 Step 1 层次发现中确定），
> 不要机械复制 entry.md / logic.md / data.md 三层结构。

## 分层导航

| 层文件 | 加载时机 | 包含内容摘要 |
|--------|---------|-------------|
| [如: handler.md] | [如: 改 API 入口 / 加新端点] | [如: 路由注册、请求处理] |
| [如: service.md] | [如: 改业务逻辑 / 加新规则] | [如: 核心规则、状态机] |

> 💡 先读本 README（数据流 + 变更影响）→ 根据上表按任务类型选择性加载层文件

## 数据流

### [操作 1]
<!-- 写出核心操作的完整链路 -->

### [操作 2]

## 变更影响

| 当你改了… | 必须同步改… | 原因 |
|-----------|-------------|------|
| [填写] | [填写] | [填写] |

## 已知陷阱

- ⚠️ [填写]
```

---

### `.ai/L1-codebase-map/infrastructure/_infrastructure-template/README.md`

```markdown
# 基础设施层

> 本文件夹文档化跨功能的底层架构和基础设施（项目级共享基础设施）。
> **加载时机**：当任务涉及框架基类、配置系统、插件机制、构建流程、测试基础设施等时加载。
>
> 📂 **本文件夹结构**（按实际项目调整）：
> - `_infrastructure-template/` — 内容格式参考（不要机械复制）
> - `[组件名]/` — 每个基础设施组件一个文件夹

## 组件索引

| 组件 | 加载时机 | 包含内容摘要 |
|------|---------|-------------|
| [如: framework/] | [如: 继承基类 / 用 DI 容器] | [如: 基类体系、DI 注册] |
| [如: config/] | [如: 加新配置项 / 改配置加载] | [如: 配置文件结构、加载顺序] |

## 架构全景

<!-- 基础设施各组件之间的关系 -->

## 变更影响

| 当你改了… | 必须同步改… | 原因 |
|-----------|-------------|------|
| [填写] | [填写] | [填写] |

## 已知陷阱

- ⚠️ [填写]
```

---

### `.ai/L2-rules/_module-template.md`

```markdown
# 模块规则模板

> **使用方法**: 复制本文件，重命名为模块名（如 `api.md`、`auth.md`）。
> 仅在处理该模块相关任务时加载。

## 模块身份

- **模块名**: [填写]
- **路径**: [填写]
- **状态**: [🟢 stable / 🟡 active / 🔴 legacy]

## 对外合约

### 公开 API

<!-- ✅ STABLE = 不可随意改名/删除  🔧 INTERNAL = 可以重构 -->

### 使用规则

- [填写]

## 模块内编码规则

- [填写]

## 模块边界

| 交互方向 | 允许？ | 方式 | 违反后果 |
|----------|--------|------|----------|
| [填写] | [✅/❌] | [填写] | [填写] |

## 测试策略

- **测试类型**: [填写]
- **Mock 规则**: [填写]
- **运行命令**: [填写]
```

---

### `.ai/L3-tasks/board.md`

```markdown
# 任务看板

> 所有任务的状态一览。每次对话时加载，了解全局进度。
>
> **状态**: 📋 `open` | 🔨 `ongoing` | ✅ `review`
>
> **操作**:
> - 新建任务 → 复制 `_task-template.md`，在下表添加一行
> - 代码完成 + 测试通过 → 状态改为 ✅ review，将任务文件移入 `review/`
> - 人类确认后 → 删除任务文件，从下表移除

## 活跃任务

| ID | 任务 | 状态 | 测试 | 详情 |
|----|------|------|------|------|
| | *暂无任务* | | | |
```

---

### `.ai/L3-tasks/_task-template.md`

```markdown
# TASK-XXX: [任务标题]

> **状态**: 📋 open / 🔨 ongoing / ✅ review
> **创建**: YYYY-MM-DD

## 任务输入

<!-- 人类用自然语言写下要做什么 -->

[填写]

---

## AI 计划

### 概要

**目标**: [AI 填写]
**分析**: [AI 填写 — 涉及哪些功能/模块，有什么风险]
**范围**: [AI 填写 — 涉及模块和文件]

### 验收问题

1. [AI 填写] → [人类答]
2. [AI 填写] → [人类答]
3. [AI 填写] → [人类答]

### 执行步骤

- [ ] **→ 步骤 1：[AI 填写]** ← CURRENT
  - 要改：`[文件路径]`
  - 验证：`[命令]`

### 约束与风险

- ❌ 禁止：[AI 填写]
- ⚠️ 风险：[AI 填写]
- 🔙 回退：[AI 填写]

---

## 测试用例

<!-- AI 根据验收问题的答案生成 -->
```

---

### `.ai/L3-tasks/decision-log.md`

```markdown
# 架构决策记录

> 记录重要的技术决策及其理由。遇到"为什么这样做"时查阅。

## 模板

### DEC-XXX: [决策标题]

**日期**: YYYY-MM-DD
**状态**: 已决定 / 已废弃 / 讨论中

**背景**: [什么情况下需要做这个决定]

**选项**:
1. [方案 A] — 优点：... / 缺点：...
2. [方案 B] — 优点：... / 缺点：...

**决定**: 选择方案 [X]
**理由**: [为什么选这个]
**后果**: [这个决定会带来什么影响]

---

## 决策列表

<!-- 按上方模板添加决策 -->
```

---

### `.ai/L4-session/active-session.md`

```markdown
# 当前会话状态

> ⚡ 每次对话必读 + 对话结束时更新

## 最后更新

- **时间**: [YYYY-MM-DD HH:mm]
- **对话主题**: [简述上次对话在做什么]

## 当前工作焦点

**正在做**: [具体到函数级别]
**当前任务**: [如: TASK-001 步骤 3]
**涉及文件**:
- `[文件路径]` — [状态]

## 已完成（本轮）

- [x] [具体描述]

## 下一步具体动作

1. [ ] [可直接执行的操作]
2. [ ] [可直接执行的操作]

## 测试状态

- [测试结果]
```
