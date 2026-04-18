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

> **环检测（必要）**：进入本步前先检查当前变更 proposal.md 的 `depth` 字段。
>
> - 如果当前 `depth >= 2`：不得再创建嵌套 fix 变更。定位到最上游的 parent-change，请用户直接处理根问题。
> - 创建新 fix 变更时，必须写 `parent-change: <当前变更名>` 和 `depth: <父 depth + 1>`。

1. 在 `.ai/L3-specs/changes/` 下创建或复用 fix 变更（如 `fix-empty-password-validation`）
2. 写 `proposal.md`（Why: bug 描述；What: spec 修正；parent-change/depth 必填）
3. 写 delta spec：
   - 缺失 → `## ADDED Requirements`
   - 歧义 → `## MODIFIED Requirements`，用明确的 WHEN/THEN 消除歧义
4. **展示 delta spec 给用户确认** — 这是一次额外的轻确认（不是完整的门槛 1，但因为 spec 变更是业务决策，必须人确认）
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
