---
name: skill-creator
description: "创建、更新或精简当前项目的 Skill，明确 trigger boundary、Workflow 和必要 resources，并完成结构与行为验证。Use when the user asks to add, author, revise, rename, merge, split, or validate a project-local Skill; not for installing third-party Skills or ordinary product code changes."
---

# Skill Creator

把用户能够独立表达的目标转化为 concise、可触发、可验证的 project-local Skill。优先更新或合并已有能力；只有现有 Skill 无法自然承载目标时才新增。

## Boundary

- 维护 Compass 源码仓时，canonical Skill root 是 `compass/skills/`。
- 已把 Compass 装进目标项目后，编辑各已选平台的 project-level Skill directory（例如 `.cursor/skills/`、`.claude/skills/`）。不要写回已删除的 `.compass/skills/` staging。
- 默认只修改 project-local Skill。不要写入 global Skill directory、安装 third-party Skill 或发布 package，除非用户明确要求。
- Skill idea 尚未形成明确用户目标时，先按 [`brainstorm`](../brainstorm/SKILL.md) 收敛，再在同一任务中继续。
- Commit、push 和 release 只有用户明确要求时才执行。

## Flow

### 1. 确认 source of truth

读取最小相关材料：根 `AGENTS.md` / `CLAUDE.md`、README、`doc/`、canonical Skill inventory、最相近的现有 `SKILL.md`。

Source of truth 与现有 Skill 冲突时先标记 conflict，不通过复制规则掩盖漂移。

### 2. 定义 trigger contract

在修改文件前明确：用户会怎样表达这个目标、必须完成的 observable outcome、哪些相邻请求不应触发、默认只读还是允许写入、完成后是否 handoff 到其他 Skill。

### 3. 选择最小 design

1. 这是 Agent 已有的通用能力吗？是则不新增 Skill。
2. 这是现有 Skill 的内部 stage 吗？是则合并进去。
3. 这是用户可以单独请求、具有独立 input/output 的目标吗？只有此时才保留独立 Skill。

设计时：folder name 与 frontmatter `name` 一致；`description` 写清做什么、何时触发、何时不触发；body 先 big picture 和 boundary，再最小 Flow、Output 与 Anti-pattern。

### 4. 组织 resources

默认只创建 `SKILL.md`。只有重复执行且值得测试时才加 `scripts/`；详细 domain fact 才会使主体过重时才加 `references/`；最终输出需要直接复用 artifact 时才加 `assets/`。

不要创建 Skill-local README、changelog 或空目录。

### 5. 创建或更新

- 新建时优先用环境已有的官方 initializer；不可用时创建最小合法目录和 `SKILL.md`。
- 更新时保留仍有效的用户规则，只移除已确认冗余或冲突的内容。
- 已选多个平台时，每个平台 native directory 都更新同一份 Skill，不要只改一处。

### 6. 验证

检查 `name` 与 folder 一致、frontmatter 可解析、description 含正负边界、相对引用能解析、`git diff --check` 通过。环境有官方 validator 时先跑。

### 7. Forward-test

只有 routing、write behavior 或复杂 Workflow 值得独立验证，并且平台允许 Subagent 时才 forward-test。简单 rename 或纯措辞调整不强制。

## Output

报告：创建或更新的 Skill 与 trigger boundary、resource、实际 validation、未解决的 conflict。不要把 initializer 或 checklist 转交给用户执行。

## Anti-patterns

- 为同一用户目标创建多个相邻 Skill。
- 为内部 Workflow stage 单独创建用户入口。
- 用长篇通用知识填充 Skill，而没有 project-specific procedure。
- 未经用户要求修改 global environment、commit、push 或 publish。
