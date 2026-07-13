# Validation Analytics Dashboard

> 级别：扩展层
> 优先级：P1
> 一句话：把 L5 和 review 流程沉淀的数据，转成可追踪的质量信号和趋势视图。

## 要解决的问题

- 现在已经有 traceability、test-specs 和 validation reports，但很难看出趋势。
- 团队无法快速回答“哪些 change 经常 review-failed”“哪些模块最容易 false-pass”。
- 没有稳定的质量指标，就很难判断某个 workflow 或 skill 的改动到底有没有提升效果。

## 为什么现在做

- Compass 的差异化之一就是验证严谨性，应该把这一点从文档层推进到观测层。
- 多 Agent 和跨工具扩展之前，需要先知道质量是如何变化的。
- L5 已经是天然的数据采集面，适合往上做聚合和可视化。

## 规划范围

- 聚合 spec coverage、scenario coverage、false-pass 发现数、archive latency 等核心指标。
- 汇总 review-failed 原因、风险模块、未闭环 gaps。
- 支持按 change、按 capability、按时间窗口查看趋势。
- 产出轻量 dashboard 或汇总报告，而不是只保留离散 Markdown 文件。

## 非目标

- 不在第一阶段做重型 SaaS 级 BI 平台。
- 不采集与 Compass 目标无关的泛化开发者行为数据。
- 不用 dashboard 取代原始 validation 文档。

## 关键依赖

- `review-tests`、`fix-bug`、`archive-change` 的输出需要更结构化。
- L5 报告格式需要具备可聚合字段。
- 需要约定哪些指标是 Compass 的一等公民。

## 里程碑建议

1. 先定义指标字典和 L5 报告的结构化字段。
2. 再做聚合脚本和摘要报告。
3. 最后视需要做图表化展示或简单 Web/CLI dashboard。

## 开放问题

- 指标采集是否只依赖本地 Markdown，还是需要额外 JSON sidecar。
- 哪些指标可以跨项目比较，哪些只能项目内看趋势。
- 如何避免为了好看指标而牺牲 workflow 简洁度。

## 相关文档

- [扩展层索引](README.md)
- [路线图总索引](../README.md)
- [根 README](../../../README.md)
- [工作流分析](../../workflow-analysis.md)