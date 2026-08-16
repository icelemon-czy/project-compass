# Codex Platform Installer

> 本文件由 `.compass/INSTALL.md` 调用，只负责 Codex 的项目入口、project Skill、只读 Subagent 和可选 CLI worker hook 适配。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- Subagent 角色列表；默认包含内置只读 `sdd-reviewer`，可追加用户明确要求的 `codebase-explorer`。
- 总 installer 在 Step 6 判定 CLI worker 之后，若 `status=enabled`，再调用本文件的 hook 步骤。

## 平台边界

- Codex 直接读取项目根 `AGENTS.md`，基础安装不需要创建 `.codex/config.toml`。
- `.compass/skills/` 是本次 installation source；Codex 的 project Skill 安装到 `.agents/skills/<skill>/`。
- 按总 installer 的受管 copy 规则安装 Skill，不创建软链接，也不写入 global Skill directory。
- 不修改已有 `.codex/config.toml`。CLI worker hook 只写入 `.codex/hooks.json` 与 `.codex/hooks/`。
- Main Agent 负责状态机；生成角色保持 read-only。

## Step 1：安装 Codex project instructions

1. 检查项目是否已有根 `AGENTS.md`、`.codex/config.toml`、`.codex/agents/` 和 `.agents/skills/`。
2. 按 `.compass/INSTALL.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块安装到根 `AGENTS.md`。
3. 已有 Codex 配置和 marker 外的根 `AGENTS.md` 内容全部保留；本安装器不把 `.codex/config.toml` 当作受管文件。

## Step 2：安装 Codex project Skill

按 `.compass/INSTALL.md` Step 4 的 source inventory 和受管 copy 规则，将每个 `.compass/skills/<skill>/` 完整安装到：

```text
.agents/skills/<skill>/
```

保留 `.agents/skills/` 中其他名称的用户 Skill。同名 Skill 与 source 完全一致时复用；存在 legacy `.compass-generated` 时按总 installer 的 migration rule 更新并删除 marker；其他内容不同的同名 Skill 跳过并报告 conflict，不影响其他 Skill 和 Subagent 安装。

如果 Skill 在当前 Codex session 启动后才安装或更新，最终报告提醒用户在新 session 中验证 Skill discovery；本轮仍须完成 filesystem validation。

## Step 3：渲染内置与可选 Subagent

对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 使用同一角色 ID 渲染 `.compass/platforms/codex/agent.toml.template`。
4. 将结果写入 `.codex/agents/<role>.toml`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告该角色使用 Main Agent inline fallback。

渲染要求：

- `name`：角色 ID。
- `description`：简洁合并 Purpose 与委派条件。
- `developer_instructions`：保留角色的职责、边界、步骤与输出契约。
- 保持 `sandbox_mode = "read-only"`，除非用户明确为该角色批准更大的权限。

## Step 4：验证

- [ ] 根 `AGENTS.md` 包含且只包含一个最新 Compass 受管区块，原有规则没有丢失。
- [ ] 没有创建或修改 `.codex/config.toml`。
- [ ] `.agents/skills/` 中每个无 conflict 的 Compass Skill 都包含 `SKILL.md` 和完整 resources，且没有 installer metadata file。
- [ ] 没有覆盖用户自建的同名 Skill，没有创建 Skill 软链接或修改 global Skill directory。
- [ ] `sdd-reviewer` 已生成且保持 read-only，或明确记录 inline fallback。
- [ ] 未明确选择时没有生成 `codebase-explorer`。
- [ ] 每个已生成 TOML 都包含 `name`、`description` 和 `developer_instructions`。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。

## Step 5：安装 CLI worker hook（仅 `enabled`）

只有总 installer 传入 `cli-worker=enabled` 时才执行本步。否则报告 `Hooks：skipped` 并跳过。

1. 读取 `.compass/hooks/cli-worker/CONTRACT.md` 与 `run.py`。
2. 将 `run.py` 完整复制到 `.codex/hooks/cli-worker.py`；设置可执行；不创建软链接。
3. 在 `.codex/hooks.json` 中 merge Compass 条目。识别条件：`command` 包含 `.codex/hooks/cli-worker.py`。保留用户 hook；无法安全 merge 时不覆盖整份文件，记录 fallback。不要改 `.codex/config.toml`。

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
            "statusMessage": "Compass CLI worker",
            "timeout": 660
          }
        ]
      }
    ]
  }
}
```

4. Destination 不存在时创建上述最小文件。已存在时只更新或追加 Compass 那一条。
5. 不写入 `~/.codex/hooks.json`。最终报告提醒：Codex 可能要求用 `/hooks` trust 新 hook，本轮 filesystem validation 仍须完成。

### Hook 验证

- [ ] `.codex/hooks/cli-worker.py` 存在且含 `compass:generated hook=cli-worker`。
- [ ] `.codex/hooks.json` 含 Compass cli-worker `PreToolUse` 条目。
- [ ] 没有修改 `.codex/config.toml`。
- [ ] 用户原有 hook 没有丢失。

## 返回总安装器

报告：

```text
codex
- Instructions：根 AGENTS.md（created / updated / reused）
- Skill destination：.agents/skills/
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
2. Skill 不含 ownership marker；列出待移除的 `.agents/skills/<skill>/`，只有用户逐项明确确认后才删除，否则保留并报告 manual cleanup。
3. 只删除带 `compass:generated` 标记的 `.codex/agents/*.toml`。
4. 删除 `.codex/hooks/cli-worker.py`；从 `.codex/hooks.json` 只移除 command 指向该脚本的条目；文件因此变空且没有用户 hook 时才删除它。
5. 保留用户自建 agent 和 `.codex/config.toml`。
6. 受管目录变空时可删除对应空目录；不要删除仍有其他内容的 `.agents/` 或 `.codex/`。

## 官方参考

- [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex Skills](https://learn.chatgpt.com/docs/customization/overview)
- [Codex Hooks](https://developers.openai.com/codex/hooks)
