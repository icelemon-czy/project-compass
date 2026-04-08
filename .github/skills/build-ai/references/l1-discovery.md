# L1 Discovery — Phase 1-3

Scan the project, identify features, and write the overview index.

## Core Principles

- ❌ 不要在 overview.md 里塞详情（数据流、涉及文件列表）— 放到 feature 文件
- ✅ overview.md 只做索引：功能名 + 一句话 + 指向 feature 文件的路径
- ❌ 不要写 AI 能从 tree/grep 推导出来的信息
- ✅ 要写 AI 从代码推导不出来的信息（数据流路径、变更联动、陷阱）
- ✅ 每个功能文件自包含：读了这一个文件就够做该功能相关的任务

## Phase 1: 快速收集原始信息

> 只用命令收集，不要逐文件阅读。自动检测项目类型。

```bash
# 目录结构（3 层深度，排除常见生成目录）
find . -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/__pycache__/*' -not -path '*/venv/*' -not -path '*/.venv/*' -not -path '*/build/*' -not -path '*/target/*' | head -120 | sort

# 项目配置（自动检测）
cat package.json pyproject.toml go.mod pom.xml build.gradle Cargo.toml 2>/dev/null

# README
cat README.md 2>/dev/null

# 入口文件（自动检测常见入口）
# Node: src/index.ts, src/main.ts, src/app.ts, server.ts
# Python: main.py, app.py, manage.py, src/__main__.py
# Go: cmd/*/main.go, main.go
# Java: src/main/java/**/Application.java
# 找到后 cat 对应文件

# Lint / 格式化配置
cat .eslintrc* tsconfig.json .prettierrc* pyproject.toml setup.cfg .golangci.yml 2>/dev/null

# 构建/测试命令
cat Makefile 2>/dev/null; cat package.json 2>/dev/null | grep -A 30 '"scripts"'

# Import / 依赖关系
grep -rn "import\|from\|require" --include='*.ts' --include='*.py' --include='*.java' --include='*.go' | head -100

# 潜在陷阱
grep -rn "TODO\|FIXME\|HACK\|WARN\|DEPRECATED\|LEGACY" --include='*.ts' --include='*.py' --include='*.java' --include='*.go' | head -50

# 模块公开 API
grep -rn "^export\|module\.exports\|__all__" --include='*.ts' --include='*.py' --include='*.js' | head -80

# 测试文件分布
find . -name "*.test.*" -o -name "*_test.*" -o -name "test_*" | head -30

# 最近 commit 模式
git log --oneline -20 2>/dev/null

# 分支命名模式
git branch -a 2>/dev/null | head -20
```

> 💡 如果用户提供了补充上下文文件（架构说明、团队规范等），先读取它作为额外背景。

## Phase 2: 识别功能边界

> **构建顺序**：先识别基础设施（地基），再识别功能（建在基础设施之上），最后识别跨功能模式。

### 2a: 识别基础设施层

> **Infrastructure** = 被 ≥2 个 feature 共享的底层机制（如框架基类、配置系统、CI/CD、测试框架、通用工具等）。
> 只服务于单个 feature 的 helper → 归入该 feature 的层文件，不放 infrastructure。

输出：

| 基础设施组件 | 代表文件/目录 | 一句话说明 |
|---------------|----------------|------------|

> 项目简单无明显基础设施层 → 标记"无"并跳过。

### 2b: 划分功能清单

从 Phase 1 信息中识别核心业务功能（通常 3-8 个）。

> **Feature** = 产品经理叫得出名字的业务能力（如"用户认证"、"订单处理"）。不是代码模块。

**输出功能清单表**：

| 功能名 | 疑似入口文件 | 追踪起点（函数/方法名） | 规模 | 一句话说明 |
|--------|-------------|----------------------|------|------------|
| user-auth | src/auth/routes.ts | Login() | medium | 用户登录/注册/token 刷新 |

规模说明：
- `small` — 逻辑集中，README.md 一个文件即可
- `medium` — 有 2-3 个明显的层，需要分层文件
- `large` — 层次复杂或文件众多，需要完整分层

> ☸️ 每个功能的深入分析交给 Phase 4 的 subagents 处理，这里只做划分。

### 2c: 识别跨功能通用模式
- 3-5 个相似实现 → 提取任务食谱线索（用于 key-files.md）
- 雷区（自动生成的文件、legacy 代码）
- 全局的变更影响（改配置文件 → 影响范围）

## Phase 3: 写 overview.md

在 `.ai/L1-codebase-map/overview.md` 创建以下内容，**控制在 60 行以内**：

```markdown
# 项目导航首页

> ⚠️ AI 每次对话**必读**。保持极精简（< 60 行）。

## 项目身份

- **名称**: [填写]
- **做什么**: [一句话]
- **技术栈**: [如 TypeScript + Next.js + Prisma + PostgreSQL]

## 架构约束

[只写禁止的依赖方向]

## 功能索引

| 功能 | 一句话描述 | 详情 | 入口文件 |
|------|-----------|------|----------|
| [功能名] | [描述] | → `features/[name]/` | [入口] |
| — 基础设施 | [描述] | → `infrastructure/` | — |

## 按需加载导航

收到任务
 ├─ 匹配到具体功能 → features/[功能名]/README.md
 ├─ 做常见开发任务 → key-files.md
 ├─ 修改涉及多个模块 → module-map.md
 └─ 改底层基础设施 → infrastructure/README.md

## 领域术语

| 术语 | 在本项目中的含义 | 容易混淆的点 |
|------|-----------------|-------------|

## 雷区

- 🚫 [自动生成的文件/目录]
- ⚠️ [重要的后置动作]
```

## Phase 4（交接）: 写 _handoff.md

将以下信息写入 `.ai/L1-codebase-map/_handoff.md`，供 Phase 4-5（深入分析）使用：

```markdown
# L1 构建交接摘要

## 基础设施层

[Phase 2a 的组件表，或「无」]

## 功能清单

[Phase 2b 的功能清单表]

## 跨功能通用模式

[Phase 2c 的内容]

## 补充上下文

[如有补充上下文文件内容，否则「无」]

## overview.md 全文

[刚写好的 overview.md 完整内容]
```

Phase 1-3 完成后，继续执行 Phase 4-5（L1 深入分析）。
如果上下文已接近限制，提示用户开新对话并指向 `_handoff.md`。
