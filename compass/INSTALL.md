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
│   │   ├── L5-validation/
│   │   └── cli-worker.md
│   ├── skills/
│   ├── subagents/
│   ├── hooks/
│   └── platforms/
└── ...Project A files
```

`.compass/` 在安装期间同时承载 installation source 和项目上下文。Installer 必须先将 instructions、Skill 和 Subagent materialize 到每个已选平台的 project-level native destination，判定 CLI worker，必要时再安装 planner hook，完成验证，最后删除 `.compass/` 中除 `context/` 之外的全部 installation source。

安装完成后的稳定产物只有：

```text
projectA/
├── .compass/
│   └── context/
├── AGENTS.md or CLAUDE.md
├── platform-native Skill directories
├── platform-native Subagent files
├── planner-native CLI worker hooks（仅判定 enabled 时）
└── ...Project A files
```

如果目标项目是 Git worktree，installer 还必须在该 repository 的 local `info/exclude` 中维护一个 Compass 受管区块，使上述 `.compass/`、已选 platform instructions、Skills、Subagents 和已安装 hook 不进入项目的共享 Git 变更。该区块位于 Git metadata，不是 worktree 中的 installation artifact。

复制来的 `context/` 就是项目上下文，直接在其中填写事实；不再存在单独的 `context-template/`。每个已选平台默认生成一个只读 `sdd-reviewer`，作为 `develop` 的内部实现细节；用户不需要选择或编排它。Planner platform 是 Codex、Cursor 和 OpenCode。Claude Code 是 worker platform：当前 session 已经在 Claude Code 里时不安装 CLI worker hook。

`.compass/AGENTS.md`、`.compass/INSTALL.md`、`.compass/skills/`、`.compass/subagents/`、`.compass/hooks/` 和 `.compass/platforms/` 都是 installation staging，不是安装后的项目接口。

## 不可违反的安全规则

- 将 `.compass/` 的父目录视为目标项目根目录。
- `.compass/` 内不得包含它自己的 `.git/`。发现嵌套 Git 仓库时停止安装，要求用户确认后重新复制或移除该元数据。
- 如果 `.compass/` 在本次安装前已存在，禁止用复制命令覆盖它；先检查差异并请求用户决定合并方式。
- 安装前先读取目标项目现有规则、配置和 Git 状态。
- 不覆盖已有根 `AGENTS.md`、`CLAUDE.md`、`opencode.json` 或已有的项目上下文。
- 不删除旧 `.ai/`、用户 Skill 或其他历史文件；先迁移、验证并报告，再由用户决定是否删除。Step 9 规定的 installation staging cleanup 不受此条限制。
- 当前 installation staging 中的 `.compass/skills/` 是本次 Skill deployment source；平台 Skill directory 是 plain copy，不得反向作为 source。安装完成后的更新必须重新取得 Compass installation source。
- Skill 必须安装到已选平台的 project-level native directory，不创建 Skill 软链接，也不修改 global Skill directory。
- 已有同名平台 Skill 与本次 source 完全一致时复用；内容不同时不得自动覆盖，记录 conflict 并继续处理其他 Skill。
- `sdd-reviewer` 必须保持只读，Main Agent 是状态 owner。角色文件冲突或平台不支持时记录 inline fallback，不覆盖用户文件，也不阻断公共安装。
- CLI worker 是否可调用只在本次安装判定一次，并写入 `.compass/context/cli-worker.md`。不为这个再询问用户。后续 Skill 不重新探测、不把调用步骤抄进各个 Skill。
- 只有 `status=enabled` 时才给已选 planner 平台安装 worker hook。Claude Code 永不安装该 hook。
- Hook 与 Skill/agent 一样从 canonical source 按平台迁移；不写入 user-global hook directory，不创建软链接。
- 将 `.compass/` 和每个已选 platform 实际安装的 instruction、Skill、Subagent 与 hook 精确 path 写入 local Git exclude；不得忽略整个 platform parent directory，不得写入未安装的 conflict path。
- 不修改项目 `.gitignore`，不使用 `skip-worktree` 或 `assume-unchanged` 隐藏 tracked file。
- 遇到无法安全合并的现有文件时停止该项操作并向用户说明，不要猜测。

## Step 1：安装前检查

确认以下事实并记录结果：

1. 当前目标项目根目录。
2. `.compass/.git/` 不存在。
3. `.compass/INSTALL.md`、`AGENTS.md`、`context/`、`skills/` 和 `hooks/cli-worker/` 均存在。
4. 当前项目是否已有：
   - 根 `AGENTS.md`
   - 根 `CLAUDE.md`
   - 根 `opencode.json`
   - `.cursor/hooks.json` / `.codex/hooks.json`
   - 旧 `.ai/`
   - 由此前安装产生的 `.compass/context/` 项目事实
5. 用户需要 Codex、Cursor、Claude Code、OpenCode 中的哪些平台。能从请求明确判断时直接采用；无法判断时询问一次。
6. 可选 Subagent 只识别用户明确要求的 `codebase-explorer`；不要主动让用户选择。内置角色列表固定为 `sdd-reviewer`。
7. 目标项目是否位于 Git worktree 中。如果是，使用 `git rev-parse --git-path info/exclude` 取得实际 local exclude path，并检查其是否为 symlink、是否已有 Compass marker 以及哪些候选 artifact 已经 tracked。不要假设 Git metadata 一定位于目标根的实体 `.git/` directory。

## Step 2：填写或迁移项目上下文

复制来的 `.compass/context/` 是 L1–L5 的空白结构，也是项目唯一的上下文目录。不要创建 `context-template/` 或第二个 `context/`。`cli-worker.md` 属于 installer 填写的判定结果，到 Step 6 再写，不要在本步把它编成项目事实。

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
6. 不要把 CLI worker 调用步骤写进 instruction file；触发器是 hook。

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
8. 不把 CLI worker 步骤写进 Skill。

## Step 5：执行平台安装器

总安装器不实现平台专用文件格式。根据 Step 1 选择的平台，逐个读取并完整执行对应安装器的 Skill / instruction / Subagent 步骤。Hook 步骤留到 Step 6 判定之后。

| Platform | Kind | Installer |
|:---------|:-----|:----------|
| Codex | planner | `.compass/platforms/codex/INSTALL.md` |
| Cursor | planner | `.compass/platforms/cursor/INSTALL.md` |
| OpenCode | planner | `.compass/platforms/opencode/INSTALL.md` |
| Claude Code | worker | `.compass/platforms/claude-code/INSTALL.md` |

执行规则：

1. 先完成本文件 Step 2–4，再运行平台安装器。
2. 向每个平台安装器传入内置角色 `sdd-reviewer`，再追加 Step 1 得到的可选角色；默认列表不是空，而是 `[sdd-reviewer]`。
3. 平台安装器独占该平台 instruction destination、native Skill destination、Subagent 渲染和平台验证规则；不要在这里自行猜测格式。
4. 已选择多个平台时依次执行，分别保存创建、合并、跳过、冲突和验证结果。
5. 平台入口或配置发生无法安全合并的冲突时，停止该平台并报告。仅 `sdd-reviewer` 目标文件冲突时不覆盖，记录 inline fallback 后继续安装。
6. 本步不要安装 CLI worker hook。

## Step 6：判定 CLI worker 并安装 planner hook

本步整次安装只做一次，不按平台重复探测。不为这个再问用户。

Planner platforms：Codex、Cursor、OpenCode。

### 6a. 判定

1. 若本次 **没有** 选择任何 planner 平台（只选了 Claude Code）：将 `.compass/context/cli-worker.md` 填写为：

   ```text
   status: not-applicable
   reason: 当前安装没有 planner platform；Claude Code 自己就是 worker
   cli: claude
   invoke: none
   timeout-seconds: 600
   checked-at: <ISO-8601>
   ```

   不要探测 CLI，不要安装 hook。

2. 若已选至少一个 planner：在目标项目根探测本机 Claude Code CLI 是否 **可以调用**：
   - `command -v claude` 成功
   - `claude --version` 非交互退出码为 0
   两项都成立 → `enabled`。任一项失败 → `disabled`，`reason` 写明失败项。
   不安装 Claude Code、不写 `~/.claude`、不写 API key、不引导用户去装。

3. `enabled` 时填写：

   ```text
   status: enabled
   reason: 本机 claude CLI 可调用
   cli: claude
   invoke: claude -p --permission-mode acceptEdits
   timeout-seconds: 600
   checked-at: <ISO-8601>
   ```

   不要把 `--dangerously-skip-permissions` 写进 `invoke`。用 `--permission-mode acceptEdits`，让 headless CLI 能无人值守改文件，但不跳过全部权限。hook 会把这次 pending tool call pass 给该 invoke，由 CLI 做同一件动作。

4. 覆盖 `cli-worker.md` 里 installer 管理的字段，保留文件标题和说明段落。空白 `unknown` 不得留到安装完成。

### 6b. 安装 hook

1. 读取 `.compass/hooks/cli-worker/CONTRACT.md`。
2. 仅当 `status=enabled` 时，对每个已选 planner 平台执行该平台 installer 的 “CLI worker hook” 步骤，传入 `cli-worker=enabled`。
3. `disabled` 或 `not-applicable`：对所有平台传入 skip；Claude Code 即使同时被选也不安装该 hook。
4. Hook 冲突不阻断公共安装：记录 fallback（不自动调 CLI；Main Agent 自己做 implementation）。

用户以后才配置 `claude` 时，必须重新执行本次安装判定（或同等的 installer 探测步骤）才能把 status 改为 `enabled` 并补迁 hook。普通 `develop` 不得改这份文件。

## Step 7：维护 local Git exclude

本步只修改 repository-local Git metadata，不修改会被共享的 `.gitignore`。目标是将 `.compass/` 与已选 platform 的全部 Compass installation artifact 收口到一个可幂等更新的受管区块。

受管 marker 固定为：

```text
# compass:local-exclude:start
...
# compass:local-exclude:end
```

### Path inventory

| Artifact | 写入条件 | Pattern |
|:---------|:---------|:--------|
| Compass context 与 installation staging | 始终 | `/.compass/` |
| Platform instruction | 已选 platform 的 instruction 结果为 created、updated 或 reused；即使文件还有 marker 外内容也写入 | `/AGENTS.md` 或 `/CLAUDE.md` |
| Platform Skill | 该具体 Skill 的平台结果为 installed、reused 或 migrated；conflict 不写入 | 例如 `/.agents/skills/develop/` 或 `/.cursor/skills/develop/` |
| Platform Subagent | 该具体文件存在 Compass generated marker；fallback 或无 marker conflict 不写入 | 例如 `/.codex/agents/sdd-reviewer.toml` |
| CLI worker hook script | 该文件已安装 | 例如 `/.cursor/hooks/cli-worker.py` |
| CLI worker hook registration | Compass 已写入或更新该文件 | 例如 `/.cursor/hooks.json`、`/.codex/hooks.json`、`/.opencode/plugins/compass-cli-worker.js` |

执行规则：

1. 如果目标不是 Git worktree，记录 `not applicable` 并继续；不创建 `.git/` 或 `.gitignore`。
2. 根据本轮已选 platform 的真实安装结果生成 inventory。只写入 repository-root anchored 的精确 pattern，directory pattern 以 `/` 结尾；不写 `/.agents/`、`/.claude/`、`/.codex/`、`/.cursor/` 或 `/.opencode/` 这类宽泛 parent pattern。
3. 如果受管区块不存在，在保留现有 exclude content 的前提下追加一个区块；如果恰好存在一个完整区块，只替换 marker 之间的 inventory 并去重。已存在的用户 pattern 和 comment 原样保留。
4. 受管 marker 缺失、顺序错误或重复，或 local exclude 本身是 symlink 时，不改写该文件，将 installation 标记为 incomplete 并报告 conflict。
5. 对每个 inventory path 使用 `git check-ignore --no-index -v -- <path>` 验证命中本受管区块。同时确认 conflict path 没有被新增的宽泛 pattern 意外覆盖。
6. `info/exclude` 不影响 tracked file。已 tracked 的 instruction 或其他 Compass artifact 仍按 inventory 写入 pattern，但不运行 `git update-index`；保留其 Git 变更可见，并在最终报告列入 `tracked Compass paths still visible`。

## Step 8：公共验证

逐项检查：

- [ ] 每个已选平台的必读 instruction file 已由对应 platform installer 创建或合并。
- [ ] 每个受管 instruction file 的原有内容没有丢失，Compass 标记区块只出现一次。
- [ ] Platform installer 只修改已选平台需要的 destination；共用根 `AGENTS.md` 的平台只合并同一个受管区块。
- [ ] `.compass/context/` 存在，包含 L1–L5 和已填写的 `cli-worker.md`，且没有第二个 context 目录。
- [ ] `cli-worker.md` 的 `status` 是 `enabled`、`disabled` 或 `not-applicable`，不是 `unknown`。
- [ ] `status=enabled` 当且仅当已选至少一个 planner 且本机 `claude` 探测成功。
- [ ] `status=enabled` 时每个已选 planner 已安装 worker hook，或逐项记录 fallback；`disabled` / `not-applicable` 时没有 Compass worker hook。
- [ ] Claude Code 没有 CLI worker hook。
- [ ] 已有项目上下文没有被空白模板覆盖。
- [ ] `.compass/skills/` 包含 9 个 `SKILL.md`。
- [ ] 每个已选平台的 native Skill directory 都包含从 `.compass/skills/` 安装的 9 个 Skill，或逐项记录了未覆盖的同名 conflict。
- [ ] 每个已安装 Skill directory 都没有 `.compass-generated`、额外 README、manifest 或其他 installer metadata file。
- [ ] Skill 自带的 `references/`、`scripts/` 和 `assets/` 已随 Skill directory 完整安装。
- [ ] 没有 Skill 或 hook 软链接，也没有修改 global Skill / hook directory。
- [ ] 未选择的平台没有被创建 Skill directory 或写入 Skill。
- [ ] 每个支持的已选平台已生成只读 `sdd-reviewer`，或明确记录无 Subagent 的 inline fallback。
- [ ] 未明确选择可选角色时，没有生成 `codebase-explorer`。
- [ ] 每个已选平台的 `INSTALL.md` 均已执行并返回验证结果。
- [ ] 平台已有配置和用户内容没有丢失。
- [ ] Git worktree 中的 local exclude 包含且只包含一个 Compass 受管区块，其 inventory 覆盖 `/.compass/` 以及本轮已选 platform 实际安装的 instruction、Skill、Subagent 和 hook。非 Git 项目已记录 `not applicable`。
- [ ] Local exclude 中原有的用户 pattern 没有丢失，conflict path 和宽泛 platform parent directory 没有被新增到受管区块。
- [ ] 安装没有修改 `.gitignore`、没有设置 `skip-worktree` 或 `assume-unchanged`；tracked Compass path 仍可见的限制已被记录。
- [ ] Git diff 不包含无关或无法解释的修改。

## Step 9：清理 installation staging

只有 Step 8 的公共验证已经完成，且每个创建、更新、跳过或 conflict 都有明确结果时，才执行 cleanup。Cleanup 是安装成功的一部分，不能跳过。

1. 保留完整 `.compass/context/`，包括 L1–L5、`README.md`、`doc-sync.md`、已填写的 `cli-worker.md` 和已经填写的项目事实。
2. 删除 `.compass/` 下除 `context/` 之外的所有一级 entry，包括 `AGENTS.md`、`INSTALL.md`、`skills/`、`subagents/`、`hooks/`、`platforms/` 以及 installation package 中其他 source-only entry。删除目录或 symlink 时不得跟随到 `.compass/` 外部。
3. 确认 `.compass/` 的直接子项只有 `context/`；不得保留 installer、canonical copy、cache、manifest 或临时文件。
4. 再次确认平台 instructions、native Skill、Subagent 和已安装 hook 仍存在，且不通过 import、symlink 或 runtime path 依赖已删除的 installation source。
5. 如果 Step 8 未完成或 cleanup 无法安全执行，不得报告“安装完成”；保留 installation staging，报告 incomplete 状态和具体 blocker，供下一次重试。

安装完成后的 `.compass/` 必须满足：

```text
.compass/
└── context/
```

## Step 10：最终报告

最终对话报告是唯一的 installation report。除 Git metadata 中必需的 local exclude 受管区块外，不要为了保存安装结果在 worktree 中创建 marker、manifest、report Markdown 或其他 metadata file。`cli-worker.md` 是项目 context，不是 installation report。

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
    - Hooks：installed / skipped / fallback / conflict / none
  - cursor：...
  - claude-code：...
  - opencode：...
- CLI worker：enabled / disabled / not-applicable
- CLI worker reason：...
- 冲突或待确认：...
- 旧路径待清理：...
- 最终产物：platform instructions、native Skills、native Subagents、optional planner hooks、.compass/context/
- Local Git exclude：updated / reused / not applicable / conflict
- Excluded Compass paths：...
- Tracked Compass paths still visible：...
- Installation manifest/report file：none
- Installation staging cleanup：completed（.compass/ 仅保留 context/）
- 验证结果：...
```

