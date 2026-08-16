# OpenCode Platform Installer

> 本文件由 `.compass/INSTALL.md` 调用，只负责 OpenCode 的项目入口、project Skill、只读 Subagent 和可选 CLI worker hook 适配。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- Subagent 角色列表；默认包含内置只读 `sdd-reviewer`，可追加用户明确要求的 `codebase-explorer`。
- 总 installer 在 Step 6 判定 CLI worker 之后，若 `status=enabled`，再调用本文件的 hook 步骤。

## 平台边界

- OpenCode 原生读取项目根 `AGENTS.md`，基础安装不需要创建或修改 `opencode.json`。
- 不通过 `opencode.json.instructions` 再加载一次根 `AGENTS.md`。
- `.compass/skills/` 是本次 installation source；OpenCode 的 project Skill 安装到 `.opencode/skills/<skill>/`。
- 按总 installer 的受管 copy 规则安装 Skill，不创建软链接，也不写入 global Skill directory。
- CLI worker 以本地 plugin 形式安装到 `.opencode/plugins/`，不修改 `opencode.json` / `opencode.jsonc`。
- Main Agent 负责状态机；生成角色保持 read-only。

## Step 1：安装 OpenCode project instructions

1. 检查项目是否已有根 `AGENTS.md`、`opencode.json`、`opencode.jsonc`、`.opencode/agents/` 和 `.opencode/skills/`。
2. 按 `.compass/INSTALL.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块安装到根 `AGENTS.md`。
3. 已有 OpenCode 配置和 marker 外的根 `AGENTS.md` 内容全部保留；基础安装不需要修改 `opencode.json` 或 `opencode.jsonc`。

## Step 2：安装 OpenCode project Skill

按 `.compass/INSTALL.md` Step 4 的 source inventory 和受管 copy 规则，将每个 `.compass/skills/<skill>/` 完整安装到：

```text
.opencode/skills/<skill>/
```

即使 OpenCode 兼容其他 Skill location，本 installer 也只管理 `.opencode/skills/`，避免 platform ownership 不清。保留其中其他名称的用户 Skill；同名 Skill 与 source 完全一致时复用；存在 legacy `.compass-generated` 时按总 installer 的 migration rule 更新并删除 marker；其他内容不同的同名 Skill 跳过并报告 conflict，不影响其他 Skill 和 Subagent 安装。

如果 Skill 在当前 OpenCode session 启动后才安装或更新，最终报告提醒用户在新 session 中验证 Skill discovery；本轮仍须完成 filesystem validation。

## Step 3：渲染内置与可选 Subagent

对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 渲染 `.compass/platforms/opencode/agent.md.template`。
4. 将结果写入 `.opencode/agents/<role>.md`；文件名就是 OpenCode 中的角色名。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告该角色使用 Main Agent inline fallback。

## Step 4：验证

- [ ] 根 `AGENTS.md` 包含且只包含一个最新 Compass 受管区块，原有规则没有丢失。
- [ ] 没有创建或修改 `opencode.json` / `opencode.jsonc`。
- [ ] 没有通过 instructions 重复加载根 `AGENTS.md`。
- [ ] `.opencode/skills/` 中每个无 conflict 的 Compass Skill 都包含 `SKILL.md` 和完整 resources，且没有 installer metadata file。
- [ ] 没有覆盖用户自建的同名 Skill，没有创建 Skill 软链接或修改 global Skill directory。
- [ ] `sdd-reviewer` 已生成且保持 read-only，或明确记录 inline fallback。
- [ ] 未明确选择时没有生成 `codebase-explorer`。
- [ ] 每个已生成 agent 文件都有 `description`、`mode: subagent`、权限配置和 generated 标记。
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

报告：

```text
opencode
- Instructions：根 AGENTS.md（created / updated / reused）
- Skill destination：.opencode/skills/
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
2. Skill 不含 ownership marker；列出待移除的 `.opencode/skills/<skill>/`，只有用户逐项明确确认后才删除，否则保留并报告 manual cleanup。
3. 只删除带 `compass:generated` 标记的 `.opencode/agents/*.md`。
4. 删除 `.opencode/hooks/cli-worker.py`；只删除带 `compass:generated hook=cli-worker` 的 `.opencode/plugins/compass-cli-worker.js`。
5. 保留用户自建 agent、`opencode.json`、`opencode.jsonc` 和其他 `.opencode/` 内容。
6. 受管目录变空时可删除对应空目录；不要删除仍有其他内容的 `.opencode/`。

## 官方参考

- [OpenCode rules](https://opencode.ai/docs/rules)
- [OpenCode skills](https://opencode.ai/docs/skills)
- [OpenCode agents](https://opencode.ai/docs/agents/)
- [OpenCode plugins](https://opencode.ai/docs/plugins/)
