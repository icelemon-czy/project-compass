---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
  }
  section.lead h1 {
    font-size: 2.5em;
    text-align: center;
  }
  section.lead p {
    text-align: center;
  }
  table {
    font-size: 0.85em;
  }
  blockquote {
    border-left: 4px solid #0366d6;
    padding: 0.5em 1em;
    color: #555;
  }
  code {
    font-size: 0.9em;
  }
  h1 {
    color: #0366d6;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1em;
  }
  section.philosophy h1 {
    color: #d73a49;
  }
  em {
    color: #d73a49;
  }
---

<!-- _class: lead -->

# Project Compass

**Spec-Driven 的 AI 上下文管理框架**

通用模板 · 零依赖 · 工具无关

---

# AI 编程的两个根本问题

<br>

| 问题 | 现状 | 后果 |
|:------|:------|:------|
| **上下文有限** | 真实项目代码塞不进窗口 | AI 不知道看哪个文件，每次对话从零开始 |
| **没有需求驱动** | AI 的本能是"直接改代码"，跳过需求 | 改了什么没记录，测试事后补，需求与代码脱节 |

<br>

> 我们需要两件事：
> **让 AI 只加载需要的** + **让 AI 从 Spec 出发写代码**

---

# 解法：五层架构

Project Compass 在项目中建立一个 `.ai/` 目录，用 **5 层纯 Markdown 文档**同时解决这两个问题：

```
.ai/
├── L1-codebase-map/        ← 项目结构：代码导航（低频更新）
│   ├── overview.md          ← 唯一入口 < 60 行
│   ├── features/            ← 按功能拆分，渐进式深入
│   ├── module-map.md        ← 模块耦合 + 变更联动表
│   ├── architecture.md      ← 运行时架构
│   └── infrastructure/      ← 框架/中间件/构建
│
├── L2-rules/                ← 编码规则（低频更新）
│   ├── global.md            ← 可执行规则 + 反模式清单
│   └── templates.md         ← 新建文件的代码模板
│
├── L3-specs/                ← 需求：Spec-Driven（随变更更新）
│   ├── specs/               ← 当前系统需求（TOR → HLR）
│   ├── changes/             ← 进行中变更（文件系统 = 状态）
│   └── archive/             ← 已完成变更
│
├── L4-session/              ← 会话延续（每次对话更新）
│
└── L5-validation/           ← 测试：追溯 + 验证（验证后更新）
    ├── traceability/        ← Spec ↔ Code ↔ Test 映射
    └── test-specs/          ← 测试用例设计
```

> L1/L2 解决"上下文有限" · L3/L5 解决"没有需求驱动" · L4 让 AI 不再失忆

---

<!-- _class: philosophy -->

# 哲学一：渐进式加载

AI 每次对话 **只读 < 60 行索引**，根据任务按需深入

```
对话启动（自动）
  → 加载 overview.md（功能索引）+ global.md（规则）+ active-session.md（进度）

收到任务
  → overview.md 索引匹配
    ├─ 匹配到具体功能  → features/[功能名]/README.md → 按需深入层文件
    ├─ 做常见开发任务  → key-files.md（任务食谱 + 调查起点）
    ├─ 修改涉及多模块  → module-map.md（模块合约 + 依赖规则 + 变更联动）
    ├─ 理解运行时/排查跨层问题  → architecture.md（请求生命周期 + 启动顺序）
    └─ 改底层基础设施  → infrastructure/README.md

  → 路径可组合（跨功能修改同时加载 feature doc + module-map）
```

| 传统方式 | Project Compass |
|:---------|:----------------|
| 全量塞入上下文，浪费窗口 | 自动加载 3 个基础文件，其余按需 |
| 每次对话从零开始 | L4 会话层延续上次进度 |
| AI 不知道该看哪 | 索引 + 决策树精准定位 |

---

<!-- _class: philosophy -->

# 哲学二：Spec-Driven Development

**一切代码基于需求** — 没有 Spec 就不写代码

任何变更（Bug / 新功能 / 重构）都走同一条路：

```
收集上下文（L1 导航定位 + L3 现有 Spec）
      ↓
创建 Proposal（为什么做 + 改什么 + 备选方案）
      ↓
写 Delta Spec（WHEN/THEN 场景化需求）
      ↓
提验收问题 → 等人确认
      ↓
先写/更新测试用例 ← 从 Spec Scenario 直接映射
      ↓
再写代码 ← 让测试从红变绿
      ↓
更新追溯矩阵（Spec ↔ Code ↔ Test）
      ↓
归档（delta spec 合并到主 spec）
```

核心纪律：**永远 Spec → Test → Code，不允许跳过**

---

<!-- _class: philosophy -->

# 哲学三：结构 → 需求 → 测试 → 代码

四者形成闭环，代码是 *最后一环*，不是第一环

<br>

| 链条 | 对应层 | 作用 |
|:------|:-------|:------|
| **项目结构** | L1 导航 + L2 规则 | AI 知道"在哪"和"怎么写" |
| **需求** | L3 Spec | 定义"做什么" — TOR → HLR → Scenario |
| **测试** | L5 验证 | 证明"做对了" — 追溯矩阵 + 测试用例 |
| **代码** | 实际代码库 | 最后才动手 — 被 Spec 约束、被 Test 验证 |

<br>

> L4 会话层贯穿其中 — 让 AI 跨对话延续进度，不再每次失忆

