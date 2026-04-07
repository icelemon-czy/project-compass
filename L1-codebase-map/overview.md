# 项目导航首页

> ⚠️ AI 每次对话**必读**。保持极精简（< 60 行）。
> 这是**索引**，不是详情。详情在 `features/` 子目录下按功能拆分，每个功能一个文件夹。

## 项目身份

- **名称**: [填写]
- **做什么**: [一句话，如"多租户 SaaS 电商后台"]
- **技术栈**: [如 TypeScript + Next.js + Prisma + PostgreSQL]

## 架构约束

```
[只写禁止的依赖方向，不画完整架构图]

例：
  禁止：Domain ✗→ Infrastructure（Domain 层零外部依赖）
  禁止：Controller ✗→ 直接访问数据库（必须经过 Service）
```

## 功能索引

<!-- 收到任务时，AI 从这张表定位该加载哪个功能文件 -->

| 功能 | 一句话描述 | 详情 | 入口文件 |
|------|-----------|------|----------|
| [如: 用户认证] | JWT 登录/注册/token 刷新 | → `features/user-auth/` | `src/auth/controller.ts` |
| [如: 订单处理] | 创建/取消/支付，触发通知 | → `features/order-management/` | `src/orders/service.ts` |
| [如: 通知系统] | 异步队列推送邮件/短信 | → `features/notification/` | `src/notifications/dispatcher.ts` |
| [填写] | [填写] | → `features/[name]/` | [填写] |
| — 基础设施 | 框架基类、配置系统、插件机制、构建流程、测试基础设施等 | → `infrastructure/` | — |

## 按需加载导航

<!-- 读完上面的功能索引后，根据任务类型走对应路径 -->

```
收到任务
 ├─ 匹配到具体功能 → features/[功能名]/README.md → 按需深入层文件
 ├─ 做常见开发任务（加端点/加表/修 bug） → key-files.md（任务食谱 + 调查起点）
 ├─ 修改涉及多个模块 → module-map.md（模块合约 + 依赖规则 + 变更联动）
 └─ 改底层基础设施 → infrastructure/README.md
```

> 💡 多条路径可叠加：如"跨模块加新端点"先查 key-files.md 拿食谱，再查 module-map.md 确认联动。

## 领域术语

<!-- 只列 AI 可能误解的术语 -->

| 术语 | 在本项目中的含义 | 容易混淆的点 |
|------|-----------------|-------------|
| [如: Tenant] | [独立的企业客户] | [和 Organization 不同，一个 Org 可有多个 Tenant] |

## 雷区

- 🚫 `[如: src/generated/]` — 自动生成，不要手动编辑
- 🚫 `[如: migrations/]` — 已执行的迁移禁止修改，只能新增
- ⚠️ [如: 改 User model 后必须 `pnpm generate` 重新生成类型]
- ⚠️ [如: 新增环境变量要同步 `.env.example`]

## 构建和运行

```bash
[填写：环境要求 / 安装 / 启动 / 测试 / lint 命令]
```
