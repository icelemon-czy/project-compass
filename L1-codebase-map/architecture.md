# 运行时架构

> **来源**：从 `overview.md` 的「按需加载导航」跳转到这里。
> **加载时机**：需要理解系统整体运行方式、请求生命周期、或排查跨层问题时。
> **相关文件**：`overview.md`（功能索引）| `module-map.md`（代码级依赖）| `infrastructure/`（基础设施详情）
>
> **与其他文件的区别**：
> - `module-map.md` = **代码级**依赖（谁 import 了谁、允许/禁止的依赖方向）
> - `architecture.md`（本文件）= **运行时**结构（东西实际怎么跑起来、请求怎么流转、进程怎么通信）

## 部署拓扑

<!-- 系统在运行时由哪些进程/服务/容器组成，它们之间如何通信 -->
<!-- 用 ASCII 图展示，只画运行时实体，不画代码模块 -->

```
[如:
  ┌──────────────┐     HTTP      ┌──────────────┐
  │   Nginx      │ ────────────→ │  API Server   │
  │  (反向代理)   │               │  (Node.js)    │
  └──────────────┘               └──────┬───────┘
                                        │ TCP
                                 ┌──────▼───────┐
                                 │  PostgreSQL   │
                                 └──────────────┘

  独立进程：
  ┌──────────────┐   Redis Pub/Sub   ┌──────────────┐
  │  API Server   │ ───────────────→ │  Worker       │
  │               │                  │ (后台任务)     │
  └──────────────┘                  └──────────────┘
]
```

> 💡 如果是单体应用只有一个进程，画出内部的关键运行时组件（HTTP server、定时器、连接池等）。

## 请求生命周期

<!-- 一个典型请求从进入系统到返回响应，经过的完整路径 -->
<!-- 这是全局视角，展示 infrastructure 层和 feature 层如何在运行时协作 -->
<!-- 单个 feature 的数据流在 features/[name]/README.md 中 -->

### 典型 HTTP 请求

```
[如:
  客户端请求
    → Nginx (SSL termination, 静态资源)
    → Express middleware 管道:
        1. cors()
        2. bodyParser()
        3. requestLogger()        ← infrastructure: 日志系统
        4. rateLimiter()          ← infrastructure: 限流
        5. authenticate()         ← feature: 用户认证
    → Router 匹配路由
    → Controller.[method]()       ← feature: 具体功能
        → Service.[method]()      ← feature: 业务逻辑
            → Repository.[method]() ← feature: 数据访问
            → 外部服务调用（如有）
        ← 返回结果
    → Response serializer         ← infrastructure: 序列化
    → errorHandler()（如果抛异常）← infrastructure: 错误处理
    → HTTP 响应
]
```

### [其他请求类型，如: WebSocket / gRPC / 消息消费 / 定时任务]

```
[填写完整路径，格式同上]
```

## Feature ↔ Infrastructure 运行时协作

<!-- 哪个 feature 在运行时实际调用了哪个 infrastructure 组件 -->
<!-- 标注调用方式：同步调用 / 异步事件 / 中间件注入 / DI 注入 -->
<!-- 这帮助 AI 理解改一个 infra 组件会影响哪些 feature 的运行时行为 -->

| Feature | 使用的 Infrastructure | 调用方式 | 说明 |
|---------|----------------------|----------|------|
| [如: 用户认证] | [如: 配置系统, 日志系统] | [如: DI 注入] | [如: 读取 JWT secret 和 token 过期时间] |
| [如: 订单处理] | [如: 消息队列, 日志系统, 缓存] | [如: 异步事件] | [如: 订单创建后发送事件到通知队列] |
| [如: 通知系统] | [如: 消息队列, 模板引擎] | [如: 消息消费] | [如: 从队列消费事件，渲染模板后发送] |
| [填写] | [填写] | [填写] | [填写] |

## 启动与初始化顺序

<!-- 系统启动时各组件的初始化顺序，哪些必须先于哪些 -->
<!-- 这对排查启动失败、理解 DI 装配过程至关重要 -->

```
[如:
  1. 加载环境变量 (.env)
  2. 初始化配置系统 (ConfigLoader.load())
  3. 建立数据库连接池 (DatabasePool.init())     ← 失败则退出
  4. 初始化缓存连接 (RedisClient.connect())     ← 失败则降级
  5. 注册 DI 容器 (Container.register())
  6. 加载所有 Controller → 自动注册路由
  7. 启动 HTTP Server (listen on :3000)
  8. 启动后台 Worker（如有独立进程则跳过）
  9. 输出 "Server ready" 日志
]
```

> ⚠️ 标注哪些步骤失败会导致进程退出，哪些可以降级运行。

## 中间件 / 拦截器管道

<!-- 如果项目有中间件链或拦截器管道，列出完整顺序 -->
<!-- 顺序很重要：调换顺序会导致不同行为 -->

```
[如:
  请求方向 →
  1. cors           — 跨域处理（所有请求）
  2. helmet         — 安全头（所有请求）
  3. bodyParser     — 解析请求体（所有请求）
  4. requestId      — 生成请求 ID（所有请求）
  5. logger         — 记录请求日志（所有请求）
  6. rateLimiter    — 限流（所有请求）
  7. authenticate   — 鉴权（需要认证的路由）
  8. authorize      — 权限检查（需要授权的路由）
  9. [路由处理]
  ← 响应方向
  10. serializer    — 统一响应格式
  11. errorHandler  — 全局错误捕获（兜底）
]
```

## 错误传播路径

<!-- 错误从抛出到最终处理的路径，帮助排查问题 -->

```
[如:
  业务层抛出 AppError
    → Controller 不 catch（向上冒泡）
    → Express errorHandler 中间件捕获
        → 已知错误（AppError）→ 返回对应 HTTP 状态码 + 错误消息
        → 未知错误 → 返回 500 + 通用消息 + 写 error 日志
        → 验证错误（ValidationError）→ 返回 400 + 字段级错误详情

  后台任务抛出错误
    → Worker catch → 写日志 + 重试（最多 3 次）→ 移入死信队列
]
```

## 关键运行时配置

<!-- 影响运行时行为的核心配置项，不写在代码里但决定系统行为 -->

| 配置项 | 来源 | 影响 | 默认值 |
|--------|------|------|--------|
| [如: DB_POOL_SIZE] | [如: 环境变量] | [如: 数据库并发连接数] | [如: 10] |
| [如: JWT_EXPIRY] | [如: 环境变量] | [如: Token 过期时间] | [如: 1h] |
| [如: WORKER_CONCURRENCY] | [如: 配置文件] | [如: 后台任务并行数] | [如: 5] |
| [填写] | [填写] | [填写] | [填写] |
