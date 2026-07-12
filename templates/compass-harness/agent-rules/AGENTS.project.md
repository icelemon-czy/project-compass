# {{PROJECT_NAME}} Project Rules

{{PROJECT_SUMMARY}}

## Project commands

- Source root: `{{SOURCE_ROOT}}`
- Test: `{{TEST_COMMAND}}`
- Build/type-check: `{{BUILD_COMMAND}}`
- Lint/format: `{{LINT_COMMAND}}`

If an optional command is blank, discover the real command from project configuration before running it. Do not guess.

## Context navigation

Read only the context needed for the current task:

- `.compass-harness/context/L1-codebase-map/` for feature locations, architecture, and dependencies.
- `.compass-harness/context/L2-rules/` for coding and testing constraints.
- `.compass-harness/context/L3-specs/` for requirements and active changes.
- `.compass-harness/context/L4-session/` for resumable session state when it exists.
- `.compass-harness/context/L5-validation/` for traceability and validation evidence.

Missing optional context must not block ordinary development. Fall back to source-code evidence and flag the missing context.

## Change discipline

- Confirm business ambiguity before implementation.
- Follow existing code and testing conventions.
- Keep documentation synchronized when public structure, behavior, or commands change.
- Never mark a change verified solely because a document says it is verified.

