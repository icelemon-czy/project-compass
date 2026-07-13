# Entrypoint and Installation Boundary

Use this reference only when `build-ai` must verify that Agents can discover Compass context and Skill references. Installation and platform file generation remain the responsibility of `.compass/INSTALL.md` and the selected platform installer.

## Shared project entrypoint

The target project's root `AGENTS.md` is the shared rule body. Its Compass-managed section uses stable markers:

```text
<!-- compass:start -->
...
<!-- compass:end -->
```

The section must navigate Agents to:

- `.compass/context/L1-codebase-map/` for codebase navigation.
- `.compass/context/L2-rules/` for confirmed coding and testing rules.
- `.compass/context/L3-specs/` for requirements and active changes.
- `.compass/context/L4-session/` only for resumable state.
- `.compass/context/L5-validation/` only for checked evidence.
- `.compass/skills/<skill>/SKILL.md`, followed by only the references required for the task.

Do not duplicate detailed context or Skill bodies into `AGENTS.md`.

## Platform routing

| Platform | Shared rule handling | Platform installer |
|:---------|:---------------------|:-------------------|
| Codex | Reads root `AGENTS.md` directly | `.compass/platforms/codex/INSTALL.md` |
| Claude Code | Root `CLAUDE.md` imports `@AGENTS.md` | `.compass/platforms/claude-code/INSTALL.md` |
| OpenCode | Reads root `AGENTS.md` directly | `.compass/platforms/opencode/INSTALL.md` |

`build-ai` must not guess or reproduce platform formats. If an entrypoint is absent or incorrect, report it and execute `.compass/INSTALL.md` only when the user's task includes installation or repair.

## Verification

Check without overwriting user content:

1. Root `AGENTS.md` exists.
2. The Compass marker block appears exactly once.
3. The block points to `.compass/context/` and `.compass/skills/`.
4. The selected platform's installer has completed its own checks.
5. No second Skill tree or Skill symlink exists.
6. Optional Subagent files exist only for roles the user explicitly selected.

If any of these fail during a context-only request, report the installation problem separately instead of silently changing platform files.
