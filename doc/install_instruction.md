# 安装

这是 Compass 的安装 design。没有安装脚本。本文在源码仓 `doc/`，不进入 `compass/` 模板。

把 `compass/` 复制为目标项目的 `.compass/` 之后，以那个项目为根执行下列 Step。下文 `.compass/` 一律指目标项目里的副本。安装器不编造 `doc/` 下的 feature design；根 README 按模版整理结构。

## 目标

```text
projectA/
├── .compass/
│   ├── AGENTS.md
│   ├── context/
│   │   ├── README.md
│   │   └── cli-worker.md
│   ├── skills/
│   ├── subagents/
│   ├── hooks/
│   ├── platforms/
│   └── templates/
├── README.md
├── doc/
└── ...Project A files
```

`.compass/` 在安装期间承载模板副本。先把 instructions 和可选 Subagent materialize 到每个已选平台的 native destination，判定 CLI worker，必要时再安装 planner hook，完成 filesystem validation，最后删除 `.compass/` 中除 `context/` 之外的全部 staging。Hook files 落盘后还要按平台分别完成 runtime activation 与手工 probe；两者未完成时不能把 hook 报告为 active。

安装完成后的稳定产物只有：

```text
projectA/
├── .compass/
│   └── context/
├── AGENTS.md or CLAUDE.md
├── README.md
├── doc/
├── 已选平台的 Compass Skills
├── 可选 platform-native Subagent files
├── planner-native CLI worker hooks（仅判定 enabled 时）
└── ...Project A files
```

如果目标项目是 Git worktree，还要在该 repository 的 local `info/exclude` 中维护 Compass 受管区块，使 `.compass/`、已选 platform instructions、Skills、Subagents 和已安装 hook 不进入共享 Git 变更。**不要**把根 `README.md` 或 `doc/` 写入 exclude。

复制来的 `context/` 只承载 `cli-worker.md` 和本目录 README。不要在其中填写项目描述或 design。默认不生成 Subagent，只有用户明确要求的 canonical role 才安装。Planner platform 是 Codex、Cursor 和 OpenCode。Claude Code 是 worker platform：当前 session 已经在 Claude Code 里时不安装 CLI worker hook。

`.compass/AGENTS.md`、`.compass/skills/`、`.compass/subagents/`、`.compass/hooks/`、`.compass/platforms/` 和 `.compass/templates/` 都是 installation staging，不是安装后的项目接口。

## 不可违反的安全规则

- 将 `.compass/` 的父目录视为目标项目根目录。
- `.compass/` 内不得包含它自己的 `.git/`。发现嵌套 Git 仓库时停止安装，要求用户确认后重新复制或移除该元数据。
- 如果 `.compass/` 在本次安装前已存在，禁止用复制命令覆盖它；先检查差异并请求用户决定合并方式。
- 安装前先读取目标项目现有规则、配置和 Git 状态。
- 不覆盖已有根 `AGENTS.md`、`CLAUDE.md`、`opencode.json` 或 `doc/` 下的已有文件。根 `README.md` 按 `.compass/templates/README.md` 整理结构，保留原有事实，不编造产品内容。
- 不删除旧 `.ai/`、用户自建 Skill 或其他历史文件；先报告，再由用户决定是否删除。Step 8 规定的 staging cleanup 不受此条限制。
- `.compass/skills/` 是本次 Skill source，只含 [skills_design.md](skills_design.md) 的 canonical inventory。安装到已选平台的 project-level directory，不创建软链接，不修改 global Skill directory。同名用户 Skill 内容不同时不覆盖。
- 用户自建其他 Skill 全部保留。
- 不在 `.compass/context/` 填写项目描述或 design；除 `cli-worker.md` 与 `README.md` 外不在该目录新建项目文档。
- 若 `.compass/context/` 里已有旧层文件：保留不删，报告 leftover，不要当成项目知识，也不要复制进 `doc/`。
- CLI worker 是否可调用只在本次安装判定一次，并写入 `.compass/context/cli-worker.md`。不为这个再询问用户。
- 只有 `status=enabled` 时才给已选 planner 平台安装 worker hook。Claude Code 永不安装该 hook。
- `status=enabled` 只证明 Claude Code CLI 可调用，不证明任何 planner hook 已 trust、loaded、active 或通过 probe。
- Hook 从 canonical source 按平台迁移；不写入 user-global hook directory，不创建软链接。
- 将 `.compass/` 和每个已选 platform 实际安装的 instruction、Skill、Subagent 与 hook 精确 path 写入 local Git exclude；不得忽略整个 platform parent directory；不得 exclude `README.md` 或 `doc/`。
- 不修改项目 `.gitignore`，不使用 `skip-worktree` 或 `assume-unchanged` 隐藏 tracked file。
- 遇到无法安全合并的现有文件时停止该项操作并向用户说明，不要猜测。

