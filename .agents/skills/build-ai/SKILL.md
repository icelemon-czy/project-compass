---
name: build-ai
description: "Install Compass Harness and build project context for AI-assisted development. Use when: init compass harness, setup ai context, new project setup, 构建AI上下文, 初始化compass harness, build ai docs, scaffold ai context, 新项目配置"
---

# Build Compass Harness Project Context

在目标项目安装根 `AGENTS.md` 项目规则，以及 `.compass-harness/` 中的上下文、Skills、Subagent 角色模板和配置，再生成所选平台需要的发现适配。

> **模板依赖**：使用 `templates/compass-harness/manifest.yaml` 声明的模板与 `.agents/skills/` 原始 Skill。找不到任何必需源文件时告知用户并停止，不要自行编造另一套目录或格式。

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

Four steps. Execute in order.

---

### Step 1: Install the canonical `.compass-harness/` tree

从 Compass Harness 模板仓库复制权威内容。项目规则直接使用根 `AGENTS.md`，不设置 global/project 分层：

```bash
mkdir -p /path/to/your-project/.compass-harness/context
mkdir -p /path/to/your-project/.compass-harness/skills
mkdir -p /path/to/your-project/.compass-harness/subagents

cp /path/to/compass-harness/templates/compass-harness/installed-manifest.yaml.template /path/to/your-project/.compass-harness/manifest.yaml
cp /path/to/compass-harness/templates/compass-harness/config.yaml /path/to/your-project/.compass-harness/config.yaml
cp /path/to/compass-harness/templates/compass-harness/AGENTS.md /path/to/your-project/AGENTS.md
cp -R /path/to/compass-harness/templates/compass-harness/context/. /path/to/your-project/.compass-harness/context/
cp -R /path/to/compass-harness/.agents/skills/. /path/to/your-project/.compass-harness/skills/
cp -R /path/to/compass-harness/templates/compass-harness/subagents/. /path/to/your-project/.compass-harness/subagents/
```

渲染根 `AGENTS.md`、`.compass-harness/manifest.yaml` 和 `.compass-harness/config.yaml` 中的项目占位符。复制后，L1–L5 结构和必要模板已就位；不要强制一次性填满所有层。

> 如果 `.compass-harness/` 已存在且用户想重建，先确认备份或增量合并，不得覆盖项目自定义内容。

---

### Step 2: Build L1 → L2 → L3 → L5

读取目标项目的源码、配置、测试和用户提供的需求文档，再按以下顺序填写模板：

| Order | Layer | What to establish |
|-------|-------|-------------------|
| 1 | L1 | 最小功能索引、入口、数据流和模块依赖 |
| 2 | L2 | 从实际代码/配置中确认的编码和测试规则 |
| 3 | L3 | 已知系统需求、能力 Spec 和变更状态机 |
| 4 | L4 | 只在需要恢复中断工作时写会话状态 |
| 5 | L5 | 只记录已检查的 Spec–Code–Test 证据 |

对无法从代码或用户输入确认的内容标记为待确认，不要猜测。

---

### Step 3: Generate platform discovery adapters

根据用户选择的工具，从 `templates/compass-harness/adapters/` 读取对应模板：

| AI Tool | Template directory | Project target |
|---------|--------------------|----------------|
| Codex | `AGENTS.md` | project-root `AGENTS.md` |
| Claude Code | `adapters/claude-code/` | `CLAUDE.md` |
| OpenCode | `AGENTS.md` + `adapters/opencode/` | project-root `AGENTS.md` + optional `opencode.json` |

`AGENTS.md` 是 Codex/OpenCode 直接读取的项目规则本体，并导航到 `.compass-harness/context/` 和 `.compass-harness/skills/`。Claude Code 的 `CLAUDE.md` 只引用 `AGENTS.md`，不复制规则正文。

按所选平台生成 Skill 发现镜像：Codex/OpenCode 使用 `.agents/skills/`，Claude Code 使用 `.claude/skills/`。这些目录由 `.compass-harness/skills/` 生成，不允许手工维护。如果项目已有入口文件，先合并用户规则，不要覆盖。

不要自动生成真实 Subagent 配置。`.compass-harness/subagents/` 只保存通用角色定义和示例；仅在用户明确选择角色后，才生成平台私有 agents 文件。

---

### Step 4: Verify

All steps done. Run through this checklist. **每条必须实际执行验证命令，不允许"看了一下没问题"。**

```bash
# 1. 权威安装树
test -f .compass-harness/manifest.yaml || echo "❌ manifest.yaml 缺失"
test -f .compass-harness/config.yaml || echo "❌ config.yaml 缺失"
test -f AGENTS.md || echo "❌ AGENTS.md 项目规则缺失"
test "$(find .compass-harness/skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')" = "13" || echo "❌ Skill 数量不是 13"

# 2. overview.md 长度检查
wc -l .compass-harness/context/L1-codebase-map/overview.md  # 必须 ≤ 60 行

# 3. feature 文档完整性
for f in .compass-harness/context/L1-codebase-map/features/*/README.md; do
  grep -q "层.*表\|layer" "$f" || echo "❌ $f 缺少层导航表"
done

# 4. 关键文件存在性（每个都 test -f）
test -f .compass-harness/context/L1-codebase-map/architecture.md || echo "❌ architecture.md 缺失"
test -f .compass-harness/context/L2-rules/global.md || echo "❌ global.md 缺失"
test -f .compass-harness/context/L2-rules/testing.md || echo "❌ testing.md 缺失"
test -f .compass-harness/context/L3-specs/specs/system.md || echo "❌ system.md 缺失"
test -f .compass-harness/context/L3-specs/change-management.md || echo "❌ change-management.md 缺失"
test -f .compass-harness/context/doc-sync.md || echo "❌ doc-sync.md 缺失"
test -f .compass-harness/context/L5-validation/validation-rules.md || echo "❌ validation-rules.md 缺失"

# 5. 至少 1 个能力域 spec
ls .compass-harness/context/L3-specs/specs/*/spec.md 2>/dev/null | wc -l  # 必须 ≥ 1

# 6. 每个能力域有追溯文件
for d in .compass-harness/context/L3-specs/specs/*/; do
  domain=$(basename "$d")
  [[ "$domain" == "_capability-template" ]] && continue
  test -f ".compass-harness/context/L5-validation/traceability/${domain}.md" || echo "❌ 追溯文件缺失: $domain"
done

# 7. global.md 规则非空
wc -l .compass-harness/context/L2-rules/global.md  # 必须 > 5 行（排除空模板）

# 8. "Can AI derive this from code?" 冗余检查
# 对 overview.md 中每个条目，检查是否仅是文件路径列表（如果是 → 删除，AI 可以 ls 获取）
```

以上检查有任何 ❌ → **修复后再宣告完成**，不允许带着缺失项交付。
