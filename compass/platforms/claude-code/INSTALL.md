# Claude Code Platform Installer

> 本文件由 `.compass/INSTALL.md` 调用，只负责 Claude Code 的项目入口和可选 Subagent。本版本不安装 Compass Skill，也不安装 CLI worker hook。

## 输入

- 目标项目根目录。
- 已准备好的 `.compass/AGENTS.md` 和 `.compass/context/`。
- Subagent 角色列表；默认空。可追加用户明确要求的 `codebase-explorer`。

## 平台边界

- Claude Code 原生读取根 `CLAUDE.md`；本 installer 将 canonical instructions 直接合并到该文件。
- 不通过 `@AGENTS.md` 或其他 instruction file 间接加载规则。
- 不安装 Compass Skill，不创建 `.claude/skills/` 来承载 Compass Skill。
- 不安装 CLI worker hook。当前 session 已经是 Claude Code，不能再套一层 `claude` CLI。

## Step 1：安装 Claude Code 入口

1. 检查项目是否已有根 `CLAUDE.md`、`.claude/agents/`。
2. 旧安装若包含 `<!-- compass:claude:start -->` / `<!-- compass:claude:end -->` import 区块，将该 legacy 区块原位替换为 canonical instructions 区块；标准 marker 与 legacy marker 同时存在或重复时停止并报告 conflict。
3. 其他情况按 `.compass/INSTALL.md` Step 3 的受管 merge 规则，将 `.compass/AGENTS.md` 区块直接安装到根 `CLAUDE.md`。
4. 保留 marker 外的全部 Claude Code 和用户规则；不创建或依赖根 `AGENTS.md`。

## Step 2：跳过 Compass Skill

报告 `Skills：none`。不要复制 Skill，不要新建 `.claude/skills/`。

## Step 3：渲染可选 Subagent

角色列表为空时跳过。对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 渲染 `.compass/platforms/claude-code/agent.md.template`。
4. 将结果写入 `.claude/agents/<role>.md`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时不覆盖，报告 inline fallback。

## Step 4：验证

- [ ] 根 `CLAUDE.md` 包含且只包含一个最新 Compass 受管区块，且含 Project Knowledge 约定。
- [ ] 原有 `CLAUDE.md` 内容没有丢失。
- [ ] 新受管区块没有创建或依赖 `@AGENTS.md` import。
- [ ] 没有为 Compass 创建或写入 `.claude/skills/`。
- [ ] 未明确选择时没有生成 Subagent。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。
- [ ] 没有写入 Claude Code settings 或 `.claude/` 下的 CLI worker hook。

## 返回总安装器

```text
claude-code
- Instructions：根 CLAUDE.md（created / updated / reused）
- Skills：none
- Subagents：none / ...
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

1. 从根 `CLAUDE.md` 删除 Compass 标记区块，保留其他内容。
2. 不自动删除用户 Skill。
3. 只删除带 `compass:generated` 标记的 `.claude/agents/*.md`。
4. 不删除根 `README.md` 或 `doc/`。

## 官方参考

- [Claude Code memory](https://code.claude.com/docs/en/memory)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
