# OpenCode Platform Installer

> 本文件由 Compass 源码仓 `doc/install_instruction.md` 调用，只负责 OpenCode 的项目入口、project Skill、可选 Subagent 和可选 CLI worker hook。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- 总 installer 已验证的 Subagent 角色列表；默认空。
- 总 installer 在判定 CLI worker 之后，若 `status=enabled`，再调用本文件的 hook 步骤。

## 平台边界

- OpenCode 原生读取项目根 `AGENTS.md`，基础安装不需要创建或修改 `opencode.json`。
- 不通过 `opencode.json.instructions` 再加载一次根 `AGENTS.md`。
- `.compass/skills/` 是本次 Skill source；OpenCode 的 project Skill 安装到 `.opencode/skills/<skill>/`。
- 按源码仓 `doc/install_instruction.md` 的 Skill inventory 和 copy 规则安装全部 Compass Skill，不创建软链接，也不写入 `~/.config/opencode` 的 Skill directory。
- 不修改用户自建其他 Skill。
- CLI worker 以本地 plugin 形式安装到 `.opencode/plugins/`，不修改 `opencode.json` / `opencode.jsonc`。

## Step 1：安装 OpenCode project instructions

1. 检查项目是否已有根 `AGENTS.md`、`opencode.json`、`opencode.jsonc`、`.opencode/agents/` 和 `.opencode/skills/`。
2. 按源码仓 `doc/install_instruction.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块安装到根 `AGENTS.md`。
3. 已有 OpenCode 配置和 marker 外的根 `AGENTS.md` 内容全部保留。

## Step 2：安装 OpenCode project Skill

按源码仓 `doc/install_instruction.md` 的 Skill inventory 和 copy 规则，将每个 Compass Skill 完整安装到：

```text
.opencode/skills/<skill>/
```

即使 OpenCode 兼容其他 Skill location，本 installer 也只管理 `.opencode/skills/`。保留其中其他名称的用户 Skill。同名 Skill 与 source 完全一致时复用；内容不同则跳过并报告 conflict，不覆盖。

如果 Skill 在当前 OpenCode session 启动后才安装或更新，最终报告提醒用户在新 session 中验证 Skill discovery；本轮仍须完成 filesystem validation。

## Step 3：渲染可选 Subagent

角色列表为空时跳过。对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 渲染 `.compass/platforms/opencode/agent.md.template`。
4. 将结果写入 `.opencode/agents/<role>.md`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告 inline fallback。

## Step 4：验证

- [ ] 根 `AGENTS.md` 包含且只包含一个最新 Compass 受管区块。
- [ ] 没有创建或修改 `opencode.json` / `opencode.jsonc`。
- [ ] `.opencode/skills/` 中每个无 conflict 的 Compass Skill 都包含 `SKILL.md`。
- [ ] 没有覆盖用户自建的同名 Skill，没有创建 Skill 软链接或修改 global Skill directory。
- [ ] 未明确选择时没有生成 Subagent。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。

## Step 5：安装 CLI worker hook（仅 `enabled`）

只有总 installer 传入 `cli-worker=enabled` 时才执行本步。否则报告 `Hooks：skipped` 并跳过。OpenCode 没有通用 `hooks.json`；本地 plugin 就是它的 hook dest。

1. 读取 `.compass/hooks/cli-worker/CONTRACT.md` 与 `run.py`。
2. 将 `run.py` 完整复制到 `.opencode/hooks/cli-worker.py`；设置可执行；不创建软链接。
3. 将 `.compass/platforms/opencode/compass-cli-worker.js` 安装到 `.opencode/plugins/compass-cli-worker.js`。目标不存在时创建；已有文件含 `compass:generated hook=cli-worker` 时更新；无 marker 且内容不同时不覆盖，记录 fallback。
4. 不修改 `opencode.json` / `opencode.jsonc`，不写入 `~/.config/opencode/plugins/`。

### Hook 验证

- [ ] `.opencode/hooks/cli-worker.py` 存在且含 `compass:generated hook=cli-worker`。
- [ ] `.opencode/plugins/compass-cli-worker.js` 存在且含 generated 标记，或已记录 fallback。
- [ ] 没有修改 `opencode.json` / `opencode.jsonc`。

## 返回总安装器

```text
opencode
- Instructions：根 AGENTS.md（created / updated / reused）
- Skills：<skill>（installed / reused / conflict）
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
2. Skill 不含 ownership marker；按 Skill inventory 列出 `.opencode/skills/<skill>/`，只有用户逐项明确确认后才删除。
3. 只删除带 `compass:generated` 标记的 `.opencode/agents/*.md`。
4. 删除 `.opencode/hooks/cli-worker.py`；只删除带 `compass:generated hook=cli-worker` 的 `.opencode/plugins/compass-cli-worker.js`。
5. 不删除根 `README.md` 或 `doc/`。

## 官方参考

- [OpenCode rules](https://opencode.ai/docs/rules)
- [OpenCode skills](https://opencode.ai/docs/skills)
- [OpenCode agents](https://opencode.ai/docs/agents/)
- [OpenCode plugins](https://opencode.ai/docs/plugins/)
