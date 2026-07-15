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

`.compass/` 在安装期间同时承载 installation source 和项目上下文。Installer 必须先将 instructions、Skill 和 Subagent materialize 到每个已选平台的 project-level native destination，再完成验证，最后删除 `.compass/` 中除 `context/` 之外的全部 installation source。

安装完成后的稳定产物只有：

```text
projectA/
├── .compass/
│   └── context/
│       ├── L1-codebase-map/
│       ├── L2-rules/
│       ├── L3-specs/
│       ├── L4-session/
│       └── L5-validation/
├── AGENTS.md or CLAUDE.md
├── platform-native Skill directories
├── platform-native Subagent files
└── ...Project A files
```

复制来的 `context/` 就是项目上下文，直接在其中填写事实；不再存在单独的 `context-template/`。每个已选平台默认生成一个只读 `sdd-reviewer`，作为 `develop` 的内部实现细节；用户不需要选择或编排它。`.compass/AGENTS.md`、`.compass/INSTALL.md`、`.compass/skills/`、`.compass/subagents/` 和 `.compass/platforms/` 都是 installation staging，不是安装后的项目接口。

## 不可违反的安全规则

- 将 `.compass/` 的父目录视为目标项目根目录。
- `.compass/` 内不得包含它自己的 `.git/`。发现嵌套 Git 仓库时停止安装，要求用户确认后重新复制或移除该元数据。
- 如果 `.compass/` 在本次安装前已存在，禁止用复制命令覆盖它；先检查差异并请求用户决定合并方式。
- 安装前先读取目标项目现有规则、配置和 Git 状态。
- 不覆盖已有根 `AGENTS.md`、`CLAUDE.md`、`opencode.json` 或已有的项目上下文。
- 不删除旧 `.ai/`、用户 Skill 或其他历史文件；先迁移、验证并报告，再由用户决定是否删除。Step 7 规定的 installation staging cleanup 不受此条限制。
- 当前 installation staging 中的 `.compass/skills/` 是本次 Skill deployment source；平台 Skill directory 是 plain copy，不得反向作为 source。安装完成后的更新必须重新取得 Compass installation source。
- Skill 必须安装到已选平台的 project-level native directory，不创建 Skill 软链接，也不修改 global Skill directory。
- 已有同名平台 Skill 与本次 source 完全一致时复用；内容不同时不得自动覆盖，记录 conflict 并继续处理其他 Skill。
- `sdd-reviewer` 必须保持只读，Main Agent 是唯一 writer 和状态 owner。角色文件冲突或平台不支持时记录 inline fallback，不覆盖用户文件，也不阻断公共安装。
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
6. 可选 Subagent 只识别用户明确要求的 `codebase-explorer`；不要主动让用户选择。内置角色列表固定为 `sdd-reviewer`。

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

## Step 3：准备 platform instructions

本次安装的 instructions source 位于 `.compass/AGENTS.md`，由以下标记包围：

```text
<!-- compass:start -->
...
<!-- compass:end -->
```

本步骤只定义统一的受管 merge 规则；实际 destination 由 Step 5 的 platform installer 决定。

1. Destination 不存在时创建文件并写入完整受管区块。
2. Destination 已存在但没有受管区块时，保留全部原内容并追加区块。
3. Destination 已存在受管区块时，只更新两个 marker 之间的内容，保留 marker 外的平台或用户规则。
4. Destination 是软链接、包含重复 marker 或无法安全编辑时，不替换、不猜测，停止该平台并报告 conflict。
5. 不通过 import 或第二个 instruction file 间接加载 installation source；每个平台的必读文件直接包含受管区块。

## Step 4：准备 Skill deployment

本次安装的 Skill source：

```text
.compass/skills/<skill>/
```

本步骤只确认 source inventory 和统一的受管 copy 规则；实际 destination 及安装操作由 Step 5 的 platform installer 负责。

1. 只把包含合法 `SKILL.md` 的一级子目录识别为待安装 Skill。
2. 递归复制整个 Skill directory，包括 `references/`、`scripts/` 和 `assets/`；不只复制 `SKILL.md`。
3. Destination 不存在时创建完整 copy；不要附加 marker、README、manifest 或其他 Skill-local metadata file。
4. Destination 已存在且递归内容与本次 source 完全一致时直接复用，不重写文件。
5. 旧安装若包含 `.compass-generated`，只在本次 migration 中把它作为 legacy ownership evidence：从本次 source 完整更新 Skill 后删除该 marker，且不创建替代 metadata file。
6. Destination 已存在、没有 legacy marker 且内容与 source 不同时，不覆盖、不合并，记录该 Skill conflict。只有用户明确批准替换该具体 Skill 时才可更新。
7. 不创建软链接，不向 `$HOME` 或其他 global Skill directory 安装。

## Step 5：执行平台安装器

总安装器不实现平台专用文件格式。根据 Step 1 选择的平台，逐个读取并完整执行对应安装器：

| Platform | Installer |
|:---------|:----------|
| Codex | `.compass/platforms/codex/INSTALL.md` |
| Claude Code | `.compass/platforms/claude-code/INSTALL.md` |
| OpenCode | `.compass/platforms/opencode/INSTALL.md` |

执行规则：

