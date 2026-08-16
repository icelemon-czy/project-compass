# Claude Code Platform Installer

> 本文件由 `.compass/INSTALL.md` 调用，只负责 Claude Code 的项目入口、project Skill 和只读 Subagent 适配。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- Subagent 角色列表；默认包含内置只读 `sdd-reviewer`，可追加用户明确要求的 `codebase-explorer`。

## 平台边界

- Claude Code 原生读取根 `CLAUDE.md`；本 installer 将 canonical instructions 直接合并到该文件。
- 不通过 `@AGENTS.md` 或其他 instruction file 间接加载规则。
- `.compass/skills/` 是本次 installation source；Claude Code 的 project Skill 安装到 `.claude/skills/<skill>/`。
- 按总 installer 的受管 copy 规则安装 Skill，不创建软链接，也不写入 personal Skill directory。
- Main Agent 是唯一 writer；所有生成角色保持 read-only。
- 不安装 CLI worker hook。当前 session 已经是 Claude Code，不能再套一层 `claude` CLI。

## Step 1：安装 Claude Code 入口

1. 检查项目是否已有根 `CLAUDE.md`、`.claude/agents/` 和 `.claude/skills/`。
2. 旧安装若包含 `<!-- compass:claude:start -->` / `<!-- compass:claude:end -->` import 区块，将该 legacy 区块原位替换为 canonical instructions 区块；标准 marker 与 legacy marker 同时存在或重复时停止并报告 conflict。
3. 其他情况按 `.compass/INSTALL.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块直接安装到根 `CLAUDE.md`。
4. 保留 marker 外的全部 Claude Code 和用户规则；不创建或依赖根 `AGENTS.md`。

## Step 2：安装 Claude Code project Skill

按 `.compass/INSTALL.md` Step 4 的 source inventory 和受管 copy 规则，将每个 `.compass/skills/<skill>/` 完整安装到：

```text
.claude/skills/<skill>/
```

保留 `.claude/skills/` 中其他名称的用户 Skill。同名 Skill 与 source 完全一致时复用；存在 legacy `.compass-generated` 时按总 installer 的 migration rule 更新并删除 marker；其他内容不同的同名 Skill 跳过并报告 conflict，不影响其他 Skill 和 Subagent 安装。

## Step 3：渲染内置与可选 Subagent

对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 渲染 `.compass/platforms/claude-code/agent.md.template`。
4. 将结果写入 `.claude/agents/<role>.md`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告该角色使用 Main Agent inline fallback。

Skill 和 Subagent 文件在当前 Claude Code session 启动后才安装或更新时，最终报告必须提醒用户在新 session 中验证 discovery；本轮仍须完成 filesystem validation。

## Step 4：验证

- [ ] 根 `CLAUDE.md` 包含且只包含一个最新 Compass 受管区块。
- [ ] 原有 `CLAUDE.md` 内容没有丢失。
- [ ] 新受管区块没有创建或依赖 `@AGENTS.md` import，旧 Compass import 区块已迁移。
- [ ] `.claude/skills/` 中每个无 conflict 的 Compass Skill 都包含 `SKILL.md` 和完整 resources，且没有 installer metadata file。
- [ ] 没有覆盖用户自建的同名 Skill，没有创建 Skill 软链接或修改 personal Skill directory。
- [ ] `sdd-reviewer` 已生成且保持只读，或明确记录 inline fallback。
- [ ] 未明确选择时没有生成 `codebase-explorer`。
- [ ] 每个已生成 agent 文件都有合法 frontmatter 和 generated 标记。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。
- [ ] 没有写入 Claude Code settings 或 `.claude/` 下的 CLI worker hook。

## 返回总安装器

报告：

```text
claude-code
- Instructions：根 CLAUDE.md（created / updated / reused）
- Skill destination：.claude/skills/
- Skills installed：...
- Skills reused：...
- Skills migrated：...（legacy marker removed）
- Skills conflict：...
- Skill metadata file：none
- Subagents：...
- Hooks：skipped（Claude Code is the worker）
- 创建：...
- 更新：...
- 跳过：...
- 冲突：...
- fallback：...
- 需要重启会话：是/否
- 验证：...
```

## 移除

只有总安装器正在执行用户明确要求的卸载时才处理：

1. 从根 `CLAUDE.md` 删除 Compass 标记区块，保留其他内容；文件只剩空白时才删除它。
2. Skill 不含 ownership marker；列出待移除的 `.claude/skills/<skill>/`，只有用户逐项明确确认后才删除，否则保留并报告 manual cleanup。
3. 只删除带 `compass:generated` 标记的 `.claude/agents/*.md`。
4. 保留用户自建 agent、settings 和其他 `.claude/` 内容。

## 官方参考

- [Claude Code memory](https://code.claude.com/docs/en/memory)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
