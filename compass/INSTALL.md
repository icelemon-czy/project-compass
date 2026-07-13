# Compass Installation Contract

> 本文件供安装 Agent 阅读和执行。Compass 不提供安装脚本；Agent 必须根据目标项目的现状进行非破坏安装。

## 目标

用户已将 `compass/` 复制为目标项目的 `.compass/`：

```text
projectA/
├── .compass/
│   ├── INSTALL.md
│   ├── AGENTS.md
│   ├── context/
│   │   ├── L1-codebase-map/
│   │   ├── L2-rules/
│   │   ├── L3-specs/
│   │   ├── L4-session/
│   │   └── L5-validation/
│   ├── skills/
│   ├── subagents/
│   └── platforms/
└── ...Project A files
```

安装完成后，项目使用 `.compass/skills/` 作为唯一 Skill 内容源。复制来的 `context/` 就是项目上下文，直接在其中填写事实；不再存在单独的 `context-template/`。四个 Subagent 角色定义保持可选，默认不生成任何实例。

## 不可违反的安全规则

- 将 `.compass/` 的父目录视为目标项目根目录。
- `.compass/` 内不得包含它自己的 `.git/`。发现嵌套 Git 仓库时停止安装，要求用户确认后重新复制或移除该元数据。
- 如果 `.compass/` 在本次安装前已存在，禁止用复制命令覆盖它；先检查差异并请求用户决定合并方式。
- 安装前先读取目标项目现有规则、配置和 Git 状态。
- 不覆盖已有根 `AGENTS.md`、`CLAUDE.md`、`opencode.json` 或已有的项目上下文。
- 不删除旧 `.ai/`、旧 Skill 或其他历史文件；先迁移、验证并报告，再由用户决定是否删除。
- 不复制 13 个 Skill 到多个目录，也不创建任何 Skill 软链接。Agent 直接从 `.compass/skills/` 读取所需 `SKILL.md`。
- 默认不安装 Subagent，不创建 `.codex/agents/`、`.claude/agents/` 或 `.opencode/agents/`。
- 遇到无法安全合并的现有文件时停止该项操作并向用户说明，不要猜测。

## Step 1：安装前检查

确认以下事实并记录结果：

1. 当前目标项目根目录。
2. `.compass/.git/` 不存在。
3. `.compass/INSTALL.md`、`AGENTS.md`、`context/` 和 `skills/` 均存在。
4. 当前项目是否已有：
   - 根 `AGENTS.md`
   - 根 `CLAUDE.md`
   - 根 `opencode.json`
   - 旧 `.ai/`
   - 由此前安装产生的 `.compass/context/` 项目事实
5. 用户需要 Codex、Claude Code、OpenCode 中的哪些平台。能从请求明确判断时直接采用；无法判断时询问一次。
6. 用户是否明确要求安装某些 Subagent 角色。没有明确要求时，所选角色列表必须为空。

## Step 2：填写或迁移项目上下文

复制来的 `.compass/context/` 是 L1–L5 的空白结构，也是项目唯一的上下文目录。不要创建 `context-template/` 或第二个 `context/`。

### 新安装

直接在现有 `context/` 中填写当前项目真正需要的最小事实。空白字段和示例不得被描述为项目事实。

### 已有项目上下文

如果 `context/` 已包含已确认的项目事实，保留并复用它；只在安全且必要时补充缺失内容，不从空白文件覆盖它。

### 只有旧 `.ai/`

1. 将 `.ai/` 中已确认、仍适用的内容迁移到现有 `.compass/context/` 对应层级。
2. 检查关键目录和 Markdown 文件已经迁移。
3. 更新新目录内部仍指向 `.ai/` 的当前路径引用。
4. 保留原 `.ai/`，在最终报告中列为“待用户确认清理”。

## Step 3：合并项目 AGENTS.md

规则基线位于 `.compass/AGENTS.md`，由以下标记包围：

```text
<!-- compass:start -->
...
<!-- compass:end -->
```

