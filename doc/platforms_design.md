# Platforms

这是 `compass/platforms/` 的 design。四个适配器同一套迁移：instruction、全部 Compass Skill、可选 subagent、planner 才装 hook。总安装不猜 native JSON，细节在各平台 `INSTALL.md`。

| Platform | Kind | Instruction | Skills | Subagent | Hook |
|:---------|:-----|:------------|:-------|:---------|:-----|
| Codex | planner | 根 `AGENTS.md` | `.agents/skills/<skill>/` | `.codex/agents/<role>.toml` | `.codex/hooks/cli-worker.py` + `.codex/hooks.json` |
| Cursor | planner | 根 `AGENTS.md` | `.cursor/skills/<skill>/` | `.cursor/agents/<role>.md` | `.cursor/hooks/cli-worker.py` + `.cursor/hooks.json` |
| OpenCode | planner | 根 `AGENTS.md` | `.opencode/skills/<skill>/` | `.opencode/agents/<role>.md` | `.opencode/hooks/cli-worker.py` + `.opencode/plugins/compass-cli-worker.js` |
| Claude Code | worker | 根 `CLAUDE.md` | `.claude/skills/<skill>/` | `.claude/agents/<role>.md` | 不装 |

Cursor / Codex / OpenCode 共用同一份根 `AGENTS.md` 受管区块。Claude Code 写入 `CLAUDE.md`，不套一层 `claude`。

三个 planner 的 native hook 只 enforce policy，不按 Write / Edit / Bash 启动 Claude。Implementation 通过各平台 wrapper 的 `--delegate` mode，以 `.compass/context/cli-worker-task.md` 中的 bounded task 为单位进入 fresh Claude session；raw Claude command 与重复成功 task 都被阻止。

Hook files 与 runtime activation 分开：Codex hook 的受支持 runtime target 是从项目根启动的 Codex CLI session；Codex Desktop task 不进入这条 project hook pipeline，不能通过新建 Desktop task 激活。CLI 必须用 `/hooks` trust 当前 hook definition；Cursor 必须位于 trusted workspace，OpenCode 安装或更新 project-local plugin 后必须 restart / 新建 session。三个 planner 都用各自受支持 runtime 中的真实写入 probe 与 runtime audit 证明 Claude CLI 接管；Claude Code 的 activation 与 probe 是 `not-applicable`。

编排见 [install_instruction.md](install_instruction.md) Step 4–5 与 Step 9。Skill 见 [skills_design.md](skills_design.md)。hook 见 [hooks_design.md](hooks_design.md)。subagent 见 [subagents_design.md](subagents_design.md)。
