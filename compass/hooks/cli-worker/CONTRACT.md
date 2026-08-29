# CLI Worker Hook Contract

> Canonical source：`.compass/hooks/cli-worker/`。平台 installer 把它迁到 native hook dest；安装结束后本目录会随 staging 删除。

## Purpose

Planner platform（Codex、Cursor、OpenCode）正要对仓库做 implementation 时，若安装时已判定 Claude Code CLI 可调用，hook 拦住这次 pending tool call，并在项目根直接调用 `claude` 做 **同一件动作**。X 是平台正要执行的 tool call，不是用户原始 chat。Claude Code 自己就是 worker，不安装本 hook。

## 何时安装

总 installer 在判定 `.compass/context/cli-worker.md` 的 `status` 之后：

- `enabled`：每个已选 planner 平台执行各自的 hook 安装步骤。
- `disabled` / `not-applicable` / `unknown`：不安装、不更新 worker hook。

## Canonical files

| File | 角色 |
|:-----|:-----|
| `run.py` | 唯一判定与调用脚本；复制到平台 dest，不创建软链接 |
| `CONTRACT.md` | 本契约；不复制到目标项目 |

## 拦截范围

拦截会改变 implementation 的 tool call：

- 文件写入或删除：Write / Edit / StrReplace / Delete / `apply_patch` 等
- 会改文件的 Shell：重定向、`sed -i`、`rm`、`mv` 等

不拦截：

- 只读查找与阅读
- `.compass/context/` 下的 installer / runtime artifact 写入
- 以 `claude` 开头的 CLI 调用
- 测试、lint、类型检查、只读 git 查询

## 运行时规则

1. 读取项目根的 `.compass/context/cli-worker.md`。找不到项目根或 `status` 不是 `enabled` 时放行。
2. `enabled` 只表示允许安装和调用 worker，不表示 native hook 已经 trust、loaded 或 active。Activation 由各 platform installer 和 runtime probe 单独验证。
3. `enabled` 且命中拦截时：用 flock 串行化，按 `invoke`（默认 `claude -p --permission-mode acceptEdits`）把 **这次 tool call** pass 给 Claude Code CLI；cwd 为项目根。锁文件是 `.compass/context/cli-worker.lock`，属于 runtime，不是项目知识。
4. 调用前后向 `.compass/context/cli-worker-audit.jsonl` 追加 JSON Lines。固定 event 是 `handoff_started`、`worker_succeeded` / `worker_failed`、`planner_blocked`；记录 UTC timestamp、platform、tool、可用的 session / turn / tool-use ID 和 worker exit code。不得记录 tool input、prompt、CLI stdout / stderr 或 secret。Audit 写入失败不改变 hook decision，但 runtime probe 必须判为 failed。
5. Prompt 只描述 pending action（tool 名 + input）。可让 CLI 读 README 与 `doc/`。不要把用户原始 chat 当成任务来源。
6. 默认不加 `--dangerously-skip-permissions`；`invoke` 里出现该 flag 时丢掉。`acceptEdits` 不 bypass Claude Code 的 Shell、network、managed policy 或 directory permission。
7. CLI 结束后拒绝 planner 自己再执行同一 tool call。exit 0：告诉 planner 去看 diff；需要时更新 README 或 `doc/`。非 0 或超时：blocker，不准改口本地写。
8. 拒绝时给用户显示统一结果：intercepted tool、Claude CLI success / failure、planner 原动作已阻止。Codex 用 `systemMessage`，Cursor 用 `user_message`，OpenCode adapter 显示 thrown hook error；详细 instruction 仍留给 planner。
9. 不 commit、不 push。
10. 判定「要不要交接」之前的脚本失败 fail open；已经决定交接之后 fail closed。

## Lifecycle 与 runtime probe

平台安装结果必须分别报告：

```text
Hook files: installed / skipped / conflict
Runtime activation: active / awaiting-cli-session / awaiting-trust / awaiting-workspace-trust / restart-required / not-applicable
Worker probe: passed / pending / failed / not-applicable
Last execution: claude-succeeded / claude-failed / none
```

Probe 在 platform activation 完成后由真实 platform session 创建 `.compass-worker-probe.tmp`，内容为 `compass worker probe`。只有文件内容、用户可见结果、audit event chain 和 planner 原 write 被阻止四项都成立才是 `passed`；验证后通过同一 hook 删除 probe。文件存在本身不构成 evidence。

Codex 的 `真实 platform session` 仅指从 repository root 启动、已用 `/hooks` trust 当前 definition 的 Codex CLI session。Codex Desktop task 使用的 agent / orchestrator tools 不属于本契约的 hook pipeline；Desktop 中新建 task、执行 tool 或看到文件存在都不能作为 activation evidence。CLI 尚未启动时报告 `awaiting-cli-session`，已启动但未 trust 时报告 `awaiting-trust`。

## 平台适配

总 installer 不猜 native JSON。各 planner 的 `platforms/<platform>/INSTALL.md` 负责：

1. 复制 `run.py` 到该平台 dest。
2. 用 generated 所有权识别 Compass 条目，merge 进已有用户 hook，不覆盖无 marker / 无匹配 command 的用户条目。
3. 传入 `--format cursor|codex|internal`。
4. hook `timeout` 不小于 `cli-worker.md` 的 `timeout-seconds`（默认 600）。

Claude Code installer 明确跳过本 hook。
