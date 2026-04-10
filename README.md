# Project Compass

> **[中文版 / Chinese Version](README.zh.md)**

> Universal AI context template — works with any language, any framework, any scale.
> Copy this template to your project root (rename to `.ai/`), fill in the `[fill in]` placeholders.

## Core Philosophy

AI context windows are limited. For any codebase of meaningful size, you can't fit everything into context.
You need a **layered, on-demand loading** context management system so AI can, in every conversation:

1. **Pinpoint** — Know which files to look at for a given task (feature → code mapping)
2. **Follow rules** — Know how to write and what not to do (rules + anti-patterns)
3. **Understand goals** — Know the current objective (task layer)
4. **Continue progress** — Know where the last step left off and what to do next (session layer)

### Design Principles

- **Only write what AI can't infer** — Directory structure, tech stack, module responsibilities — AI can figure these out via `tree` + `grep`, not worth documenting
- **Task-oriented indexing** — Documentation should help AI locate "which code to look at", not describe "what the code looks like"
- **Relationships > Descriptions** — File coupling and change propagation are 100x more useful than file listings
- **Progressive disclosure** — AI loads only the minimum context needed for the current task, never filling the entire window at once
- **Verifiable > Abstract** — "Domain layer must not import Infrastructure layer" is more useful than "uses Clean Architecture"

### L1 Navigation Model

AI reads **only `overview.md`** (< 60 lines) per conversation, then selects a path based on task type:

```
Receive task
 ├─ Matches a specific feature → features/[name]/README.md → drill into layer files as needed
 ├─ Common dev tasks → key-files.md (task recipes)
 ├─ Changes span multiple modules → module-map.md (change propagation table)
 └─ Modifying infrastructure → infrastructure/README.md
```

Paths are composable — e.g., cross-feature changes load both feature README + module-map.
Every target file has **bidirectional links** (source / related files) to prevent AI from getting lost.

## Four-Layer Architecture

```
.ai/
├── L1-codebase-map/          ← Code navigation layer (stable, low-frequency updates)
│   ├── overview.md           ← Single entry point (< 60 lines, feature index + routing decision tree)
│   ├── module-map.md         ← Module contracts & coupling map (loaded for cross-module changes)
│   ├── key-files.md          ← Common task recipes & investigation starting points
│   ├── architecture.md       ← Runtime architecture (deployment topology, request lifecycle, middleware pipeline)
│   ├── infrastructure/       ← Infrastructure docs (framework/middleware/utilities, peer to features)
│   │   ├── _infrastructure-template/ ← Infrastructure component doc template
│   │   │   └── README.md         ← Component overview + layer nav + format reference
│   │   └── [component-name]/     ← One folder per infrastructure component
│   │       ├── README.md         ← Component overview (must read)
│   │       └── [layer].md        ← Layer files (loaded on demand)
│   └── features/             ← Per-feature detailed context (progressive disclosure)
│       ├── _feature-template/   ← Feature doc template (copy to create new feature)
│       │   └── README.md        ← Overview + layered nav + data flow + layer file format reference
│       └── [feature-name]/      ← One folder per feature
│           ├── README.md        ← Feature overview (must read)
│           └── [layer].md       ← Layer files (dynamically named by project concepts, loaded on demand)
│
├── L2-rules/                 ← Rules layer (stable, sharded by domain)
│   ├── global.md             ← Global rules (concrete executable rules + anti-pattern checklist)
│   ├── templates.md          ← Code templates for new files (loaded when creating files)
│   ├── _module-template.md   ← Module rules template (contracts + pitfalls + boundaries)
│   └── [module-name].md      ← Created per actual project module
│
├── L3-tasks/                 ← Task layer (medium-frequency changes)
│   ├── board.md              ← Task board (status index for all tasks)
│   ├── _task-template.md     ← Task template (copy to create new task)
│   ├── TASK-xxx.md           ← Task details (input → plan → test cases)
│   ├── decision-log.md       ← Architecture Decision Records (ADR)
│   └── review/               ← Human review area (AI output goes here first, merged after approval)
│
├── L4-session/               ← Session layer (high-frequency changes, maintained per conversation)
│   └── active-session.md     ← Current session state (test status + next actions)
│
├── builders/                  ← Auto-generation prompt collection (organized by tool)
│   ├── cline/               ← Cline-specific (subagent read-only, outputs text for main agent to write)
│   │   ├── prompt-L1a.md     ← Generate L1 docs Phase 1-3 (scan + overview; infra-first discovery: 2a infra → 2b features → 2c patterns)
│   │   ├── prompt-L1b.md     ← Generate L1 docs Phase 4-5 (4a: infra docs → 4b: subagent feature analysis)
│   │   ├── prompt-L2.md      ← Generate L2 coding rules
│   │   ├── prompt-L3.md      ← Create & plan L3 tasks
│   │   └── single-agent/     ← Single-agent variant: no subagents, pause for human review after each item
│   │       ├── prompt-L1a.md
│   │       ├── prompt-L1b.md ← Core difference: main agent analyzes each feature/infra one at a time
│   │       ├── prompt-L2.md  ← Pauses for review after each module
│   │       └── prompt-L3.md
│   └── claude/              ← Claude Code-specific (subagent has read+write, creates files directly)
│       ├── prompt-L1a.md     ← Generate L1 docs Phase 1-3 (scan + overview; infra-first discovery: 2a infra → 2b features → 2c patterns)
│       ├── prompt-L1b.md     ← Generate L1 docs Phase 4-5 (4a: infra docs → 4b: subagent feature analysis)
│       ├── prompt-L2.md
│       └── prompt-L3.md
├── entrypoints/              ← AI tool entry point templates
│   ├── clinerules.md         ← Cline entry template (→ .clinerules)
│   ├── claude.md             ← Claude Code entry template (→ CLAUDE.md)
│   ├── cursorrules.md        ← Cursor entry template (→ .cursorrules)
│   └── copilot-instructions.md ← GitHub Copilot entry template
└── README.md                 ← This file
```

