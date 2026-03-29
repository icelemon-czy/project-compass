# Cline 构建 L1 代码导航文档 — Prompt 模板

> 将以下 prompt 复制到 Cline 对话中使用。
> 使用前替换 `[项目配置文件]`、`[项目目录]` 和 `[入口文件]` 为实际路径。
>
> **核心理念**: 不要让 AI 做 `tree` 搬运工。让它提取**关系、模式和陷阱** — 这些才是人/AI 从代码中不容易快速看出来的东西。
>
> **本文件范围**: 生成 L1 代码导航文档（overview.md + module-map.md + key-files.md）
> **L2 编码规则**: 完成 L1 后，使用 `clineprompt-L2.md` 在同一对话或新对话中继续

---

## Prompt

```markdown
# 任务：构建项目代码导航文档（L1）

## 背景
我需要为本项目构建 AI 上下文文档中的 **L1 代码导航层**。模板在：
- `.ai/L1-codebase-map/overview.md` — 项目导航首页
- `.ai/L1-codebase-map/module-map.md` — 模块合约与耦合地图
- `.ai/L1-codebase-map/key-files.md` — 任务食谱与变更影响索引

这些文档的目标不是"描述代码库长什么样"，而是"帮 AI 快速定位该看哪些代码"。

## 核心原则
- ❌ 不要写 AI 能从 tree/grep 推导出来的信息（目录结构、技术栈、模块职责）
- ✅ 要写 AI 从代码推导不出来的信息（功能→文件映射、数据流路径、变更联动、陷阱）
- ❌ 不要写 "auth 模块负责认证" 这种废话
- ✅ 要写 "用户登录从 routes/auth.ts → controller → service → token.ts，改 User model 要同步改 JWTPayload"

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

### Phase 2: 深入分析 — 发现关系

#### 2a: 追踪 2-3 个核心数据流
挑选项目中最常见的 2-3 个操作（如 "用户登录"、"创建订单"、"发送通知"）。
对每个操作，从入口文件开始，追踪请求经过的每个文件路径，形成完整链条：

```
POST /api/auth/login
  → src/routes/auth.ts (路由匹配)
  → src/auth/controller.ts#login (参数校验)
  → src/auth/service.ts#authenticate (查用户+验密码)
  → src/auth/token.ts#generatePair (生成 token)
  → 响应
```

#### 2b: 识别重复的开发模式（任务食谱）
在项目中找到 3-5 个相似的已有实现（如 3 个不同的 API 端点、3 个不同的 model）。
对比它们，提取出"添加新功能的标准步骤"：
- 要创建/修改哪些文件？
- 什么顺序？
- 哪个已有实现最适合作为参考模板？

#### 2c: 发现变更联动
分析 import 关系，找出非显而易见的耦合：
- 改了文件 A，哪些看似无关的文件 B 也会受影响？
- 有没有"改了 model 要手动同步改 types"这种隐式联动？
- 有没有自动生成的代码，改了源文件要重新生成？

#### 2d: 标记雷区
- 哪些文件/目录是自动生成的，不应手动编辑？
- 哪些文件有 TODO/FIXME/HACK 注释，说明有已知问题？
- 有没有 legacy 代码在迁移中？

### Phase 3: 填写 L1 模板

按顺序读取模板 → 用 Phase 1-2 的分析结果填写 → 写入对应位置：

1. **overview.md** → 保存到 [项目目录]/.ai/L1-codebase-map/overview.md
   - 重点：功能→代码映射表、核心数据流、雷区清单
   - 控制在 100 行以内

2. **module-map.md** → 同上
   - 重点：模块公开 API、变更联动表、依赖禁止规则
   
3. **key-files.md** → 同上
   - 重点：常见任务食谱、变更影响索引、调查起点

### 约束
- 每个文档控制在合理长度（overview < 100 行）
- 不确定的地方写 `[待确认：xxx]`，不要编造
- 如果某处关系复杂看不清，标注 `[需要深入分析：xxx]`
- **检验标准**：每一行都问"AI 从代码中能推导出来吗？"如果能，删掉
```

---

## 补充说明

### 质量检验清单

填完后用以下标准审查每一行内容：

| 检查项 | 通过标准 | 不通过的例子 |
|--------|----------|-------------|
| 是否可推导？ | AI 不能从 tree + grep 快速推导出来 | ❌ "auth 模块在 src/auth/ 目录下" |
| 是否面向任务？ | 收到 task 时能直接用来定位文件 | ❌ "项目代码约 5 万行" |
| 是否具体？ | 包含具体的文件路径和函数名 | ❌ "改了 model 要更新相关文件" |
| 是否可验证？ | AI 能照做并检查结果 | ❌ "遵循 Clean Architecture" |

### Sub-agent 使用指南

主 Agent（Cline）做 80% 的分析工作，Sub-agent 只在需要深入时使用：

```
主 Agent（Cline）
├── Phase 1：自己执行命令，收集原始信息
├── Phase 2a：自己追踪 2-3 个核心数据流
│     ⚠️ 如果某个数据流跨越 5+ 文件且逻辑复杂：
│     └── 【Sub-agent】"请从 [入口文件] 开始，追踪 [这个操作] 经过的每个文件，列出完整路径链"
├── Phase 2b：自己识别重复模式，提取任务食谱
├── Phase 2c：自己分析 import 关系，发现变更联动
├── Phase 2d：自己标记雷区
└── Phase 3：填写 L1 三个模板文件
```

**何时用 Sub-agent**:
- 数据流跨越 5+ 文件，主 Agent 追踪容易丢失链条
- 模块间关系错综复杂，需要单独梳理一个方向的依赖

**不要用 Sub-agent**:
- 执行 Phase 1 的命令（主 Agent 直接跑）
- 填写模板（主 Agent 自己填比交给 Sub-agent 质量更高）

### 完成后

L1 文档生成后，可以继续使用 `clineprompt-L2.md` 中的 prompt 生成 L2 编码规则。
建议在**同一对话中继续**（Phase 1-2 的分析结果可以复用），或者如果上下文已满，**开新对话**。

### 从旧版模板迁移（L1 部分）

如果项目已有旧版文档（描述性内容），可以这样迁移：

1. **保留**：构建/运行命令、领域术语表
2. **删除**：目录结构描述、模块职责描述、代码规模统计
3. **新增**：功能→代码映射表、数据流追踪、雷区清单、变更联动表
