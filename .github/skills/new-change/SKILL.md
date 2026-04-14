---
name: new-change
description: "Create a new change proposal with spec-driven workflow: proposal → delta spec → tasks → human confirm. Use when: 新需求, new feature, 加功能, add feature, 改需求, change request, 新变更, create change, 我要做, implement"
argument-hint: "Describe what you want to change or add (e.g., 'add CSV export for reports', '添加用户头像功能')"
---

# New Change (Spec-Driven)

按 spec-driven 流程创建新变更：proposal → delta spec → tasks → 人工确认后执行。

> 完整流程参考：`.ai/L3-specs/change-management.md`

## Prerequisites

- `.ai/` 目录已存在且有 L1 + L3 结构
- 用户描述了要做的变更（新功能 / 需求变更 / 重构等）

## Procedure

### Step 1: 收集上下文

1. 读取 `.ai/L1-codebase-map/overview.md` — 项目功能索引
2. 读取 `.ai/L3-specs/specs/system.md` — 系统级需求

```bash
# 已有能力域
ls .ai/L3-specs/specs/ | grep -v _capability-template | grep -v system.md

# 进行中的变更（避免冲突）
ls .ai/L3-specs/changes/ | grep -v _change-template
```

3. 根据变更描述，定位涉及的功能和模块：
   - `.ai/L1-codebase-map/features/[name]/README.md`
   - `.ai/L2-rules/[module].md`
   - `.ai/L3-specs/specs/<domain>/spec.md`（如已存在）

### Step 2: 命名变更

用 kebab-case 命名，如 `add-csv-export`、`fix-login-special-chars`。

创建变更目录：

```
.ai/L3-specs/changes/<name>/
├── proposal.md
├── specs/         (delta specs)
└── tasks.md
```

### Step 3: 写 proposal.md

参考 `.ai/L3-specs/changes/_change-template/proposal.md`，填写：

- **Why**: 为什么做、为什么是现在（1-2 句话）
- **What Changes**: 具体变更列表，标注破坏性变更为 **BREAKING**
- **Alternatives Considered**: 备选方案及选择理由
- **Capabilities Affected**: 新增/修改的能力域
- **Impact**: 影响范围

状态设为 `implementing`。

### Step 4: 生成 delta spec

为每个受影响的能力域创建 `changes/<name>/specs/<capability>/spec.md`：

| 情况 | delta spec 区段 |
|------|----------------|
| 全新能力域 | `## ADDED Requirements` — 全部为新增 |
| 修改已有能力域 | `## MODIFIED Requirements` — 完整复制要改的 Requirement 再修改 |
| 删除需求 | `## REMOVED Requirements` — 必须有 Reason 和 Migration |

**每个 Requirement 至少 1 个 Scenario**，使用 WHEN/THEN 格式。

### Step 5: 提出验收问题

主动提出 3-5 个需要人类确认的**业务**问题：

- ✅ 业务决策（"超过 10 万条时分页还是异步？"）
- ✅ 边界情况（"并发修改同一记录怎么处理？"）
- ✅ 兼容性（"旧 API 调用者需要兼容吗？"）
- ❌ 不问技术实现细节
- ❌ 不问读代码就能知道的事

**停下来等待人类回答。** 根据回答更新 delta spec。

### Step 6: 生成 tasks.md

参考 `.ai/L3-specs/changes/_change-template/tasks.md`，根据 proposal + delta spec 生成执行步骤：

- 按依赖排序（先做的放前面）
- checkbox 格式：`- [ ] X.Y 描述`
- 每个任务要小到一轮对话能完成
- 最后一组是 Verification — 从 Scenario 直接映射

### Step 7: 展示并等待确认

向用户展示完整的 proposal + delta spec + tasks，等待确认。

确认后：
1. proposal.md 状态保持 `implementing`
2. 更新 `.ai/L4-session/active-session.md` 指向该变更
3. 开始执行 tasks.md 中的第一个任务

### 输出格式

```
## 变更已就绪

**变更名称**: <name>
**受影响能力域**: [列表]

### Proposal 概要
[Why + What Changes 概述]

### Delta Spec 概要
[每个域的 ADDED/MODIFIED/REMOVED 数量]

### Tasks 概要
[N 个任务组，共 M 个具体步骤]

### 需要确认的业务问题
1. [问题]
2. [问题]
3. [问题]

等待确认后开始执行。
```
