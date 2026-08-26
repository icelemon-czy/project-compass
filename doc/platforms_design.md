# Platforms

这是 `compass/platforms/` 的 design。四个适配器同一套迁移：instruction、全部 Compass Skill、可选 subagent、planner 才装 hook。总安装不猜 native JSON，细节在各平台 `INSTALL.md`。

| Platform | Kind | Instruction | Skills | Subagent | Hook |
|:---------|:-----|:------------|:-------|:---------|:-----|
| Codex | planner | 根 `AGENTS.md` | `.agents/skills/<skill>/` | `.codex/agents/<role>.toml` | `.codex/hooks/cli-worker.py` + `.codex/hooks.json` |
| Cursor | planner | 根 `AGENTS.md` | `.cursor/skills/<skill>/` | `.cursor/agents/<role>.md` | `.cursor/hooks/cli-worker.py` + `.cursor/hooks.json` |
| OpenCode | planner | 根 `AGENTS.md` | `.opencode/skills/<skill>/` | `.opencode/agents/<role>.md` | `.opencode/hooks/cli-worker.py` + `.opencode/plugins/compass-cli-worker.js` |
| Claude Code | worker | 根 `CLAUDE.md` | `.claude/skills/<skill>/` | `.claude/agents/<role>.md` | 不装 |

Cursor / Codex / OpenCode 共用同一份根 `AGENTS.md` 受管区块。Claude Code 写入 `CLAUDE.md`，不套一层 `claude`。

编排见 [install_instruction.md](install_instruction.md) Step 4–5。Skill 见 [skills_design.md](skills_design.md)。hook 见 [hooks_design.md](hooks_design.md)。subagent 见 [subagents_design.md](subagents_design.md)。
