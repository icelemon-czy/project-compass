# Agent QA

> 级别：平台层
> 优先级：P2
> 一句话：不仅用 Compass 约束代码质量，也用它来验证自身 workflow 是否真能发现问题。

## 要解决的问题

- Compass 现在强调 `review-tests`、traceability 和 false-pass 检测，但缺少反向验证机制。
- 如果 workflow 自己无法稳定抓住“植入的坏样本”，就很难证明它真的可靠。
- 没有自测体系，后续优化很容易只停留在主观体验层。

## 为什么现在做

- 这正好对应 Agent 评估工程方向，是 Compass 很有辨识度的路线。
- 一旦要支持更多工具和 agent，workflow 本身的质量基线必须可测。
- 这项能力和 Validation Analytics 是天然互补关系。

## 规划范围

- 设计一组故意植入的失败模式，如弱断言、错层 mock、spec/test 不一致、漏测边界值。
- 运行 `review-tests`、`fix-bug` 等流程，记录它们能否识别这些问题。
- 为 workflow 给出得分、回归基线和版本间对比。
- 形成一套能持续扩展的 benchmark 样本集。

## 非目标

- 不在第一阶段做通用 LLM Benchmark 平台。
- 不追求覆盖所有可能的测试反模式或 agent 行为。
- 不让验证系统复杂到压过 Compass 本身的主线价值。

## 关键依赖

- 结构化 validation 数据和可追踪的 workflow 输出。
- 足够清晰的 false-pass 反模式定义。
- 一种可以稳定重放样例和评估结果的执行方式。

## 里程碑建议

1. 先做 5 到 10 个高价值的植入样本。
2. 再把结果接入 Validation Analytics。
3. 最后形成版本回归基线，给 workflow 迭代提供客观反馈。

## 开放问题

- 验证样本应该放在独立测试仓库还是当前仓库下。
- 评估失败时，是阻塞发布还是只做告警。
- 是否需要按模型、按工具分别维护基线。

## 相关文档

- [平台层索引](README.md)
- [Validation Analytics Dashboard](../02-scale/validation-analytics-dashboard.md)
- [路线图总索引](../README.md)
- [工作流分析](../../workflow-analysis.md)
