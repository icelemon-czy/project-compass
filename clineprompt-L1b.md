# Cline 构建 L1 代码导航文档 — Phase 4-5（深入分析阶段）

> **前置条件**：已完成 `clineprompt-L1a.md`，且 `.ai/L1-codebase-map/_handoff.md` 已存在。
> **本文件产出**：features/[name]/ 完整文档 + module-map.md + key-files.md

---

## Prompt

```markdown
# 任务：构建项目代码导航文档（L1）— Phase 4-5

## 准备工作

首先执行：
```bash
cat .ai/L1-codebase-map/_handoff.md
```

读取后，你将获得：功能清单、跨功能通用模式、overview.md 全文。这是本对话的全部背景。

---

### Phase 4: 为每个功能强制派发 Feature Sub-agent（核心步骤）

> ⚠️ 对 `_handoff.md` 功能清单里的**每个功能**，逐一派发一个独立的 Feature Sub-agent。
> 主 agent 不直接分析任何功能的代码。

---

````
你是一个代码分析 sub-agent，专门负责分析「[功能名]」这一个功能。
规模：[small / medium / large]（small → README.md 一个文件即可；large → 需要完整分层）

## 项目背景
<!-- 将 _handoff.md 中 "overview.md 全文" 部分粘贴到这里。不要附带其他文件。 -->

[粘贴 .ai/L1-codebase-map/overview.md 的完整内容]

## 你的任务
为「[功能名]」生成完整的上下文文档，存放到：
.ai/L1-codebase-map/features/[功能名]/

## 执行步骤

### Step 1 — 层次发现（先看代码，再输出清单）

1. 执行 `cat [入口文件路径]` 阅读入口文件
2. 顺着调用链，对每一层的代表文件执行 `cat [文件路径]` 实际阅读
3. **阅读完代码后**，输出层次清单：

| 层名（项目词汇） | 代表文件 | 职责一句话 |
|----------------|---------|------------|
| [填写] | [填写] | [填写] |

**命名规则**：用项目里真实存在的概念（如 handler / service / repo / proto / worker），**禁止直接使用 entry / logic / data 通用词**。

> ⚠️ 未执行 cat 命令、未阅读实际代码前，不得进入 Step 2。

### Step 2 — 追踪数据流 + 发现联动

以「[追踪起点函数/方法：[函数名]]」为起点，追踪该功能最核心的 1-2 个操作的完整路径。
同时找出：
- 改了文件 A，哪些看似无关的文件 B 也要改？
- 有 TODO/FIXME/HACK 的坑？

### Step 3 — 创建文件夹和文件

根据规模和 Step 1 的层次清单：
- **small**：只创建 `README.md`，包含数据流、变更影响表、已知陷阱
- **medium / large**：创建 `README.md` + 每一层一个 `.md` 文件（**文件名 = Step 1 中确定的层名**）

内容格式参考 `.ai/L1-codebase-map/features/_feature-template/` 里各文件的 section 结构，但文件名和文件数量完全由 Step 1 决定。

## 约束
- 每个文件自包含
- 不确定的地方写 `[待确认：xxx]`
- 检验标准：每一行都问"AI 从代码中能推导出来吗？"如果能，删掉
````

---

所有 Feature Sub-agent 完成后，主 agent 继续 Phase 5。

### Phase 5: 填写 module-map.md + key-files.md

使用 `_handoff.md` 中"跨功能通用模式"部分，结合各 feature 文档的变更影响表：

- **module-map.md** — 模块公开 API、依赖规则、跨功能的变更联动
- **key-files.md** — 通用任务食谱（不属于单一功能的）、调查起点

完成后删除 `.ai/L1-codebase-map/_handoff.md`（临时交接文件，不需要保留）。

## 约束
- 每个 feature 文件自包含，可独立加载
- 不确定的地方写 `[待确认：xxx]`
- **检验标准**：每一行都问"AI 从代码中能推导出来吗？"如果能，删掉
```

---

## 补充说明

### 质量检验清单

| 检查项 | 通过标准 | 不通过的例子 |
|--------|----------|-------------|
| feature 文件是否自包含？ | 只读这一个文件就够做该功能的任务 | ❌ 还要去 overview 查数据流 |
| 是否可推导？ | AI 不能从 tree + grep 快速推导出来 | ❌ "auth 模块在 src/auth/ 目录下" |
| 是否面向任务？ | 有具体的文件路径和步骤 | ❌ "改了 model 要更新相关文件" |
| feature 文件名是否反映实际架构？ | 文件名来自项目真实概念 | ❌ 所有功能都是 entry.md / logic.md / data.md |

### Agent 职责划分（本文件范围）

```
主 Agent（Cline）—— 本对话
├── 读取 _handoff.md（功能清单 + 跨功能模式 + overview 全文）
├── Phase 4：为功能清单里的每个功能，逐一派发 Feature Sub-agent（强制，不可选）
│     ├── 【Feature Sub-agent: user-auth】  → 独立 context，自主分析，自主决定层次结构
│     ├── 【Feature Sub-agent: order-mgmt】 → 独立 context，自主分析，自主决定层次结构
│     └── 【Feature Sub-agent: ...】
└── Phase 5：所有 sub-agent 完成后，填写 module-map.md + key-files.md
```

### 完成后

L1 文档生成后，继续用 `clineprompt-L2.md` 生成 L2 编码规则。
建议在同一对话中继续（Phase 4-5 的信息可复用），或上下文满了就开新对话。
