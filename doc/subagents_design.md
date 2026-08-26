# Subagents

这是 `compass/subagents/` 的 design。

默认不生成 Subagent。只有用户明确要求时才渲染，目前可点名的角色是：

| Role | 做什么 |
|:-----|:-------|
| `codebase-explorer` | 只读定位代码、call path 和测试 |
| `docs-reviewer` | 跨 feature 或重大文档变更后独立检查 README、`doc/` 与当前实现 |

两个角色都只返回证据，不写文件。`docs-reviewer` 只在 review 范围足够大或用户明确要求独立复核时使用；小范围检查由 Main Agent inline 完成。

源是 `compass/subagents/<role>.md`，经各平台 `agent` template 写到 native dest。目标不存在则创建；已有 Compass generated 标记则更新；无标记则不覆盖。

平台 dest 见 [platforms_design.md](platforms_design.md)。
