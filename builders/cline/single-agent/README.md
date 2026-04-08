# Cline 单 Agent 模式

本文件夹包含 **单 Agent + 人工审核** 的 L1 构建流程。

## 与标准版的区别

| | 标准版 (`builders/cline/`) | 单 Agent 版（本文件夹） |
|---|---|---|
| 功能分析 | subagent 并行分析 | 主 agent 逐个分析 |
| 基础设施分析 | 主 agent 一次完成 | 主 agent 逐个，每个暂停 |
| 人工审核 | 全部完成后统一检查 | 每个功能/组件完成后暂停审核 |
| 适用场景 | 追求效率、功能多的项目 | 对质量要求高、需要逐项把关 |

## 使用方式

1. **Phase 1-3**：使用 `builders/cline/prompt-L1a.md`（共用，无需修改）
2. **Phase 4-5**：使用本文件夹的 `prompt-L1b.md`（替代标准版的 L1b）
3. **L2/L3**：使用 `builders/cline/prompt-L2.md` 和 `prompt-L3.md`（共用）
