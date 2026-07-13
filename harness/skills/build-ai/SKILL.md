---
name: build-ai
description: "Build or initialize Compass Harness project context from source code and confirmed requirements. Use when: setup ai context, build ai docs, 构建AI上下文, 初始化上下文, brownfield onboarding, new project context"
---

# Build Compass Harness Project Context

在已经复制到目标项目的 `.compass-harness/` 中初始化并填写项目上下文。本 Skill 不安装 Skills、不生成 Subagent，也不维护平台适配；这些边界由 `.compass-harness/INSTALL.md` 定义。

## Prerequisites

- `.compass-harness/INSTALL.md` 存在。
- `.compass-harness/context/` 存在，并包含 L1–L5 空白结构。
- 目标项目已有可分析的源码、配置或已确认需求。

如果 Compass Harness 尚未复制到项目中，停止并要求用户先完成复制，不要自行构造另一套目录。

## Procedure

### Step 1: Initialize context safely

按 `.compass-harness/INSTALL.md` 的上下文规则执行：

1. `.compass-harness/context/` 是唯一上下文目录 → 保留并增量更新，不覆盖。
2. 存在旧 `.ai/` → 将已确认且仍适用的内容迁移到 `.compass-harness/context/`，验证后保留旧目录等待用户确认清理。
3. `.compass-harness/context/` 不存在或缺失 L1–L5 → 停止并要求用户重新复制完整 `harness/`；不要自行创建另一套模板目录。

不要把空模板描述为已经确认的项目事实。

### Step 2: Build the five context layers

读取目标项目的源码、配置、测试和用户提供的需求文档，按以下顺序填写：

| Order | Layer | What to establish |
|:------|:------|:------------------|
| 1 | L1 Codebase Map | 最小功能索引、入口、数据流和模块依赖 |
| 2 | L2 Rules | 从真实代码和配置确认的编码、测试与模块约束 |
| 3 | L3 Specs | 已知系统需求、能力 Spec 和变更状态机 |
| 4 | L4 Session | 只在确实需要恢复中断工作时记录 |
| 5 | L5 Validation | 只记录已经检查的 Spec–Code–Test 证据 |

无法从源码、配置、测试或用户输入确认的内容必须标记为待确认，不能猜测。

### Step 3: Verify

实际检查：

```bash
test -d .compass-harness/context
test -f .compass-harness/context/L1-codebase-map/overview.md
test -f .compass-harness/context/L2-rules/global.md
test -f .compass-harness/context/L2-rules/testing.md
test -f .compass-harness/context/L3-specs/change-management.md
test -f .compass-harness/context/L5-validation/validation-rules.md
```

然后确认：

- `overview.md` 是小型导航索引，不是源码目录转录。
- L2 规则均能追溯到真实代码或配置。
- Spec 只记录已确认需求。
- L5 不包含未经检查的“verified”结论。
- 没有修改 `.compass-harness/skills/` 或生成任何 Subagent。

## Output

报告已初始化、已填写、保留未动、待确认和验证结果。不得只回复“上下文已构建”。
