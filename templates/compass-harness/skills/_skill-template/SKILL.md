---
name: "{{SKILL_NAME}}"
description: "{{SKILL_DESCRIPTION}}"
---

# {{SKILL_TITLE}}

## Preconditions

- {{PRECONDITION}}

## Inputs

- {{INPUT}}

## Procedure

1. Read the minimum project context required for the task.
2. {{STEP}}
3. Run the relevant verification.

## Allowed writes

- {{ALLOWED_WRITE_SCOPE}}

Stop and request direction before writing outside this scope.

## Failure conditions

- Required context or input is missing and cannot be discovered safely.
- Verification fails and the failure cannot be resolved within the requested scope.
- The next action requires destructive or externally visible authority not granted by the user.

## Output contract

- Outcome: {{OUTCOME}}
- Evidence: {{EVIDENCE}}
- Remaining risk: {{REMAINING_RISK}}

## Completion

Complete only when the requested outcome exists and the stated evidence has been checked.