## Step 1：安装前检查

确认以下事实并记录结果：

1. 当前目标项目根目录。
2. `.compass/.git/` 不存在。
3. `.compass/AGENTS.md`、`context/`、`skills/`、`hooks/cli-worker/`、`platforms/` 和 `templates/` 均存在；`.compass/skills/` 与下文 Skill inventory 一致，每项都含 `SKILL.md`。
4. 当前项目是否已有：
   - 根 `AGENTS.md` / `CLAUDE.md` / `opencode.json`
   - 根 `README.md`
   - `doc/`
   - `.cursor/hooks.json` / `.codex/hooks.json`
   - `.cursor/hooks/cli-worker.py` / `.codex/hooks/cli-worker.py` / `.opencode/hooks/cli-worker.py`
   - `.opencode/plugins/compass-cli-worker.js`
   - `.compass/context/` 下除 `cli-worker.md` 与 `README.md` 以外的旧文件，或旧 `.ai/`
5. 用户需要 Codex、Cursor、Claude Code、OpenCode 中的哪些平台。能从请求明确判断时直接采用；无法判断时询问一次。
6. 可选 Subagent 只识别 [subagents_design.md](subagents_design.md) 的 canonical role；不要主动让用户选择。默认角色列表为空。
7. 目标项目是否位于 Git worktree 中。如果是，从项目根执行 `git rev-parse --git-path info/exclude`，并把返回值相对项目根解析为实际 local exclude path。不要直接拼接 `.git/info/exclude`：Git worktree、`--separate-git-dir` 和 Windows 都可能使用不同的 Git metadata path。

## Step 2：项目知识边界

不要把项目描述写进 `.compass/context/`。

- `doc/` 下已有文件全部保留，安装器不覆盖、不改写、不编造 feature design。
- 根 `README.md` 不存在时，从 `.compass/templates/README.md` 复制到项目根。
- 根 `README.md` 已存在时，按 `.compass/templates/README.md` 整理：开头写目的，用 Document map 标出 `doc/<feature>_design.md` 这一层。原有目的、已有 `doc/` 条目和 License 留下；模块设计不要写回 README，应落到对应 design 或只在 map 里 refer。
- `doc/todo.md` 只在目标项目已经使用或用户明确要求时保留/创建；安装器不主动生成当前工作，也不把永久 design 放进 todo。
- 整理后的 README 进 Git，不写进 local exclude。
- `cli-worker.md` 到 Step 5 再写。
- 若存在旧 `.ai/` 或 `.compass/context/` 下除 `cli-worker.md` / `README.md` 以外的文件：保留不删，报告 leftover；不要迁移进 context，也不要复制成第二份 design。

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

## Skill copy 规则

Source：`.compass/skills/`。Skill inventory 以 [skills_design.md](skills_design.md) 为准。

1. 只把含合法 `SKILL.md` 的 inventory 一级子目录识别为待安装 Skill。
2. 递归复制整个 Skill directory；不只复制 `SKILL.md`。
3. Destination 不存在时创建完整 copy；与 source 完全一致时复用；内容不同时不覆盖，记录 conflict。
4. 不创建软链接，不写入 global Skill directory，不把 CLI worker 步骤写进 Skill。

## Step 4：执行平台安装器

总安装器不实现平台专用文件格式。根据 Step 1 选择的平台，逐个读取并完整执行对应安装器的 instruction / Skill / 可选 Subagent 步骤。Hook 步骤留到 Step 5 判定之后。

| Platform | Kind | Installer |
|:---------|:-----|:----------|
| Codex | planner | `.compass/platforms/codex/INSTALL.md` |
| Cursor | planner | `.compass/platforms/cursor/INSTALL.md` |
| OpenCode | planner | `.compass/platforms/opencode/INSTALL.md` |
| Claude Code | worker | `.compass/platforms/claude-code/INSTALL.md` |

执行规则：

