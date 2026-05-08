# Project Compass Roadmap

> Updated: 2026-05-08
> Positioning: evolve Project Compass from an AI context template into an executable AI workflow harness.

## North Star

Project Compass already has the right building blocks: five layers of context, spec-driven workflows, validation artifacts, and reusable skills. The next stage is to make those pieces more executable, observable, and scalable.

The long-term goal is not "more Markdown". The goal is a lightweight harness that can:

- scaffold AI context for real projects
- route work to the right rules, specs, and validation surfaces
- make AI workflows executable instead of purely prompt-driven
- support multi-agent collaboration without losing traceability
- measure quality over time instead of relying on intuition

## Level Definitions

- **Level 1 — Foundation**: must-have capabilities for making Compass easier to run, validate, and adopt.
- **Level 2 — Scale**: capabilities that expand Compass across agents, tools, and longer-running workflows.
- **Level 3 — Platform**: strategic capabilities that make Compass team-grade and defensible as infrastructure.

## Level 1 — Foundation

### 1. Compass Harness CLI

**Why now**: today many Compass rules live in docs and depend on the agent to follow them correctly.

**What to build**:
- `compass doctor` to validate structure, missing files, and public-interface drift
- `compass validate` for change/spec/task/session state checks
- `compass generate` for entrypoints and tool-specific skill scaffolding
- deterministic checks for proposal/task/status transitions

**Outcome**: Compass becomes runnable infrastructure instead of a prompt bundle.

### 2. Workflow Macros

**Why now**: the current skills are strong but still relatively atomic.

**What to build**:
- reusable macro flows such as `hotfix`, `feature`, `qa-sweep`, and `release-readiness`
- persisted state handoff between `new-change`, `fix-bug`, `review-tests`, `archive-change`, and `git-commit`
- a small contract for preconditions, checkpoints, and failure recovery

**Outcome**: users choose a workflow shape, not a manual sequence of chat commands.

### 3. Brownfield Onboarding Analyzer

**Why now**: initial Compass adoption for existing repositories is still high-friction.

**What to build**:
- scan existing code, tests, lint config, and git history
- draft L1/L2/L3/L5 artifacts with confidence labels
- highlight low-confidence sections that require human review
- preserve migrated legacy docs instead of overwriting them

**Outcome**: Compass becomes materially easier to adopt on real brownfield codebases.

## Level 2 — Scale

### 4. Multi-Agent Worktree Mode

**Why now**: Project Compass is still fundamentally single-agent, while real engineering teams are moving toward parallel agent workflows.

**What to build**:
- Lead/Teammate operating model with one board and per-agent sessions
- git worktree-based local isolation as the first supported mode
- merge rules for L3 and L4 to avoid session and task-board conflicts
- task claim, status handoff, and completion conventions carried via git metadata

**Outcome**: Compass supports parallel AI execution without breaking its traceability model.

**Research basis**: see [multi-agent-collaboration-research.md](multi-agent-collaboration-research.md).

### 5. Validation Analytics Dashboard

**Why now**: L5 already captures reports, but Compass does not yet show trend lines or operational quality signals.

**What to build**:
- aggregate L5 reports into spec coverage, scenario coverage, false-pass findings, and archive latency
- compare model/tool performance over time
- track recurring review failures and high-risk modules
- generate summary dashboards for active changes and release readiness

**Outcome**: Compass can improve based on measured quality, not anecdotal experience.

### 6. Cross-Tool Adapter Layer

**Why now**: builders exist per tool, but the core workflow knowledge is still duplicated across prompt sets.

**What to build**:
- one canonical workflow schema for skills, entrypoints, and validation hooks
- generators for Claude Code, Copilot, Cline, Cursor, Codex, and adjacent tools
- compatibility tests that detect instruction drift across tool adapters
- a stable contract between Compass workflow definitions and generated tool assets

**Outcome**: Compass becomes portable infrastructure rather than a collection of parallel prompt forks.

## Level 3 — Platform

### 7. Agent QA Harness

**Why now**: if Compass claims to detect weak tests and workflow regressions, it should test that claim directly.

**What to build**:
- mutation-style probes that deliberately inject false-pass patterns
- checks that remove assertions, mock the wrong layer, or break spec alignment on purpose
- scorecards for how well `review-tests` and related workflows catch planted failures
- benchmark suites for evaluating workflow reliability across models and tools

**Outcome**: Compass gains its own harness engineering loop for verifying AI workflow quality.

### 8. Stack And Domain Packs

**Why now**: many projects repeat the same L1/L2/L3/L5 setup work per stack or domain.

**What to build**:
- reusable packs for common stacks such as React + Node, Django, FastAPI, and Go services
- domain packs for auth, billing, background jobs, audit logging, and regulated workflows
- pack-level rules, testing conventions, and anti-pattern catalogs
- versioned pack composition on top of the core Compass skeleton

**Outcome**: Compass starts with domain knowledge instead of an empty template.

### 9. Team And Enterprise Governance

**Why now**: Compass already behaves like a public interface, but it does not yet provide organizational controls.

**What to build**:
- audit trail for proposal, review, archive, and release decisions
- policy hooks for rollback plans, compliance checks, and risk acknowledgment
- role gates for who can approve, archive, or bypass validation
- plugin surface for organization-specific rules without forking the whole repo

**Outcome**: Compass becomes viable as shared engineering infrastructure, not just an individual workflow kit.

## Suggested Sequencing

| Milestone | Focus |
|-----------|-------|
| `v0.4` | Harness CLI MVP, structure validation, entrypoint generation |
| `v0.5` | Workflow macros, multi-agent worktree MVP |
| `v0.6` | Validation analytics, cross-tool adapter alpha |
| `v0.7` | Brownfield analyzer, agent QA harness, first stack packs |
| `v1.0` | Governance model, stable plugin surface, compatibility contract |

## Guardrails

- Keep Compass differentiated from OpenSpec by focusing on context navigation, workflow harnessing, and validation rigor.
- Prefer executable guardrails over additional prose whenever possible.
- Treat `L*` templates, `entrypoints/`, and `.github/skills/` as public interfaces.
- Let multi-agent support start with simple local isolation before chasing large-scale orchestration.

## Inputs

- [multi-agent-collaboration-research.md](multi-agent-collaboration-research.md)
- `README.md`, `README.zh.md`, and `WORKFLOW-ANALYSIS.md`
- OpenSpec references under `OpenSpec-1.2.0/`