# 全局规则

> 适用于整个项目的通用规则。每次对话必加载。
> 原则：写具体可执行的规则，不写抽象声明。每条规则 AI 都应能直接照做。

## 技术栈

- **语言 + 版本**: [填写，如 TypeScript 5.4 / Python 3.12 / Java 21]
- **框架**: [填写，如 Next.js 14 + Prisma / Django 5.0 / Spring Boot 3.2]
- **数据库**: [填写，如 PostgreSQL 16 / MySQL 8 / MongoDB 7]
- **包管理器**: [填写，如 pnpm / uv / maven]

## 编码规范

### 命名约定

| 元素 | 约定 | 正确示例 | 错误示例 |
|------|------|----------|----------|
| 文件名 | [如 kebab-case] | [如 `user-service.ts`] | [如 ~~`UserService.ts`~~] |
| 类 | [如 PascalCase] | [如 `OrderService`] | [如 ~~`orderService`~~] |
| 函数 | [如 camelCase] | [如 `getUserById()`] | [如 ~~`get_user_by_id()`~~] |
| 变量 | [如 camelCase] | [如 `isActive`] | [如 ~~`is_active`~~] |
| 常量 | [如 UPPER_SNAKE] | [如 `MAX_RETRY_COUNT`] | [如 ~~`maxRetryCount`~~] |

### 语言特定规则

<!-- 写具体的、可执行的规则，不写"保持代码整洁"之类的废话 -->

- [如: `strict: true` 在 tsconfig.json 中，禁止使用 `any`（用 `unknown` + 类型收窄）]
- [如: 所有异步函数必须用 `async/await`，禁止 `.then()` 链]
- [如: 优先用 `const` 声明，只在需要重新赋值时用 `let`，禁止 `var`]
- [填写]

### 导入规则

- 导入顺序：[如: 1) Node 内置 → 2) 第三方 → 3) `@/` 别名 → 4) 相对路径，每组之间空一行]
- 路径别名：[如: `@/` → `src/`]
- ❌ 禁止：[如: 禁止跨层级的相对路径 `../../..`，超过两级必须用 `@/`]

## 架构规则

### 依赖方向（具体的禁止规则）

<!-- 不要写"采用 Clean Architecture"，要写具体哪层不能 import 哪层 -->

- ✅ [如: Controller → Service → Repository → Database — 允许]
- ❌ [如: Service 禁止直接 import Repository 的实现类，必须通过接口]
- ❌ [如: Domain 层（`src/domain/`）禁止 import 任何外部库，零依赖]
- ❌ [如: 前端组件禁止直接调 fetch，必须走 `src/api/` 层]
- 验证方式：[如: ESLint `import/no-restricted-paths` 规则 / 手动 review]

### 错误处理模式

<!-- 写具体的模式，不写"使用统一错误处理" -->

```
[用代码示例展示错误处理的标准模式]

例（TypeScript）：
- Service 层：throw 自定义错误类 (AppError / NotFoundError / ValidationError)
- Controller 层：不 try-catch，让全局 error handler 统一处理
- 全局 handler 在 src/middleware/error-handler.ts，将 AppError → HTTP 响应
- 日志：只在全局 handler 记录，Service 层不要 console.log

例（Go）：
- 函数返回 (result, error)，调用方必须检查 error
- 用 fmt.Errorf("context: %w", err) 包装错误，保留链路
- 不使用 panic（除了初始化阶段的不可恢复错误）
```

### 数据验证规则

- 验证位置：[如: 在 Controller 层用 zod schema 验证，Service 层假设输入已验证]
- 验证库：[如: zod / joi / class-validator]
- ❌ 禁止：[如: 禁止在 Service 层重复验证已在 Controller 验证过的数据]

## 反模式清单

<!-- ❌ 明确列出不要做的事 — 比正面规则更好记 -->

- ❌ [如: 不要用 `default export`（除了 Next.js page 组件），统一用 named export]
- ❌ [如: 不要把业务逻辑写在 Controller/Route handler 里，必须放 Service 层]
- ❌ [如: 不要在循环里做数据库查询（N+1 问题），用 batch/join]
- ❌ [如: 不要硬编码配置值，全部走 `src/config/` 读取]
- ❌ [如: 不要 `catch(e) {}` 吞掉错误，至少要 log]
- ❌ [填写]

## 版本控制规范

<!-- commit 格式、分支命名等 -->

- Commit 格式：[如: Conventional Commits — `feat(auth): add refresh token`]
- 分支命名：[如: `feat/xxx` / `fix/xxx` / `refactor/xxx`]

## 测试规范

- 框架：[如: Jest / pytest / go test]
- 文件位置：[如: 同目录 `*.test.ts` / 单独 `tests/` 目录]
- 命名：[如: `should_xxx_when_yyy` / `test_xxx`]
- 运行命令：[如: `pnpm test` / `pytest -v`]

> 💡 新建文件的代码模板在 `templates.md` 中（创建新文件时加载）。

## 版本控制

- **分支命名**: [如: `feat/xxx`, `fix/xxx`, `refactor/xxx`]
- **Commit 格式**: [如: `feat(scope): description` — Conventional Commits]
- **PR 要求**: [如: 必须有描述 + 影响范围 + 测试说明]

## 构建与验证命令

```bash
# 安装依赖
[填写]

# 开发模式
[填写]

# 构建
[填写]

# 测试
[填写]

# Lint + 类型检查
[填写]
```

## 测试规范

- **框架**: [如: Vitest / pytest / JUnit]
- **文件位置**: [如: 同目录 `*.test.ts` / `tests/` 目录]
- **命名**: [如: `should_动作_when_条件`]
- **覆盖要求**: [如: Service 层必须有单元测试，Controller 层要有集成测试]
- **Mock 规则**: [如: 只 mock 外部依赖（数据库、第三方 API），不 mock 内部模块]
