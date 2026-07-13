# Cross-Tool Adapter Layer

> 级别：扩展层
> 优先级：P2
> 一句话：把 Compass 的核心 workflow 定义收束成单一来源，再为不同 AI 工具生成适配层，而不是维护多份平行 prompt。

## 要解决的问题

- 工具要求不同的根入口、Skill 发现目录和 Subagent 格式，若直接维护容易出现知识重复。
- 同一个 workflow 在不同工具上容易逐渐漂移，最终出现行为不一致。
- 新增工具支持时，维护成本会随工具数量线性上升。

## 为什么现在做

- 工具生态在继续分化，Compass 不应该把价值建立在某一套 prompt 文案上。
- 多 Agent、governance、macro 等后续能力都需要更稳定的 workflow 契约。
- OpenSpec 在多工具支持上的经验说明，适配层值得成为独立设计面。

## 规划范围

- 定义 Compass workflow 的 canonical schema。
- 为 Codex、Claude Code 和 OpenCode 生成对应的 instructions/skills。
- 建立适配器测试，检查不同工具资产是否跟 canonical schema 保持同步。
- 让 `.compass/` 成为唯一权威源，平台入口和发现目录全部由它生成。

## 非目标

- 不追求所有工具表现出完全相同的交互体验。
- 不在第一阶段支持所有新工具的高级特性。
- 不把 Compass 变成只面向某个 vendor 的封闭工具链。

## 关键依赖

- Compass CLI 或生成器能力。
- 更明确的 workflow schema 和公共接口定义。
- 针对不同工具最小能力模型的整理。

## 里程碑建议

1. 先抽出 canonical schema，验证能生成当前三套主要资产。
2. 再补自动对比和 drift 检测。
3. 最后扩大支持范围，并评估是否引入插件式 adapter。

## 开放问题

- schema 的表示是 YAML、JSON Schema 还是 Markdown + frontmatter。
- 适配器层是仓库内生成，还是独立 package 分发。
- 工具特性差异过大时，哪些行为允许偏离，哪些必须一致。

## 相关文档

- [扩展层索引](README.md)
- [路线图总索引](../README.md)
- [根 README](../../../README.md)
