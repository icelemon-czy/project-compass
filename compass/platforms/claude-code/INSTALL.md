# Claude Code Platform Installer

> 本文件由 `.compass/INSTALL.md` 调用，只负责 Claude Code 的项目入口和可选 Subagent 适配。

## 输入

- 目标项目根目录。
- 已完成公共安装的根 `AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- 用户明确选择的 Subagent 角色列表；默认是空列表。

## 平台边界

- Claude Code 原生读取 `CLAUDE.md`，通过 `@AGENTS.md` 导入共享项目规则。
- 不把 `AGENTS.md` 正文复制到 `CLAUDE.md`。
- Skills 仍只保存在 `.compass/skills/`，由导入的 `AGENTS.md` 指引按需读取。
- 不创建 `.claude/skills`，不复制或软链接 Skill。
- 只有角色列表非空时，才创建项目级 `.claude/agents/` 文件。

## Step 1：安装 Claude Code 入口

处理目标项目根 `CLAUDE.md`：

- 不存在：使用 `.compass/platforms/claude-code/CLAUDE.md.template` 创建。
- 已存在且包含 `@AGENTS.md`：保留原文件，记录为复用。
- 已存在 Compass 标记区块：只更新标记区块。
- 已存在但没有导入：保留全部原内容，在合适位置追加模板区块。
- 是软链接或无法安全编辑：停止该项并报告，不替换目标。

## Step 2：确认 Skill 访问方式

确认 `CLAUDE.md` 导入根 `AGENTS.md`，且根规则要求 Claude Code 在任务匹配时直接读取 `.compass/skills/<skill>/SKILL.md`。不安装第二份 Skill。

## Step 3：按需渲染 Subagent

角色列表为空时跳过本步骤，并且不创建 `.claude/agents/`。

对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 渲染 `.compass/platforms/claude-code/agent.md.template`。
4. 将结果写入 `.claude/agents/<role>.md`。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时停止该角色并报告冲突。

Subagent 文件在 Claude Code 会话启动时加载；如果当前会话中刚创建文件，最终报告必须提醒用户重新启动会话后再验证角色发现。

## Step 4：验证

- [ ] 根 `CLAUDE.md` 存在并且只导入一次 `@AGENTS.md`。
- [ ] 原有 `CLAUDE.md` 内容没有丢失。
- [ ] 没有复制 `AGENTS.md` 正文。
- [ ] 没有复制或软链接 Skill。
- [ ] 未选择角色时没有创建 `.claude/agents/`。
- [ ] 每个已生成 agent 文件都有合法 frontmatter 和 generated 标记。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。

## 返回总安装器

报告：

```text
claude-code
- 入口：...
- 创建：...
- 更新：...
- 跳过：...
- 冲突：...
- 需要重启会话：是/否
- 验证：...
```

## 移除

只有总安装器正在执行用户明确要求的卸载时才处理：

1. 从根 `CLAUDE.md` 删除 Compass 标记区块，保留其他内容；文件只剩空白时才删除它。
2. 只删除带 `compass:generated` 标记的 `.claude/agents/*.md`。
3. 保留用户自建 agent、settings 和其他 `.claude/` 内容。

## 官方参考

- [Claude Code memory and AGENTS.md import](https://code.claude.com/docs/en/memory#agentsmd)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