---

# Spec-Driven 变更流程

**从"用户说一句话"到"代码落地"的完整路径**

```
"修复用户登录的 token 刷新 bug"
      ↓
  ① 收集上下文 — L1 定位功能 + L3 查现有 Spec
      ↓
  ② Proposal — 为什么做 + 改什么 + 影响范围
      ↓
  ③ Delta Spec — 补写/修改 WHEN/THEN 场景
      ↓
  ④ 验收问题 — 提 3-5 个业务问题 → 🧑 等人确认
      ↓
  ⑤ Tasks — 生成 checkbox 执行步骤
      ↓
  ⑥ 🧑 人确认 proposal + spec + tasks
      ↓
  ⑦ 执行 — 先写测试（红灯）→ 再改代码（绿灯）
      ↓
  ⑧ 归档 — delta spec 合并到主 spec → 移入 archive/
```

> **文件系统即状态** — `changes/` = 进行中，`archive/` = 已完成
> **人参与 2 个节点** — ④ 回答验收问题 + ⑥ 确认方案

---

# 验证闭环：以 Spec 为中心

Spec 是核心驱动 — 代码和测试都围绕它生长

```
                  ┌──────────┐
          ┌──────→│   Spec   │←──────┐
          │       │ (L3 需求) │       │
          │       └────┬─────┘       │
    正向追溯│            │ 驱动        │反向追溯
    Spec→Code→Test     ↓        Code→Spec
          │    ┌───────┴───────┐     │
          │    ↓               ↓     │
      ┌───┴────┐         ┌────┴───┐
      │  Code  │←───验证──│  Test  │
      │ (代码)  │         │ (测试)  │
      └────────┘         └────────┘
```

| Spec Scenario | 代码 | 测试 | 状态 |
|:------------|:---------|:---------|:-----|
| 用户登录 — 正常登录 | auth.ts:45 | auth.test.ts:12 | ✅ verified |
| 用户登录 — 空密码 | auth.ts:52 | — | ⚠️ untested |
| 用户登录 — Token 过期 | — | — | ❌ unimplemented |

> 缺口一目了然。AI 自动为 ⚠️ / ❌ 生成测试用例并补全代码。

---

# 自动化：Builder + 6 个 Skill

**Builder Prompt**：5 个独立 prompt 从零构建 `.ai/`（`builders/cline/` 下）

| 顺序 | Prompt | 构建内容 |
|:-----|:-------|:---------|
| 1 | `prompt-L1a.md` | overview.md + 功能清单 + `_handoff.md` |
| 2 | `prompt-L1b.md` | features/ 文档 + architecture + module-map + key-files |
| 3 | `prompt-L2.md` | global.md + templates.md + 模块规则 |
| 4 | `prompt-L3.md` | system.md (TOR) + 能力域 spec (HLR) |
| 5 | `prompt-L5.md` | 追溯矩阵 + 验证报告 |

**6 个 Copilot Skill（关键词自动触发，中英文支持）**

| 哲学归属 | Skill | 触发词 | 做什么 |
|:---------|:------|:-------|:-------|
| 渐进式加载 | `/build-ai` | "初始化 .ai" | 从零构建完整上下文 |
| 渐进式加载 | `/update-ai` | "刷新 .ai" | 代码变了同步上下文 |
| Spec-Driven | `/new-change` | "加个功能" | 走完 proposal → spec → tasks |
| Spec-Driven | `/spec-fix` | "有 bug" | Spec → Test → Code 修复 |
| 验证闭环 | `/review-tests` | "测试够吗" | 交叉比对 spec 与测试覆盖率 |
| 验证闭环 | `/check-changes` | "变更状态" | 汇总所有进行中变更进度 |

---

# 工具无关 · 零安装

**纯 Markdown 模板，`cp` 即用，不锁定任何平台**

<br>

| AI 工具 | Entrypoint 文件 | 放置位置 |
|:--------|:----------------|:---------|
| Cline | `entrypoints/clinerules.md` | 项目根目录 `.clinerules` |

<br>

> 同一套 `.ai/` 文档，切换工具只需换 entrypoint。
> 团队成员可以用不同的 AI 工具，共享同一份上下文。

---

# 核心价值

<br>

### 🗺️ 渐进式加载
AI 不再迷路 — 每次只看需要的，< 60 行即可开始工作

<br>

### 📋 Spec-Driven
代码不再野蛮生长 — Bug 和新功能都走 Spec → Test → Code

<br>

### 🔄 结构 → 需求 → 测试 → 代码
完整闭环 — 测试不是事后补丁，是代码落地的前提

<br>

> **一切变更有据可查，一切代码基于需求**

---

<!-- _class: lead -->

# 三步上手

<br>

**① 复制模板到项目**
`cp -r project-compass /your-project/.ai/`

**② 用 Builder Prompt 构建上下文**
在 Cline 中依次执行 L1a → L1b → L2 → L3 → L5
两种模式可选：`sub-agent/`（子代理只读）或 `single-agent/`（逐项暂停人工审）
每个 prompt 独立，复制到新对话中执行即可

**③ 部署 Entrypoint 入口文件**
复制 `entrypoints/clinerules.md` 到项目根目录 `.clinerules`
→ 此后每次 AI 对话自动加载 `.ai/` 上下文并自主导航

<br>

**让 AI 按规矩做事，从 Spec 开始。**
