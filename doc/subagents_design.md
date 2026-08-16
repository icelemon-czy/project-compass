# Subagents

这是 `compass/subagents/` 的 design。

默认不生成 Subagent。只有用户明确要求时才渲染，目前可点名的角色是 `codebase-explorer`（只读查代码）。

源是 `compass/subagents/<role>.md`，经各平台 `agent` template 写到 native dest。目标不存在则创建；已有 Compass generated 标记则更新；无标记则不覆盖。

平台 dest 见 [platforms_design.md](platforms_design.md)。
