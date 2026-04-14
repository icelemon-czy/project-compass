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
