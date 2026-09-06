# CLI Worker Hook Contract

> Canonical source：`.compass/hooks/cli-worker/`。平台 installer 把它迁到 native hook dest；安装结束后本目录会随 staging 删除。

## Purpose

Planner platform（Codex、Cursor、OpenCode）把一个完整且 bounded 的 implementation task 交给 Claude Code CLI。Native hook 只阻止 planner 直接做 implementation 写入并引导 task-level delegation；它**不再为每个 pending tool call 启动 Claude**。Claude Code 自己就是 worker，不安装本 hook。

## 何时安装

总 installer 在判定 `.compass/context/cli-worker.md` 的 `status` 之后：

- `enabled`：每个已选 planner 平台执行各自的 hook 安装步骤。
- `disabled` / `not-applicable` / `unknown`：不安装、不更新 worker hook。

## Canonical files

| File | 角色 |
|:-----|:-----|
| `run.py` | 唯一判定与调用脚本；复制到平台 dest，不创建软链接 |
| `CONTRACT.md` | 本契约；不复制到目标项目 |

## 两条入口

### Native hook：policy boundary

拦截会改变 implementation 的 tool call：

- 文件写入或删除：Write / Edit / StrReplace / Delete / `apply_patch` 等
- 会改文件的 Shell：重定向、`sed -i`、`rm`、`mv` 等

不拦截：

- 只读查找与阅读
- `.compass/context/` 下的 installer / runtime artifact 写入
- 测试、lint、类型检查
- git（含 status / diff / add / commit / push / checkout / mv；VCS 不是 implementation。commit / push 仍由 planner 在用户明确要求时执行，不委托给 worker）

Raw `claude` CLI invocation 也拦截，避免 planner 绕过 fresh-session、dedup 与 bounded-task policy；只放行 `command -v claude` 和 `claude --version` 探测。唯一 implementation 入口是受控 wrapper 的 `--delegate` mode。

命中后 hook 立即 deny，并返回本平台的 `--delegate` command；不调用 Claude。这样一次 Agent implementation 不会被放大成 N 次 Claude session。

### `--delegate`：task execution

Planner 先覆盖 `.compass/context/cli-worker-task.md`，内容必须是一个 self-contained task，包含 goal、confirmed scope、acceptance criteria、out-of-scope，以及一行 `model: sonnet` 或 `model: opus`（也可 `haiku` / `fable`）；再执行一次：

```text
python3 <platform hook path>/cli-worker.py --format <platform> --delegate
```

Codex、Cursor、OpenCode 的具体 path 由各 platform installer 写入 instruction。Task spec 最多 40,000 characters；超出说明 scope 仍不 bounded，应先收窄。

## 运行时规则

1. 读取项目根的 `.compass/context/cli-worker.md`。Native hook 找不到项目根或 `status` 不是 `enabled` 时放行；显式 `--delegate` 则返回 non-zero。
2. `enabled` 只表示允许安装和调用 worker，不表示 native hook 已经 trust、loaded 或 active。Activation 由各 platform installer 和 runtime probe 单独验证。
3. Native hook 命中时追加 `planner_blocked` audit，明确显示“未按 tool call 启动 Claude，需 task-level delegation”。Codex 用 `systemMessage`，Cursor 用 `user_message`，OpenCode adapter 显示 thrown hook error。
4. `--delegate` 用 flock 串行化，读取 task spec，并按 `invoke`（默认 `claude -p --permission-mode acceptEdits`）在项目根启动一次 Claude。task spec 里整行 `model: sonnet|opus|haiku|fable` 决定 `--model` alias；出现多次时以最后一次合法值为准。缺省用 `cli-worker.md` 的 `default-model`（默认 `sonnet`）。句子中间或非法值不会写入 `--model`。invoke 里已有的 `--model` 会被覆盖。audit 可记录 alias，不记录 task 正文。
5. 每次 invocation 都强制 fresh、non-persistent session：丢弃 `--resume` / `-r`、`--continue` / `-c`、`--session-id`、`--from-pr`、`--teleport` 和 `--fork-session`，并加入 `--no-session-persistence`。`invoke` 不能把 session continuity 重新打开。
6. 默认加入 `--max-turns 30`；`cli-worker.md` 的 `max-turns` 可在 1–100 之间调整。已在 `invoke` 明确设置时保留它。
7. Task prompt 明确 bounded scope、minimum complete change、focused verification 和遇到 blocker 即停止；不得把 task 自动扩大为 repository refactor、migration、audit 或 cleanup。
8. `.compass/context/cli-worker-state.json` 只保存最近最多 100 个成功 task content hash、当前 status、timestamp 与 exit code。相同 task content 已成功时，即使 planner 重写同样内容或在其他 task 后重新切回来，后续 `--delegate` 也只记录 `delegation_reused` 并直接返回，不再调用 Claude；只有 scope 或 acceptance criteria 确实改变时才形成新 revision。
9. 调用前后向 `.compass/context/cli-worker-audit.jsonl` 追加 JSON Lines。固定 execution event 是 `delegation_started`、`worker_succeeded` / `worker_failed`、可选 `delegation_reused`；记录 UTC timestamp、platform、tool、可用 ID、exit code 与非敏感 failure category。不得记录 task 内容、tool input、prompt、CLI stdout / stderr 或 secret。
10. 默认不加 `--dangerously-skip-permissions`；`invoke` 里出现 dangerous flag 时丢掉。`acceptEdits` 不 bypass Claude Code 的 Shell、network、managed policy 或 directory permission。
11. exit 0 后 planner 检查 diff 并做独立 verification。非 0 或超时是 blocker，不准改口本地写或连续创建 task revision 绕过。
12. 不 commit、不 push。Native hook 判定拦截前失败 fail open；已进入 `--delegate` 后失败返回 non-zero。

## Lifecycle 与 runtime probe

平台安装结果必须分别报告：

```text
Hook files: installed / skipped / conflict
Runtime activation: active / awaiting-cli-session / awaiting-trust / awaiting-workspace-trust / restart-required / not-applicable
Worker probe: passed / pending / failed / not-applicable
Last execution: claude-succeeded / claude-failed / none
```

Probe 在 platform activation 完成后验证两条入口：先让 planner 直接创建 `.compass-worker-probe.tmp`，确认 hook 阻止且没有启动 Claude；再把创建动作写成 bounded task spec 并执行一次 `--delegate`。只有文件内容、用户可见的 policy message、`planner_blocked` + `delegation_started` + `worker_succeeded` audit chain、planner 原 write 被阻止四项都成立才是 `passed`。验证后用新的 cleanup task revision 删除 probe。文件存在本身不构成 evidence。

Codex 的 `真实 platform session` 仅指从 repository root 启动、已用 `/hooks` trust 当前 definition 的 Codex CLI session。Codex Desktop task 使用的 agent / orchestrator tools 不属于本契约的 hook pipeline；Desktop 中新建 task、执行 tool 或看到文件存在都不能作为 activation evidence。CLI 尚未启动时报告 `awaiting-cli-session`，已启动但未 trust 时报告 `awaiting-trust`。

## 平台适配

总 installer 不猜 native JSON。各 planner 的 `platforms/<platform>/INSTALL.md` 负责：

1. 复制 `run.py` 到该平台 dest。
2. 用 generated 所有权识别 Compass 条目，merge 进已有用户 hook，不覆盖无 marker / 无匹配 command 的用户条目。
3. 传入 `--format cursor|codex|internal`。
4. hook `timeout` 不小于 `cli-worker.md` 的 `timeout-seconds`（默认 600）。

Claude Code installer 明确跳过本 hook。
