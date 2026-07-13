<!-- compass:start -->
## Compass

- Read the smallest relevant project context before changing code.
- Project context, when installed, lives under `.compass/context/`.
- Use `.compass/context/L1-codebase-map/` for navigation and architecture.
- Use `.compass/context/L2-rules/` for confirmed coding and testing constraints.
- Use `.compass/context/L3-specs/` for requirements and active changes.
- Use `.compass/context/L4-session/` only when resumable session state exists.
- Use `.compass/context/L5-validation/` only for evidence that has actually been checked.
- Workflow Skills live only under `.compass/skills/`; read the relevant `SKILL.md` there when the requested work matches a workflow, then load only the `references/` files that `SKILL.md` requires for the current scope.
- Discover real build, test, lint, and formatting commands from the target project; never guess them.
- Preserve existing project rules and user changes.
- Before completing a code-changing workflow, apply `.compass/context/doc-sync.md` automatically; do not ask the user to trigger a separate context-update workflow.
- Do not install or generate Subagents unless the user explicitly asks for them.
- Do not claim completion without concrete evidence such as a passing check or inspected diff.
<!-- compass:end -->
