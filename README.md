# Compass

> [中文版](README.zh.md) · [Changelog](CHANGELOG.md) · [Version](VERSION)

A copyable AI-assisted development kit for **Codex**, **Claude Code**, and **OpenCode**.

The only directory copied into a target project is [`compass/`](compass/). It contains the project-rule baseline, L1–L5 context, 9 Skills, a built-in read-only SDD reviewer, an optional explorer role, and platform installers. Repository documentation stays here for maintainers.

Compass exposes goal-oriented entry points. A normal `develop` task handles planning, TDD, review, context sync, and archival internally; users do not chain workflow commands.

For an idea that is not yet defined, `brainstorm` uses `ask-codebase` to gather current-state evidence, converges on a direction, and moves into `develop` only when the user asks to implement it.

Ordinary code review remains a built-in Agent capability: ask for a review directly. Use `audit-tests` only for a dedicated assessment of test coverage and trustworthiness.

Use `skill-creator` to create or revise project-local Skills; it does not install third-party Skills or modify the global environment by default.

## Install in a project

For a new Project A, copy the package directory itself. Do not run this command when Project A already has `.compass/`.

```bash
cp -R /path/to/project-compass/compass /path/to/projectA/.compass
```

Then ask the Agent working in Project A:

> Read `.compass/INSTALL.md` and install Compass for the current project.

The Agent merges the rule baseline with existing project rules, fills the copied L1–L5 context in place, and delegates platform-specific work to each selected platform's `INSTALL.md`. It does not create a second context directory or duplicate Skills. Each selected platform receives the read-only `sdd-reviewer`; the Main Agent remains the sole writer.

## Copyable package

```text
compass/
├── AGENTS.md       baseline merged into the target project's root AGENTS.md
├── INSTALL.md      Agent-executable installation and migration contract
├── context/        L1–L5 blank context, filled in place for each project
├── skills/         9 canonical Skills (7 core entries + optional ralph-loop and skill-creator)
├── subagents/      built-in sdd-reviewer + optional codebase-explorer
└── platforms/      Codex, Claude Code, and OpenCode installers and templates
    ├── codex/INSTALL.md
    ├── claude-code/INSTALL.md
    └── opencode/INSTALL.md
```

`docs/` is source-repository maintenance material. It is intentionally not part of the copied package.

## License

MIT License
