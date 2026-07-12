# Compass Harness

> **[中文版 / Chinese Version](README.zh.md)** · Version: see [VERSION](VERSION) · [CHANGELOG](CHANGELOG.md)

An open AI engineering harness for reusable project context, skills, agent guidance, and platform adapters.

Compass Harness currently targets **Codex**, **Claude Code**, and **OpenCode**.

## What Phase 2 Provides

Phase 2 separates existing working assets from newly introduced templates:

- The repository's 13 existing workflows are maintained as real Skills under `.agents/skills/`.
- AGENTS guidance, project context, new-Skill scaffolding, Subagent roles, and platform adapters live under `templates/compass-harness/`.
- Installed projects use root `AGENTS.md` as the project-rule source and keep context, Skills, Subagent roles, and configuration under `.compass-harness/`.
- Subagents are examples only. Phase 2 does not install `.codex/agents/`, `.claude/agents/`, or `.opencode/agents/` into this repository.
- Validation is deterministic and structural. It does not claim to prove model behavior or cross-platform reasoning quality.

## Repository Layout

```text
project-compass/
├── .agents/skills/                   # Canonical source for the 13 existing Skills
├── templates/compass-harness/
│   ├── manifest.yaml                 # Components, placeholders, and install targets
│   ├── installed-manifest.yaml.template
│   ├── config.yaml                   # Installed project configuration template
│   ├── AGENTS.md                     # Single project-rule template
│   ├── context/                      # L1–L5 context templates
│   ├── skills/_skill-template/       # Template for future Skills
│   ├── subagents/                    # Canonical role template + four examples
│   └── adapters/
│       ├── codex/
│       ├── claude-code/
│       └── opencode/
├── scripts/validate-phase2.rb       # Deterministic static validation
├── builders/claude/                 # Existing Claude context-builder prompts
├── roadmap/                         # Product roadmap and historical research
└── compass                          # CLI entry point; generation is planned for Phase 3
```

## Target Project Layout

```text
.compass-harness/
├── manifest.yaml                    # Installed version and managed paths
├── config.yaml                      # Project values and enabled platforms
├── context/                         # L1–L5 project context
├── skills/                          # Installed canonical Skills
└── subagents/                       # Canonical role definitions and examples

AGENTS.md                            # Native Codex/OpenCode project rules
CLAUDE.md                            # Claude Code adapter to AGENTS.md
.agents/skills/                      # Generated Codex/OpenCode discovery mirror
.claude/skills/                      # Generated Claude Code discovery mirror
tool-specific agent directories      # Generated only for selected roles
```

Edit project rules in root `AGENTS.md`. Edit context, Skills, Subagent roles, and configuration under `.compass-harness/`. Generated discovery mirrors must be reproducible and must not contain the only copy of project knowledge.

## Context Model

The optional `.compass-harness/context/` context uses five layers:

| Layer | Purpose |
|:------|:--------|
| L1 Codebase Map | Feature locations, architecture, entry points, and dependencies |
| L2 Rules | Coding, testing, module, and file-creation constraints |
| L3 Specs | System requirements, capability specs, and active changes |
| L4 Session | Resumable work state when a project needs it |
| L5 Validation | Traceability, test design, and checked evidence |

Projects do not need to populate every layer. Start with the minimum context that can be supported by source code or user-provided requirements, then add more only when it becomes useful.

## Existing Skills

The template repository maintains Skill source under `.agents/skills/`. When installed into another project, the canonical copy is `.compass-harness/skills/`:

| Category | Skills |
|:---------|:-------|
| Bootstrap | `git-init`, `init-project`, `build-ai`, `setup-testing` |
| Develop | `new-change`, `continue-change` |
| Review and archive | `review-tests`, `archive-change`, `check-changes` |
| Fix | `fix-bug` |
| Query | `ask-codebase` |
| Docs and delivery | `update-ai`, `git-commit` |

Each Skill has a `SKILL.md` with only `name` and `description` in its canonical YAML frontmatter. Platform-specific metadata belongs in adapter or generated output, not in the canonical source.

## Templates

### AGENTS.md

`AGENTS.md` is the only project-rule template. It contains the necessary working principles, project commands, and `.compass-harness/context/` navigation without a global/project split.

### Skill template

`skills/_skill-template/SKILL.md` is for creating future Skills. It does not duplicate the 13 existing Skills.

### Subagent templates

`subagents/` contains a generic role contract and four examples:

- Codebase Explorer
- Impact Analyst
- Test Reviewer
- Spec Validator

They define responsibilities, permissions, forbidden actions, and output contracts. They are not installed or behaviorally validated agents.

### Platform adapters

| Platform | Generated discovery adapters |
|:---------|:-----------------------------|
| Codex | Native root `AGENTS.md`, `.agents/skills/`, optional `.codex/agents/*.toml` |
| Claude Code | `CLAUDE.md`, `.claude/skills/`, optional `.claude/agents/*.md` |
| OpenCode | Native root `AGENTS.md`, `.agents/skills/`, optional `opencode.json` and `.opencode/agents/*.md` |

Codex and OpenCode use `AGENTS.md` directly. Claude Code's adapter references `AGENTS.md` instead of duplicating it. Automated installation and discovery-mirror generation belong to the Phase 3 CLI.

## Manual Use

Until the generator is implemented:

1. Create `.compass-harness/{context,skills,subagents}` in the target project.
2. Render `installed-manifest.yaml.template` and `config.yaml` into `.compass-harness/`.
3. Render the single `AGENTS.md` template to project-root `AGENTS.md`; merge existing project rules instead of overwriting them.
4. Copy context templates, 13 Skills, and Subagent role templates into `.compass-harness/`, then generate the platform's Skill discovery mirror.
5. Generate a platform-specific Subagent only when the project explicitly selects that role.

Claude Code may add a `CLAUDE.md` adapter that references `AGENTS.md`. Never edit generated Skill or Subagent mirrors as canonical content.

## Static Validation

Run:

```bash
ruby scripts/validate-phase2.rb
```

The validator checks:

- exactly 13 canonical Skills;
- Skill names, directories, and frontmatter;
- manifest parsing and declared sources;
- the root `AGENTS.md` plus `.compass-harness/` installation contract;
- required AGENTS, Skill, Subagent, and adapter templates;
- registered placeholders and relative Markdown links;
- OpenCode JSON syntax;
- absence of installed root Agent/Subagent instances;
- absence of current `.ai/` dependencies in Skills and templates.

These checks validate repository structure only, not model behavior.

## Roadmap

- Phase 1: Compass Harness rebrand and compatibility baseline.
- Phase 2: canonical Skill migration plus reusable templates for the three supported platforms.
- Phase 3: CLI-driven init, rendering, validation, and upgrade.

See [doc/todo.md](doc/todo.md) for the implementation checklist.

## License

MIT License
