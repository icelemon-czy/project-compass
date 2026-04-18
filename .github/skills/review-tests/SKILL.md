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
- ❌ 跳过虚假通过清单的某几条（清单是强制的）
---
name: review-tests
description: "Review test coverage by cross-referencing L3 specs, L5 traceability, and actual test code. Use when: review tests, 审查测试, test coverage, 测试覆盖, 测试够吗, are tests sufficient, 缺什么测试, missing tests, 测试质量"
argument-hint: "Optional: specific domain or feature to review (e.g., 'auth', 'payment'). Defaults to all domains."
---

# Review Test Coverage

交叉比对 L3 spec、L5 traceability 和实际测试代码，找出测试缺口。

## Prerequisites

- `.ai/` 目录已存在且有 L3 + L5 结构
- 项目有测试代码

## Procedure

### Step 1: 确定审查范围

- 如果用户指定了域/功能 → 只审查该域
- 如果用户说"全部" → 审查所有 `specs/` 下的能力域
- 默认 → 审查所有域

```bash
# 列出所有能力域
ls .ai/L3-specs/specs/ | grep -v _capability-template | grep -v system.md

# 列出已有追溯文件
ls .ai/L5-validation/traceability/ | grep -v _domain-template

# 列出已有测试设计
ls .ai/L5-validation/test-specs/ | grep -v _domain-template
```

### Step 2: 逐域审查

对每个能力域执行：

#### 2a: 收集 spec 中的 Scenario

读取 `specs/<domain>/spec.md`，提取所有 Requirement + Scenario。
同时检查 `changes/` 下是否有涉及该域的未归档 delta spec，一并统计。

#### 2b: 读取追溯状态

读取 `traceability/<domain>.md`（如存在），获取每个 Scenario 的当前状态：
- ✅ verified — 有代码实现 + 有测试覆盖
- ⚠️ untested — 有代码实现但无测试
- ⚠️ partial — 测试存在但不完整
- ❌ unimplemented — 代码都没实现

#### 2c: 验证实际测试代码

读取 `.ai/L2-rules/testing.md`（如存在）— 作为审查基准。

对追溯文件中标记为 ✅ verified 的 Scenario，**抽样验证**实际测试代码是否真正覆盖：

1. 根据追溯文件中的测试文件路径，读取实际测试代码
2. 检查测试是否真正验证了 WHEN → THEN 逻辑
3. 如果测试只检查了 happy path，没覆盖 edge case → 降级为 ⚠️ partial

#### 2d: 检查 test-specs 完整性

读取 `test-specs/<domain>.md`（如存在），检查：
- 是否每个 ⚠️ / ❌ Scenario 都有对应的测试用例设计
- 测试用例是否有具体数据（不能只写 "valid input"）
- 是否覆盖 happy path + edge case + error path

### Step 3: 输出审查报告

```
## 测试审查报告

### 概要

| 能力域 | Requirement | Scenario | ✅ verified | ⚠️ gap | ❌ missing |
|--------|-------------|----------|------------|--------|-----------|
| auth   | 5           | 12       | 8 (67%)    | 3 (25%)| 1 (8%)    |
| ...    |             |          |            |        |           |
| **总计** | **N**     | **N**    | **N (%)**  | **N (%)**| **N (%)** |

### 按域明细

#### <domain>

| Requirement | Scenario | 追溯状态 | 实际测试 | 问题 |
|-------------|----------|---------|---------|------|
| REQ-001     | 正常登录  | ✅      | ✅ auth.test.ts:45 | — |
| REQ-001     | 空密码    | ⚠️ untested | ❌ 无测试 | 需要补写 |

### 优先修复建议

按优先级排序（SHALL/MUST 优先于 SHOULD，核心路径优先于边缘）：

1. **高** — [domain] REQ-XXX Scenario: [name] — [原因]
2. **中** — ...
3. **低** — ...

### 缺失的 test-specs

以下 Scenario 缺少测试用例设计（需要先补 test-specs 再写测试）：
- [ ] [domain] REQ-XXX: [scenario name]
```

### Step 4: 提供行动建议

根据审查结果，提供明确的下一步：

| 发现 | 建议 |
|------|------|
| traceability 文件不存在 | 建议运行 L5 builder 或手动执行一次正向追溯 |
| test-specs 缺失 | 为 ⚠️/❌ Scenario 生成测试用例设计 |
| 有 test-specs 但无实际测试 | 按 test-specs 生成测试代码 |
| 追溯标记与实际测试不一致 | 更新 traceability 文件中的状态 |

> 如果用户确认，可以当场为缺口 Scenario 生成 test-specs 中的测试用例设计。
