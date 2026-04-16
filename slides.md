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

| 问题 | 现状 | 后果 |
|:------|:------|:------|
| **上下文有限** | 真实项目代码塞不进窗口 | 超出窗口 → AI 产生幻觉，编造不存在的 API 和文件 |
| **目标游离式开发** | AI 的本能是"直接改代码"，跳过需求 | 改了什么没记录，测试事后补，需求与代码脱节 |

<br>

> 我们需要两件事：
> **让 AI 只检索需要的文件** + **让 AI 从 Spec 出发写代码**

---

# `.ai/` Framework — 五层结构，一个目录

在项目中建一个 `.ai/` 目录，系统性解决上面两个问题：

| 层 | 解决什么 | 一句话 |
|:---|:---------|:-------|
| **L1** 代码导航 | AI 不知道看哪 | < 60 行索引，按需深入 |
| **L2** 编码规则 | AI 不知道怎么写 | 规则 + 测试规范 + 模板 |
| **L3** 需求 | 代码没有需求驱动 | Spec → 变更 → 归档 |
| **L4** 会话 | 每次对话从零开始 | 跨对话延续进度 |
| **L5** 验证 | 改了不知道对不对 | Spec ↔ Code ↔ Test 追溯 |

> **闭环**：结构（L1/L2）→ 需求（L3）→ 编写测试（L5）→ 代码 → 测试验证 — 代码是最后一环

---

<!-- _class: philosophy -->

# 哲学一：渐进式加载

AI 每次对话 **只读 < 60 行索引**，根据任务按需深入

| 传统方式 | Project Compass |
|:---------|:----------------|
| 全量塞入上下文，浪费窗口 | 自动加载 3 个基础文件，其余按需 |
| 每次对话从零开始 | L4 会话层延续上次进度 |
| AI 不知道该看哪 | 索引 + 决策树精准定位 |

| 阶段 | 加载内容 |
|:-----|:---------|
| **启动**（自动） | 功能索引 `overview.md` + 编码规则 `global.md` + 上次进度 `active-session.md` |
| **定位**（按需） | 匹配任务类型 → `features/` · `key-files.md` · `module-map.md` |
| **组合**（按需） | 跨功能修改同时加载多个文档，路径可组合 |

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

# 日常工作流：说句话，AI 全自动

**常备 Skill — 自然语言触发，覆盖开发全生命周期**

| Skill | 说明 | 你说的话 | AI 做什么 | **省了什么** |
|:------|:-----|:---------|:----------|:------------|
| `/new-change` | 新功能/需求 | "加个 CSV 导出" | proposal → spec → TDD | 手写需求和测试计划 |
| `/continue-change` | 接续开发 | "继续昨天的" | 读进度 → 接续 TDD | 回忆上次做到哪 |
| `/spec-fix` | 修 Bug | "登录报 500" | 查 spec → 补测试 → 修代码 | 手动定位根因 |
| `/archive-change` | 归档变更 | "做完了" | 合并 spec → archive | 手动整理文档 |
| `/review-tests` | 测试审查 | "测试够吗" | spec ↔ test 交叉比对 | 逐个核对覆盖率 |
| `/check-changes` | 进度查看 | "什么进度" | 汇总变更状态 | 翻文件看进度 |
| `/build-ai` | 首次构建 | "初始化 .ai" | 5 个 Builder 一键构建 | 手写全套文档 |
| `/update-ai` | 刷新文档 | "代码改了" | 增量刷新上下文 | 手动同步文档 |
| `/setup-testing` | 测试规范 | "配置测试" | 扫描代码生成 testing.md | 从零写规范 |

> **核心收益**：开发者只做业务决策（确认 Proposal），文档、测试、追溯全自动

**让 AI 按规矩做事，从 Spec 开始。**