1. 先完成本文件 Step 2–3，再运行平台安装器。
2. 向每个平台安装器传入 Step 1 得到的可选角色；默认列表为空。不要默认生成 reviewer。
3. 平台安装器独占该平台 instruction destination、native Skill destination、Subagent 渲染和平台验证规则。
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
   default-model: sonnet
   timeout-seconds: 600
   max-turns: 30
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
   default-model: sonnet
   timeout-seconds: 600
   max-turns: 30
   checked-at: <ISO-8601>
   ```

   不要把 `--dangerously-skip-permissions`、`--resume`、`--continue` 或 session ID 写进 `invoke`。Executor 即使遇到旧配置也会移除 session continuity flag，并强制 `--no-session-persistence`。

4. 覆盖 `cli-worker.md` 里 installer 管理的字段，保留文件标题和说明段落。空白 `unknown` 不得留到安装完成。

### 5b. 安装 hook

1. 读取 `.compass/hooks/cli-worker/CONTRACT.md`。
2. 仅当 `status=enabled` 时，对每个已选 planner 平台执行该平台 installer 的 “CLI worker hook” 步骤，传入 `cli-worker=enabled`。
3. `disabled` 或 `not-applicable`：对所有平台传入 skip；Claude Code 即使同时被选也不安装该 hook。
4. Hook 冲突不阻断公共安装：记录 fallback（Main Agent 自己做 implementation）。

用户以后才配置 `claude` 时，必须重新执行本次安装判定才能把 status 改为 `enabled` 并补迁 hook。普通开发不得改这份文件。

### 5c. 初始化 lifecycle report

每个已选平台先建立四个彼此独立的结果字段：

```text
Hook files: installed / skipped / conflict
Runtime activation: active / awaiting-cli-session / awaiting-trust / awaiting-workspace-trust / restart-required / not-applicable
Worker probe: passed / pending / failed / not-applicable
Last execution: claude-succeeded / claude-failed / none
```

本步骤只能根据 filesystem operation 填写 `Hook files`。`status=enabled` 时，Codex 只支持从项目根启动的 CLI hook runtime：installer 不在该 CLI runtime 中或无法 authoritative 地确认时初始化为 `awaiting-cli-session`；已在目标 CLI session 但当前 definition 未 trust 时为 `awaiting-trust`。Cursor 初始化为 `awaiting-workspace-trust`，本轮 created / updated plugin 的 OpenCode 初始化为 `restart-required`，对应 probe 初始化为 `pending`。`status=disabled` 的 planner 与 Claude Code 都是 `Hook files: skipped`、`Runtime activation: not-applicable`、`Worker probe: not-applicable`、`Last execution: none`。

## Step 6：维护 local Git exclude

本步只修改 repository-local Git metadata，不修改会被共享的 `.gitignore`。

macOS、Linux 与 Windows 使用同一套 Git 命令和 exclude syntax：

- 从项目根执行 `git rev-parse --is-inside-work-tree`；结果不是 `true` 时记录 `not applicable`。
- 执行 `git rev-parse --git-path info/exclude` 取得路径。返回 absolute path 时直接使用，返回 relative path 时相对项目根解析；不要假设 `.git` 是 directory，因为 linked worktree 中它通常是 file。
- 用当前 runtime 的 filesystem API 读写该文件，不依赖 `sed -i`、`realpath`、PowerShell 或其他单平台命令。保留文件原有 UTF-8 BOM（如有）与 newline style；新文件在 Windows 使用 CRLF，其他平台使用 LF。
- exclude pattern 是 Git syntax，不是 OS filesystem path；所有平台都使用 `/` separator，禁止在 Windows 写 `\\`。

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
| Platform Skill | 该 Skill 结果为 installed 或 reused；conflict 不写入 | 例如 `/.cursor/skills/brainstorm/` |

不要写入 `/README.md` 或 `/doc/`。

执行规则：

1. 如果目标不是 Git worktree，记录 `not applicable` 并继续。
2. 只写入 repository-root anchored 的精确 pattern；不写宽泛 parent pattern。
3. 受管区块不存在时追加；恰好存在一个完整区块时只替换 marker 之间的 inventory。重复执行且 inventory 未变时不重写文件。
4. marker 损坏、exclude 是 symlink，或无法安全保留原 encoding / newline 时不改写，标记 incomplete。
5. 用 `git check-ignore --no-index -v -- <path>` 逐项验证命中本受管区块；该命令在 macOS 与 Windows 上都从项目根执行，并以 repository-relative path 作为参数。
6. 不运行 `git update-index`。已 tracked 的 instruction 仍写入 pattern，并在报告列入 `tracked Compass paths still visible`。
7. 本步为 Git worktree installation 的必做步骤；验证失败时不得报告 installation completed，而要报告 `Local Git exclude: conflict` 及未命中的 path。

## Step 7：公共验证

- [ ] 每个已选平台的必读 instruction file 已创建或合并，Compass 标记区块只出现一次。
- [ ] 没有在 `.compass/context/` 填写项目描述或 design。
- [ ] `cli-worker.md` 的 `status` 是 `enabled`、`disabled` 或 `not-applicable`。
- [ ] `status=enabled` 当且仅当已选至少一个 planner 且本机 `claude` 探测成功。
- [ ] `status=enabled` 时每个已选 planner 已安装 worker hook，或逐项记录 fallback；否则没有 Compass worker hook。
- [ ] `status=enabled` 没有被当作 `Runtime activation: active` 的 evidence。
- [ ] Claude Code 没有 CLI worker hook。
- [ ] 未明确选择时没有生成 Subagent。
- [ ] `.compass/skills/` 与 Skill inventory 一致，每项都含 `SKILL.md`。
- [ ] 每个已选平台已安装全部 Skill inventory，或逐项记录了未覆盖的同名 conflict。
- [ ] 没有 Skill 或 hook 软链接，也没有修改 global Skill directory。
- [ ] 根 `README.md` 已按 `.compass/templates/README.md` 整理（或由该模版新建）；原有事实没有丢失。
- [ ] `doc/` 下已有文件没有被覆盖，也没有编造 feature design。
- [ ] Git worktree 的 local exclude 覆盖 `/.compass/` 以及本轮实际安装的 instruction、Skill、Subagent 和 hook；没有 exclude `README.md` 或 `doc/`。
- [ ] 没有修改 `.gitignore`，没有 hook 软链接。

## Step 8：清理 installation staging

1. 保留 `.compass/context/`（`cli-worker.md`、`README.md`，以及 runtime 已生成的 `cli-worker-task.md` / `cli-worker-state.json` / `cli-worker.lock` / `cli-worker-audit.jsonl`）。
2. 删除 `.compass/` 下除 `context/` 之外的所有一级 entry。
3. 确认 `.compass/` 的直接子项只有 `context/`。
4. 再次确认平台 instructions、native Skill 和已安装 hook 仍存在。

```text
.compass/
└── context/
```

## Step 9：Runtime activation 与 worker probe

本步骤验证 native runtime，不用文件存在代替。只对 `Hook files: installed` 且 `cli-worker status: enabled` 的 planner 执行；其他平台保持 `not-applicable` 或已记录的 conflict。

### 9a. Platform activation

| Platform | Activation requirement | 未完成时的结果 |
|:---------|:-----------------------|:---------------|
| Codex | 从项目根启动 Codex CLI，在同一 CLI session 用 `/hooks` review 并 trust 当前 hook definition；definition hash 变化后重新 trust。Codex Desktop task 不属于本 hook runtime | CLI 未启动或当前 runtime 不是 CLI：`awaiting-cli-session`；CLI 未 trust：`awaiting-trust` |
| Cursor | 当前 project 是 trusted workspace；hook config 自动 reload | `awaiting-workspace-trust` |
| OpenCode | 安装或更新 `.opencode/plugins/` 后，从 project root 新建 session / restart | `restart-required` |
| Claude Code | 不安装 worker hook | `not-applicable` |

只有当前 platform runtime 的 authoritative evidence 满足对应 requirement，才把 `Runtime activation` 改为 `active`。Codex Desktop 的 task、tool output 或新建 task 都不是 Codex CLI activation evidence；Desktop 中完成 filesystem installation 后，必须引导用户从项目根启动 `codex`，在该 CLI session 中运行 `/hooks` 并继续 probe。需要用户在当前安装 turn 之外完成 CLI startup、trust、workspace trust 或 restart 时，不阻塞其他 filesystem 安装；最终报告必须写 `Overall status: action required` 和准确 next action。

### 9b. 手工 task-level probe

Activation 成为 `active` 后，在真实 platform session 中请求；Codex 必须继续使用刚才完成 `/hooks` trust 的同一个 CLI session，不能改在 Desktop task 中执行：

1. 先请求 planner 直接创建项目根的 `.compass-worker-probe.tmp`，内容固定为 `compass worker probe`。Native hook 必须阻止原始 write，显示没有按单个 tool call 启动 Claude，并返回 platform `--delegate` instruction。
2. Planner 将同一创建动作连同 scope 与 acceptance criteria 写入 `.compass/context/cli-worker-task.md`。
3. Planner 执行 platform installer 指定的 `--delegate` command 一次。Executor 必须使用 fresh、non-persistent Claude session。

Probe 通过必须同时取得四类 evidence：

1. `.compass-worker-probe.tmp` 内容恰好是 `compass worker probe`。
2. 平台 UI 明确显示 planner original action blocked、没有 tool-call-level Claude invocation，并要求 task-level delegation。
3. `.compass/context/cli-worker-audit.jsonl` 在本次操作之后出现 `planner_blocked`、`delegation_started` 和 `worker_succeeded`；audit 不含 task、tool input、prompt 或 CLI output。
4. 当前 transcript 没有成功执行 planner 原始 write tool；后续只读核对不算原始 write。

四项都成立 → `Worker probe: passed`、`Last execution: claude-succeeded`。任一缺失 → `failed`；尚未运行 → `pending`。文件存在本身不能证明 worker 身份。

通过或失败后都要清理 probe：覆盖 task spec 为 bounded cleanup task，再执行一次 `--delegate`。确认文件不存在、audit 有对应 cleanup execution、Git status 没有 probe 遗留。这个 probe 是安装后的手工 runtime validation，不新增 automated test。

## Step 10：最终报告

```text
安装结果
- 项目根目录：...
- 启用平台：...
- 平台结果：
  - cursor：
    - Instructions：created / updated / reused / conflict
    - Skills：<skill>（installed / reused / conflict）
    - Subagents：none / ...
    - Hook files：installed / skipped / conflict
    - Runtime activation：active / awaiting-cli-session / awaiting-trust / awaiting-workspace-trust / restart-required / not-applicable
    - Worker probe：passed / pending / failed / not-applicable
    - Last execution：claude-succeeded / claude-failed / none
    - 需要用户操作：none / start-codex-cli-from-project-root / review-and-trust-current-hook / trust-workspace / restart-opencode / run-probe-in-active-runtime
  - ...
