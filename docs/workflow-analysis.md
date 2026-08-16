# Compass Workflow Analysis

> 本分支是 Compass simplify。项目知识在 README + `doc/`；不安装 Skill；不维护 L1–L5。

## 设计判断

- 同一事实只留一份：根 `README.md` 讲项目，`doc/<feature>_design.md` 讲模块，`doc/todo.md` 讲当前工作。
- 不为文档再造 Compass context，不为工作再造 Skill 入口。
- `main` 保留完整五层 + 9 个 Skill + SDD。

## 日常工作

```text
用户目标 → 读 README / 相关 design / todo → 改代码 → 跑测试
        → 行为变了更新同一份 design；任务变了更新 todo
```

没有 `/develop`、`/fix-bug`、`/build-context`。Agent 按 `AGENTS.md` 的 Project Knowledge 约定工作。

## CLI worker

安装时判定本机 `claude`。`enabled` 时 planner hook 把 pending tool call 交给 CLI。`disabled` 不装 hook。Claude Code 不装该 hook。

## 人工门槛

| 门槛 | 何时出现 |
|:-----|:---------|
| 产品决策 | 不同答案会改变范围、行为或主要成本 |
| 权限/外部副作用 | 部署、发布、push 或新权限 |
