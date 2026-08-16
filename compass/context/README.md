# Compass Context

This directory becomes a project's `.compass/context/` when `compass/` is copied into that project.

This edition does not store project knowledge here. The project README, `doc/<feature>_design.md`, and `doc/todo.md` are the source of truth.

| File | Requirement | Purpose |
|:-----|:------------|:--------|
| `cli-worker.md` | Filled by installer | Whether planner platforms may invoke Claude Code CLI |

`cli-worker.md` is written by installation. Ordinary product work must not change its `status`.
