# Compass Installation Contract

> 本文件供安装 Agent 阅读和执行。Compass 不提供安装脚本；Agent 必须根据目标项目的现状进行非破坏安装。
>
> 本版本是 **simplify**：不安装 Compass Skill，不填写 L1–L5。项目知识在根 `README.md`、`doc/<feature>_design.md` 和 `doc/todo.md`。

## 目标

用户已将 `compass/` 复制为目标项目的 `.compass/`：

```text
projectA/
├── .compass/
│   ├── INSTALL.md
│   ├── AGENTS.md
│   ├── context/
│   │   └── cli-worker.md
│   ├── subagents/
│   ├── hooks/
│   └── platforms/
├── README.md
├── doc/
│   ├── todo.md
│   └── <feature>_design.md
└── ...Project A files
```

`.compass/` 在安装期间承载 installation source。Installer 必须先将 instructions 和可选 Subagent materialize 到每个已选平台的 native destination，判定 CLI worker，必要时再安装 planner hook，完成验证，最后删除 `.compass/` 中除 `context/` 之外的全部 installation source。

安装完成后的稳定产物只有：

```text
projectA/
├── .compass/
│   └── context/
├── AGENTS.md or CLAUDE.md
├── README.md
├── doc/
├── 可选 platform-native Subagent files
├── planner-native CLI worker hooks（仅判定 enabled 时）
└── ...Project A files
```

如果目标项目是 Git worktree，installer 还必须在该 repository 的 local `info/exclude` 中维护一个 Compass 受管区块，使 `.compass/`、已选 platform instructions、Subagents 和已安装 hook 不进入项目的共享 Git 变更。**不要**把根 `README.md` 或 `doc/` 写入 exclude；它们是项目知识，应当被 Git 跟踪。

复制来的 `context/` 只用于 `cli-worker.md`。不要在其中填写项目描述、design 或 todo。默认不生成 Subagent；`codebase-explorer` 只有用户明确要求时才安装。Planner platform 是 Codex、Cursor 和 OpenCode。Claude Code 是 worker platform：当前 session 已经在 Claude Code 里时不安装 CLI worker hook。

`.compass/AGENTS.md`、`.compass/INSTALL.md`、`.compass/subagents/`、`.compass/hooks/` 和 `.compass/platforms/` 都是 installation staging，不是安装后的项目接口。

## 不可违反的安全规则

- 将 `.compass/` 的父目录视为目标项目根目录。
- `.compass/` 内不得包含它自己的 `.git/`。发现嵌套 Git 仓库时停止安装，要求用户确认后重新复制或移除该元数据。
- 如果 `.compass/` 在本次安装前已存在，禁止用复制命令覆盖它；先检查差异并请求用户决定合并方式。
- 安装前先读取目标项目现有规则、配置和 Git 状态。
- 不覆盖已有根 `AGENTS.md`、`CLAUDE.md`、`opencode.json`、根 `README.md` 或 `doc/` 下的已有文件。
- 不删除旧 `.ai/`、用户 Skill 或其他历史文件；先报告，再由用户决定是否删除。Step 8 规定的 installation staging cleanup 不受此条限制。
- **不安装 Compass Skill。** 不创建平台 Skill directory 来承载 Compass Skill，不创建 Skill 软链接，也不修改 global Skill directory。用户自建 Skill 全部保留。
- 不创建 L1–L5、Spec、proposal 或 `.compass/context/` 下除 `cli-worker.md` 与 `README.md` 以外的项目文档。
- CLI worker 是否可调用只在本次安装判定一次，并写入 `.compass/context/cli-worker.md`。不为这个再询问用户。
- 只有 `status=enabled` 时才给已选 planner 平台安装 worker hook。Claude Code 永不安装该 hook。
- Hook 从 canonical source 按平台迁移；不写入 user-global hook directory，不创建软链接。
- 将 `.compass/` 和每个已选 platform 实际安装的 instruction、Subagent 与 hook 精确 path 写入 local Git exclude；不得忽略整个 platform parent directory；不得 exclude `README.md` 或 `doc/`。
- 不修改项目 `.gitignore`，不使用 `skip-worktree` 或 `assume-unchanged` 隐藏 tracked file。
- 遇到无法安全合并的现有文件时停止该项操作并向用户说明，不要猜测。

## Step 1：安装前检查

确认以下事实并记录结果：