1. 先完成本文件 Step 2–4，再运行平台安装器。
2. 向每个平台安装器传入内置角色 `sdd-reviewer`，再追加 Step 1 得到的可选角色；默认列表不是空，而是 `[sdd-reviewer]`。
3. 平台安装器独占该平台 instruction destination、native Skill destination、Subagent 渲染和平台验证规则；不要在这里自行猜测格式。
4. 已选择多个平台时依次执行，分别保存创建、合并、跳过、冲突和验证结果。
5. 平台入口或配置发生无法安全合并的冲突时，停止该平台并报告。仅 `sdd-reviewer` 目标文件冲突时不覆盖，记录 inline fallback 后继续安装。

## Step 6：公共验证

逐项检查：

- [ ] 每个已选平台的必读 instruction file 已由对应 platform installer 创建或合并。
- [ ] 每个受管 instruction file 的原有内容没有丢失，Compass 标记区块只出现一次。
- [ ] Platform installer 只修改已选平台需要的 destination；Codex 与 OpenCode 共用根 `AGENTS.md` 时只合并同一个受管区块。
- [ ] `.compass/context/` 存在，包含 L1–L5，且没有第二个 context 目录。
- [ ] 已有项目上下文没有被空白模板覆盖。
- [ ] `.compass/skills/` 包含 9 个 `SKILL.md`。
- [ ] 每个已选平台的 native Skill directory 都包含从 `.compass/skills/` 安装的 9 个 Skill，或逐项记录了未覆盖的同名 conflict。
- [ ] 每个已安装 Skill directory 都没有 `.compass-generated`、额外 README、manifest 或其他 installer metadata file。
- [ ] Skill 自带的 `references/`、`scripts/` 和 `assets/` 已随 Skill directory 完整安装。
- [ ] 没有 Skill 软链接，也没有修改 global Skill directory。
- [ ] 未选择的平台没有被创建 Skill directory 或写入 Skill。
- [ ] 每个支持的已选平台已生成只读 `sdd-reviewer`，或明确记录无 Subagent 的 inline fallback。
- [ ] 未明确选择可选角色时，没有生成 `codebase-explorer`。
- [ ] 每个已选平台的 `INSTALL.md` 均已执行并返回验证结果。
- [ ] 平台已有配置和用户内容没有丢失。
- [ ] Git diff 不包含无关或无法解释的修改。

## Step 7：清理 installation staging

只有 Step 6 的公共验证已经完成，且每个创建、更新、跳过或 conflict 都有明确结果时，才执行 cleanup。Cleanup 是安装成功的一部分，不能跳过。

1. 保留完整 `.compass/context/`，包括 L1–L5、`README.md`、`doc-sync.md` 和已经填写的项目事实。
2. 删除 `.compass/` 下除 `context/` 之外的所有一级 entry，包括 `AGENTS.md`、`INSTALL.md`、`skills/`、`subagents/`、`platforms/` 以及 installation package 中其他 source-only entry。删除目录或 symlink 时不得跟随到 `.compass/` 外部。
3. 确认 `.compass/` 的直接子项只有 `context/`；不得保留 installer、canonical copy、cache、manifest 或临时文件。
4. 再次确认平台 instructions、native Skill 和 Subagent 仍存在，且不通过 import、symlink 或 runtime path 依赖已删除的 installation source。
5. 如果 Step 6 未完成或 cleanup 无法安全执行，不得报告“安装完成”；保留 installation staging，报告 incomplete 状态和具体 blocker，供下一次重试。

安装完成后的 `.compass/` 必须满足：

```text
.compass/
└── context/
```

## Step 8：最终报告

最终对话报告是唯一的 installation record。不要为了保存安装结果在项目中创建 marker、manifest、report Markdown 或其他 metadata file。

向用户报告：

```text
安装结果
- 项目根目录：...
- 启用平台：...
- 平台结果：
  - codex：
    - Instructions：created / updated / reused / conflict
    - Skills installed：skill-a, skill-b, ...
    - Skills reused：...
    - Skills migrated：...（如有，legacy marker 已删除）
    - Skills conflict：...
    - Subagents：...
  - claude-code：...
  - opencode：...
- 冲突或待确认：...
- 旧路径待清理：...
- 最终产物：platform instructions、native Skills、native Subagents、.compass/context/
- Installation metadata file：none
- Installation staging cleanup：completed（.compass/ 仅保留 context/）
- 验证结果：...
```

每个已选 platform 必须逐项列出 Skill name；没有对应结果时写 `none`，不要省略字段。不得只回复“安装完成”。

## 移除

只有用户明确要求卸载时才执行：

1. 目标项目不会保留 platform installer。重新取得与待卸载版本兼容的 Compass installation package，并从临时 staging 中读取对应 `platforms/<platform>/INSTALL.md` 的“移除”章节。
2. 对每个已安装平台执行移除规则。Instructions 与 Subagent 只按各自的 inline generated marker 删除；Skill 没有 ownership metadata，不得自动删除，必须列出具体路径并取得用户明确确认。
3. 删除本次卸载使用的临时 installation staging，不要把它留在目标项目中。
4. `.compass/context/` 属于项目上下文，默认保留；只有用户明确要求删除项目上下文时才删除整个 `.compass/`。
