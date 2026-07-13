# Research: 多 Agent 并行协作方案

> 调研日期：2026-03-31
> 目的：研究多个 AI Agent 如何在同一代码库上并行工作，了解任务分配、隔离、冲突解决和通信机制
> 相关产出：基于本调研整理的正式路线图见 [Compass Roadmap](../README.md)

---

## 1. Anthropic 的方案：16 个 Claude 造 C 编译器

### 1.1 一句话总结

16 个 Agent 各自在独立 Docker 容器中运行，共享一个 Git 仓库，通过**文件锁认领任务**——没有总指挥，每个 Agent 自己决定做什么。

### 1.2 形象解释

想象一家 16 人的装修公司在翻新一栋大楼：

```
                        🏢 大楼（Git 仓库）
                              │
            ┌─────┬─────┬─────┼─────┬─────┬─────┐
            │     │     │     │     │     │     │
          🧑‍🔧   🧑‍🔧   🧑‍🔧   🧑‍🔧   🧑‍🔧   🧑‍🔧   🧑‍🔧  ... ×16
         Agent1 Agent2 Agent3 Agent4 Agent5 Agent6 ...
```

- **每个工人有自己的工具间**（独立 Docker 容器）
- **大楼有一块公告板**（`current_tasks/` 目录）
- **工作流程**就像建筑工地的日常：

```
早上到工地
    ↓
看公告板 → "3楼卫生间瓷砖" 没人认领
    ↓
在公告板上贴个便签："我在做3楼卫生间" ← 这就是锁文件
    ↓
去3楼干活（写代码、编译、测试）
    ↓
干完了 → 把成果推到仓库（git push）
    ↓
撕掉便签 → 回公告板找下一个活
    ↓
如果搬材料时跟别人撞车了（git 冲突）→ 自己解决
```

### 1.3 核心机制

**任务认领 — 文件锁模式**：

```
current_tasks/
├── implement-lexer.lock        ← Agent3 正在做
├── implement-parser.lock       ← Agent7 正在做
├── implement-codegen.lock      ← (空) 等待认领
└── ...

锁文件内容示例：
{
  "claimed_by": "agent-3",
  "claimed_at": "2026-03-31T10:00:00Z",
  "description": "实现 C 词法分析器"
}
```

**关键设计决策和为什么它能工作**：

| 决策 | 好处 |
|------|------|
| 无总指挥 | 没有单点故障，不会因为 boss 挂了全停 |
| 独立 Docker 容器 | 编译互不干扰，不会"我的 build 把你的搞崩" |
| Git 作为唯一通信渠道 | 简单可靠，不需要自定义协议 |
| Agent 自己解决冲突 | 如果等人来解决，16 个 Agent 都在空转 |
| 文件锁而非数据库锁 | 锁的状态就在仓库里，git log 就能追溯 |

### 1.4 Claude Code 的产品化版本

Anthropic 把这套机制产品化为三个概念：

```
┌─────────────────────────────────────────────┐
│            Claude Code Team Mode            │
│                                             │
│  1. Shared Task List（共享任务列表）          │
│     = current_tasks/ 目录的结构化版本        │
│     每个 agent 认领、完成、释放任务          │
│                                             │
│  2. Inter-Agent Messaging（Agent 间通信）    │
│     = agent 之间可以留言                     │
│     "我改了 parser.h 的接口，你的代码要更新"  │
│                                             │
│  3. Lead / Teammates 角色分配               │
│     Lead = 分解任务 + 监控进度               │
│     Teammates = 专注执行分配的任务           │
└─────────────────────────────────────────────┘
```

**Lead 和 Teammate 的分工**：

```
Lead Agent（队长）:
├── 读取需求/issue
├── 拆解为具体子任务
├── 写入 shared task list
├── 监控 teammates 进度
├── 处理跨任务依赖
└── 最终集成验证

Teammate Agent（队员）:
├── 从 task list 认领任务
├── 在自己的 worktree 中工作
├── 完成后 push + 标记完成
├── 遇到阻塞 → 给 lead 留言
└── 去认领下一个任务
```

---