每个已选 platform 必须逐项列出 Skill name；没有对应结果时写 `none`，不要省略字段。不得只回复“安装完成”。Codex hook 若需要 `/hooks` trust，在验证结果中写明。

## 移除

只有用户明确要求卸载时才执行：

1. 目标项目不会保留 platform installer。重新取得与待卸载版本兼容的 Compass installation package，并从临时 staging 中读取对应 `platforms/<platform>/INSTALL.md` 的“移除”章节。
2. 对每个已安装平台执行移除规则。Instructions、Subagent 与 generated hook 只按各自的 inline generated marker 或可识别 command path 删除；Skill 没有 ownership metadata，不得自动删除，必须列出具体路径并取得用户明确确认。
3. 删除本次卸载使用的临时 installation staging，不要把它留在目标项目中。
4. `.compass/context/` 属于项目上下文，默认保留（包括 `cli-worker.md`）；只有用户明确要求删除项目上下文时才删除整个 `.compass/`。`.compass/context/L4-session/cli-worker.lock` 是 CLI worker 的 runtime 锁文件，不是项目知识；卸载 hook 时可删除它。
5. 如果存在 Compass local exclude 受管区块，只移除已经实际删除或已不再属于 Compass installation 的 artifact pattern；仍保留的 Skill 和 `.compass/context/` 继续保留对应 pattern。区块变空时只删除该区块，不改动其他 local exclude content。
