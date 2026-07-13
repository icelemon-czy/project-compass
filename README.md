# Compass

> [中文版](README.zh.md) · [Changelog](CHANGELOG.md) · [Version](VERSION)

A copyable AI-assisted development kit for **Codex**, **Claude Code**, and **OpenCode**.

The only directory copied into a target project is [`compass/`](compass/). It contains the project-rule baseline, L1–L5 context, 13 Skills, optional Subagent roles, and platform installers. Repository documentation stays here for maintainers.

## Install in a project

For a new Project A, copy the package directory itself. Do not run this command when Project A already has `.compass/`.

```bash
cp -R /path/to/project-compass/compass /path/to/projectA/.compass
```

Then ask the Agent working in Project A:

> Read `.compass/INSTALL.md` and install Compass for the current project.

The Agent merges the rule baseline with existing project rules, fills the copied L1–L5 context in place, and delegates platform-specific work to each selected platform's `INSTALL.md`. It does not create a second context directory, duplicate Skills, or generate Subagent instances by default.

## Copyable package

```text
compass/
├── AGENTS.md       baseline merged into the target project's root AGENTS.md
├── INSTALL.md      Agent-executable installation and migration contract
├── context/        L1–L5 blank context, filled in place for each project
├── skills/         13 canonical Skills with optional on-demand references
├── subagents/      four optional, concrete delegation roles
└── platforms/      Codex, Claude Code, and OpenCode installers and templates
    ├── codex/INSTALL.md
    ├── claude-code/INSTALL.md
    └── opencode/INSTALL.md
```

`docs/` is source-repository maintenance material. It is intentionally not part of the copied package.

## License

MIT License
