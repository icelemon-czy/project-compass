---
name: review-tests
description: "Review test quality by running tests, cross-referencing specs, and hunting false-pass anti-patterns. Use when: review tests, 审查测试, test coverage, 测试覆盖, 测试够吗, are tests sufficient, 缺什么测试, missing tests, 测试质量, 虚假通过, false pass"
argument-hint: "Optional: specific domain or change name (e.g., 'auth', 'add-csv-export'). Defaults to the change currently in pending-review."
---

# Review Tests — 审查 + 跑测试 + 虚假通过审查

三件事一起做：**跑测试** + **覆盖审查** + **虚假通过狩猎**。

> 这是工作流中的 **人工门槛 2（Review 批准）** 所在环节。Reviewer 在此决定能不能归档。

## Prerequisites

- `.ai/` 目录已存在且有 L3 + L5 结构
- 项目有测试代码
- 目标变更处于 `pending-review` 状态（或用户显式指定审查范围）

## Procedure

### Step 0: 跑测试（强制，新增）

```bash
# 先运行项目的完整测试套件，捕获结果
<项目测试命令，读 L2-rules/testing.md 获取>
```

根据结果分支：

| 测试结果 | 处理 |
|:---------|:-----|
| ❌ 有失败 | **立即转 `/fix-bug`**，把失败输出作为输入。本 Skill 到此结束 |
| ✅ 全绿 | 继续 Step 1 — 但**不代表通过**，还要查虚假通过 |

### Step 1: 确定审查范围

- 参数指定了域/变更名 → 只审查该范围
- 无参数 → 优先审查所有 `pending-review` 状态的变更；否则审查所有域

```bash
ls .ai/L3-specs/specs/ | grep -v _capability-template | grep -v system.md
ls .ai/L3-specs/changes/
ls .ai/L5-validation/traceability/ | grep -v _domain-template
```

### Step 2: 逐域审查（静态部分）

对每个范围内的能力域：

#### 2a: 收集 Scenario

读取 `specs/<domain>/spec.md` + `changes/` 下相关 delta，统计全部 Requirement + Scenario。

#### 2b: 读取追溯状态

读取 `traceability/<domain>.md`：
- ✅ verified — 有代码 + 有测试
- ⚠️ untested — 有代码无测试
- ⚠️ partial — 测试存在但不完整
- ❌ unimplemented — 代码都没实现

#### 2c: 抽样验证实际测试代码

对 ✅ verified 的 Scenario，打开测试文件，验证是否真的覆盖 WHEN → THEN。

### Step 3: 虚假通过狩猎（关键，新增）

测试"绿"不等于"对"。逐个 ✅ verified 的测试，用以下 **7 条反模式清单** 过一遍：

| # | 反模式 | 信号 | 风险等级 |
|:--|:-------|:-----|:---------|
| 1 | **断言缺失** | 测试跑完没有 `assert` / `expect` | 🔴 高 |
| 2 | **断言太弱** | 只断言 `toBeTruthy()`、`not null`、`>= 0`，不验证具体值 | 🔴 高 |
| 3 | **Happy path only** | 只有 1 个用例，没有 edge case / error path | 🔴 高 |
| 4 | **Mock 了要测的东西** | 把被测函数本身 mock 掉，只验证 mock 被调用 | 🔴 高 |
| 5 | **Assertion 绕开 spec THEN** | 测试 assert 的内容和 spec 的 THEN 不一致 | 🟡 中 |
| 6 | **条件永真** | `expect(x).toBe(x)` / `if (true) assert` / 只 snapshot 不检查内容 | 🔴 高 |
| 7 | **忽略异常** | `try { ... } catch { }` 吞掉异常，测试依然绿 | 🔴 高 |

> **清单可扩展**：项目可在 `.ai/L2-rules/testing.md` 追加第 8+ 条（例：时间依赖、快照没 assert、race condition、fixture 硬编码）。前 7 条是底线，不可删除。Review 时按 “7 + 项目自定义" 全部過一遍。

**对每个命中的反模式**，记录：
- 测试文件 : 行号
- 命中的反模式编号
- 对应的 Spec Scenario
- 建议修复：通常是走 `/fix-bug` 的 **Step 3B（虚假通过分支）**

### Step 4: 输出审查报告

```
## 测试审查报告

### 执行结果
- 测试运行: ✅ 全绿 / ❌ N 个失败（已转 /fix-bug）
- 审查范围: [变更名 / 能力域]

### 覆盖概要

| 能力域 | Requirement | Scenario | ✅ verified | ⚠️ gap | ❌ missing |
|--------|-------------|----------|------------|--------|-----------|
| auth   | 5           | 12       | 8 (67%)    | 3 (25%)| 1 (8%)    |
| **总计** | **N**     | **N**    | **N (%)**  | **N (%)**| **N (%)** |

### 虚假通过检查

| 测试文件 : 行 | 反模式 | Scenario | 建议 |
|---------------|--------|----------|------|
| auth.test.ts:45 | #2 断言太弱 | REQ-001 空密码拒绝 | 补具体错误码断言 |
| ... | ... | ... | ... |

### 按域明细

| Requirement | Scenario | 追溯状态 | 实际测试 | 问题 |
|-------------|----------|---------|---------|------|
| REQ-001     | 正常登录  | ✅      | ✅ auth.test.ts:45 | — |
| REQ-001     | 空密码    | ⚠️ untested | ❌ 无测试 | 需要补写 |

### 结论（必填）

- [ ] ✅ 通过 — 可以 `/archive-change`
- [ ] ⚠️ 有缺口但非阻塞 — 列出可延后项
- [ ] ❌ 打回 — 列出必须修复项，走 `/fix-bug`

### 打回原因（如适用）
1. **高** — [file:line] 虚假通过：[描述] → 走 /fix-bug Step 3B
2. **高** — [domain] 缺 Scenario: [name] → 走 /fix-bug Step 3B 补测试
```

### Step 5: 状态回流

根据 Step 4 结论：

| 结论 | 变更状态流转 |
|:-----|:-------------|
| ✅ 通过 | 保持 `pending-review`，提示用户运行 `/archive-change` |
| ❌ 打回 | `pending-review` → `review-failed` → `implementing`（记录在 proposal.md） |
| ⚠️ 有缺口但非阻塞 | 保持 `pending-review`，问题登记到 proposal.md 的"Known Gaps" |

更新 `.ai/L4-session/active-session.md`，记录审查结果和下一步动作。

## 反模式（Reviewer 禁止）

- ❌ 不跑测试就签字通过
- ❌ 只看 traceability 的 ✅，不打开测试文件
- ❌ 发现虚假通过只记录不打回
- ❌ 跳过虚假通过清单的某几条（清单是强制的；项目可追加，但不可删除）
