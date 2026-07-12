# 模块合约与耦合地图

> **来源**：从 `overview.md` 的「按需加载导航」跳转到这里。
> **加载时机**：修改涉及多个模块时。
> **相关文件**：`key-files.md`（通用任务食谱）| `features/[功能名]/`（单功能深入）
>
> 重点：每个模块对外暴露什么、模块间的变更联动关系。

## 模块概览

<!-- 只写 AI 推导不出来的信息：对外暴露什么、稳定性、状态 -->

| 模块 | 路径 | 对外暴露 | 状态 |
|------|------|----------|------|
| [如: Auth] | `src/auth/` | `requireAuth()` 中间件, `generateToken()`, `verifyToken()` | 🟢 stable |
| [如: Orders] | `src/orders/` | `OrderService.create()`, `OrderService.cancel()` | 🟡 active |
| [如: Legacy Billing] | `src/billing-v1/` | `calculateTotal()` — 正在迁移到 billing-v2，勿新增代码 | 🔴 legacy |
| [填写] | [填写] | [填写] | [填写] |

> 状态说明：🟢 stable = 核心基础设施，少改 | 🟡 active = 频繁变更 | 🔴 legacy = 在迁走，别加新代码

## 模块公开 API 清单

<!-- 每个模块对外暴露的关键接口，标注稳定性 -->
<!-- 这帮助 AI 知道哪些函数名不能随意重命名/删除 -->

### [模块名，如: Auth]

```
# 稳定 API（不可随意改名/删除，有外部调用者）
export authenticate(credentials): Promise<Token>     ✅ STABLE
export requireAuth(): Middleware                      ✅ STABLE
export verifyToken(token): Promise<User>              ✅ STABLE

# 内部 API（可以重构）
validateCredentials()                                 🔧 INTERNAL
hashPassword()                                        🔧 INTERNAL
```

### [模块名，如: Orders]

```
[填写，同上格式]
```

## 依赖拓扑

<!-- 全局视角的分层依赖图：从下往上读，底层被上层依赖 -->

```
┌─── 功能层（Features）───────────────────────────────┐
│  [用户认证]  [订单处理]  [通知系统]  [报表导出]      │
└──────┬──────────┬─────────────┬──────────────────────┘
       │          │             │
┌──────▼──────────▼─────────────▼──────────────────────┐
│  [框架基类]  [配置系统]  [日志系统]  [测试基础设施]   │
└─── 基础设施层（Infrastructure）──────────────────────┘
```

> 💡 请根据项目实际情况替换上面的 ASCII 图。用箭头标出功能 → 基础设施的依赖方向。

## 依赖规则

<!-- 用「允许/禁止」表代替 ASCII 依赖图 — 更具体、可验证 -->

| 来源 → 目标 | 允许？ | 方式 | 违反后果 |
|-------------|--------|------|----------|
| [如: API → Service] | ✅ | 直接调用 | — |
| [如: Service → Domain] | ✅ | 接口调用 | — |
| [如: Domain → Infrastructure] | ❌ | — | 破坏核心层独立性，导致测试必须 mock 数据库 |
| [如: Controller → 直接访问 DB] | ❌ | — | 绕过业务规则校验，数据可能不一致 |
| [填写] | [填写] | [填写] | [填写] |

## 变更联动表

<!-- ⚡ 核心价值：当 AI 修改某处代码时，提醒它必须同步修改的其他位置 -->
<!-- 只列非显而易见的联动（如改了 interface 要改实现类，这种太明显不用写） -->

| 当你改了… | 必须同步改… | 原因 |
|-----------|-------------|------|
| [如: `src/models/user.ts` 的字段] | `src/auth/types.ts` 的 `JWTPayload` + `src/generated/` 重新生成 | User 字段变更不会自动同步到 JWT payload 类型 |
| [如: `src/config/pricing.ts` 的价格规则] | `src/billing/webhook.ts` 的 handler + `tests/billing/` 的 fixture | Webhook 有独立的价格校验逻辑不走 pricing 模块 |
| [如: `.env.example` 新增变量] | `docker-compose.yml` 的 environment 段 + CI 配置 | 否则 CI 和 Docker 环境会缺变量导致启动失败 |
| [填写] | [填写] | [填写] |

## 共享代码与跨模块约定

<!-- 跨模块共享的代码位置 + 使用规则 -->

| 共享代码 | 路径 | 使用规则 |
|----------|------|----------|
| [如: 通用类型定义] | `src/shared/types/` | 修改类型后运行 `pnpm typecheck` 确认所有消费者兼容 |
| [如: 工具函数] | `src/utils/` | 只放纯函数，不允许有副作用或 import 业务模块 |
| [如: 数据库迁移] | `migrations/` | 只能新增，不能修改已执行的迁移 |
| [填写] | [填写] | [填写] |
