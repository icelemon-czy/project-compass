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

## 拦什么

拦会改变 implementation 的写入；不拦只读、`.compass/context/cli-worker.md`、测试 / lint、只读 git、以及以 `claude` 开头的命令。具体 matcher 以 CONTRACT 为准。

## 交接之后

- 用 flock 串行化；锁文件 `.compass/context/cli-worker.lock` 是 runtime
- Prompt 只描述 pending action；CLI 可读目标项目的 README 与 `doc/`
- CLI 结束后拒绝 planner 再执行同一 tool call
- exit 0：planner 看 diff；需要时更新 README 或 `doc/`
- 非 0 或超时：blocker，不准改口本地写
- 判定「要不要交接」之前失败则放行；已经决定交接之后失败则挡住
- 不 commit、不 push