- CLI worker：enabled / disabled / not-applicable
- CLI worker reason：...
- 文档骨架：README copied / reshaped / already matched
- context leftover 或 .ai leftover：...
- 冲突或待确认：...
- 最终产物：platform instructions、native Skills、optional Subagents、optional planner hooks、.compass/context/cli-worker.md
- Local Git exclude：updated / reused / not applicable / conflict
- Excluded Compass paths：...
- Tracked Compass paths still visible：...
- Installation staging cleanup：completed（.compass/ 仅保留 context/）
- Overall status：completed / action required / conflict
- 验证结果：...
```

不得只回复“安装完成”。`Hook files: installed` 不等于 runtime active。Codex 尚未从项目根启动 CLI 或未在该 CLI session trust 当前 definition、Cursor workspace 未 trust、OpenCode 未 restart 或 planner probe 未运行时，分别写明 waiting status、next action 与 `Overall status: action required`。不要建议通过新建 Codex Desktop task 激活 CLI hook。

只有所有已选 planner 都是 `Runtime activation: active` 且 `Worker probe: passed`，或其 hook 明确为 skipped / not-applicable，并且没有 filesystem conflict，才能报告 `Overall status: completed`。

## 移除

只有用户明确要求卸载时才执行：

1. 重新取得兼容的 Compass 模板，按本文执行各平台“移除”章节。
2. Instructions、Subagent 与 generated hook 只按 marker 或可识别 command path 删除。
3. Compass Skill 不含 ownership marker；列出各已选平台 native Skill path，只有用户逐项确认后才删除。
4. 不删除根 `README.md` 或 `doc/`。
5. `.compass/context/` 默认保留（`cli-worker.md` 与 `README.md`）；用户明确要求时才删除整个 `.compass/`。`.compass/context/cli-worker.lock` 是 runtime 锁，卸载 hook 时可删。
6. 更新 local exclude：只移除已删除的 artifact pattern。
