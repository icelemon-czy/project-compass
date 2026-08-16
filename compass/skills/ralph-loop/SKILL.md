---
name: ralph-loop
description: "对有客观完成条件的任务持续迭代，直到验证通过或出现真实阻塞。Use only when the user explicitly asks for Ralph Loop, persistent iteration, or not to stop until checks pass."
---

# Ralph Loop — 持续迭代直到可验证终点

把一个明确任务变成外层循环：读取当前证据，执行一轮最小有效改进，重新验证，然后在未达到终点时继续。优先使用平台已经提供的持久 goal/continuation 能力；不要为了本 Skill 安装 Stop hook、复制 Skill 或在仓库中创建循环状态文件。

## Loop contract

开始前提取并明确：

1. **Objective**：最终要实现什么。
2. **Completion criteria**：哪些客观事实同时成立才算完成。
3. **Verifier**：实际运行什么测试、构建、lint、类型检查、基准或 eval。
4. **Scope**：允许修改和禁止触碰的范围。
5. **Safety cap**：可选的最大轮次、token budget 或完成承诺；用户没有提供时不要虚构。

优先从 README、项目配置和现有测试中发现验证命令，不要猜测。能够安全推断时直接开始；完全没有诚实的完成判据时，只问一个阻塞问题。

开放式 idea exploration 没有客观 Completion criteria，不启动 Ralph Loop；改用 `/brainstorm` 与用户收敛 design direction。

## Start persistent execution

显式调用 `/ralph-loop`、`$ralph-loop` 或明确要求 Ralph Loop，表示用户授权为该任务启动持久执行。

1. 平台已有 goal 工具时，先检查当前 goal：同一目标未完成则继续；不同目标未完成则不要覆盖；没有未完成 goal 则创建。
2. 只有用户明确提供 token budget 时才设置 token budget。
3. 平台没有持久 goal/continuation 能力时，在当前运行中执行同一循环，并说明无法保证跨 turn 自动续跑。
4. 不修改平台配置，不为本 Skill 安装 Stop hook。CLI worker hook 由 installer 拥有；本循环不得另装持续性 hook。

用户指定最大轮次时，把目标定义为“最多执行 N 轮”。达到上限但底层任务未完成时，循环可以结束，但必须把底层任务报告为 incomplete。

## Iteration cycle

每轮只做一个有证据支持的最小推进：

1. **Measure**：运行最小且最相关的 verifier。
2. **Choose**：选一个失败、瓶颈或新诊断假设作为本轮目标。
3. **Route**：创建或更新 project-local Skill 时走 `/skill-creator`。其他实现、修复、只读调查在本循环内直接做，读 README 与 `doc/`。
4. **Act**：在授权范围内实现或诊断。
5. **Verify**：有意义的改动后重新运行相关 verifier。
6. **Decide**：完成条件均成立则结束；仍失败且有新假设则下一轮；到达权限或外部依赖则按阻塞处理。

## Integrity rules

- 不删除、跳过、弱化或改写正确测试来制造绿灯。
- 不用未运行、过期、局部或不可复现的结果宣称完成。
- 不重复完全相同的失败动作。
- 不因循环持续执行而扩大权限或外部副作用。
- 不输出 completion promise，除非与它绑定的全部条件真实成立。

## Stop conditions

### Success

仅当所有 Completion criteria 成立、所需 verifier 已实际成功运行且没有剩余必做项时宣布成功。

### Finite-cap exit

达到最大轮次但底层任务仍未完成时，报告已完成内容、仍失败内容、最新 verifier 证据、最佳下一假设，以及 `Ralph loop finished; underlying task incomplete.`

### Blocked

只有真正缺少外部依赖、必要权限或用户业务决策，并且已经穷尽安全替代路径时才报告阻塞。困难、耗时或一次尝试失败都不构成阻塞。