## 2. 其他平台的方案

### 2.1 Cursor — 递归规划者 + 隔离 Worker

Cursor 在构建自驾浏览器项目时，经历了 **4 代架构进化**，最终方案最成熟：

**失败的前 3 代**：

| 代 | 方案 | 为什么失败 |
|----|------|-----------|
| 1 | Agent 共享状态文件 + 文件锁 | Agent 不能可靠地遵守锁语义，死锁频发 |
| 2 | 中央协调者统一分配 | 协调者成为瓶颈，所有 agent 排队等指令 |
| 3 | 一个超大 agent 做所有事 | context 窗口爆炸，迷失在百万行代码中 |

**第 4 代成功方案**：

```
                    Root Planner
                   （全局规划者）
                    │        │
            ┌───────┘        └───────┐
            │                        │
      SubPlanner A             SubPlanner B
     （HTML 解析器）           （CSS 引擎）
       │    │    │              │    │
   Worker Worker Worker     Worker Worker
    各自独立 VM/副本，不互相通信
```

**与 Anthropic 方案的关键区别**：

| | Anthropic | Cursor |
|--|-----------|--------|
| **任务分配** | 去中心化（自己认领） | 中心化（Planner 分配） |
| **层级** | 扁平（16 个平级 agent） | 递归（planner→subplanner→worker） |
| **通信** | Git + 文件锁 | Handoff 消息（结构化回调） |
| **冲突策略** | Agent 自己解决 | 接受有限错误率，自然收敛 |
| **规模** | ~16 并行 | ~1000 并行（峰值） |

**Cursor 的核心洞察 — 接受有限错误率**：

```
传统思维：每个 agent 必须 100% 正确 → 需要全局锁 → 序列化 → 慢
Cursor 思维：允许 0.5-2% 错误率 → 不需要锁 → 并行 → 快 → 错误自动修复

就像高速公路：
  ❌ 100% 安全 = 每辆车排队，一辆一辆通过 → 没人能到达
  ✅ 接受极小事故率 = 全速并行 → 偶尔追尾 → 拖车处理 → 整体更快
```

### 2.2 Devin（Cognition）— 独立 VM 父子模式

```
Parent Devin（协调者）
    │
    ├── send_message("测试登录页面")──→ Child Devin 1（独立 VM）
    ├── send_message("测试支付页面")──→ Child Devin 2（独立 VM）
    └── send_message("测试设置页面")──→ Child Devin 3（独立 VM）
                                          │
                                      各自有独立的:
                                      - 终端
                                      - 浏览器
                                      - 代码副本
                                      - dev 环境
```

**特色**：
- Parent 可以随时给 Child 发消息修正方向
- 可以暂停/恢复/终止 Child
- 每个 Child 有完整的可观测性（日志、截图、操作历史）
- 实战成果：Cognition 自己用 Devin 达到 659 PR/周

**典型场景**：
- 并行 QA（每个页面一个 Devin）
- 大规模迁移（按服务拆分，并行处理）
- 安全审计（每个服务一个 session）

### 2.3 GitHub Copilot Coding Agent — 按 Issue 分支

```
GitHub Issue #42: "修复登录 bug"
         │
         ↓
   Copilot 自动:
   1. 创建分支 copilot/fix-42
   2. 在云端 VM 中工作
   3. 生成 PR
   4. 等待 human review
         │
         ↓ （同时）
GitHub Issue #43: "添加导出功能"
         │
         ↓
   另一个 Copilot:
   1. 创建分支 copilot/fix-43
   2. 独立工作...
```

**隔离策略**：每个 issue 一个分支，天然不冲突。合并时由 PR review 处理冲突。

### 2.4 Git Worktree 模式（本地并行通用方案）

```bash
# 主仓库
my-project/
├── .git/              ← 共享 git 对象
├── src/
└── ...

# 为每个 agent 创建 worktree（秒级创建）
git worktree add ../agent-1-workspace feature-1
git worktree add ../agent-2-workspace feature-2
git worktree add ../agent-3-workspace feature-3

# 每个 worktree:
# - 独立的文件系统（编译不冲突）
# - 共享 .git 对象（节省 50% 磁盘）
# - 独立的分支
# - 秒级创建/删除
```

