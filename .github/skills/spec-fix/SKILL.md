---
name: spec-fix
description: "Fix a bug or unexpected behavior using spec-first discipline: check spec → update test → fix code → run tests. Use when: bug, 有bug, 行为不对, unexpected behavior, fix issue, 修bug, 不符合预期, something broken, 测试失败, test failed"
argument-hint: "Describe the bug or unexpected behavior (e.g., 'login allows empty password', '导出的 CSV 缺少 header')"
---

# Spec-First Bug Fix

发现 bug 或行为与预期不一致时，强制执行 **spec → test → code** 的修复顺序。

> **核心纪律**：绝不先改代码。先确认"正确行为"是什么（spec），再确认"怎么验证"（test），最后才动手修（code）。

## Prerequisites

- `.ai/` 目录已存在且有 L1 + L3 + L5 结构
- 用户描述了具体的 bug 或不符合预期的行为

## Procedure

### Step 1: 定位相关 spec

根据用户描述的 bug，定位到受影响的功能和需求：

1. 读取 `.ai/L1-codebase-map/overview.md` — 匹配涉及的功能
2. 读取对应的 `features/[name]/README.md` — 理解数据流和相关代码
3. 读取 `.ai/L3-specs/specs/` 下对应能力域的 `spec.md` — 找到相关 Requirement + Scenario
4. 检查 `.ai/L3-specs/changes/` — 是否有正在进行中的相关变更

### Step 2: 判断 spec 状态

对照 bug 描述和 spec，判断是以下哪种情况：

| 情况 | 含义 | 下一步 |
|------|------|--------|
| **A: Spec 正确，代码违反** | Spec 已定义了正确行为，但代码没实现对 | → Step 3（跳过 spec 修改） |
| **B: Spec 缺失** | 这个行为没有 spec 覆盖 | → Step 2b 先补 spec |
| **C: Spec 错误** | Spec 定义的行为本身就不对 | → Step 2b 先改 spec |

#### Step 2b: 更新 Spec（仅情况 B / C）

1. 在 `.ai/L3-specs/changes/` 下创建一个 fix 变更（如 `fix-empty-password-validation`）
2. 写简短的 `proposal.md`（Why: bug 描述；What: spec 修正）
3. 写 delta spec：
   - 情况 B → `## ADDED Requirements`：补写缺失的 Requirement + Scenario
   - 情况 C → `## MODIFIED Requirements`：修正错误的 Requirement / Scenario
4. **展示 delta spec 给用户确认，再继续**

### Step 3: 更新测试用例

在改代码之前，先确保测试能捕获正确行为：

1. 读取 `.ai/L2-rules/testing.md`（如存在）— 遵守项目测试规范
2. 读取 `.ai/L5-validation/traceability/` 对应域的追溯文件 — 找到该 Scenario 对应的测试
3. 读取 `.ai/L5-validation/test-specs/` 对应域的测试设计 — 检查是否有该场景

**三种情况**：

| 测试状态 | 操作 |
|---------|------|
| 有测试但断言错误 | 修正测试的预期值，使其符合 spec |
| 有测试但未覆盖该场景 | 在 test-specs 中补写用例，然后在代码中添加测试 |
| 无测试 | 在 test-specs 中写完整用例（happy path + edge case + error path），然后在代码中创建测试 |

写测试时从 spec 的 WHEN/THEN 直接映射：
- **WHEN** → 测试的 setup + action
- **THEN** → 测试的 assertion

> **此时运行测试，确认测试失败**（因为代码还没修）。如果测试已经通过，说明问题定位有误，回到 Step 1 重新检查。

### Step 4: 修复代码

现在有了失败的测试作为目标，修复代码：

1. 读取 `.ai/L2-rules/global.md` + 相关模块规则 — 遵守编码约束
2. 定位 bug 所在的代码（L1 feature 文档中有代码位置）
3. 修复代码
4. **运行测试，确认通过**

> 如果修复涉及跨模块变更，先读 `.ai/L1-codebase-map/module-map.md` 查变更联动表。

### Step 5: 更新追溯 & 收尾

1. 更新 `.ai/L5-validation/traceability/<domain>.md` — 将该 Scenario 状态改为 ✅ verified
2. 如果 Step 2b 创建了变更：
   - 生成 `tasks.md` 并勾选所有完成的任务
   - 将 proposal 状态改为 `pending-review`
   - 告知用户可以归档（合并 delta spec → 主 spec → 移到 archive/）
3. 更新 `.ai/L4-session/active-session.md` — 记录修复内容和测试结果

### 输出格式

完成后向用户报告：

```
## Bug 修复完成

**问题**: [用户描述的 bug]
**根因**: [A/B/C 哪种情况 + 具体原因]
**Spec 变更**: [有/无，如有列出 delta]
**测试变更**: [新增 N 个 / 修改 N 个测试用例]
**代码变更**: [修改了哪些文件]
**测试结果**: ✅ 全部通过 / ❌ 仍有失败

### 受影响的 Requirement
| Requirement | Scenario | 修复前状态 | 修复后状态 |
|-------------|----------|-----------|-----------|
```
