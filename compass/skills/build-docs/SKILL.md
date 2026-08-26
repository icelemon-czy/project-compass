---
name: build-docs
description: "为已有项目首次建立或整体重整 README 和 doc design。Use when project documentation is missing, scattered, or needs a broad rebuild; not for routine drift review, incremental sync, or product implementation."
---

# Build Docs

把项目已有事实整理成轻量、可导航的 README + `doc/`，不恢复另一套 context hierarchy。

## Boundary

- 只维护项目 README 和 `doc/`；不修改 product code、安装配置或 global environment。
- 首次建立、整体重整或重大结构变化后的 broad rebuild 使用本 Skill；局部 review 和增量修复使用 `maintain-docs`。
- 保留仍有效的已有事实。用户确认和产品文档决定 intended behavior；code、config、test 和 runtime evidence 只证明 current implementation。
- 无法确认的产品语义标记为 conflict 或待确认，不从当前实现反推需求。

## Flow

1. 读取 project instructions、README、现有 `doc/`、主要入口、配置、测试和必要 Git history，区分 canonical fact、重复说明和 stale content。
2. 按独立目的、observable behavior 和 ownership 识别 feature boundary；不要按源码目录逐个生成 design。
3. 先形成最小 document map。只有 merge、rename 或删除会产生多种合理结果或丢失用户内容时才询问用户。
4. 整理 README：开头说明项目持续解决什么，用 Document map 链接每份 canonical design；不要把 feature detail 写回 README。
5. 为每个已确认 feature 创建或整理 `doc/<feature>_design.md`。从 big picture 展开目的、behavior、boundary、主要 flow 和真正影响维护的 decision；简单 feature 不强制填满固定 heading。
6. 仅在项目确实需要当前工作清单时保留或创建 `doc/todo.md`；不把永久 design 或已完成历史放进去。
7. 验证所有链接与 referenced path，检查孤立 document、重复 fact、缺失 feature 和与源码冲突的陈述。大范围独立复核且已安装 `docs-reviewer` 时可以委派；Main Agent 仍负责写入和最终判断。

## Output

报告建立或重整的 document map、创建/合并/保留的文件、依据、仍待确认的产品 conflict 和验证结果。

## Anti-patterns

- 复制源码目录树作为文档结构。
- 为每个 module、class 或 file 创建 design。
- 用当前代码覆盖已确认但尚未实现的产品行为。
- 同时在 README 和 feature design 维护同一段事实。