**这是最轻量的本地多 agent 隔离方案**，Cursor Background Agent 和 Claude Code 都支持。

---

## 3. 核心模式对比

### 3.1 隔离策略

| 方案 | 隔离方式 | 创建成本 | 适合规模 |
|------|---------|---------|---------|
| Docker 容器（Anthropic） | 完全隔离 | 中（秒-分钟） | 10-20 |
| 独立 VM（Cursor Cloud, Devin） | 完全隔离 | 高（分钟） | 100-1000 |
| Git Worktree（本地） | 文件系统隔离 | 低（秒） | 5-10 |
| 分支隔离（Copilot） | Git 分支 | 低 | 5-20 |

### 3.2 任务分配

| 模式 | 代表 | 优点 | 缺点 |
|------|------|------|------|
| **自认领**（去中心化） | Anthropic | 无单点故障，简单 | Agent 可能重复认领或挑简单的 |
| **中央分配**（递归规划） | Cursor | 全局最优，避免冲突 | Planner 成为瓶颈 |
| **父子指令** | Devin | Parent 可实时修正 | Parent 空转等 child |
| **Issue 触发** | Copilot | 与项目管理天然集成 | 每个 issue 独立，缺乏跨任务协调 |

### 3.3 冲突解决

| 策略 | 适用场景 | 代价 |
|------|---------|------|
| **文件锁** | 修改同一文件时互斥 | 可能死锁，Agent 不善于遵守 |
| **自然收敛** | 允许冲突，事后修复 | 额外 token 消耗，~2% 错误率 |
| **分支隔离** | 各自独立分支 | 合并时才暴露冲突 |
| **Agent 自解决** | Git conflict 由 agent 处理 | Agent 可能解决错误 |

### 3.4 通信机制

| 机制 | 代表 | 形式 |
|------|------|------|
| **Git 提交/推送** | Anthropic | 代码就是消息，pull 即同步 |
| **Handoff 回调** | Cursor | 结构化 JSON（状态 + 变更 + 建议） |
| **父子消息** | Devin | Parent 给 Child 发文本指令 |
| **锁文件 / 状态文件** | Anthropic | 文件系统即通信通道 |
| **Scratchpad** | Cursor | 共享的 .cursor/scratchpad.md |

---

## 4. 关键洞察

### 4.1 "没有银弹"

不存在一种方案适合所有场景。选择取决于：

```
任务可拆分度高 + 文件交叉少 → 分支隔离（最简单）
需要实时协调 + 共享状态  → 父子消息（Devin 式）
超大规模（100+ agent）  → 递归规划（Cursor 式）
中等规模 + 简单可靠     → 文件锁认领（Anthropic 式）
```

### 4.2 共同趋势

1. **隔离优于协调** — 给每个 agent 独立副本，比让他们共享更有效
2. **接受不完美** — 0% 错误率的代价太高，不如允许小错误后修复
3. **文件系统即协议** — 锁文件、任务文件、scratchpad 比自定义 API 简单可靠
4. **递归分治** — 大任务拆成小任务，每层只管自己的范围
5. **Human-in-the-loop 仍必须** — 所有方案都保留了人类 review 环节

### 4.3 令人意外的发现

- **Cursor 的文件锁方案失败了**，但 Anthropic 的成功了 — 区别在于：Anthropic 用外部协调者管理锁，不让 agent 自己操作锁
- **659 PR/周**（Cognition 自己用 Devin）— 多 agent 已不是实验，而是日常生产力
- **错误率 0.5-2% 是可接受的** — Cursor 发现追求 0% 反而更慢，因为需要全局等待

---

## 5. 对 Compass 的启示

### 当前状态

Compass 的 L3（任务层）和 L4（会话层）本质上是**单 agent 设计**：
- board.md 的一个任务 → 一个 agent 执行
- active-session.md 追踪一个 agent 的进度

### 如果要支持多 Agent

可以参考的模式：

