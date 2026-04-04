---
name: build-ai
description: "Build .ai project context for AI-assisted development from scratch. Use when: init .ai, setup ai context, new project setup, 构建AI上下文, 初始化.ai, build ai docs, create .ai directory, scaffold ai context, 新项目配置"
argument-hint: "Optional: target project path or specific phases (e.g., 'L1 only', 'skip L2')"
---

# Build .ai Project Context

Creates a complete `.ai/` context directory for AI-assisted development.

## Four-Layer Architecture

| Layer | Purpose | Key Output |
|-------|---------|------------|
| L1 Codebase Map | Project navigation for AI | overview.md, feature docs, module-map, key-files |
| L2 Coding Rules | Coding standards from actual code | global.md, templates.md, module rules |
| L3 Task Management | Task board and workflow | board.md, task template, decision log |
| L4 Session State | AI working memory | active-session.md |

## Prerequisites

- Target project has source code to analyze
- No existing `.ai/` directory (or user wants to rebuild)

## Procedure

Follow phases in order. Each builds on the previous.

### Phase 0: Scaffold

Create the `.ai/` directory structure with template files.
Read and follow [scaffold instructions](./references/scaffold.md).

→ Output: directory tree + reference templates + initialized files

### Phase 1-3: L1 Discovery

Scan the project, identify features, write the overview index.
Read and follow [L1 discovery instructions](./references/l1-discovery.md).

→ Output: `overview.md` + feature list + `_handoff.md`

### Phase 4-5: L1 Deep Analysis

Analyze each feature in depth using subagents, build module map.
Read and follow [L1 deep analysis instructions](./references/l1-deep-analysis.md).

→ Output: `features/*/` docs + `module-map.md` + `key-files.md`

### Phase 6: L2 Coding Rules

Extract coding patterns from the actual codebase.
Read and follow [L2 coding rules instructions](./references/l2-rules.md).

→ Output: `global.md` + `templates.md` + per-module rule files

### Phase 7: Entrypoint

Create the AI navigation entrypoint. Read [entrypoint template](./references/entrypoint.md).

Ask the user which tool(s) they use, then create the appropriate file:

| Tool | File | Location |
|------|------|----------|
| Claude Code | `CLAUDE.md` | Project root |
| Cline | `.clinerules` | Project root |
| Cursor | `.cursorrules` | Project root |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/` |

### Phase 8: Verify

Run through this checklist:

- [ ] `overview.md` is under 60 lines, only index entries (no details)
- [ ] Each feature has README.md with a layer navigation table
- [ ] `global.md` rules are extracted from actual code patterns, not invented
- [ ] Every line passes: "Can AI derive this from code?" If yes → delete it
- [ ] Entrypoint file created and points to correct `.ai/` paths
- [ ] Clean up: delete `_handoff.md` (temporary file)
