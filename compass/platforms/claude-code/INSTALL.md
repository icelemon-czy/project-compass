# Claude Code Platform Installer

> 本文件由 Compass 源码仓 `doc/install_instruction.md` 调用，只负责 Claude Code 的项目入口、project Skill 和可选 Subagent。不安装 CLI worker hook。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- 总 installer 已验证的 Subagent 角色列表；默认空。

## 平台边界

- Claude Code 原生读取根 `CLAUDE.md`；本 installer 将 canonical instructions 直接合并到该文件。
- 不通过 `@AGENTS.md` 或其他 instruction file 间接加载规则。
- `.compass/skills/` 是本次 Skill source；Claude Code 的 project Skill 安装到 `.claude/skills/<skill>/`。
- 按源码仓 `doc/install_instruction.md` 的 Skill inventory 和 copy 规则安装全部 Compass Skill，不创建软链接，也不写入 `~/.claude/skills/`。
- 不修改用户自建其他 Skill。
- 不安装 CLI worker hook。当前 session 已经是 Claude Code，不能再套一层 `claude` CLI。

## Step 1：安装 Claude Code 入口

1. 检查项目是否已有根 `CLAUDE.md`、`.claude/agents/` 和 `.claude/skills/`。
2. 旧安装若包含 `<!-- compass:claude:start -->` / `<!-- compass:claude:end -->` import 区块，将该 legacy 区块原位替换为 canonical instructions 区块；标准 marker 与 legacy marker 同时存在或重复时停止并报告 conflict。
3. 其他情况按源码仓 `doc/install_instruction.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块直接安装到根 `CLAUDE.md`。
4. 保留 marker 外的全部 Claude Code 和用户规则；不创建或依赖根 `AGENTS.md`。

## Step 2：安装 Claude Code project Skill

按源码仓 `doc/install_instruction.md` 的 Skill inventory 和 copy 规则，将每个 Compass Skill 完整安装到：

```text
.claude/skills/<skill>/
```

保留 `.claude/skills/` 中其他名称的用户 Skill。同名 Skill 与 source 完全一致时复用；内容不同则跳过并报告 conflict，不覆盖。

Skill 在当前 Claude Code session 启动后才安装或更新时，最终报告提醒用户在新 session 中验证 discovery；本轮仍须完成 filesystem validation。

## Step 3：渲染可选 Subagent

角色列表为空时跳过。对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 渲染 `.compass/platforms/claude-code/agent.md.template`。
4. 将结果写入 `.claude/agents/<role>.md`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告 inline fallback。

## Step 4：验证

- [ ] 根 `CLAUDE.md` 包含且只包含一个最新 Compass 受管区块。
- [ ] 原有 `CLAUDE.md` 内容没有丢失。
- [ ] 新受管区块没有创建或依赖 `@AGENTS.md` import。
- [ ] `.claude/skills/` 中每个无 conflict 的 Compass Skill 都包含 `SKILL.md`。
- [ ] 没有覆盖用户自建的同名 Skill，没有创建 Skill 软链接或修改 `~/.claude/skills/`。
- [ ] 未明确选择时没有生成 Subagent。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。
- [ ] 没有写入 Claude Code settings 或 `.claude/` 下的 CLI worker hook。

## Step 5：Worker permission boundary

Claude Code 是 worker，不安装或 trust Compass CLI worker hook。Planner 通过各自安装的 wrapper 做 task-level delegation；wrapper 默认使用 `claude -p --permission-mode acceptEdits --no-session-persistence --max-turns 30`，不会按 planner tool call 逐次调用：

- File edit 在 `acceptEdits` 下可以自动执行。
- 每个 bounded task 使用 fresh session；即使 `invoke` 配置含 `--resume`、`--continue` 或 session ID，wrapper 也会删除。
- Shell、network、managed policy、additional directory 或 OS protected folder 仍按 Claude Code permission 处理。
- Compass 不使用 `--dangerously-skip-permissions`，也不把非零退出伪装成成功。
- 权限导致 Claude CLI 非零、超时或无法启动时，planner hook 返回 blocker，并报告 `Last execution: claude-failed`。

本平台固定报告 `Hook files: skipped`、`Runtime activation: not-applicable`、`Worker probe: not-applicable`。不要要求 Claude Code 为 Compass worker hook 执行 `/hooks` 或 probe。

## 返回总安装器

```text
claude-code
- Instructions：根 CLAUDE.md（created / updated / reused）
- Skills：<skill>（installed / reused / conflict）
- Subagents：none / ...
- Hook files：skipped（Claude Code is the worker）
- Runtime activation：not-applicable
- Worker probe：not-applicable
- Last execution：none
- 创建：...
- 更新：...
- 跳过：...
- 冲突：...
- fallback：...
- 需要用户操作：none / new-session-for-skill-discovery
- 验证：...
```

## 移除

1. 从根 `CLAUDE.md` 删除 Compass 标记区块，保留其他内容。
2. Skill 不含 ownership marker；按 Skill inventory 列出 `.claude/skills/<skill>/`，只有用户逐项明确确认后才删除。
3. 只删除带 `compass:generated` 标记的 `.claude/agents/*.md`。
4. 不删除根 `README.md` 或 `doc/`。

## 官方参考

- [Claude Code memory](https://code.claude.com/docs/en/memory)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code permissions](https://code.claude.com/docs/en/permissions)