**方案 A — Anthropic 式（最小改动）**：
```
L3-tasks/
├── board.md                ← 任务看板（加 assignee 列）
├── TASK-001-xxx.md         ← Agent A 认领
├── TASK-002-xxx.md         ← Agent B 认领
└── locks/
    ├── TASK-001.lock       ← Agent A 的锁
    └── TASK-002.lock       ← Agent B 的锁

L4-session/
├── agent-a-session.md      ← Agent A 的进度
└── agent-b-session.md      ← Agent B 的进度
```

**方案 B — Lead/Teammate 式**：
```
L3-tasks/
├── board.md                ← Lead 维护
├── TASK-001-xxx.md         ← Teammate 1 执行
└── TASK-002-xxx.md         ← Teammate 2 执行

L4-session/
├── lead-session.md         ← Lead 的全局视图
├── teammate-1-session.md   ← Teammate 1 进度
└── teammate-2-session.md   ← Teammate 2 进度
```

**方案 C — Git Worktree 隔离（推荐起步方案）**：
- 每个 agent 在自己的 worktree/分支工作
- 各自有独立的 `.ai/L4-session/active-session.md`
- 合并时只合并代码，L4 状态各自维护

> ⚠️ 这些都是**可能的方向**，不是立即要做的。当前 Compass 的单 agent 设计对大多数使用场景已经足够。

### Git Worktree 工作原理

Git Worktree 允许一个仓库同时拥有多个工作目录，每个目录在不同的分支上独立工作：

```
my-project/                          ← 主 worktree
├── .git/                            ← 唯一的 Git 对象数据库
│   ├── objects/                     ← 所有 commit、blob、tree（共享）
│   ├── refs/                        ← 分支引用（共享）
│   └── worktrees/                   ← 每个 linked worktree 的元数据
│       ├── agent-1/
│       │   ├── HEAD                 ← agent-1 的 HEAD（独立）
│       │   ├── index                ← agent-1 的暂存区（独立）
│       │   └── gitdir               ← 指回 linked worktree 的路径
│       └── agent-2/
│           └── ...
├── .ai/                             ← Compass 文档
├── src/
└── ...

../agent-1-workspace/                ← linked worktree 1（独立文件系统）
├── .git                             ← 不是目录，是文件！内容: "gitdir: /path/.git/worktrees/agent-1"
├── .ai/                             ← 独立副本（关键设计点）
├── src/
└── ...

../agent-2-workspace/                ← linked worktree 2
├── .git
├── .ai/
├── src/
└── ...
```

**共享 vs 独立**：

| 内容 | 共享/独立 | 说明 |
|------|----------|------|
| Git 对象（commits, blobs） | 共享 | 不复制，节省 50%+ 磁盘 |
| 分支引用（refs/heads） | 共享 | 所有 worktree 看到相同的分支列表 |
| Git 配置（.git/config） | 共享 | 可通过 `extensions.worktreeConfig` 启用独立配置 |
| HEAD | **独立** | 每个 worktree 可以在不同分支上 |
| Index（暂存区） | **独立** | 各自的 `git add` 互不影响 |
| 工作目录文件 | **独立** | 完全隔离的文件系统，编译/运行不冲突 |

**常用命令**：

```bash
# 创建 worktree（秒级，不复制 .git/objects）
git worktree add ../agent-1 -b task/TASK-001-login-fix

# 列出所有 worktree
git worktree list

# 完成后删除
git worktree remove ../agent-1

# 清理残留元数据
git worktree prune
```

### `.ai/` 四层在多 Worktree 下的行为分析

每个 worktree 会得到 `.ai/` 的**独立文件副本**。四层的性质各不相同：

| 层 | 性质 | 多 worktree 时 | 冲突风险 |
|----|------|---------------|---------|
| **L1 代码导航** | 稳定，跟代码结构绑定 | 跟随各自分支，**自然正确** — 分支改了代码结构，L1 也应对应更新 | 低 |
| **L2 规则** | 稳定，全局统一 | 跟随各自分支，所有分支共享同一套编码规则，**自然正确** | 极低 |
| **L3 任务** | 中频变化 | ⚠️ board.md 是多 agent 都要读写的 — **冲突高发区** | **高** |
| **L4 会话** | 高频变化，每个 agent 独立 | ⚠️ active-session.md 每个 agent 需要自己的，**不能共享** | **高**（如果共享） |

