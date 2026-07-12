# Compass Harness Roadmap

> 更新日期：2026-07-12
> 说明：正文保留中文，按层分目录；每个路线方向单独一个 Markdown 文件。

## 如何阅读

- 先读每一层的 `README.md`，理解该层的定位和优先级。
- 再进入单个方向文档，查看问题定义、范围、依赖和里程碑建议。
- `research/` 只放支撑判断的调研资料，不直接承载路线优先级结论。

## 分层目录

- [基础层 / 01-foundation](01-foundation/README.md)：近期最值得落地的基础能力。
- [扩展层 / 02-scale](02-scale/README.md)：面向多 Agent、跨工具和长期运行的扩展能力。
- [平台层 / 03-platform](03-platform/README.md)：面向组织、生态和平台化的长期能力。
- [研究资料 / research](research/README.md)：路线判断的背景研究和方案比对。

## 当前优先顺序

1. [Compass Harness CLI](01-foundation/compass-harness-cli.md)
2. [Multi-Agent Worktree Mode](02-scale/multi-agent-worktree-mode.md)
3. [Validation Analytics Dashboard](02-scale/validation-analytics-dashboard.md)
4. [Brownfield Onboarding Analyzer](01-foundation/brownfield-onboarding-analyzer.md)
5. [Cross-Tool Adapter Layer](02-scale/cross-tool-adapter-layer.md)

## 路线图原则

- Compass Harness 要从“文档模板”演进为“可执行的 AI workflow harness”。
- 优先补执行层、验证层和协作层，不优先堆更多说明性文档。
- 保持和 OpenSpec 的差异化：更强调上下文导航、验证严谨性和多 Agent 协作。
- 把 `.agents/skills/` 和 `templates/compass-harness/` 视为公共接口来设计。
