---
name: build-ai
description: "Build .ai project context for AI-assisted development from scratch. Use when: init .ai, setup ai context, new project setup, 构建AI上下文, 初始化.ai, build ai docs, create .ai directory, scaffold ai context, 新项目配置"
argument-hint: "Optional: target project path or specific layers (e.g., 'L1 only', 'skip L3')"
---

# Build .ai Project Context

为项目搭建完整的 `.ai/` AI 上下文目录。

> **依赖的 Builder Prompts**：本 Skill 的 L1/L2 生成步骤依赖仓库根目录的 `builders/*.md`。运行前请确认 `builders/` 的 commit 与本 Skill 同一仓库同一版本。如果 builders 被单独更新过，可能与本 Skill 的接口不兼容。期望导航：
> - L1 builder：`builders/build-l1.md`（或此目录下等效文件）
> - L2 builder：`builders/build-l2.md`
> - 查找不到时：告知用户并停止，不要自己编造 builder 逻辑。

## Five-Layer Architecture

| Layer | Purpose | Key Output |
|-------|---------|------------|
| L1 Codebase Map | Project navigation for AI | overview.md, feature docs, architecture.md, module-map, key-files |
| L2 Coding Rules | Coding standards from actual code | global.md, templates.md, module rules |
| L3 Spec-Driven Changes | Requirements specs & change management | system.md, capability specs, change-management.md |
| L4 Session State | AI working memory | active-session.md |
| L5 Validation | Spec-to-code traceability & verification | traceability matrices, validation reports |

## Prerequisites

- Target project has source code to analyze
- Know the project root path

## Procedure

Three steps. Execute in order.

---

### Step 1: Copy project-compass to `.ai/`

将 project-compass 模板复制到目标项目下：

```bash
cp -r /path/to/project-compass /path/to/your-project/.ai/
```

复制后，目录结构、模板文件、`change-management.md`、`doc-sync.md`、`L4-session/active-session.md` 等已就位。

> 如果 `.ai/` 已存在且用户想重建，先确认是否备份。

---

### Step 2: Build L1 → L2 → L3 → L5

选择与用户 AI 工具匹配的 builder（`builders/claude/` 或 `builders/cline/`），**按顺序**执行 prompt。

每个 prompt 是独立的完整指令。复制到 AI 新对话中，填入 `[占位符]`，让 AI 执行。

| Order | Builder Prompt | What it builds | External input |
|-------|---------------|----------------|----------------|
| 1 | `prompt-L1a.md` | overview.md + feature list + `_handoff.md` | Optional: supplementary context file |
| 2 | `prompt-L1b.md` | features/ docs + architecture.md + module-map.md + key-files.md | Reads `_handoff.md` from step 1 |
| 3 | `prompt-L2.md` | global.md + templates.md + module rules | Reads L1 output |
| 4 | `prompt-L3.md` | system.md (TOR) + capability specs (HLR) | Optional: PRD / product spec / API docs |
| 5 | `prompt-L5.md` | traceability matrices + validation report | Reads L1 + L3 output |

#### Builder variants

| Tool | Directory | Subagent behavior |
|------|-----------|-------------------|
| Claude Code | `builders/claude/` | Subagent can read+write, creates files directly |
| GitHub Copilot | `builders/copilot/` | No subagents, sequential analysis, auto-continues |
| Cline (sub-agent) | `builders/cline/sub-agent/` | Subagent read-only, outputs text for main agent to write |
| Cline (single-agent) | `builders/cline/single-agent/` | No subagents, pauses for human review after each item |

#### Builder prompt details (reference)

For the detailed logic inside each prompt, see these reference docs:

- [L1 discovery (Phase 1-3)](./references/l1-discovery.md) — scan project, identify features, write overview
- [L1 deep analysis (Phase 4-5)](./references/l1-deep-analysis.md) — feature deep dive, module-map, key-files, architecture
- [L2 coding rules (Phase 6)](./references/l2-rules.md) — extract patterns from actual code
- [L3 spec bootstrap (Phase 7)](./references/l3-specs.md) — build initial specs from code + optional user docs

> These references are for understanding the build logic. Users interact with the builder prompts directly, not these files.

---

### Step 3: Deploy entrypoint

将对应的 entrypoint 模板复制到项目根目录：

| AI Tool | Source | Target |
|---------|--------|--------|
| Claude Code | `.ai/entrypoints/claude.md` | Project root `CLAUDE.md` (if `CLAUDE.md` already exists, append content) |
| Cline | `.ai/entrypoints/clinerules.md` | Project root `.clinerules` |

---

### Verify

All steps done. Run through this checklist:

- [ ] `overview.md` is under 60 lines, only index entries (no details)
- [ ] Each feature has README.md with a layer navigation table
- [ ] `architecture.md` exists and covers request lifecycle / startup sequence
- [ ] `global.md` rules are extracted from actual code patterns, not invented
- [ ] `testing.md` exists with project-specific test conventions
- [ ] Every line passes: "Can AI derive this from code?" If yes → delete it
- [ ] `specs/system.md` has System Boundary and Cross-Cutting Requirements
- [ ] Each capability domain has `specs/<domain>/spec.md` with Requirement + Scenario
- [ ] `L3-specs/change-management.md` exists
- [ ] `doc-sync.md` exists at `.ai/` root
- [ ] `L5-validation/validation-rules.md` exists
- [ ] Each spec domain has a traceability file in `L5-validation/traceability/`
- [ ] Entrypoint file created and points to correct `.ai/` paths
