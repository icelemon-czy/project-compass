---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
    font-size: 22px;
    padding: 40px 50px;
  }
  section.lead h1 {
    font-size: 2.5em;
    text-align: center;
  }
  section.lead p {
    text-align: center;
  }
  table {
    font-size: 0.7em;
    width: 100%;
  }
  td, th {
    padding: 0.2em 0.4em;
  }
  blockquote {
    border-left: 4px solid #0366d6;
    padding: 0.3em 0.8em;
    margin: 0.3em 0;
    color: #555;
    font-size: 0.85em;
  }
  code {
    font-size: 0.85em;
  }
  pre {
    font-size: 0.7em;
    padding: 0.4em;
    margin: 0.3em 0;
  }
  h1 {
    color: #0366d6;
    margin-bottom: 0.3em;
  }
  p, ul, ol {
    margin: 0.2em 0;
  }
  li {
    margin: 0.1em 0;
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

让 AI 编程可控、高效、可追溯
通用模板 · 零依赖 · 工具无关

---

# AI 编程的两个根本问题

| 痛点 | 场景 | 代价 |
|:------|:------|:------|
| **上下文有限** | 真实项目代码塞不进窗口 | 超出窗口 → AI 产生幻觉，编造不存在的 API 和文件 |
| **目标游离式开发** | AI 的本能是"直接改代码"，跳过需求 | 改了什么没记录，测试事后补，需求与代码脱节 |

<br>

> 我们需要两件事：
> **让 AI 检索需要的文件** + **让 AI 从需求出发写代码**

---

# `.ai/` Framework

在项目中建一个 `.ai/` 目录，系统性解决上面两个问题：

| 层 | 解决什么 | 一句话 |
|:---|:---------|:-------|
| **L1** 项目导航 | AI 不知道看哪 | < 60 行索引，按需深入 |
| **L2** 编码规则 | AI 不知道怎么写 | 规则 + 测试规范 + 模板 |
| **L3** 需求文档 | 代码没有需求驱动 | Spec → 变更 → 归档 |
| **L4** 会话记忆 | 每次对话从零开始 | 跨对话延续进度 |
| **L5** 测试追溯 | 改了不知道对不对 | Spec ↔ Code ↔ Test 追溯 |

> **核心原则**：人类意图(Prompt) -> 需求对齐 → 编写测试 → 代码 -> 测试通过

---

<!-- _class: philosophy -->

# 哲学一：渐进式加载

AI 每次对话 **只读 < 60 行索引**，根据任务按需深入

| 阶段 | 加载内容 |
|:-----|:---------|
| **启动**（自动） | 功能索引 `overview.md` + 编码规则 `global.md` + 上次进度 `active-session.md` |
| **定位**（按需） | 匹配任务类型 → `features/` · `key-files.md` · `module-map.md` |
| **组合**（按需） | 跨功能修改同时加载多个文档，路径可组合 |

| 工作场景 | 以前怎么做 | 使用之后 |
|:---------|:-----------|:---------|
| 开始一个新任务 | 手动粘贴相关代码给 AI，经常漏 | AI 自动按索引定位，直接进入正题 |
| 跨天继续开发 | 重新解释背景，浪费 10-20 分钟 | 会话层记录进度，接上就能继续 |
| AI 编造不存在的函数 | 频繁出现，靠人工盲审 | 上下文精准，幻觉大幅减少 |
| 大项目多模块修改 | 上下文爆窗口，AI 只看到局部 | 按需组合加载，窗口始终有效 |

---

<!-- _class: philosophy -->

# 哲学二：Spec-Driven — 需求驱动一切

```
              ┌──────────┐
              │   Spec   │
              │ (L3 需求) │
              └────┬─────┘
                   │ 驱动
           ┌───────┴───────┐
           ↓               ↓
      ┌────────┐     ┌────────┐
      │  Test  │──→──│  Code  │
      │ (测试)  │ 验证 │ (代码)  │
      └────────┘     └────────┘
```

**例：用户报告"登录后偶尔跳回登录页"**

没有 Spec：直接猜 token 问题 → 改代码 → 手动测 → 不确定有没有新 bug → 没记录

**用 Spec-Driven**：
1. 查 Spec → 发现"Token 过期"场景 ❌ 未实现（根因定位）
2. 补 Delta Spec — WHEN token 过期 THEN 自动刷新或跳转登录
3. 🧑 确认 Proposal（唯一人工门槛）
4. 写测试 → 红灯（证明确实缺这个行为）
5. 改代码 → 绿灯（测试通过 = 修复完成）
6. 更新追溯 + 归档（变更全程可查）

---

# 日常工作流：

**常备 Skill — 开发者说一句话，AI 走完全流程**

| Skill | 说明 | 你说的话 | AI 做什么 | **省了什么** |
|:------|:-----|:---------|:----------|:------------|
| `/new-change` | 新功能/需求 | "加个 CSV 导出" | proposal → spec → TDD | 手写需求和测试计划 |
| `/spec-fix` | 修 Bug | "登录报 500" | 查 spec → 补测试 → 修代码 | 手动定位根因 |
| `/archive-change` | 归档变更 | "做完了" | 合并 spec → archive | 手动整理文档 |
| `/review-tests` | 测试审查 | "测试够吗" | spec ↔ test 交叉比对 | 逐个核对覆盖率 |
| ... | 还有 6 个 | 建项目 · 接续开发 · 进度查看 · 构建/刷新 .ai · 测试规范 等 | | |

> **核心收益**：开发者只做业务决策（确认 Proposal），文档、测试、追溯全自动

**让 AI 按规矩做事，从 Spec 开始。**
