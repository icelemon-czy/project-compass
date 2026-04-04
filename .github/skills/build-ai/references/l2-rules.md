# L2 Coding Rules — Phase 6

Extract coding patterns from the actual codebase. **Only write rules observed in real code, never invent.**

## 核心原则

- ✅ 从代码中的**实际模式**提取，不要编造项目没在用的规范
- ✅ 每条规则给出 ✅ 正确写法和 ❌ 错误写法的具体代码示例
- ✅ 不确定的地方标 `[待人工确认]`
- ❌ 不要写 "使用 Repository 模式"（除非代码里真的在用）

## Phase 6a: 提取全局规则（→ global.md）

### 技术栈与构建命令

从 `package.json` / `pyproject.toml` / `go.mod` / `pom.xml` 提取语言版本、框架、依赖。
从 `scripts` / `Makefile` / CI 配置提取构建、测试、lint 命令。

### 命名约定

```bash
# 文件名模式
ls src/**/*.ts src/**/*.py 2>/dev/null | head -20

# 类名 / 函数名模式
grep -rn "^class \|^export class \|^def \|^func \|^function " --include='*.ts' --include='*.py' --include='*.go' | head -30
```

判断：文件名 kebab-case 还是 camelCase？类名 PascalCase？函数名风格？

### 依赖方向规则

从 import 分析提取允许/禁止的依赖方向。从 ESLint 的 `import/no-restricted-paths` 验证。

### 错误处理模式

```bash
grep -rn "extends Error\|class.*Error\|class.*Exception" --include='*.ts' --include='*.py' --include='*.java' | head -20
grep -rn "errorHandler\|error_handler\|@ExceptionHandler\|recover()" --include='*.ts' --include='*.py' --include='*.java' --include='*.go' | head -10
grep -rn "catch\|except\|rescue" --include='*.ts' --include='*.py' --include='*.rb' | head -20
```

### 反模式清单

```bash
# ESLint 禁用规则
grep -A 2 '"error"\|"warn"' .eslintrc* 2>/dev/null | head -30

# 项目中的 disable 注释
grep -rn "eslint-disable\|noqa\|noinspection\|@SuppressWarnings" --include='*.ts' --include='*.py' --include='*.java' | head -20
```

### 版本控制规范

```bash
git log --oneline -20 2>/dev/null
git branch -a 2>/dev/null | head -20
```

### 测试规范

从测试文件提取：框架、文件位置、命名模式、mock 方式。

### 输出 global.md

创建 `.ai/L2-rules/global.md`：

```markdown
# 全局规则

> 适用于整个项目。每次对话必加载。

## 技术栈

- **语言 + 版本**: [从代码提取]
- **框架**: [从代码提取]
- **数据库**: [从代码提取]
- **包管理器**: [从代码提取]

## 编码规范

### 命名约定

| 元素 | 约定 | 正确示例 | 错误示例 |
|------|------|----------|----------|

### 语言特定规则

- [从代码中观察到的规则]

### 导入规则

- 导入顺序：[观察到的模式]
- 路径别名：[如有]
- ❌ 禁止：[从 lint 配置提取]

## 架构规则

### 依赖方向

- ✅ [允许的方向]
- ❌ [禁止的方向]
- 验证方式：[如何验证]

### 错误处理模式

[从代码中提取的实际模式，附代码示例]

### 数据验证规则

- 验证位置：[观察到的模式]
- 验证库：[实际使用的库]

## 反模式清单

- ❌ [从 lint 配置和代码注释中提取]

## 版本控制规范

- Commit 格式：[从 git log 推断]
- 分支命名：[从 branch 名推断]

## 测试规范

- 框架：[实际使用的]
- 文件位置：[观察到的模式]
- 命名：[观察到的模式]
- 运行命令：[从 package.json / Makefile 提取]
```

## Phase 6b: 新建文件模板（→ templates.md）

找到 3+ 个同类型文件，提取公共结构：

```bash
head -30 src/services/*.ts src/**/service.ts 2>/dev/null
head -30 src/**/*.test.ts tests/*.py 2>/dev/null
```

创建 `.ai/L2-rules/templates.md`：

```markdown
# 新建文件模板

> 创建新文件时的标准结构。**加载时机**：创建新文件时。

## [类型] 模板

[从实际代码提取的模板，带注释]

## 测试模板

[从实际测试文件提取的模板]
```

## Phase 6c: 模块规则（→ L2-rules/[module].md）

对 L1 module-map.md 中的每个主要模块：

1. 复制 `_module-template.md`，重命名为模块名
2. 提取模块的公开 API 清单（区分 STABLE / INTERNAL）
3. 提取模块边界（import 关系分析）
4. 提取测试策略
5. 提取已知陷阱

```bash
# 公开 API
grep -rn "^export" src/[模块名]/ --include='*.ts' | head -30

# 谁 import 了这个模块？
grep -rn "from.*[模块名]\|import.*[模块名]" --include='*.ts' --include='*.py' | grep -v "[模块名]/" | head -20

# 模块内的 TODO / 陷阱
grep -rn "TODO\|FIXME\|HACK" src/[模块名]/ | head -20

# 模块活跃度
git log --oneline --since="3 months ago" -- src/[模块名]/ | wc -l
```

> 💡 项目较大（模块 > 5 个）时可分批处理。

## 质量检验

- [ ] 每条规则都从实际代码中观察到
- [ ] 有 ✅ 正确写法和 ❌ 错误写法的代码示例
- [ ] 不确定的地方标了 `[待人工确认]`
- [ ] templates.md 模板来自实际文件，不是编造
