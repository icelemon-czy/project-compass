# Workflow Macros

> 级别：基础层
> 优先级：P2
> 一句话：把现有的原子 skills 组合成更贴近真实工程任务的可复用流程。

## 要解决的问题

- 现在的 skills 粒度清晰，但用户仍需要记住命令顺序和切换条件。
- 从 `new-change` 到 `review-tests` 再到 `archive-change` 的衔接，更多依赖提示词而不是流程定义。
- 同类任务会反复重复相同步骤，既增加上下文噪音，也降低一致性。

## 为什么现在做

- Compass 的工作流已经足够丰富，开始适合抽象成宏流程而不是继续增加原子命令。
- 一旦有了 Harness CLI，macro 可以成为最直接的用户入口。
- 这能显著降低新用户理解成本，也方便后续团队化使用。

## 规划范围

- 内置宏流程：`hotfix`、`feature`、`qa-sweep`、`release-readiness`。
- 为每个 macro 定义前置条件、执行阶段、失败回退和交付物。
- 允许 macro 在多个已有 skills 之间传递状态，而不是重新描述上下文。
- 记录每次 macro 执行后更新哪些文档和状态。

## 非目标

- 不做“全自动黑盒 autopilot”，每一步仍应保留可审查的中间状态。
- 不在第一版支持任意图灵完备的自定义工作流脚本。
- 不把所有特例都编码进核心宏流程。

## 关键依赖

- Harness CLI 或等价执行层。
- 更稳定的 change 状态定义和恢复机制。
- 对 `fix-bug`、`review-tests`、`archive-change` 等 skill 的输入输出约束做统一整理。

## 里程碑建议

1. 定义 macro 清单和每个宏的状态转移表。
2. 先实现 2 到 3 个内置宏，验证真实使用体验。
3. 视情况开放项目级自定义宏，但要保留可验证边界。

## 开放问题

- macro 是通过 CLI 触发，还是也要生成对应的 slash command。
- 宏流程执行失败后，如何以最少文案恢复到人工接管状态。
- 是否需要给 macro 单独的执行日志文件。

## 相关文档

- [基础层索引](README.md)
- [Compass Harness CLI](compass-harness-cli.md)
- [路线图总索引](../README.md)
- [工作流分析](../../workflow-analysis.md)