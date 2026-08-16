# Codex Platform Installer

> 本文件由 `.compass/INSTALL.md` 调用，只负责 Codex 的项目入口、可选 Subagent 和可选 CLI worker hook。本版本不安装 Compass Skill。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md` 和 `.compass/context/`。
- Subagent 角色列表；默认空。可追加用户明确要求的 `codebase-explorer`。
- 总 installer 在判定 CLI worker 之后，若 `status=enabled`，再调用本文件的 hook 步骤。

## 平台边界

- Codex 直接读取项目根 `AGENTS.md`，基础安装不需要创建 `.codex/config.toml`。
- 不安装 Compass Skill，不创建 `.agents/skills/` 来承载 Compass Skill。
- 不修改已有 `.codex/config.toml`。CLI worker hook 只写入 `.codex/hooks.json` 与 `.codex/hooks/`。

## Step 1：安装 Codex project instructions

1. 检查项目是否已有根 `AGENTS.md`、`.codex/config.toml`、`.codex/agents/`。
2. 按 `.compass/INSTALL.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块安装到根 `AGENTS.md`。
3. 已有 Codex 配置和 marker 外的根 `AGENTS.md` 内容全部保留。

## Step 2：跳过 Compass Skill

报告 `Skills：none`。不要复制 Skill，不要新建 `.agents/skills/`。

## Step 3：渲染可选 Subagent

角色列表为空时跳过。对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 使用同一角色 ID 渲染 `.compass/platforms/codex/agent.toml.template`。
4. 将结果写入 `.codex/agents/<role>.toml`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告 inline fallback。

渲染要求：`name`、`description`、`developer_instructions`；保持 `sandbox_mode = "read-only"`，除非用户明确批准更大权限。

## Step 4：验证

- [ ] 根 `AGENTS.md` 包含且只包含一个最新 Compass 受管区块，且含 Project Knowledge 约定。
- [ ] 没有创建或修改 `.codex/config.toml`。
- [ ] 没有为 Compass 创建或写入 `.agents/skills/`。
- [ ] 未明确选择时没有生成 Subagent。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。

## Step 5：安装 CLI worker hook（仅 `enabled`）

只有总 installer 传入 `cli-worker=enabled` 时才执行本步。否则报告 `Hooks：skipped` 并跳过。

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
5. 不写入 `~/.codex/hooks.json`。最终报告提醒：Codex 可能要求用 `/hooks` trust 新 hook。

### Hook 验证

- [ ] `.codex/hooks/cli-worker.py` 存在且含 `compass:generated hook=cli-worker`。
- [ ] `.codex/hooks.json` 含 Compass cli-worker `PreToolUse` 条目。
- [ ] 没有修改 `.codex/config.toml`。
- [ ] 用户原有 hook 没有丢失。

## 返回总安装器

```text
codex
- Instructions：根 AGENTS.md（created / updated / reused）
- Skills：none
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
2. 不自动删除用户 Skill。
3. 只删除带 `compass:generated` 标记的 `.codex/agents/*.toml`。
4. 删除 `.codex/hooks/cli-worker.py`；从 `.codex/hooks.json` 只移除 command 指向该脚本的条目。
5. 不删除根 `README.md` 或 `doc/`。保留 `.codex/config.toml`。

## 官方参考

- [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex Skills](https://learn.chatgpt.com/docs/customization/overview)
- [Codex Hooks](https://developers.openai.com/codex/hooks)
