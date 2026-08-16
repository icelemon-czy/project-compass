---
name: brainstorm
description: "通过对话澄清尚未定型的 idea，结合现有 codebase facts 比较 alternatives 并收敛 design direction。Use when the user asks to brainstorm, explore options, shape a vague feature or project, or make a design decision before implementation; not for clear implementation requests, bug fixes, or factual codebase questions."
---

# Brainstorm

把尚未定型的 idea 收敛为用户能够判断的 design direction。先理解现状，再讨论未来；默认只对话，不写 code、plan 或 commit。

## Boundary

- 用户已经明确目标、behavior 和约束时，直接开始 implementation，不强制 brainstorm。
- 用户只询问现有 codebase 事实时，只读回答，不展开未来 design。
- 只有真正影响 scope、behavior、compatibility、cost 或 risk 的 choice 才交给用户。

## Flow

### 1. 建立 current-state facts

对已有项目，读根 README、`doc/` 里相关 design，以及与 idea 直接相关的最小源码：

- 能从仓库确认的事实不要询问用户。
- 区分 confirmed fact、reasonable inference 和 product choice。

没有现有代码时，从用户目标、约束和 success criteria 开始，不虚构 architecture。

### 2. 定义 problem

先用简短 big picture 重述：要解决的 user problem、已确认的 scope 和 constraint、仍会改变 design 的 unknown、可观察的 success criteria。

如果 idea 包含多个可独立交付的 subsystem，先拆分边界与顺序，只对第一个可决策 scope 继续 brainstorm。

### 3. 澄清 material choice

- 每轮最多询问一个最关键的 product question。
- 优先给出 2–3 个互斥 option，说明每个 option 会改变什么。
- 不把 naming、内部 helper、library preference 等低风险 implementation choice 交给用户。

### 4. 比较 alternatives

只有存在真实 alternatives 时才比较：先给 recommendation 和核心理由，再说明其他方案及 trade-off。不要为了凑数量制造伪方案。

### 5. 收敛 design direction

从 big picture 到 detail 展开。只覆盖当前需要的部分：goal / non-goal、user-visible behavior、system boundary、data flow 与风险。

### 6. 自然 handoff

- 默认在 conversation 中返回 design conclusion，不创建或修改任何 project file。
- 用户明确要求保存时，写入 `doc/<feature>_design.md`（已有则更新同一份）；不要另建第二套地图。
- 用户确认要创建或更新 Skill 时，按 [`skill-creator`](../skill-creator/SKILL.md) 在同一任务中继续。
- 用户确认实施时，在同一任务中直接改代码，复用已确认 decision，不要求再调用 Skill。

## Output

先返回一段 design big picture，再按需包含 Current facts、Recommendation、Alternatives、Decisions、Validation。

不要输出内部 Skill 编排或 mandatory checklist。

## Anti-patterns

- 把 brainstorm 设为所有开发任务的强制前置。
- 询问可以从 README、`doc/` 或代码找到的事实。
- 未经用户要求自动写 design doc、plan 或 commit。
- 用户只想探索时擅自开始 implementation。
