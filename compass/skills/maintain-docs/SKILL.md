---
name: maintain-docs
description: "检查并维护项目 README 和 doc design；用于 review 文档准确性、发现 code drift，或按已确认实现增量同步和修复文档。Not for 首次建立整套文档、实现 product code，或从当前代码猜测产品需求。"
---

# Maintain Docs

用同一次 evidence review 完成文档审查或增量更新；review 和 update 只是不同的收尾方式，不是两个 Skill。

## Mode

- 用户要求检查、review 或 audit，或明确禁止修改：`review-only`，不写文件。
- 用户要求更新、同步、修复或整理：`update`，先 review，再做最小必要修改。
- 普通 code work 改变了 behavior、boundary、flow、dependency 或重要 decision：作为该工作的内部 postcondition，只同步实际影响的 design；不扩大到全库重建。

意图不明确时默认 `review-only`。首次建立、整体重整或需要重新识别多数 feature boundary 时改用 `build-docs`。

## Flow

1. 确定 scope：优先使用用户指定的 feature、文件或 change；普通 code work 使用本次实际 diff；只有用户要求周期性检查时才扩到 recent commits 或全库。
2. 先读 project instructions、README 和相关 `doc/`，再用 source、config、test、runtime evidence 与必要 Git history验证。Git diff 是定位线索，不是 feature 语义的 ground truth。
3. 找出并引用证据：stale 或错误事实、缺失 design、重复 source of truth、失效链接、孤立 document、错误 feature boundary，以及 README 中过深的 feature detail。
4. `review-only`：按影响排序返回 findings、证据、建议修改和 uncertainty，不修改任何文件。
5. `update`：只修改已由证据确认的内容；同步 README Document map 与 rename/split/merge reference。产品意图冲突只暂停受影响项，其余明确项继续。
6. 验证链接、referenced path、Document map、重复事实和本次变更覆盖面。跨多个 feature、重大重构或用户要求独立复核时，可委派已安装的只读 `docs-reviewer`；Main Agent 复核其证据。

## Output

- `review-only`：scope、findings、证据、建议和 uncertainty。
- `update`：更新文件、修复的 drift、保留未动内容、验证和仍待确认 conflict。
- 普通 code work：最终摘要只说明同步了哪些 design 或为何无需同步。

## Anti-patterns

- review 请求中擅自修改文件。
- 每次小改都扫描和重写整个 `doc/`。
- 仅凭文件增删判断 feature 新增、删除或 rename。
- 为措辞变化制造无意义 document churn。
