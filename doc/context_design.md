# Context

这是 `compass/context/` 的 design。

复制进目标项目后成为 `.compass/context/`。这里不是产品知识。

| 文件 | 谁写 | 是什么 |
|:-----|:-----|:-----|
| `cli-worker.md` | 安装器 | 本机能不能调 Claude Code CLI，从而要不要给 planner 装 hook |
| `README.md` | 模板 | 说明这个目录不是产品知识 |

`cli-worker.lock` 是 runtime，安装不创建。普通产品工作不得改 `cli-worker.md` 的 `status`。

判定字段见 [install_instruction.md](install_instruction.md) Step 5。hook 见 [hooks_design.md](hooks_design.md)。
