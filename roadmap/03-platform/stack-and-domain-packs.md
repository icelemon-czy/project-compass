# Stack And Domain Packs

> 级别：平台层
> 优先级：P2
> 一句话：把常见技术栈和业务领域的经验沉淀成可组合的 Compass 包，而不是每次都从空模板开始。

## 要解决的问题

- 很多项目会重复构建类似的 L1/L2/L3/L5 内容，尤其是常见技术栈和通用业务域。
- 没有 pack 的情况下，Compass 更像空白框架，难以立刻体现领域经验价值。
- 用户很难判断“哪些规则是通用 Compass，哪些规则属于某个 stack/domain 的最佳实践”。

## 为什么现在做

- Brownfield analyzer 和基础层稳定之后，开始有条件把经验沉淀为可复用资产。
- 这能显著提升首轮体验，也让 Compass 更有生态位。
- Pack 机制也能为组织级定制和插件化铺路。

## 规划范围

- 技术栈 pack：如 React + Node、FastAPI、Django、Go service。
- 业务域 pack：如 auth、billing、background jobs、audit logging。
- 每个 pack 包含建议的 L1 导航方式、L2 规则、L3 spec 模板和 L5 测试要点。
- 支持在核心骨架之上组合多个 pack，而不是复制一整套模板。

## 非目标

- 不在第一阶段做庞大的公开 marketplace。
- 不承诺 pack 一装即用、无需人工调整。
- 不把所有项目差异压平为单一模板。

## 关键依赖

- 更明确的 Compass 核心层与扩展层边界。
- Brownfield analyzer 或初始化流程能识别适合的 pack。
- 一种可版本化、可组合的 pack 描述方式。

## 里程碑建议

1. 先做 2 到 3 个高频技术栈 pack。
2. 再做 2 个有代表性的业务域 pack。
3. 最后评估 pack 组合、版本兼容和发布机制。

## 开放问题

- pack 的分发形态是仓库目录、独立 package，还是两者并存。
- 技术栈 pack 和业务域 pack 的冲突如何合并。
- 是否需要给 pack 建立维护者和兼容版本矩阵。

## 相关文档

- [平台层索引](README.md)
- [Brownfield Onboarding Analyzer](../01-foundation/brownfield-onboarding-analyzer.md)
- [路线图总索引](../README.md)
- [根 README](../../README.md)