# Cursor Platform Installer

> 本文件由 Compass 源码仓 `doc/install_instruction.md` 调用，只负责 Cursor 的项目入口、project Skill、可选 Subagent 和可选 CLI worker hook。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- Subagent 角色列表；默认空。可追加用户明确要求的 `codebase-explorer`。
- 总 installer 在判定 CLI worker 之后，若 `status=enabled`，再调用本文件的 hook 步骤。

## 平台边界

- Cursor 原生读取项目根 `AGENTS.md`；本 installer 将 canonical instructions 直接合并到该文件。
- 不把 `CLAUDE.md` 或 `.cursor/rules/*.mdc` 当作 Compass 入口。
- `.compass/skills/` 是本次 Skill source；Cursor 的 project Skill 安装到 `.cursor/skills/<skill>/`。
- 按源码仓 `doc/install_instruction.md` 的 Skill copy 规则安装 `brainstorm`、`ralph-loop`、`skill-creator`，不创建软链接，也不写入 `~/.cursor/skills/`。
- 不修改用户自建其他 Skill。
- 不修改 Cursor user settings，也不写入 `~/.cursor/hooks.json`。

## Step 1：安装 Cursor project instructions

1. 检查项目是否已有根 `AGENTS.md`、`.cursor/skills/`、`.cursor/agents/` 和 `.cursor/hooks.json`。
2. 按源码仓 `doc/install_instruction.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块安装到根 `AGENTS.md`。
3. 已有 Cursor 规则和 marker 外的根 `AGENTS.md` 内容全部保留。Codex 或 OpenCode 已写入同一文件时，只更新同一个受管区块。

## Step 2：安装 Cursor project Skill

按源码仓 `doc/install_instruction.md` 的 Skill copy 规则，将 `.compass/skills/` 下 `brainstorm`、`ralph-loop`、`skill-creator` 完整安装到：

```text
.cursor/skills/<skill>/
```

保留 `.cursor/skills/` 中其他名称的用户 Skill。同名 Skill 与 source 完全一致时复用；内容不同则跳过并报告 conflict，不覆盖。

如果 Skill 在当前 Cursor session 启动后才安装或更新，最终报告提醒用户在新 session 中验证 Skill discovery；本轮仍须完成 filesystem validation。

## Step 3：渲染可选 Subagent

角色列表为空时跳过。对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 渲染 `.compass/platforms/cursor/agent.md.template`。
4. 将结果写入 `.cursor/agents/<role>.md`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告 inline fallback。

## Step 4：验证

- [ ] 根 `AGENTS.md` 包含且只包含一个最新 Compass 受管区块。
- [ ] `.cursor/skills/` 中每个无 conflict 的 Compass Skill 都包含 `SKILL.md`。
- [ ] 没有覆盖用户自建的同名 Skill，没有创建 Skill 软链接或修改 `~/.cursor/skills/`。
- [ ] 未明确选择时没有生成 Subagent。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。

## Step 5：安装 CLI worker hook（仅 `enabled`）

只有总 installer 传入 `cli-worker=enabled` 时才执行本步。否则报告 `Hooks：skipped` 并跳过。

1. 读取 `.compass/hooks/cli-worker/CONTRACT.md` 与 `run.py`。
2. 将 `run.py` 完整复制到 `.cursor/hooks/cli-worker.py`；设置可执行；不创建软链接。
3. 在 `.cursor/hooks.json` 中 merge 以下 Compass 条目。识别条件：`command` 包含 `.cursor/hooks/cli-worker.py`。已有用户 hook 全部保留。

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "command": "python3 .cursor/hooks/cli-worker.py --format cursor",
        "matcher": "Write|StrReplace|Edit|Delete|Shell",
        "failClosed": false,
        "timeout": 660
      }
    ]
  }
}
```

4. Destination 不存在时创建上述最小文件。已存在时只更新或追加 Compass 那一条。
5. 不写入 `~/.cursor/hooks.json`。

### Hook 验证

- [ ] `.cursor/hooks/cli-worker.py` 存在且含 `compass:generated hook=cli-worker`。
- [ ] `.cursor/hooks.json` 含且只含一条 Compass cli-worker `preToolUse` 条目。
- [ ] 用户原有 hook 没有丢失。

## 返回总安装器

```text
cursor
- Instructions：根 AGENTS.md（created / updated / reused）
- Skills：brainstorm, ralph-loop, skill-creator（installed / reused / conflict）
- Subagents：none / ...
- Hooks：installed / skipped / fallback / conflict
- 创建：...
- 更新：...
- 跳过：...
- 冲突：...
- fallback：...
- 需要新 session：是/否
- 验证：...
```

## 移除

1. 如果没有仍在使用根 `AGENTS.md` 受管区块的其他已安装平台，从根 `AGENTS.md` 删除 Compass 区块并保留其他规则。
2. Skill 不含 ownership marker；列出待移除的 `.cursor/skills/brainstorm/`、`.cursor/skills/ralph-loop/`、`.cursor/skills/skill-creator/`，只有用户逐项明确确认后才删除。
3. 只删除带 `compass:generated` 标记的 `.cursor/agents/*.md`。
4. 删除 `.cursor/hooks/cli-worker.py`；从 `.cursor/hooks.json` 只移除 command 指向该脚本的条目。
5. 不删除根 `README.md` 或 `doc/`。

## 官方参考

- [Cursor Skills](https://cursor.com/docs/skills)
- [Cursor Subagents](https://cursor.com/docs/subagents)
- [Cursor Hooks](https://cursor.com/docs/hooks)
