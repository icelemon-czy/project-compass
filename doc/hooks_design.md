# Hooks

Cursor / Codex / OpenCode 负责 plan 和 review；implementation 交给本机 Claude Code。`compass/hooks/` 是为这件事才有的，不是独立功能。

装进去之后：planner 正要改仓库时，hook 拦住这次 pending tool call，在项目根调用 `claude` CLI 做同一件事。X 是平台正要执行的动作，不是用户原始 chat。Claude Code 自己就是 worker，不装这只 hook。

探测和填写见 [install_instruction.md](install_instruction.md) Step 5。拦截范围、fail-open / fail-closed、平台 dest 见 [CONTRACT.md](../compass/hooks/cli-worker/CONTRACT.md)。

## 安装时判定

整次安装只探测一次，不为这个再问用户。结论写入 `.compass/context/cli-worker.md`。模板默认 `unknown`，安装结束不得留下。

- 只选了 Claude Code → `not-applicable`，不探测、不装 hook
- 已选至少一个 planner，且 `command -v claude` 与 `claude --version` 都成功 → `enabled`
- 任一项失败 → `disabled`，planner 自己写代码

`enabled` 时的默认 invoke：`claude -p --permission-mode acceptEdits`。不要写 `--dangerously-skip-permissions`。以后才装 `claude` 时，必须重新跑安装判定才能补 hook。

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

拦会改变 implementation 的写入；不拦只读、`.compass/context/` 下的 installer / runtime artifact、测试 / lint、只读 git、以及以 `claude` 开头的命令。具体 matcher 以 CONTRACT 为准。

## 交接之后

- 用 flock 串行化；锁文件 `.compass/context/cli-worker.lock` 是 runtime
- 在 `.compass/context/cli-worker-audit.jsonl` 追加不含 tool input、prompt 或 CLI output 的 runtime audit
- Prompt 只描述 pending action；CLI 可读目标项目的 README 与 `doc/`
- CLI 结束后拒绝 planner 再执行同一 tool call
- 对用户显示 intercepted tool、Claude CLI 结果和 planner 原动作已阻止；不能只把原因放进 model context
- exit 0：planner 看 diff；需要时更新 README 或 `doc/`
- 非 0 或超时：blocker，不准改口本地写
- 判定「要不要交接」之前失败则放行；已经决定交接之后失败则挡住
- 不 commit、不 push

## Runtime probe

Planner 完成 activation 后，用真实 platform session 创建 repository root 的 `.compass-worker-probe.tmp`，内容固定为 `compass worker probe`。通过条件必须同时满足：

1. 文件内容正确。
2. UI 明确显示 Claude CLI 已执行、planner 原动作已阻止。
3. `cli-worker-audit.jsonl` 在本次 probe 之后出现 `handoff_started`、`worker_succeeded` 和 `planner_blocked`。
4. Planner transcript 没有成功执行原始 write tool。

文件存在本身不能证明通过。验证后删除 probe 文件并确认 repository 没有遗留；删除也应走同一 worker hook。Probe 是安装后的手工 runtime validation，不是自动化 test。