1. 当前目标项目根目录。
2. `.compass/.git/` 不存在。
3. `.compass/INSTALL.md`、`AGENTS.md`、`context/` 和 `hooks/cli-worker/` 均存在。本版本 **没有** `.compass/skills/`。
4. 当前项目是否已有：
   - 根 `AGENTS.md` / `CLAUDE.md` / `opencode.json`
   - 根 `README.md`
   - `doc/todo.md` 与 `doc/*_design.md`
   - `.cursor/hooks.json` / `.codex/hooks.json`
   - 旧 `.ai/` 或旧 L1–L5 `.compass/context/`
5. 用户需要 Codex、Cursor、Claude Code、OpenCode 中的哪些平台。能从请求明确判断时直接采用；无法判断时询问一次。
6. 可选 Subagent 只识别用户明确要求的 `codebase-explorer`；不要主动让用户选择。默认角色列表为空。
7. 目标项目是否位于 Git worktree 中。如果是，使用 `git rev-parse --git-path info/exclude` 取得实际 local exclude path。

## Step 2：项目知识边界

不要把项目描述写进 `.compass/context/`。

- 根 `README.md`、`doc/<feature>_design.md`、`doc/todo.md` 是唯一项目知识。已有内容全部保留，安装器不覆盖、不改写。
- 缺失时 **不要** 由安装器编造产品 README 或 feature design。在最终报告里列出缺失项，由后续普通工作按 `AGENTS.md` 补齐。
- `cli-worker.md` 到 Step 5 再写。
- 若存在旧 L1–L5 或 `.ai/`：保留不删，报告为 leftover；不要迁移进 `.compass/context/`，也不要复制成第二份 design。

## Step 3：准备 platform instructions

本次安装的 instructions source 位于 `.compass/AGENTS.md`，由以下标记包围：

```text
<!-- compass:start -->
...
<!-- compass:end -->
```

本步骤只定义统一的受管 merge 规则；实际 destination 由 Step 4 的 platform installer 决定。

1. Destination 不存在时创建文件并写入完整受管区块。
2. Destination 已存在但没有受管区块时，保留全部原内容并追加区块。
3. Destination 已存在受管区块时，只更新两个 marker 之间的内容，保留 marker 外的平台或用户规则。
4. Destination 是软链接、包含重复 marker 或无法安全编辑时，不替换、不猜测，停止该平台并报告 conflict。
5. 不要把 CLI worker 调用步骤写进 instruction file；触发器是 hook。

## Step 4：执行平台安装器

总安装器不实现平台专用文件格式。根据 Step 1 选择的平台，逐个读取并完整执行对应安装器的 instruction / 可选 Subagent 步骤。Hook 步骤留到 Step 5 判定之后。

| Platform | Kind | Installer |
|:---------|:-----|:----------|
| Codex | planner | `.compass/platforms/codex/INSTALL.md` |
| Cursor | planner | `.compass/platforms/cursor/INSTALL.md` |
| OpenCode | planner | `.compass/platforms/opencode/INSTALL.md` |
| Claude Code | worker | `.compass/platforms/claude-code/INSTALL.md` |

执行规则：

1. 先完成本文件 Step 2–3，再运行平台安装器。
2. 向每个平台安装器传入 Step 1 得到的可选角色；默认列表为空。不要安装 Compass Skill，不要默认生成 reviewer。
3. 平台安装器独占该平台 instruction destination、Subagent 渲染和平台验证规则。
4. 已选择多个平台时依次执行，分别保存结果。
5. 平台入口无法安全合并时停止该平台并报告。仅可选 Subagent 冲突时不覆盖，记录 fallback 后继续。
6. 本步不要安装 CLI worker hook。

## Step 5：判定 CLI worker 并安装 planner hook

本步整次安装只做一次，不按平台重复探测。不为这个再问用户。

Planner platforms：Codex、Cursor、OpenCode。

### 5a. 判定

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

   不要把 `--dangerously-skip-permissions` 写进 `invoke`。用 `--permission-mode acceptEdits`。

4. 覆盖 `cli-worker.md` 里 installer 管理的字段，保留文件标题和说明段落。空白 `unknown` 不得留到安装完成。

### 5b. 安装 hook

1. 读取 `.compass/hooks/cli-worker/CONTRACT.md`。
2. 仅当 `status=enabled` 时，对每个已选 planner 平台执行该平台 installer 的 “CLI worker hook” 步骤，传入 `cli-worker=enabled`。
3. `disabled` 或 `not-applicable`：对所有平台传入 skip；Claude Code 即使同时被选也不安装该 hook。
4. Hook 冲突不阻断公共安装：记录 fallback（Main Agent 自己做 implementation）。

用户以后才配置 `claude` 时，必须重新执行本次安装判定才能把 status 改为 `enabled` 并补迁 hook。普通开发不得改这份文件。

## Step 6：维护 local Git exclude

