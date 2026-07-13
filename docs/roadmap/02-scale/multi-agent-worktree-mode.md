# Multi-Agent Worktree Mode

> 级别：扩展层
> 优先级：P1
> 一句话：用 git worktree 作为第一阶段隔离方案，让多个 agent 在同一代码库里并行工作且不破坏 Compass 的追溯模型。

## 要解决的问题

- 当前 Compass Harness 的 L3 和 L4 本质上还是单 agent 设计。
- 多个 agent 同时修改任务状态或会话状态时，最容易出现冲突和信息错乱。
- 如果没有明确的协作协议，多 Agent 只会把已有流程噪音和冲突放大。

## 为什么现在做

- 多 Agent 已经从研究话题变成真实工程实践。
- Worktree 是本地最轻量、最现实的第一阶段隔离手段，适合 Compass 先落 MVP。
- Compass 的结构天然有利于分层处理冲突：L1/L2 跟随分支，重点需要设计的是 L3/L4。

## 规划范围

- 采用 Lead/Teammate 模式，主 worktree 维护任务板，子 worktree 维护各自 session。
- 约定 `board.md`、`active-session.md`、commit message、branch naming 的协作规则。
- 定义 worktree 下哪些文档可以合并，哪些文档应被视为局部状态。
- 在 entrypoints 或 CLI 中加入“当前是否处于 linked worktree”识别逻辑。

## 非目标

- 不在第一阶段做 Cursor 式的超大规模递归调度器。
- 不要求实时 agent messaging 或中心化云端协调服务。
- 不试图一次解决所有多人协作和 merge policy 问题。

## 关键依赖

- 更稳定的任务板和 session 文件契约。
- Harness CLI 或等价检查层，帮助识别 worktree 模式下的违规写入。
- 对 `.gitattributes`、merge 规则和任务命名的一致约定。

## 里程碑建议

1. 先定义多 Agent 模式下的文档协议和 branch/worktree 命名规则。
2. 再做 worktree 模式的 entrypoint/CLI 检测与提示。
3. 最后补合并策略、冲突规避建议和演示案例。

## 开放问题

- L3 任务板是否仍放在当前结构，还是单独抽出 multi-agent board。
- 多 Agent 状态是否只通过 git 元数据传达，还是需要最小消息文件。
- 是否要对不同工具的 subagent/worktree 兼容性分别建规则。

## 相关文档

- [扩展层索引](README.md)
- [多 Agent 并行协作方案调研](../research/multi-agent-collaboration-research.md)
- [路线图总索引](../README.md)
- [工作流分析](../../workflow-analysis.md)
