# 任务看板

> 所有任务的状态一览。每次对话时加载，了解全局进度。
>
> **状态说明**：
> - 📋 `open` — 等待启动（未规划或已规划但未开始）
> - 🔨 `ongoing` — 正在进行（L4 session 追踪执行细节）
> - ⚠️ `done` — 代码完成，测试未补或未通过
> - *(deleted)* — 测试通过，人类确认后删除任务文件
>
> **操作**：
> - 新建任务 → 复制 `_task-template.md`，命名为 `TASK-XXX-简短描述.md`，在下表添加一行
> - 开始任务 → 状态改为 🔨，L4 session 指向该任务文件
> - 代码完成 → 状态改为 ⚠️ done
> - 测试通过 → 删除任务文件，从下表移除该行

## 活跃任务

| ID | 任务 | 状态 | 测试 | 详情 |
|----|------|------|------|------|
| | *暂无任务* | | | |

<!-- 示例：
| TASK-001 | 用户导出功能 | 🔨 ongoing | 5/8 pass | → TASK-001-user-export.md |
| TASK-002 | 登录 500 bug | 📋 open | — | → TASK-002-login-bug.md |
| TASK-003 | 重构 UserService | ⚠️ done | 0/3 pass | → TASK-003-refactor-user.md |
-->
