# Codex Platform Installer

> 本文件由 Compass 源码仓 `doc/install_instruction.md` 调用，只负责 Codex 的项目入口、project Skill、可选 Subagent 和可选 CLI worker hook。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- 总 installer 已验证的 Subagent 角色列表；默认空。
- 总 installer 在判定 CLI worker 之后，若 `status=enabled`，再调用本文件的 hook 步骤。

## 平台边界

- Codex 直接读取项目根 `AGENTS.md`，基础安装不需要创建 `.codex/config.toml`。
- `.compass/skills/` 是本次 Skill source；Codex 的 project Skill 安装到 `.agents/skills/<skill>/`。
- 按源码仓 `doc/install_instruction.md` 的 Skill inventory 和 copy 规则安装全部 Compass Skill，不创建软链接，也不写入 `~/.codex` 的 Skill directory。
- 不修改用户自建其他 Skill。
- 不修改已有 `.codex/config.toml`。CLI worker hook 只写入 `.codex/hooks.json` 与 `.codex/hooks/`。

## Step 1：安装 Codex project instructions

1. 检查项目是否已有根 `AGENTS.md`、`.codex/config.toml`、`.codex/agents/` 和 `.agents/skills/`。
2. 按源码仓 `doc/install_instruction.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块安装到根 `AGENTS.md`。
3. 已有 Codex 配置和 marker 外的根 `AGENTS.md` 内容全部保留。

## Step 2：安装 Codex project Skill

按源码仓 `doc/install_instruction.md` 的 Skill inventory 和 copy 规则，将每个 Compass Skill 完整安装到：

```text
.agents/skills/<skill>/
```

保留 `.agents/skills/` 中其他名称的用户 Skill。同名 Skill 与 source 完全一致时复用；内容不同则跳过并报告 conflict，不覆盖。

如果 Skill 在当前 Codex session 启动后才安装或更新，最终报告提醒用户在新 session 中验证 Skill discovery；本轮仍须完成 filesystem validation。

## Step 3：渲染可选 Subagent

角色列表为空时跳过。对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 使用同一角色 ID 渲染 `.compass/platforms/codex/agent.toml.template`。
4. 将结果写入 `.codex/agents/<role>.toml`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告 inline fallback。

渲染要求：`name`、`description`、`developer_instructions`；保持 `sandbox_mode = "read-only"`，除非用户明确批准更大权限。

## Step 4：验证

- [ ] 根 `AGENTS.md` 包含且只包含一个最新 Compass 受管区块。
- [ ] 没有创建或修改 `.codex/config.toml`。
- [ ] `.agents/skills/` 中每个无 conflict 的 Compass Skill 都包含 `SKILL.md`。
- [ ] 没有覆盖用户自建的同名 Skill，没有创建 Skill 软链接或修改 global Skill directory。
- [ ] 未明确选择时没有生成 Subagent。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。

## Step 5：安装 CLI worker hook（仅 `enabled`）

只有总 installer 传入 `cli-worker=enabled` 时才执行本步。否则报告 `Hook files：skipped` 并跳过。

1. 读取 `.compass/hooks/cli-worker/CONTRACT.md` 与 `run.py`。
2. 将 `run.py` 完整复制到 `.codex/hooks/cli-worker.py`；设置可执行；不创建软链接。
3. 在 `.codex/hooks.json` 中 merge Compass 条目。识别条件：`command` 包含 `.codex/hooks/cli-worker.py`。不要改 `.codex/config.toml`。

```json
{
  "description": "Compass CLI worker hooks.",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|apply_patch|Edit|Write|Delete",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .codex/hooks/cli-worker.py --format codex",
            "statusMessage": "Compass: enforcing task-level delegation",
            "timeout": 660
          }
        ]
      }
    ]
  }
}
```

4. Destination 不存在时创建上述最小文件。已存在时只更新或追加 Compass 那一条。
5. 不写入 `~/.codex/hooks.json`。
6. Planner 做 implementation 时先覆盖 `.compass/context/cli-worker-task.md`，再执行一次 `python3 .codex/hooks/cli-worker.py --format codex --delegate`。Native hook 命中普通 Write / Edit / Bash 时只 deny 和返回这条 instruction，不直接调用 Claude。
7. 本 installer 安装的 `.codex/hooks.json` CLI worker hook 只以**从项目根目录启动的 Codex CLI session**作为受支持 runtime target。Codex Desktop task 使用 Desktop agent / orchestrator tools，不得假设它会进入这条 project hook pipeline；在 Desktop 中新建 task 不能作为 activation 操作或 evidence。
8. Codex CLI 对 non-managed project hook 要求 review 并 trust **当前 hook definition**。从项目根启动 `codex`，在该 CLI session 中使用 `/hooks` 完成 review 与 trust；definition 变化导致 hash 变化后必须重新 trust。
9. Installer 当前不在项目根的 Codex CLI runtime 中，或无法 authoritative 地确认该 runtime 时，即使文件完整也报告 `Runtime activation: awaiting-cli-session`。已确认位于目标 CLI session、但当前 definition 尚未 trust 时报告 `awaiting-trust`；只有同一 CLI session 提供当前 definition 的 authoritative trust evidence 时才能报告 `active`。不得从 Desktop task、旧 session、其他项目或文件存在推断 active。

### Runtime activation 与 probe

1. 从 repository root 启动新的 Codex CLI session；不要在 Codex Desktop 中新建 task 代替这一步。CLI 未启动时保持 `awaiting-cli-session`。
2. 在该 CLI session 中运行 `/hooks`，review 并 trust 当前 definition。完成前保持 `awaiting-trust`；有同一 CLI session 对当前 definition 的 authoritative trust evidence 时报告 `Runtime activation: active`。
3. 仍在同一 Codex CLI session 中，先让 Codex 直接创建 `.compass-worker-probe.tmp`，确认 hook deny、没有启动 Claude，且 UI 要求 task-level delegation。
4. 让 Codex 把创建 probe 的 bounded task 写入 `.compass/context/cli-worker-task.md`，执行一次 `python3 .codex/hooks/cli-worker.py --format codex --delegate`。
5. 按 `.compass/hooks/cli-worker/CONTRACT.md` 同时检查 CLI UI message、`planner_blocked` + `delegation_started` + `worker_succeeded` audit chain、文件内容和原始 write tool 未执行。
6. 四项都成立才报告 `Worker probe: passed`；任一缺失报告 `Worker probe: failed`。未执行时保持 `pending`。
7. Probe 通过后覆盖 task spec 为 cleanup task，再执行一次 `--delegate` 删除文件并确认无遗留。

### Hook 验证

- [ ] `.codex/hooks/cli-worker.py` 存在且含 `compass:generated hook=cli-worker`。
- [ ] `.codex/hooks.json` 含 Compass cli-worker `PreToolUse` 条目。
- [ ] 没有修改 `.codex/config.toml`。
- [ ] 用户原有 hook 没有丢失。
- [ ] Hook files、Runtime activation、Worker probe 与 Last execution 分开报告。
- [ ] Codex Desktop task 没有被当作支持的 hook runtime，也没有被当作 activation evidence。
- [ ] `Runtime activation: active` 有项目根 Codex CLI session 对当前 definition 的 trust evidence；CLI 尚未启动时是 `awaiting-cli-session`，未 trust 时是 `awaiting-trust`。
- [ ] `Worker probe: passed` 有 UI、audit、文件和 transcript 四类 evidence。

## 返回总安装器

```text
codex
- Instructions：根 AGENTS.md（created / updated / reused）
- Skills：<skill>（installed / reused / conflict）
- Subagents：none / ...
- Hook files：installed / skipped / conflict
- Runtime target：project-root Codex CLI（Codex Desktop unsupported）
- Runtime activation：active / awaiting-cli-session / awaiting-trust / not-applicable
- Worker probe：passed / pending / failed / not-applicable
- Last execution：claude-succeeded / claude-failed / none
- 创建：...
- 更新：...
- 跳过：...
- 冲突：...
- fallback：...
- 需要用户操作：none / start-codex-cli-from-project-root / review-and-trust-current-hook / run-probe-in-same-cli-session
- 验证：...
```

## 移除

1. 如果没有仍在使用根 `AGENTS.md` 受管区块的其他已安装平台，从根 `AGENTS.md` 删除 Compass 区块并保留其他规则。
2. Skill 不含 ownership marker；按 Skill inventory 列出 `.agents/skills/<skill>/`，只有用户逐项明确确认后才删除。
3. 只删除带 `compass:generated` 标记的 `.codex/agents/*.toml`。
4. 删除 `.codex/hooks/cli-worker.py`；从 `.codex/hooks.json` 只移除 command 指向该脚本的条目。
5. 不删除根 `README.md` 或 `doc/`。保留 `.codex/config.toml`。

## 官方参考

- [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex Skills](https://learn.chatgpt.com/docs/customization/overview)
- [Codex Hooks](https://learn.chatgpt.com/docs/hooks)
