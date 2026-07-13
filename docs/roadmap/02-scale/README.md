# 扩展层路线图

> 定位：在基础层稳定之后，把 Compass 扩展到多 Agent、跨工具和可观测的长期工作流场景。

## 收录方向

- [Multi-Agent Worktree Mode](multi-agent-worktree-mode.md)：让多个 agent 能在同一仓库中并行、安全地协作。
- [Validation Analytics Dashboard](validation-analytics-dashboard.md)：把验证数据汇总为趋势和质量信号。
- [Cross-Tool Adapter Layer](cross-tool-adapter-layer.md)：减少不同 AI 工具之间的重复 prompt 维护。

## 为什么这是第二层

- 这层的价值建立在基础层已经把执行和结构约束收稳的前提上。
- 多 Agent 和跨工具都需要统一契约，否则只会把当前的不稳定放大。
- 这层更偏“扩大适用范围”，而不是“先把最小系统跑起来”。