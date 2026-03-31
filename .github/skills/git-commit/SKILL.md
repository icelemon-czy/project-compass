---
name: git-commit
description: "Stage, commit, and push changes with an auto-generated conventional commit message. Use when: ready to commit, git push, summarize changes, commit message."
argument-hint: "optional branch or extra context"
tools: [run_in_terminal]
---

## Step 1 — Summarize Changes

Run `git status --short` and `git diff HEAD`. If nothing changed, report "nothing to commit" and stop.

Summarize what changed and why into a **conventional commit message**:
- Subject: `<type>(<scope>): <summary>` (imperative mood, ≤72 chars)
- Body: bullet points grouped by change area

Do NOT ask the user to write the message.

## Step 2 — Commit & Push

Using the summary from Step 1:
1. `git add -A`
2. `git commit -m "<subject>" -m "<body>"`
3. Set proxy before pushing: `export http_proxy="http://127.0.0.1:10080" https_proxy="http://127.0.0.1:10080"`
4. Push to current branch (`--set-upstream` if new branch)

Report the commit hash and branch name after pushing.
