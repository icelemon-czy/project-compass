# Compass Harness

> [中文版](README.zh.md) · [Changelog](CHANGELOG.md) · [Version](VERSION)

A copyable AI-assisted development kit for **Codex**, **Claude Code**, and **OpenCode**.

The only directory copied into a target project is [`harness/`](harness/). It contains the project-rule baseline, L1–L5 context, 13 Skills, optional Subagent roles, and platform-specific formats. Repository documentation stays here for maintainers.

## Install in a project

For a new Project A, copy the package directory itself. Do not run this command when Project A already has `.compass-harness/`.

```bash
cp -R /path/to/project-compass/harness /path/to/projectA/.compass-harness
```

Then ask the Agent working in Project A:

> Read `.compass-harness/INSTALL.md` and install Compass Harness for the current project.

The Agent merges the rule baseline with existing project rules and fills the copied L1–L5 context in place. It does not create a second context directory, duplicate Skills, or generate Subagent instances by default.

## Copyable package

```text
harness/
├── AGENTS.md       baseline merged into the target project's root AGENTS.md
├── INSTALL.md      Agent-executable installation and migration contract
├── context/        L1–L5 blank context, filled in place for each project
├── skills/         13 canonical Skills; the only Skill content source
├── subagents/      four optional, concrete delegation roles
└── platforms/      Codex, Claude Code, and OpenCode role formats
```

`docs/` is source-repository maintenance material. It is intentionally not part of the copied package.

## License

MIT License
