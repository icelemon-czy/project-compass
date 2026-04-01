# Cline 构建 L1 代码导航文档 — Prompt 模板

> 将以下 prompt 复制到 Cline 对话中使用。
> 使用前替换 `[项目配置文件]`、`[项目目录]` 和 `[入口文件]` 为实际路径。
>
> **核心理念**: 渐进式披露 — overview.md 只做轻量索引，详情拆到 `features/` 子目录按功能独立加载。
>
> **本文件范围**: 生成 L1 代码导航文档（overview.md + module-map.md + key-files.md + features/[name]/）
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
    ├── _feature-template/   ← 模板文件夹（复制来创建新功能）
    │   ├── README.md        ← 功能概览：数据流、变更影响、已知陷阱
    │   ├── entry.md         ← 入口层：路由/Handler/CLI/事件监听
    │   ├── logic.md         ← 逻辑层：Service/UseCase/业务规则
    │   └── data.md          ← 数据层：Model/Repository/迁移
    ├── user-auth/           ← 功能 1 的完整上下文
    ├── order-management/    ← 功能 2
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

### Phase 2: 识别功能边界（仅做划分，不深入分析）

#### 2a: 划分功能，输出功能清单
从 Phase 1 的信息中，识别项目的核心业务功能（通常 3-8 个）。
每个「功能」是用户视角的一个业务能力（如"用户认证"、"订单处理"），不是代码模块。

判断标准：
- 产品经理会说的功能名
- 有相对独立的入口（路由/命令/事件）
- 涉及的文件有一定的聚合性

**输出格式（只输出这张表，不要在这里追踪数据流或分析细节）**：

| 功能名 | 疑似入口文件 | 追踪起点（函数/方法名） | 规模 | 一句话说明 |
|--------|-------------|----------------------|------|------------|
| user-auth | src/auth/routes.ts | Login() | medium | 用户登录/注册/token 刷新 |
| order-management | src/orders/handler.go | CreateOrder() | large | 订单创建、取消、查询 |
| config-loader | src/config/loader.go | Load() | small | 读取并合并配置文件 |

**规模说明**：
- `small` — 逻辑集中，README.md 一个文件即可
- `medium` — 有 2-3 个明显的层，需要分层文件
- `large` — 层次复杂或文件众多，需要完整分层 + 详细追踪

> ⚠️ 主 agent 到此为止。每个功能的深入分析、数据流追踪、变更联动发现全部交给 Feature Sub-agent（Phase 4）。

#### 2b: 识别跨功能的通用模式
- 3-5 个相似实现 → 提取任务食谱（用于 key-files.md）
- 雷区（自动生成的文件、legacy 代码）
- 全局的变更影响（改配置文件 → 影响范围）

### Phase 3: 填写 overview.md（轻量索引）

读取 `.ai/L1-codebase-map/overview.md` 模板，填写：
- 项目身份（3 行）
- 架构约束（只写禁止的方向）
- **功能索引表**：每行一个功能，只有功能名 + 一句话 + 指向 feature 文件 + 入口文件
- 术语、雷区、构建命令

**控制在 60 行以内。不要在这里写数据流或详细文件列表。**

### Phase 4: 为每个功能强制派发 Feature Sub-agent（核心步骤）

> ⚠️ **必须在 Phase 3 的 overview.md 写完后再执行。**
> 主 agent 不直接分析任何功能。对 Phase 2a 功能清单里的每个功能，逐一派发一个独立的 Feature Sub-agent，使用以下标准 prompt：

---

````
你是一个代码分析 sub-agent，专门负责分析「[功能名]」这一个功能。
规模：[small / medium / large]（small → README.md 一个文件即可；large → 需要完整分层）

## 项目背景
<!-- 主 agent 在发送此 prompt 时，将 overview.md 的完整内容粘贴到这里。
     overview.md 在 Phase 3 刚写完，是现成的。不要摘要，直接粘贴全文。
     这是 sub-agent 唯一需要的项目背景，不要附带其他文件。 -->

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
| feature 文件名是否反映实际架构？ | 文件名来自项目真实概念 | ❌ 所有功能都是 entry.md / logic.md / data.md |

### Agent 职责划分

```
主 Agent（Cline）
├── Phase 1：执行命令，收集原始信息
├── Phase 2a：划分功能，输出功能清单（功能名 + 入口文件 + 追踪起点 + 规模 + 一句话）
├── Phase 2b：识别跨功能的通用模式
├── Phase 3：填写 overview.md（此时 context 还干净，质量高）
├── Phase 4：为功能清单里的每个功能，逐一派发 Feature Sub-agent← 强制，不可选
│     ├── 【Feature Sub-agent: user-auth】  → 独立 context，自主分析，自主决定层次结构
│     ├── 【Feature Sub-agent: order-mgmt】 → 独立 context，自主分析，自主决定层次结构
│     └── 【Feature Sub-agent: ...】
└── Phase 5：所有 sub-agent 完成后，填写 module-map.md + key-files.md
```

**为什么这样设计**：
- 主 agent 在 Phase 1 已消耗大量 context，强制卸载功能分析任务可防止 context 饱和后质量退化
- 每个 Feature Sub-agent 拥有全新空 context，传入功能名 + 入口文件 + overview.md 最小必要上下文，分析深度更有保障
- Sub-agent 触发是架构上的确定行为，不依赖主 agent 的运行时判断
### 完成后

L1 文档生成后，继续用 `clineprompt-L2.md` 生成 L2 编码规则。
建议在同一对话中继续（Phase 1-2 的信息可复用），或上下文满了就开新对话。

### 从旧版迁移

1. **保留**：构建命令、领域术语
2. **删除**：overview 里的详细数据流和文件列表
3. **拆分**：原来 overview 里的数据流 → 移到对应的 `features/[name]/` 文件夹
4. **新增**：功能索引表、feature 独立文件