**核心洞察**：L1 和 L2 天然适配 worktree（跟代码绑定，各自分支各自对）。真正需要设计的是 **L3（任务分配）和 L4（会话状态）在多 agent 间如何协调**。

### 方案 C-Enhanced：Worktree + Compass 集成方案

```
主 worktree（人类 + Lead Agent）
├── .ai/
│   ├── L1, L2               ← 跟代码绑定，自然正确
│   ├── L3-tasks/
│   │   └── board.md          ← 唯一的任务看板（只在主 worktree 维护）
│   └── L4-session/
│       └── active-session.md ← Lead 的会话状态

agent-1-workspace/（git worktree add ../agent-1 -b task/TASK-001）
├── .ai/
│   ├── L1, L2               ← 跟随分支
│   ├── L3-tasks/
│   │   └── board.md          ← 只读参考（不在这里改，避免合并冲突）
│   └── L4-session/
│       └── active-session.md ← Agent 1 独立维护自己的会话状态

agent-2-workspace/（git worktree add ../agent-2 -b task/TASK-002）
├── .ai/
│   ├── L1, L2
│   ├── L3-tasks/
│   │   └── board.md          ← 只读参考
│   └── L4-session/
│       └── active-session.md ← Agent 2 独立维护
```

**规则**：
1. **board.md** — 只在主 worktree 更新，各 agent worktree 中的 board.md 是创建分支时的快照（只读参考）
2. **active-session.md** — 每个 worktree 各自维护，合并时**不合并** L4（各自的进度互不相干）
3. **L1/L2** — 如果 agent 的修改涉及架构变更，在自己的分支中更新对应的 L1 文档，合并时自然带入
4. **任务状态传达** — 通过 git commit message 或 PR description，而非直接改 board.md

### 落地步骤（如果要做）

**第一步：board.md 加 assignee + branch 列**

```markdown
| ID | 任务 | 状态 | 分配给 | 分支 |
|----|------|------|--------|------|
| TASK-001 | 修复登录 bug | 🔄 进行中 | agent-1 | task/TASK-001 |
| TASK-002 | 添加导出功能 | 🔄 进行中 | agent-2 | task/TASK-002 |
| TASK-003 | 重构通知模块 | ⏳ 待认领 | — | — |
```

**第二步：entrypoints 加多 agent 指令段**

在入口文件模板（clinerules / claude.md 等）中添加：

```markdown
## 多 Agent 模式（worktree）

如果你在一个 linked worktree 中工作（可通过 `git worktree list` 确认）：
- L4-session/active-session.md → 只维护你自己的进度
- L3-tasks/board.md → 只读参考，不要修改
- 任务状态变更通过 git commit message 传达（如 "[TASK-001] 完成登录修复"）
- 完成后 push 到你的分支，由 Lead 或人类在主 worktree 合并
- 合并时只合并代码和 L1/L2 变更，L4 session 不合并
```

**第三步：合并时的 `.ai/` 处理**

```bash
# 合并 agent-1 的分支时，忽略 L4 session 文件的冲突
git merge task/TASK-001
# 如果 L4 冲突 → 直接用主 worktree 的版本
git checkout --ours .ai/L4-session/active-session.md
```

或在 `.gitattributes` 中配置永远用 ours 策略：
```
.ai/L4-session/active-session.md merge=ours
```

---

## 参考来源

- Anthropic Engineering Blog — "Building a C compiler with a team of parallel Claudes"
- Claude Code 官方文档 — Shared Task List / Inter-Agent Messaging / Lead-Teammates
- Cursor Blog — "How we built a self-driving codebase"（递归规划者架构 4 代进化）
- Cognition (Devin) — Managed Devins API / Playbooks
- GitHub Copilot — Coding Agent / Agent HQ
- Linear — Agent Interaction Design Guidelines
