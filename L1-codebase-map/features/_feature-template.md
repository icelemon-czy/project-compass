# [功能名称]

> 本文件包含「[功能名称]」的完整上下文。
> **加载时机**：当任务涉及此功能时，从 overview.md 的功能索引跳转到这里。

## 涉及的文件

<!-- 列出实现此功能的所有关键文件，按调用链顺序 -->

| 文件 | 角色 | 说明 |
|------|------|------|
| [如: `src/routes/auth.ts`] | 路由入口 | [如: 定义 /api/auth/* 路由] |
| [如: `src/auth/controller.ts`] | 控制器 | [如: 参数校验 + 调用 service] |
| [如: `src/auth/service.ts`] | 业务逻辑 | [如: 核心认证逻辑] |
| [如: `src/auth/token.ts`] | 工具 | [如: JWT 生成/验证] |
| [如: `src/models/user.ts`] | 数据模型 | [如: User schema 定义] |

## 数据流

<!-- 写出核心操作的完整链路，从入口到响应 -->

### [操作 1，如: 用户登录]
```
POST /api/auth/login
  → src/routes/auth.ts (路由匹配)
  → src/auth/controller.ts#login (参数校验: email + password)
  → src/auth/service.ts#authenticate (查用户 + bcrypt 验密码)
  → src/auth/token.ts#generatePair (生成 access + refresh token)
  → 响应: { accessToken, refreshToken } + httpOnly cookie
```

### [操作 2，如: Token 刷新]
```
[填写完整链路]
```

## 变更影响

<!-- 改这个功能时，哪些"看似无关"的地方也要动 -->

| 当你改了… | 必须同步改… | 原因 |
|-----------|-------------|------|
| [如: User model 的字段] | `src/auth/types.ts` 的 JWTPayload | Token 里的字段不会自动同步 |
| [如: 认证逻辑] | `tests/auth/` 的测试 + mock 数据 | [如: mock 的 user 对象要和新逻辑匹配] |
| [填写] | [填写] | [填写] |

## 已知陷阱

<!-- 只写从代码中不容易看出来的坑 -->

- ⚠️ [如: `token.ts#generatePair` 的 secret 来自环境变量，本地开发用 `.env.local`，不要硬编码]
- ⚠️ [如: refresh token 存在 Redis 中，改了过期时间要同步改 Redis TTL 配置]
- ⚠️ [填写]

## 常见修改的步骤

<!-- 针对这个功能最常见的修改任务，给出具体步骤 -->

### [如: 给登录添加新的验证方式]

**参考实现**: [如: `src/auth/strategies/local.ts` — 本地密码登录]

```
1. 在 src/auth/strategies/ 创建新策略文件（复制 local.ts 的结构）
2. 在 src/auth/service.ts 的 authenticate() 中注册新策略
3. 在 src/routes/auth.ts 添加新路由
4. 在 tests/auth/ 添加测试
5. 验证：pnpm test -- --grep "auth"
```

### [如: 修改 token 中携带的用户信息]

```
[填写步骤]
```

---

> 💡 此文件随功能演进更新。加了新的子功能或发现新陷阱时请同步维护。
