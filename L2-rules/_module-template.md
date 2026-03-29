# 模块规则模板

> **使用方法**: 复制本文件，重命名为模块名（如 `api.md`、`auth.md`、`orders.md`），
> 然后根据实际模块情况填写内容。
>
> 仅在处理该模块相关任务时加载。
> 原则：写 AI 从代码读不出来的合约、陷阱和操作指南。

## 模块身份

- **模块名**: [填写]
- **路径**: [填写，如 `src/auth/`]
- **状态**: [🟢 stable / 🟡 active / 🔴 legacy]

## 对外合约

<!-- 这个模块对外暴露了什么？调用者应该怎么用？ -->
<!-- 不要写"负责认证"这种废话，写具体的函数签名和使用规则 -->

### 公开 API

```
[列出该模块对外暴露的关键接口，标注稳定性]

例：
export authenticate(credentials: LoginDTO): Promise<TokenPair>    ✅ STABLE
export requireAuth(): ExpressMiddleware                           ✅ STABLE
export requireRole(role: Role): ExpressMiddleware                 ✅ STABLE

内部函数（可重构，外部不应调用）：
  validatePassword()     🔧 INTERNAL
  rotateRefreshToken()   🔧 INTERNAL
```

### 使用规则

- [如: 调用 `requireAuth()` 后，`req.user` 上会有 `{ id, role, tenantId }`]
- [如: token 过期返回 401，权限不足返回 403，不要用 400]
- [如: refreshToken 在 httpOnly cookie 中，不在 response body]
- [填写]

## 模块特定技术

- [如: 使用 `passport.js` 实现策略模式认证]
- [如: 使用 `bcrypt` 哈希密码，saltRounds=12]
- [填写]

## 文件组织

```
[描述该模块内文件的组织方式]

例：
auth/
├── middleware.ts      ← requireAuth / requireRole 中间件
├── controller.ts      ← HTTP 端点 handler
├── service.ts         ← 核心认证业务逻辑
├── token.ts           ← JWT 生成/验证
├── strategies/        ← passport 策略（email, oauth...）
├── types.ts           ← 导出类型（JWTPayload, LoginDTO...）
└── __tests__/         ← 测试
```

## 关键模式

<!-- 这个模块内必须遵循的设计模式和约定 -->

- [如: 所有新的认证方式必须实现 `AuthStrategy` 接口，放在 `strategies/` 下]
- [如: 数据库操作必须使用事务]
- [如: 响应格式统一为 `{ data, error, meta }`]
- [填写]

## 已知陷阱与技术债

<!-- ⚡ 高价值：AI 容易踩的坑，从代码里不容易看出来的隐患 -->

- ⚠️ [如: `token.ts` 中 JWT_SECRET 在测试环境用的是 `TEST_JWT_SECRET`，不是 `JWT_SECRET`]
- ⚠️ [如: `refreshToken` 的过期时间在 `config.ts` 而不是 `token.ts` 中配置]
- ⚠️ [如: 修改 User model 后必须同步更新 `types.ts` 的 `JWTPayload` 类型，否则 token 解析会缺字段]
- 🔧 [如: `service.ts` 中有一段 legacy 代码处理 v1 token 格式，计划在 Q2 删除]
- [填写]

## 模块边界

<!-- 该模块与其他模块的交互规则 + 违反后果 -->

| 交互方向 | 允许？ | 方式 | 违反后果 |
|----------|--------|------|----------|
| 本模块 → [如: User model] | ✅ | 直接 import | — |
| 本模块 → [如: Payment] | ❌ | — | [如: 会导致循环依赖，auth 启动时 payment 还没初始化] |
| [如: 任何模块] → 本模块 | ✅ | 只通过公开 API | [如: 直接 import 内部函数会在重构时 break] |

## 测试策略

<!-- 这个模块的测试怎么写、mock 什么、fixture 在哪 -->

- **测试类型**: [如: middleware 需要集成测试，service 需要单元测试]
- **Mock 规则**: [如: mock 数据库层(`src/auth/__mocks__/repository.ts`)，不 mock service 层]
- **Fixture 位置**: [如: `tests/fixtures/auth/` 下有标准用户和 token 数据]
- **运行命令**: [如: `pnpm test -- auth`]
- [填写]