本步只修改 repository-local Git metadata，不修改会被共享的 `.gitignore`。

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
| Platform instruction | 已选 platform 的 instruction 结果为 created、updated 或 reused | `/AGENTS.md` 或 `/CLAUDE.md` |
| Platform Subagent | 该具体文件存在 Compass generated marker | 例如 `/.codex/agents/codebase-explorer.toml` |
| CLI worker hook script | 该文件已安装 | 例如 `/.cursor/hooks/cli-worker.py` |
| CLI worker hook registration | Compass 已写入或更新该文件 | 例如 `/.cursor/hooks.json`、`/.codex/hooks.json`、`/.opencode/plugins/compass-cli-worker.js` |

不要写入 `/README.md`、`/doc/` 或任何 Compass Skill path。

执行规则：

1. 如果目标不是 Git worktree，记录 `not applicable` 并继续。
2. 只写入 repository-root anchored 的精确 pattern；不写宽泛 parent pattern。
3. 受管区块不存在时追加；恰好存在一个完整区块时只替换 marker 之间的 inventory。
4. marker 损坏或 exclude 是 symlink 时不改写，标记 incomplete。
5. 用 `git check-ignore --no-index -v -- <path>` 验证命中本受管区块。
6. 不运行 `git update-index`。已 tracked 的 instruction 仍写入 pattern，并在报告列入 `tracked Compass paths still visible`。

## Step 7：公共验证

- [ ] 每个已选平台的必读 instruction file 已创建或合并，Compass 标记区块只出现一次，且包含 Project Knowledge 约定。
- [ ] 没有安装 Compass Skill，也没有为 Compass 新建平台 Skill directory。
- [ ] 没有在 `.compass/context/` 填写项目描述、design 或 todo。
- [ ] 没有创建 L1–L5 目录。
- [ ] `cli-worker.md` 的 `status` 是 `enabled`、`disabled` 或 `not-applicable`。
- [ ] `status=enabled` 当且仅当已选至少一个 planner 且本机 `claude` 探测成功。
- [ ] `status=enabled` 时每个已选 planner 已安装 worker hook，或逐项记录 fallback；否则没有 Compass worker hook。
- [ ] Claude Code 没有 CLI worker hook。
- [ ] 未明确选择时没有生成 Subagent。
- [ ] 根 `README.md` 和 `doc/` 没有被安装器覆盖。
- [ ] Git worktree 的 local exclude 覆盖 `/.compass/` 以及本轮实际安装的 instruction、Subagent 和 hook；没有 exclude `README.md` 或 `doc/`。
- [ ] 没有修改 `.gitignore`，没有 Skill 或 hook 软链接。

## Step 8：清理 installation staging

1. 保留 `.compass/context/`（`cli-worker.md` 与 `README.md`）。
2. 删除 `.compass/` 下除 `context/` 之外的所有一级 entry。
3. 确认 `.compass/` 的直接子项只有 `context/`。
4. 再次确认平台 instructions 和已安装 hook 仍存在。

```text
.compass/
└── context/
```

## Step 9：最终报告

```text
安装结果
- 项目根目录：...
- 启用平台：...
- 平台结果：
  - cursor：
    - Instructions：created / updated / reused / conflict
    - Skills：none（本版本不安装 Compass Skill）
    - Subagents：none / ...
    - Hooks：installed / skipped / fallback / conflict / none
  - ...
- CLI worker：enabled / disabled / not-applicable
- CLI worker reason：...
- 项目知识：README.md ... / doc/todo.md ... / design files ...
- 缺失项目知识（安装器未编造）：...
- 旧 L1–L5 或 .ai leftover：...
- 冲突或待确认：...
- 最终产物：platform instructions、optional Subagents、optional planner hooks、.compass/context/cli-worker.md
- Local Git exclude：updated / reused / not applicable / conflict
- Excluded Compass paths：...
- Tracked Compass paths still visible：...
- Installation staging cleanup：completed（.compass/ 仅保留 context/）
- 验证结果：...
```

不得只回复“安装完成”。Codex hook 若需要 `/hooks` trust，在验证结果中写明。

## 移除

只有用户明确要求卸载时才执行：

1. 重新取得兼容的 Compass installation package，执行各平台“移除”章节。
2. Instructions、Subagent 与 generated hook 只按 marker 或可识别 command path 删除。
3. 不删除根 `README.md` 或 `doc/`。
4. `.compass/context/` 默认保留（`cli-worker.md`）；用户明确要求时才删除整个 `.compass/`。`.compass/context/cli-worker.lock` 是 runtime 锁，卸载 hook 时可删。
5. 更新 local exclude：只移除已删除的 artifact pattern。
