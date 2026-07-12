# Compass Harness Context Template

Copy this directory to a project's `.compass-harness/context/` directory. Populate only what the project can support with current source code, configuration, tests, or confirmed requirements.

## Minimum set

| File | Requirement | Purpose |
|:-----|:------------|:--------|
| `L1-codebase-map/overview.md` | Required | Small feature and navigation index |
| `L2-rules/global.md` | Required | Confirmed project-wide constraints |
| `L2-rules/testing.md` | Required | Real test commands and conventions |
| `L3-specs/change-management.md` | Required only when using the change workflow | Change states and transition rules |

## Optional layers

- Add detailed L1 feature, architecture, infrastructure, and dependency documents only when they improve navigation.
- Add L2 module rules only for confirmed module-specific contracts.
- Add L3 system/capability specs and active changes only when the project uses spec-driven changes.
- Use L4 session state only when work must resume across sessions.
- Add L5 traceability, test specs, and reports only for evidence that has actually been checked.

Do not treat an empty template as project knowledge or a verification result. Delete unused example content or leave the optional file uninstalled.

