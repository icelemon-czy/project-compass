---
name: fix-bug
description: "Unified bug-fix entry: triage root cause (code / test / spec) then fix with spec-first discipline. Use when: bug, 有bug, 行为不对, unexpected behavior, fix issue, 修bug, 不符合预期, something broken, 测试失败, test failed, review 打回, review failed, 虚假通过, false pass"
argument-hint: "Describe the bug, failing test, or review feedback (e.g., 'review 打回：登录用例没覆盖空密码', '导出的 CSV 缺少 header')"
---

# Fix Bug — 统一修复入口（含分诊）

任何"不对劲"都走这个 Skill：测试红灯、review 打回、线上行为异常、虚假通过。
Skill 内部**自动分诊**，分辨是 **代码 Bug / 测试 Bug / Spec 歧义** 中的哪一种，再按对应路径修复。

> **核心纪律**：绝不先改代码。先定位"正确行为"（spec），再确认"怎么验证"（test），最后才动手修（code）。

## 覆盖场景

| 触发场景 | 所处变更状态 | 修完后回到 |
|:---------|:------------|:-----------|
| `/review-tests` 红灯 / review 打回 | `pending-review` → `implementing` | `pending-review` |
| 开发中测试突然挂了 | `implementing` | 继续 `implementing` |
| 已归档功能出现 bug（原 `/spec-fix` 用例） | `archived` | 新建 fix 变更 |
| Reviewer 发现"虚假通过"（测试绿但行为错） | `pending-review` → `implementing` | `pending-review` |

## Prerequisites

- `.ai/` 目录已存在且有 L1 + L3 + L5 结构
- 用户描述了具体的 bug / 失败的测试 / review 反馈

## Procedure

### Step 0: 场景识别（自动）

根据用户输入和上下文自动判断所处场景：

1. `ls .ai/L3-specs/changes/` — 是否有 `pending-review` 或 `implementing` 状态的变更涉及相关功能？
   - 有 → 这是 "开发中修复" 或 "review 打回"，记下变更名
   - 无 → 这是 "已归档功能 bug"，稍后需要新建 fix 变更
2. 记录"当前变更上下文"供后续步骤使用

### Step 1: 定位相关 spec

1. 读取 `.ai/L1-codebase-map/overview.md` — 匹配涉及的功能
2. 读取对应的 `features/[name]/README.md` — 理解数据流和相关代码
3. 读取 `.ai/L3-specs/specs/` 下对应能力域的 `spec.md` — 找到相关 Requirement + Scenario
4. 若 Step 0 识别到进行中的变更 → 同时读取该变更的 delta spec

### Step 2: 跑测试 + 分诊（关键步骤）

**先跑一次完整测试**，拿到失败输出（或确认全绿但行为仍错）。

对照 **测试 assertion ↔ Spec WHEN/THEN ↔ 实际行为**，三方比对判断根因：

| # | 情况 | 判据 | 根因分类 | 处理路径 |
|:--|:-----|:-----|:---------|:---------|
| A | 测试红 + assertion 与 spec THEN 一致 | 测试正确，代码没实现对 | **代码 Bug** | → Step 3A |
| B | 测试红 + assertion 与 spec THEN 不一致 | 测试写错了（断言写反、mock 错、数据错） | **测试 Bug** | → Step 3B |
| C | 测试绿但行为错 / 覆盖不到 | 测试只过了 happy path，缺 edge case；或 assert 太弱 | **虚假通过** | → Step 3B（补/改测试让它红，再 Step 3A） |
| D | Spec 本身模糊，代码/测试理解不一致 | 对同一 WHEN 有两种 THEN 解读 | **Spec 歧义** | → Step 3C |
| E | Spec 完全没覆盖这个行为 | 功能已存在但 spec 找不到对应 Requirement | **Spec 缺失** | → Step 3C |

**把分诊结论明确告知用户**：

```
## 分诊结论
根因类型: [A/B/C/D/E]
证据: [具体的 spec 条款 / 测试代码片段 / 失败输出]
下一步: [对应的 Step 3X]
```

### Step 3A: 代码 Bug 路径

1. 读取 `.ai/L2-rules/global.md` + 相关模块规则
2. 定位 bug 代码（L1 feature 文档中有位置）
3. 修复代码
4. 跑测试，确认由红转绿
5. 跳到 Step 4

### Step 3B: 测试 Bug / 虚假通过路径

1. 读取 `.ai/L2-rules/testing.md`
2. 对照 spec 的 WHEN/THEN 重写 / 加强测试：
   - 断言写反 → 修正断言
   - Mock 错 → 修正 mock，最好换成更真实的 fixture
   - 虚假通过 → 补 edge case / error path，让测试能真正暴露问题
3. 跑测试，**确认此时测试是红的**（证明它有辨别能力）
4. 如果是虚假通过导致代码也有问题 → 继续 Step 3A 修代码
5. 跳到 Step 4

### Step 3C: Spec 歧义 / 缺失路径

1. 在 `.ai/L3-specs/changes/` 下创建或复用 fix 变更（如 `fix-empty-password-validation`）
2. 写 `proposal.md`（Why: bug 描述；What: spec 修正）
3. 写 delta spec：
   - 缺失 → `## ADDED Requirements`
   - 歧义 → `## MODIFIED Requirements`，用明确的 WHEN/THEN 消除歧义
4. **展示 delta spec 给用户确认** — 这是一次额外的人工门槛，因为 spec 变更是业务决策
5. 确认后 → 按新 spec 继续走 Step 3B（改测试）→ Step 3A（改代码）

### Step 4: 更新追溯 & 状态回流

1. 更新 `.ai/L5-validation/traceability/<domain>.md` — 该 Scenario 改为 ✅ verified
2. 根据 Step 0 识别的场景，回写变更状态：

| Step 0 场景 | proposal.md 状态 |
|:-----------|:-----------------|
| Review 打回 | `implementing` → 修完 → `pending-review` |
| 虚假通过 | `pending-review` → `implementing` → 修完 → `pending-review` |
| 开发中挂了 | 保持 `implementing` |
| 已归档功能 bug | 新建 fix 变更，状态 `pending-review` |

3. 更新 `.ai/L4-session/active-session.md`

### Step 5: 输出报告

```
## Bug 修复完成

**触发场景**: [review 打回 / 开发中测试挂 / 已归档 bug / 虚假通过]
**根因分类**: [A 代码 Bug / B 测试 Bug / C 虚假通过 / D Spec 歧义 / E Spec 缺失]
**根因描述**: [具体原因]

**变更内容**:
- Spec: [有/无变更，如有列出 delta]
- 测试: [新增 N / 修改 N]
- 代码: [修改的文件]

**测试结果**: ✅ 全部通过 / ❌ 仍有失败
**变更状态**: [变更名] → [新状态]

### 受影响的 Requirement
| Requirement | Scenario | 修复前 | 修复后 |
|-------------|----------|--------|--------|
```

## 反模式（禁止）

- ❌ 没跑测试就开始改代码
- ❌ 跳过分诊直接改代码（"看起来像代码问题"）
- ❌ 虚假通过场景下只加日志不改测试（测试依旧过不了新 assertion）
- ❌ Spec 歧义场景下不改 spec 就直接改代码（下次又会被人踩）
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