## L1 vs L2 — What's the Difference?

> **In one sentence: L1 = Map (where things are, how to navigate), L2 = Rules (how to write, what's allowed)**

An analogy:
- **L1** = City map → "The hospital is here, the school is there, take this road from home to hospital"
- **L2** = Traffic rules → "Drive on the right, red means stop, speed limit 60"

### Comparison

| Question | L1 answers | L2 answers |
|----------|-----------|-----------|
| "Where's the login code?" | ✅ `src/auth/` directory, entry at `routes/auth.ts` | — |
| "What breaks if I change User table?" | ✅ Must also update JWTPayload type | — |
| "What's the full request data flow?" | ✅ route → controller → service → repo → response | — |
| "What naming convention to use?" | — | ✅ Files kebab-case, functions camelCase |
| "What should a new Service file look like?" | — | ✅ Standard code template available |
| "How to handle errors?" | — | ✅ Service layer throws AppError, Controller doesn't try-catch |
| "Which module APIs are stable?" | — | ✅ `authenticate()` is STABLE, `validatePassword()` is INTERNAL |
| "Any gotchas in this feature?" | ✅ Async callback has race condition | — |

### File Mapping

```
L1 features/user-auth/              L2 rules/
├── README.md    → Data flow + change impact    ├── global.md     → Global coding standards
├── routes.md    → Endpoints, param structure    ├── templates.md  → Code templates for new files
├── services.md  → Business rules, state flow   └── auth.md       → auth module contracts + constraints
└── models.md    → Table schema, queries, migrations
     ↑                                              ↑
     Map: where code lives, how data flows          Rules: how to write code, what contracts exist
```

> Note: Layer file names (e.g., routes.md, services.md) are not fixed — they're dynamically named by subagents based on actual code structure.

### When Information Relates to Both

| Information | Goes in | Reasoning |
|-------------|---------|-----------|
| "Token refresh has race condition during login" | L1 | Related to feature data flow |
| "`authenticate()` is stable API, can't change signature" | L2 | Module contract / coding constraint |
| "Changing User model requires updating DTO" | L1 | Change impact (change A → must change B) |
| "All DB operations must use transactions" | L2 | Coding rule (how to write) |
| "Payment callback is async" | L1 | Data flow characteristic |
| "New auth methods must implement AuthStrategy interface" | L2 | Coding constraint (pattern to follow) |

## Quick Start

1. Copy this template to your project root, rename to `.ai/`
2. Fill in `.ai/L1-codebase-map/overview.md` — **the most important step**
   - Focus on: feature → code mapping table, core data flows, danger zone list
   - Or use `builders/cline/prompt-L1a.md` (Cline) or `builders/claude/prompt-L1a.md` (Claude Code) to let AI assist
   - The builder prompts follow **infrastructure-first order**: identify infra (Phase 2a) → features (Phase 2b) → patterns (Phase 2c), then document infra (Phase 4a) before running feature subagents (Phase 4b)
3. Fill in `.ai/L2-rules/global.md` — Write concrete coding rules and anti-patterns
4. Copy `.ai/L2-rules/_module-template.md`, create rule files for each project module
5. Create an entry point file in project root (`CLAUDE.md` / `.cursorrules`), pointing to `.ai/` docs
6. Each AI conversation, assemble context using the "Loading Strategy" below

## Loading Strategy

### Always Load (Prompt Preamble)
- `L1-codebase-map/overview.md` — Lightweight index (< 60 lines, feature directory + danger zones)
- `L4-session/active-session.md` — Current session state (with next actions)
- `L2-rules/global.md` — Global rules (with anti-pattern checklist)

### Load On Demand After Receiving Task (Progressive Disclosure)
- `L1-codebase-map/features/[name]/README.md` — **Loaded after matching feature from overview.md index, drill into layer files as needed**
- `L1-codebase-map/key-files.md` — For common dev tasks (adding endpoints, tables, fixing bugs)
- `L1-codebase-map/module-map.md` — For cross-module changes (check change propagation table)
- `L1-codebase-map/architecture.md` — For understanding runtime behavior, request lifecycle, or cross-layer issues
- `L2-rules/[module-name].md` — For specific module tasks (check contracts and pitfalls)
- `L2-rules/templates.md` — When creating new files (check standard code templates)
- `L3-tasks/board.md` — View global task status
- `L3-tasks/TASK-xxx.md` — Current in-progress task details

### Occasional Reference
- `L3-tasks/decision-log.md` — When asking "why was this done this way?"
- `L3-tasks/board.md` — When planning next steps (check open tasks)

## Workflow (Mode B: AI Self-Navigation)

> Recommended: Place an entry point file in project root. AI reads `.ai/` docs automatically and self-navigates throughout.

```
┌─────────────────────────────────────────────────────────┐
│  Step 0 (One-time setup)                                │
│  Copy template from entrypoints/ → project root entry   │
│  (.clinerules / CLAUDE.md / .cursorrules etc.)          │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 1-2 (Auto, every conversation)                    │
│  AI reads entry file → auto-loads:                      │
│    • overview.md      — Project feature index           │
│    • global.md        — Global coding rules             │
│    • active-session.md — Last progress + next steps     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3  User gives task                                │
│  "Fix the token refresh bug in user login"              │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 4  AI locates feature by index                    │
│  overview.md feature index → match "user auth"          │
│  → read features/user-auth/README.md                    │
│  → drill into layer files as needed                     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 5  AI reads module rules                          │
│  → read L2-rules/auth.md (contracts + constraints)      │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 6  AI manages tasks                               │
│  → check board.md / create new TASK-xxx.md              │
│  → write plan + verification questions → await human OK │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 7  AI writes code                                 │
│  Follow global.md + module rules, reference templates   │
│  Check module-map.md before cross-module changes        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 8  AI updates session state                       │
│  → update active-session.md                             │
│    • What was done, which files were involved           │
│    • Test results, specific next actions                │
└─────────────────────────────────────────────────────────┘
```

**Key point:** Human only does Step 0 (once) + Step 3 (give task). Everything else is autonomous.

## What Each Document Should Contain (Guide)

| Document | ✅ Should write | ❌ Don't write (AI can infer) |
|----------|----------------|------------------------------|
| overview.md | **Feature index table** (name + pointer), **dependency overview** (feature → infrastructure direction), danger zones, build commands | Data flow details, file listings (goes in features/[name]/) |
| module-map.md | **Dependency topology** (ASCII global layer diagram), public API list, change propagation table, dependency prohibition rules | Module responsibility descriptions, LOC stats |
| key-files.md | Common task recipes, investigation starting points, global change impacts | Feature-specific recipes (goes in features/[name]/) |
| features/[name]/ | Complete context for one feature, split by layer: README (overview + data flow + **infrastructure dependencies**), controller/service/data (layer details) | Cross-feature generic info |
| global.md | Concrete executable rules, anti-pattern checklist, error handling patterns | "Architecture pattern: Clean Architecture" (too abstract) |
| templates.md | Code templates for new files (Service, Test, etc.) | Should be extracted from actual code, not fabricated |
| Module rules | Public contracts (function signatures + stability), internal coding constraints, boundary rules, test strategy | Data flows, file lists, change impact (goes in L1) |
| board.md | Task status index (ID + title + status) | Task details (goes in TASK-xxx.md) |
| TASK-xxx.md | Task input + AI plan + test cases + execution steps | "Refactor some module" (too vague) |
| active-session.md | Specific next actions, test status, file states | "Working on some feature" (too vague) |

## Maintenance Cadence

| Document | Maintained by | Frequency |
|----------|--------------|-----------|
| L1 Code Navigation | Human + AI assist | On architecture changes |
| L2 Rules | Human | On convention changes |
| L3 Task Plans | Human + AI | Each task cycle |
| L3 Decision Log | Human + AI | After each important decision |
| L4 Session State | AI (human review) | End of each conversation |

## Integration

### Entry Point Files (Recommended — AI Self-Navigation)

Copy the corresponding template from `entrypoints/` to your project root:

| AI Tool | Template File | Placement |
|---------|--------------|-----------|
| Cline | `entrypoints/clinerules.md` | Project root `.clinerules` |
| Claude Code | `entrypoints/claude.md` | Project root `CLAUDE.md` |
| Cursor | `entrypoints/cursorrules.md` | Project root `.cursorrules` (or `.cursor/rules/`) |
| GitHub Copilot | `entrypoints/copilot-instructions.md` | `.github/copilot-instructions.md` |

Entry files contain complete navigation instructions. AI automatically reads `.ai/` docs and navigates on demand.
See "Workflow (Mode B)" above.
