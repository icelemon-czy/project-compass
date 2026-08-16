# Cursor Platform Installer

> 本文件由 `.compass/INSTALL.md` 调用，只负责 Cursor 的项目入口、project Skill、只读 Subagent 和可选 CLI worker hook 适配。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- Subagent 角色列表；默认包含内置只读 `sdd-reviewer`，可追加用户明确要求的 `codebase-explorer`。
- 总 installer 在 Step 6 判定 CLI worker 之后，若 `status=enabled`，再调用本文件的 hook 步骤。

## 平台边界

- Cursor 原生读取项目根 `AGENTS.md`；本 installer 将 canonical instructions 直接合并到该文件。
- 不把 `CLAUDE.md` 或 `.cursor/rules/*.mdc` 当作 Compass 入口。
- `.compass/skills/` 是本次 installation source；Cursor 的 project Skill 安装到 `.cursor/skills/<skill>/`。
- 按总 installer 的受管 copy 规则安装 Skill，不创建软链接，也不写入 `~/.cursor/skills/`。
- Main Agent 负责状态机；生成角色保持 read-only。
- 不修改 Cursor user settings，也不写入 `~/.cursor/hooks.json`。

## Step 1：安装 Cursor project instructions

1. 检查项目是否已有根 `AGENTS.md`、`.cursor/skills/`、`.cursor/agents/` 和 `.cursor/hooks.json`。
2. 按 `.compass/INSTALL.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块安装到根 `AGENTS.md`。
3. 已有 Cursor 规则和 marker 外的根 `AGENTS.md` 内容全部保留。Codex 或 OpenCode 已写入同一文件时，只更新同一个受管区块。

## Step 2：安装 Cursor project Skill

按 `.compass/INSTALL.md` Step 4 的 source inventory 和受管 copy 规则，将每个 `.compass/skills/<skill>/` 完整安装到：

```text
.cursor/skills/<skill>/
```

保留 `.cursor/skills/` 中其他名称的用户 Skill。同名 Skill 与 source 完全一致时复用；存在 legacy `.compass-generated` 时按总 installer 的 migration rule 更新并删除 marker；其他内容不同的同名 Skill 跳过并报告 conflict，不影响其他 Skill 和 Subagent 安装。

如果 Skill 在当前 Cursor session 启动后才安装或更新，最终报告提醒用户在新 session 中验证 Skill discovery；本轮仍须完成 filesystem validation。

## Step 3：渲染内置与可选 Subagent

对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 渲染 `.compass/platforms/cursor/agent.md.template`。
4. 将结果写入 `.cursor/agents/<role>.md`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告该角色使用 Main Agent inline fallback。

## Step 4：验证（Skill 与 Subagent）

- [ ] 根 `AGENTS.md` 包含且只包含一个最新 Compass 受管区块，原有规则没有丢失。
- [ ] 没有创建 `.cursor/rules/` 来承载 Compass baseline，也没有把 `CLAUDE.md` 当作 Cursor 入口。
- [ ] `.cursor/skills/` 中每个无 conflict 的 Compass Skill 都包含 `SKILL.md` 和完整 resources，且没有 installer metadata file。
- [ ] 没有覆盖用户自建的同名 Skill，没有创建 Skill 软链接或修改 `~/.cursor/skills/`。
- [ ] `sdd-reviewer` 已生成且保持 `readonly: true`，或明确记录 inline fallback。
- [ ] 未明确选择时没有生成 `codebase-explorer`。
- [ ] 每个已生成 agent 文件都有合法 frontmatter 和 generated 标记。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。

## Step 5：安装 CLI worker hook（仅 `enabled`）

只有总 installer 传入 `cli-worker=enabled` 时才执行本步。`disabled` / `not-applicable` 时报告 `Hooks：skipped` 并跳过。

1. 读取 `.compass/hooks/cli-worker/CONTRACT.md` 与 `run.py`。
2. 将 `run.py` 完整复制到 `.cursor/hooks/cli-worker.py`；设置可执行；不创建软链接。
3. 在 `.cursor/hooks.json` 中 merge 以下 Compass 条目。识别条件：`command` 包含 `.cursor/hooks/cli-worker.py`。已有用户 hook 全部保留；无匹配 command 且无法安全识别所有权时不覆盖整份文件，记录 fallback。

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

- [ ] `.cursor/hooks/cli-worker.py` 存在，内容来自本次 `run.py`，且含 `compass:generated hook=cli-worker`。
- [ ] `.cursor/hooks.json` 含且只含一条 Compass cli-worker `preToolUse` 条目。
- [ ] 用户原有 hook 没有丢失。

## 返回总安装器

报告：

```text
cursor
- Instructions：根 AGENTS.md（created / updated / reused）
- Skill destination：.cursor/skills/
- Skills installed：...
- Skills reused：...
- Skills migrated：...（legacy marker removed）
- Skills conflict：...
- Skill metadata file：none
- Subagents：...
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

只有总安装器正在执行用户明确要求的卸载时才处理：

1. 如果没有仍在使用根 `AGENTS.md` 受管区块的其他已安装平台，从根 `AGENTS.md` 删除 Compass 区块并保留其他规则；文件只剩空白时才删除它。
2. Skill 不含 ownership marker；列出待移除的 `.cursor/skills/<skill>/`，只有用户逐项明确确认后才删除，否则保留并报告 manual cleanup。
3. 只删除带 `compass:generated` 标记的 `.cursor/agents/*.md`。
4. 删除 `.cursor/hooks/cli-worker.py`；从 `.cursor/hooks.json` 只移除 command 指向该脚本的条目；文件因此变空且没有用户 hook 时才删除它。
5. 保留用户自建 agent、rules、hooks 和其他 `.cursor/` 内容。
6. 受管目录变空时可删除对应空目录；不要删除仍有其他内容的 `.cursor/`。

## 官方参考

- [Cursor Skills](https://cursor.com/docs/skills)
- [Cursor Subagents](https://cursor.com/docs/subagents)
- [Cursor Hooks](https://cursor.com/docs/hooks)
