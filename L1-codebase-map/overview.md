# 项目导航首页

> ⚠️ AI 每次对话**必读**。保持精简（< 100 行）。
> 设计原则：只写 AI 从代码推导不出来的东西。

## 项目身份

- **名称**: [填写]
- **做什么**: [一句话，如"多租户 SaaS 电商后台" / "CLI 数据库迁移工具"]
- **技术栈**: [如 TypeScript + Next.js + Prisma + PostgreSQL]

## 架构层次与依赖方向

```
[画出核心分层，重点标注「禁止的依赖方向」]

例：
  UI → API → Service → Domain → Infrastructure
                                    ↑
  禁止：Domain ✗→ Infrastructure（Domain 层零外部依赖）
  禁止：API ✗→ 直接访问数据库（必须经过 Service）
```

## 功能 → 代码 映射表

<!-- 收到任务时，AI 从这张表开始定位涉及哪些代码 -->
<!-- 按业务领域组织，列出每个功能涉及的核心文件路径 -->

| 功能领域 | 核心文件 | 说明 |
|----------|----------|------|
| [如: 用户认证] | `src/auth/strategies/`, `src/auth/middleware.ts`, `src/models/user.ts` | [如: JWT + refresh token，策略模式] |
| [如: 订单处理] | `src/orders/service.ts`, `src/orders/validator.ts`, `src/payments/` | [如: 订单创建会触发支付模块] |
| [如: 通知系统] | `src/notifications/`, `src/templates/`, `src/queue/` | [如: 异步队列推送，模板在 templates/ 下] |
| [填写] | [填写] | [填写] |

## 核心数据流（挑 2-3 个最常见的操作）

<!-- 写出请求从入口到结束经过哪些文件，这是 AI 理解系统运作最快的方式 -->

### 流程 1: [如: 用户登录]
```
[入口] → [中间件/路由] → [控制器/处理器] → [服务层] → [数据层] → [响应]

例：
POST /api/auth/login
  → src/routes/auth.ts (路由)
  → src/auth/controller.ts#login (参数校验)
  → src/auth/service.ts#authenticate (业务逻辑: 查用户 + 验密码)
  → src/auth/token.ts#generatePair (生成 access + refresh token)
  → 响应: { accessToken, refreshToken } + httpOnly cookie
```

### 流程 2: [如: 创建订单]
```
[填写完整的文件路径链]
```

## 领域术语表

<!-- 只列 AI 可能误解的术语，不列显而易见的 -->

| 术语 | 在本项目中的含义 | 容易混淆的点 |
|------|-----------------|-------------|
| [如: Tenant] | [如: 独立的企业客户，不是"租户"的字面意思] | [如: 和 Organization 不同，一个 Org 可以有多个 Tenant] |
| [如: SKU] | [填写] | [填写] |

## 雷区清单

<!-- 不要碰的文件、有隐式副作用的操作、容易踩的坑 -->

- 🚫 `[如: src/generated/]` — 自动生成的代码，不要手动编辑，改了会被覆盖
- 🚫 `[如: migrations/]` — 已执行的迁移文件禁止修改，只能新增
- ⚠️ [如: 修改 User model 后必须运行 `pnpm generate` 重新生成类型]
- ⚠️ [如: `.env.local` 不在 git 中，新增环境变量要同步更新 `.env.example`]
- ⚠️ [填写其他陷阱]

## 构建和运行

```bash
# 环境要求
[填写，如 Node.js >= 20 / Python >= 3.12]

# 安装依赖
[填写命令]

# 启动开发环境
[填写命令]

# 运行测试
[填写命令]

# 常用验证命令
[填写，如 pnpm typecheck / pnpm lint / pnpm test:unit]
```
