<!-- compass-harness:start -->
## Compass Harness

- Read the smallest relevant project context before changing code.
- Project context, when installed, lives under `.compass-harness/context/`.
- Use `.compass-harness/context/L1-codebase-map/` for navigation and architecture.
- Use `.compass-harness/context/L2-rules/` for confirmed coding and testing constraints.
- Use `.compass-harness/context/L3-specs/` for requirements and active changes.
- Use `.compass-harness/context/L4-session/` only when resumable session state exists.
- Use `.compass-harness/context/L5-validation/` only for evidence that has actually been checked.
- Workflow Skills live only under `.compass-harness/skills/`; read the relevant `SKILL.md` there when the requested work matches a workflow.
- Discover real build, test, lint, and formatting commands from the target project; never guess them.
- Preserve existing project rules and user changes.
- Do not install or generate Subagents unless the user explicitly asks for them.
- Do not claim completion without concrete evidence such as a passing check or inspected diff.
<!-- compass-harness:end -->
