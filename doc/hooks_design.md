# Hooks

Cursor / Codex / OpenCode 负责 plan 和 review；implementation 以一个 bounded task 为单位交给本机 Claude Code。`compass/hooks/` 同时提供 policy hook 与 task executor，不是独立功能。

核心边界是：native hook 只阻止 planner 直接写仓库，不为 pending Write / Edit / Bash 启动 Claude。Planner 把原始 goal、confirmed scope、acceptance criteria 与 out-of-scope 写入 `.compass/context/cli-worker-task.md`，再显式执行一次 `--delegate`。这样一次 implementation 对应一次 fresh Claude session，而不是一次 tool call 对应一次 session。

探测和填写见 [install_instruction.md](install_instruction.md) Step 5。拦截范围、fail-open / fail-closed、平台 dest 见 [CONTRACT.md](../compass/hooks/cli-worker/CONTRACT.md)。

## 安装时判定

整次安装只探测一次，不为这个再问用户。结论写入 `.compass/context/cli-worker.md`。模板默认 `unknown`，安装结束不得留下。

- 只选了 Claude Code → `not-applicable`，不探测、不装 hook
- 已选至少一个 planner，且 `command -v claude` 与 `claude --version` 都成功 → `enabled`
- 任一项失败 → `disabled`，planner 自己写代码

`enabled` 时的默认 invoke：`claude -p --permission-mode acceptEdits`。Executor 强制加入 `--no-session-persistence` 与默认 `--max-turns 30`，并删除所有 resume / continue / session-id flag。不要写 `--dangerously-skip-permissions`。以后才装 `claude` 时，必须重新跑安装判定才能补 hook。

`status: enabled` 只证明本机 Claude Code CLI 可调用，并且允许 installer 安装 hook；它不证明平台 runtime 已加载、信任或执行过 hook。

## Lifecycle status

安装与 runtime activation 分开报告：

| Field | Values | Meaning |
|:------|:-------|:--------|
| Hook files | `installed` / `skipped` / `conflict` | Native script 与 registration 是否落盘 |
| Runtime activation | `active` / `awaiting-cli-session` / `awaiting-trust` / `awaiting-workspace-trust` / `restart-required` / `not-applicable` | 当前平台是否具备运行 hook 的前置条件 |
| Worker probe | `passed` / `pending` / `failed` / `not-applicable` | 是否用真实写入证明 Claude CLI 接管且 planner 原动作被阻止 |
| Last execution | `claude-succeeded` / `claude-failed` / `none` | 最近一次 audit 能证明的 worker 结果 |

各 planner 的 activation 前置条件不同：

- Codex：本 hook 的 runtime target 是从项目根启动的 Codex CLI session。Codex Desktop task 的 agent / orchestrator tools 不在这条 hook pipeline 中；新建 Desktop task 不能激活 hook。CLI session 使用 `/hooks` review 并 trust 当前 definition，definition hash 变化后重新 trust。CLI 尚未启动时是 `awaiting-cli-session`，尚未 trust 时是 `awaiting-trust`。
- Cursor：project 必须是 trusted workspace；hook config 自动 reload，不把 Skill 的新 session 要求套到 hook。
- OpenCode：project-local plugin 在 startup 加载；安装或更新后新建 session / restart。
- Claude Code：当前平台就是 worker，不安装本 hook，activation 与 probe 都是 `not-applicable`。

缺少可信 runtime evidence 时保持 `pending` 或对应 waiting status；不能从文件存在推断 `active`。

## 拦什么

拦会改变 implementation 的写入和 raw `claude` invocation；不拦只读、`.compass/context/` 下的 installer / runtime artifact、测试 / lint、只读 git，以及 `command -v claude` / `claude --version` 探测。Raw Claude command 必须改走受控 wrapper 的 `--delegate` mode。具体 matcher 以 CONTRACT 为准。

## 交接 flow

1. Planner 直接 write 被 native hook 阻止；hook 显示 task-level delegation instruction，但不启动 Claude。
2. Planner 覆盖 `cli-worker-task.md`，让 task 成为 self-contained scope boundary。
3. Planner 执行 platform 安装的 wrapper `--delegate` 一次。
4. Executor 用 flock 串行化，强制 fresh non-persistent session，调用 Claude 并记录不含 task / prompt / CLI output 的 audit。
5. 最近最多 100 个成功 task content hash 写入 `cli-worker-state.json`；相同 task spec 即使被重写或在其他 task 后重新切回，再次调用也只返回 `delegation_reused`，不再次启动 Claude。
6. exit 0 后 planner 看 diff并独立 verification；非 0 或超时是 blocker，不准改口本地写或用连续新 revision 绕过。

Planner 可以为真正不同的 implementation scope 覆盖 task spec，但不能把一个 task 按文件或 tool call 拆开。Claude 不 commit、不 push，也不再次调用 Claude。

## Runtime probe

Planner 完成 activation 后，在真实 platform session 验证 policy 与 executor：先直接创建 repository root 的 `.compass-worker-probe.tmp`，再通过 task spec + `--delegate` 完成同一动作。通过条件必须同时满足：

1. 文件内容正确。
2. UI 明确显示 planner 原动作已阻止、没有按单个 tool call 启动 Claude，并要求 task-level delegation。
3. `cli-worker-audit.jsonl` 在本次 probe 之后出现 `planner_blocked`、`delegation_started` 和 `worker_succeeded`。
4. Planner transcript 没有成功执行原始 write tool。

文件存在本身不能证明通过。验证后覆盖 task spec 为 cleanup task，再执行一次 `--delegate` 删除 probe 并确认没有遗留。Probe 是安装后的手工 runtime validation，不是 automated test。
