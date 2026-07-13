# OpenCode Platform Installer

> 本文件由 `.compass/INSTALL.md` 调用，只负责 OpenCode 的项目入口和可选 Subagent 适配。

## 输入

- 目标项目根目录。
- 已完成公共安装的根 `AGENTS.md`、`.compass/context/` 和 `.compass/skills/`。
- 用户明确选择的 Subagent 角色列表；默认是空列表。

## 平台边界

- OpenCode 原生读取项目根 `AGENTS.md`，基础安装不需要创建或修改 `opencode.json`。
- 不通过 `opencode.json.instructions` 再加载一次根 `AGENTS.md`。
- Skills 仍只保存在 `.compass/skills/`，由 `AGENTS.md` 指引按需读取。
- 不创建其他 Skill 目录，不复制或软链接 Skill。
- 只有角色列表非空时，才创建项目级 `.opencode/agents/` 文件。

## Step 1：检查 OpenCode 入口

1. 确认根 `AGENTS.md` 存在且包含一个 Compass 标记区块。
2. 检查项目是否已有 `opencode.json`、`opencode.jsonc` 和 `.opencode/agents/`。
3. 已有 OpenCode 配置全部保留；基础安装不需要修改这些文件。

## Step 2：确认 Skill 访问方式

确认根 `AGENTS.md` 要求 OpenCode 在任务匹配时直接读取 `.compass/skills/<skill>/SKILL.md`。不安装第二份 Skill。

## Step 3：按需渲染 Subagent

角色列表为空时跳过本步骤，并且不创建 `.opencode/agents/`。

对每个已选择角色：

1. 读取 `.compass/subagents/<role>.md`。
2. 确认它包含 `Purpose`、`Delegate only when`、`Access`、`Instructions` 和 `Output contract`。
3. 渲染 `.compass/platforms/opencode/agent.md.template`。
4. 将结果写入 `.opencode/agents/<role>.md`；文件名就是 OpenCode 中的角色名。
5. 目标文件不存在时创建；存在 Compass generated 标记时更新；存在但没有标记时停止该角色并报告冲突。

## Step 4：验证

- [ ] 根 `AGENTS.md` 可用。
- [ ] 没有创建或修改 `opencode.json` / `opencode.jsonc`。
- [ ] 没有通过 instructions 重复加载根 `AGENTS.md`。
- [ ] 没有复制或软链接 Skill。
- [ ] 未选择角色时没有创建 `.opencode/agents/`。
- [ ] 每个已生成 agent 文件都有 `description`、`mode: subagent`、权限配置和 generated 标记。
- [ ] 没有覆盖无 Compass 标记的已有 agent 文件。

## 返回总安装器

报告：

```text
opencode
- 入口：复用根 AGENTS.md
- 创建：...
- 更新：...
- 跳过：...
- 冲突：...
- 验证：...
```

## 移除

只有总安装器正在执行用户明确要求的卸载时才处理：

1. 只删除带 `compass:generated` 标记的 `.opencode/agents/*.md`。
2. 保留用户自建 agent、`opencode.json`、`opencode.jsonc` 和其他 `.opencode/` 内容。
3. 平台目录变空时可删除 `.opencode/agents/` 空目录；不要删除仍有其他内容的 `.opencode/`。

## 官方参考

- [OpenCode rules](https://opencode.ai/docs/rules)
- [OpenCode agents](https://opencode.ai/docs/agents/)