处理目标项目根 `AGENTS.md`：

- 不存在：创建文件并写入完整 Compass 标记区块。
- 已存在但没有标记区块：保留全部原内容，在合适位置追加区块。
- 已存在标记区块：只更新两个标记之间的内容，保留标记外的项目规则。

合并后必须确认根 `AGENTS.md` 同时保留原项目规则和 Compass 区块。

## Step 4：直接使用唯一 Skill 源

唯一 Skill 内容源：

```text
.compass/skills/
```

不创建 `.agents/skills`、`.claude/skills` 或其他平台 Skill 目录。

- 工作流规则只保存在 `.compass/skills/`。
- 根 `AGENTS.md` 已要求 Agent 在任务匹配工作流时直接读取相应 `SKILL.md`。
- Agent 必须按 Skill 的名称和 description 判断该读哪个 `SKILL.md`，再按其中导航只读取当前任务需要的 `references/`；不复制、不链接、不生成镜像。

## Step 5：执行平台安装器

总安装器不实现平台专用文件格式。根据 Step 1 选择的平台，逐个读取并完整执行对应安装器：

| Platform | Installer |
|:---------|:----------|
| Codex | `.compass/platforms/codex/INSTALL.md` |
| Claude Code | `.compass/platforms/claude-code/INSTALL.md` |
| OpenCode | `.compass/platforms/opencode/INSTALL.md` |

执行规则：

1. 先完成本文件 Step 2–4，再运行平台安装器。
2. 把 Step 1 得到的 Subagent 角色列表传给每个平台安装器；默认传空列表。
3. 平台安装器独占该平台入口、配置、Subagent 渲染和平台验证规则；不要在这里自行猜测格式。
4. 已选择多个平台时依次执行，分别保存创建、合并、跳过、冲突和验证结果。
5. 任一平台安装器缺失或发生无法安全合并的冲突时，不得静默跳过；停止该平台并向用户报告。

## Step 6：公共验证

逐项检查：

- [ ] 目标项目根 `AGENTS.md` 存在。
- [ ] 原有 `AGENTS.md` 内容没有丢失。
- [ ] Compass 标记区块只出现一次。
- [ ] `.compass/context/` 存在，包含 L1–L5，且没有第二个 context 目录。
- [ ] 已有项目上下文没有被空白模板覆盖。
- [ ] `.compass/skills/` 包含 13 个 `SKILL.md`。
- [ ] Agent 能从根 `AGENTS.md` 找到并读取 `.compass/skills/`。
- [ ] Skill 自带的 `references/` 仍位于同一 Skill 目录，且能按 `SKILL.md` 导航读取。
- [ ] 没有第二份复制的内置 Skill 内容。
- [ ] 没有 `.agents/skills`、`.claude/skills` 或其他 Skill 软链接。
- [ ] 未明确选择 Subagent 时，没有生成任何平台 Subagent 文件。
- [ ] 每个已选平台的 `INSTALL.md` 均已执行并返回验证结果。
- [ ] 平台已有配置和用户内容没有丢失。
- [ ] Git diff 不包含无关或无法解释的修改。

## Step 7：最终报告

向用户报告：

```text
安装结果
- 项目根目录：...
- 启用平台：...
- 平台结果：
  - codex：...
  - claude-code：...
  - opencode：...
- 安装的 Subagent：...
- 创建：...
- 合并：...
- 复用：...
- 跳过：...
- 冲突或待确认：...
- 旧路径待清理：...
- 验证结果：...
```

不得只回复“安装完成”。

## 移除

只有用户明确要求卸载时才执行：

1. 对每个已安装平台，先读取并执行对应 `platforms/<platform>/INSTALL.md` 中的“移除”章节。
2. 从根 `AGENTS.md` 删除 Compass 标记区块，保留其他规则。
3. `.compass/context/` 属于项目上下文，默认保留。
4. 最后是否删除整个 `.compass/` 必须由用户确认。
