# Cline 构建 L1 代码导航文档 — Prompt 模板

> 将以下 prompt 复制到 Cline 对话中使用。
> 使用前替换 `[项目配置文件]`、`[项目目录]` 和 `[入口文件]` 为实际路径。
>
> **核心理念**: 渐进式披露 — overview.md 只做轻量索引，详情拆到 `features/` 子目录按功能独立加载。
>
> **本文件范围**: 生成 L1 代码导航文档（overview.md + module-map.md + key-files.md + features/*.md）
> **L2 编码规则**: 完成 L1 后，使用 `clineprompt-L2.md` 在同一对话或新对话中继续

---

## Prompt

```markdown
# 任务：构建项目代码导航文档（L1）

## 背景
我需要为本项目构建 AI 上下文文档中的 **L1 代码导航层**。

文件结构：
```
.ai/L1-codebase-map/
├── overview.md              ← 轻量索引（< 60 行），每次对话必读
├── module-map.md            ← 模块合约与耦合，跨模块修改时加载
├── key-files.md             ← 通用任务食谱，做常见任务时加载
└── features/                ← 按功能拆分的详细上下文
    ├── _feature-template.md ← 模板
    ├── user-auth.md         ← 功能 1 的完整上下文
    ├── order-management.md  ← 功能 2
    └── ...
```

**设计思路**：
- overview.md 只是一个索引表，告诉 AI "有哪些功能、入口在哪、详情在哪个文件"
- 收到任务时，AI 查索引 → 定位到一个功能 → **只加载那个功能文件**
- 这样无论项目多大，每次加载的上下文量都是可控的

## 核心原则
- ❌ 不要在 overview.md 里塞详情（数据流、涉及文件列表）— 那些放到 feature 文件
- ✅ overview.md 只做索引：功能名 + 一句话 + 指向 feature 文件的路径
- ❌ 不要写 AI 能从 tree/grep 推导出来的信息
- ✅ 要写 AI 从代码推导不出来的信息（数据流路径、变更联动、陷阱）
- ✅ 每个功能文件自包含：读了这一个文件就够做该功能相关的任务

## 你的工作步骤

### Phase 1: 快速收集原始信息（只用命令，不要逐文件阅读）

```bash
# 目录结构
tree -L 3 -I 'node_modules|.git|dist|__pycache__|venv|.venv|build|target'

# 项目配置
cat [项目配置文件]

# 入口文件
cat [入口文件]

# README（如果有）
cat README.md

# Lint / 格式化配置（如果有）
cat .eslintrc* tsconfig.json .prettierrc* pyproject.toml setup.cfg .golangci.yml 2>/dev/null

# 构建/测试命令来源
cat Makefile 2>/dev/null; cat package.json 2>/dev/null | grep -A 30 '"scripts"'

# 找出所有 import/依赖关系
grep -rn "import\|from\|require" --include='*.ts' --include='*.py' --include='*.java' --include='*.go' | head -100

# 找出潜在陷阱
grep -rn "TODO\|FIXME\|HACK\|WARN\|DEPRECATED\|LEGACY" --include='*.ts' --include='*.py' --include='*.java' --include='*.go' | head -50

# 找出模块公开 API（export / __all__ / public）
grep -rn "^export\|module\.exports\|__all__" --include='*.ts' --include='*.py' --include='*.js' | head -80

# 测试文件分布
find . -name "*.test.*" -o -name "*_test.*" -o -name "test_*" | head -30

# 最近的 commit 模式
git log --oneline -20 2>/dev/null

# 分支命名模式
git branch -a 2>/dev/null | head -20
```

### Phase 2: 识别功能边界 + 深入分析

#### 2a: 划分功能
从 Phase 1 的信息中，识别项目的核心业务功能（通常 3-8 个）。
每个「功能」是用户视角的一个业务能力（如"用户认证"、"订单处理"），不是代码模块。

判断标准：
- 产品经理会说的功能名
- 有相对独立的入口（路由/命令/事件）
- 涉及的文件有一定的聚合性

#### 2b: 对每个功能，追踪完整数据流
对每个功能中最核心的 1-2 个操作，从入口开始追踪请求经过的每个文件：

```
POST /api/auth/login
  → src/routes/auth.ts (路由匹配)
  → src/auth/controller.ts#login (参数校验)
  → src/auth/service.ts#authenticate (查用户+验密码)
  → src/auth/token.ts#generatePair (生成 token)
  → 响应
```

#### 2c: 对每个功能，发现变更联动和陷阱
- 改了功能内的文件 A，哪些看似无关的文件 B 也会受影响？
- 有没有隐式联动（改 model 要同步改 types）？
- 有 TODO/FIXME/HACK 的地方是什么坑？

#### 2d: 识别通用模式（跨功能）
- 3-5 个相似实现 → 提取任务食谱
- 雷区（自动生成的文件、legacy 代码）
- 全局的变更影响（改配置文件 → 影响范围）

### Phase 3: 填写 overview.md（轻量索引）

读取 `.ai/L1-codebase-map/overview.md` 模板，填写：
- 项目身份（3 行）
- 架构约束（只写禁止的方向）
- **功能索引表**：每行一个功能，只有功能名 + 一句话 + 指向 feature 文件 + 入口文件
- 术语、雷区、构建命令

**控制在 60 行以内。不要在这里写数据流或详细文件列表。**

### Phase 4: 为每个功能生成独立文件（核心步骤）

对 Phase 2a 识别的每个功能，复制 `.ai/L1-codebase-map/features/_feature-template.md`，填写：
- 涉及的文件表（按调用链顺序）
- 完整数据流（从 Phase 2b）
- 变更影响（从 Phase 2c）
- 已知陷阱
- 常见修改的步骤（针对该功能的食谱）

**每个功能文件自包含 — AI 只读这一个文件就够做该功能的任务。**

> ⚠️ 如果功能多（> 5 个），可以分批：先处理最核心的 3 个，其余开新对话补充。
> 每个功能的分析可以用 Sub-agent 并行处理（见下方使用指南）。

### Phase 5: 填写 module-map.md + key-files.md

- **module-map.md** — 模块公开 API、依赖规则、跨功能的变更联动
- **key-files.md** — 通用任务食谱（不属于单一功能的）、调查起点

### 约束
- overview.md < 60 行，只做索引
- 每个 feature 文件自包含，可独立加载
- 不确定的地方写 `[待确认：xxx]`
- **检验标准**：每一行都问"AI 从代码中能推导出来吗？"如果能，删掉
```

---

## 补充说明

### 质量检验清单

| 检查项 | 通过标准 | 不通过的例子 |
|--------|----------|-------------|
| overview 是否轻量？ | < 60 行，只有索引 + 雷区 + 构建命令 | ❌ overview 里写了完整数据流 |
| feature 文件是否自包含？ | 只读这一个文件就够做该功能的任务 | ❌ 还要去 overview 查数据流 |
| 是否可推导？ | AI 不能从 tree + grep 快速推导出来 | ❌ "auth 模块在 src/auth/ 目录下" |
| 是否面向任务？ | 有具体的文件路径和步骤 | ❌ "改了 model 要更新相关文件" |

### Sub-agent 使用指南

```
主 Agent（Cline）
├── Phase 1：自己执行命令，收集原始信息
├── Phase 2a：自己划分功能边界
├── Phase 2b-2c：追踪数据流 + 发现联动
│     ⚠️ 功能较多时，可以并行分配：
│     ├── 【Sub-agent 1】"分析 [用户认证] 功能：追踪登录/注册的完整数据流，找出涉及的所有文件、变更联动、陷阱"
│     ├── 【Sub-agent 2】"分析 [订单处理] 功能：追踪创建订单/取消订单的完整数据流..."
│     └── 【Sub-agent 3】"分析 [通知系统] 功能：..."
├── Phase 2d：自己识别通用模式
├── Phase 3：自己填写 overview.md（轻量索引）
├── Phase 4：汇总 Sub-agent 结果 → 填写每个 feature 文件
│     ⚠️ 如果没用 Sub-agent，也可以在这步分配：
│     └── 【Sub-agent】"请用 _feature-template.md 模板，填写 [功能名] 的完整上下文文件"
└── Phase 5：自己填写 module-map.md + key-files.md
```

**推荐用法**：Phase 2 时把每个功能的深入分析分配给 Sub-agent 并行执行，主 Agent 负责索引和汇总。
这样每个 Sub-agent 专注一个功能，分析质量更高，主 Agent 不会上下文过载。

### 完成后

L1 文档生成后，继续用 `clineprompt-L2.md` 生成 L2 编码规则。
建议在同一对话中继续（Phase 1-2 的信息可复用），或上下文满了就开新对话。

### 从旧版迁移

1. **保留**：构建命令、领域术语
2. **删除**：overview 里的详细数据流和文件列表
3. **拆分**：原来 overview 里的数据流 → 移到对应的 `features/*.md`
4. **新增**：功能索引表、feature 独立文件
