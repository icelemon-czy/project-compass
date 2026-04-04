---
name: update-ai
description: "Update existing .ai project context when code changes. Use when: refresh .ai docs, code changed need to update ai context, sync .ai with code, 更新AI上下文, 刷新.ai文档, update ai docs, new feature added update docs"
argument-hint: "Optional: what changed (e.g., 'new payment feature', 'refactored auth', 'L1 only')"
---

# Update .ai Project Context

Updates an existing `.ai/` directory to reflect code changes.

## When to Use

- Code has changed significantly (new features, refactored modules)
- New files/directories added that aren't documented
- Coding patterns evolved (need to update L2 rules)
- Periodic refresh to keep docs accurate

## Prerequisites

- `.ai/` directory already exists with L1-L4 structure
- Use `/build-ai` if no `.ai/` exists yet

## Procedure

### Step 1: Assess Current State

Read the existing `.ai/` structure to understand what's documented:

```bash
# What .ai docs exist?
find .ai -name "*.md" | sort

# Current overview
cat .ai/L1-codebase-map/overview.md

# Current feature list
ls .ai/L1-codebase-map/features/

# Last session state
cat .ai/L4-session/active-session.md
```

### Step 2: Detect Changes

Compare current code state with documented state:

```bash
# What changed recently?
git log --oneline -30

# New/deleted/renamed files since a reference point
git diff --name-status HEAD~30 -- . ':!.ai'

# Current project structure
tree -L 3 -I 'node_modules|.git|dist|__pycache__|venv|.venv|build|target|.ai'

# New directories that might be new features
# Compare with features listed in overview.md
```

Identify:
- **New features**: directories/modules not in `overview.md` feature index
- **Deleted features**: documented features whose code no longer exists
- **Changed features**: significant modifications to documented features
- **New patterns**: coding patterns that differ from `global.md`
- **Infrastructure changes**: framework/config/plugin changes

### Step 3: Plan Updates

Present findings to the user:

```
## 变更检测结果

### 需要新增
- [ ] 新功能: [name] — [reason]

### 需要更新
- [ ] 功能 [name] — [what changed]
- [ ] global.md — [what rules changed]

### 需要删除
- [ ] 功能 [name] — [code removed]

### 无需变更
- [features that are still accurate]
```

Wait for user confirmation before proceeding.

### Step 4: Execute Updates

Based on the plan, perform targeted updates:

#### 4a: New Features

For each new feature, run a mini L1 analysis:

1. Identify entry point and layers
2. Trace data flow
3. Create `features/[name]/README.md` + layer files
4. Add entry to `overview.md` feature index

#### 4b: Updated Features

For each changed feature:

1. Re-read the code (follow the entry points in the existing docs)
2. Check if layers changed (new layers, removed layers)
3. Update README.md data flow and change impact table
4. Update layer files as needed
5. Check if module-map.md dependencies changed

#### 4c: Deleted Features

1. Remove `features/[name]/` directory
2. Remove entry from `overview.md` feature index
3. Update `module-map.md` (remove module, update dependency rules)
4. Check `key-files.md` for references to deleted feature

#### 4d: L2 Rules Update

If coding patterns changed:

```bash
# Check for new patterns
grep -rn "^export\|module\.exports\|__all__" --include='*.ts' --include='*.py' --include='*.js' | head -80

# Check for new error patterns
grep -rn "extends Error\|class.*Error" --include='*.ts' --include='*.py' | head -20

# Check for new lint rules
cat .eslintrc* tsconfig.json pyproject.toml 2>/dev/null
```

Update `global.md` and `templates.md` accordingly.

#### 4e: Cross-cutting Updates

After individual updates, sync:

1. **overview.md** — Ensure feature index matches reality
2. **module-map.md** — Update dependency rules and change impact table
3. **key-files.md** — Update task recipes if workflows changed
4. **infrastructure/README.md** — Update if framework/config changed

### Step 5: Update Session

Update `.ai/L4-session/active-session.md`:

```markdown
- **时间**: [now]
- **对话主题**: .ai 文档更新
- **已完成**: [list of updates made]
- **下一步**: [any remaining updates or verification needed]
```

### Step 6: Verify

- [ ] `overview.md` feature index matches actual code
- [ ] No stale feature docs pointing to nonexistent code
- [ ] `module-map.md` dependency rules still accurate
- [ ] `global.md` rules match current coding patterns
- [ ] Every documented feature's entry file still exists

## Tips

- **Small updates** (1-2 features changed): Do the full procedure inline
- **Large updates** (major refactor): Consider rebuilding with `/build-ai`
- **Unsure what changed**: Use `git log --stat` to find high-impact commits
- **Regular cadence**: Run update after every significant PR merge
