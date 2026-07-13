# 通用任务食谱与调查起点

> **来源**：从 `overview.md` 的「按需加载导航」跳转到这里。
> **加载时机**：做常见开发任务（加端点、加表、修 bug）或排查问题时。
> **相关文件**：`module-map.md`（跨模块合约与联动）| `features/[功能名]/`（单功能深入）
>
> **功能相关的食谱**在 `features/[name]/` 下的各层文件中，本文件只放跨功能的通用食谱。

## 常见任务食谱

<!-- 列出项目中最高频的 3-5 种开发任务 -->
<!-- 每个食谱写清楚：改哪些文件、什么顺序、参考哪个已有实现 -->

### 食谱 1: [如: 添加新 API 端点]

**参考已有实现**: `[如: src/routes/users.ts` — 最标准的实现]`

```
步骤：
1. 在 `src/routes/` 创建路由文件（复制 users.ts 的模式）
2. 在 `src/controllers/` 创建 controller（必须继承 BaseController）
3. 在 `src/services/` 创建 service（如果有新业务逻辑）
4. 在 `src/routes/index.ts` 注册路由（⚠️ 容易忘）
5. 在 `tests/integration/` 添加集成测试
6. 在 `docs/api.md` 更新 API 文档（⚠️ 容易忘）

验证：pnpm test && pnpm lint
```

### 食谱 2: [如: 添加新数据库表/字段]

**参考已有实现**: `[如: migrations/20240101_add_orders.ts]`

```
步骤：
1. 在 `src/models/` 创建/修改 model
2. 运行 `[迁移命令，如 pnpm migration:generate]`
3. 检查生成的 migration 文件，确认 SQL 正确
4. 运行 `[如 pnpm migration:run]` 应用到开发库
5. 如果改了现有 model，检查所有 import 该 model 的文件

⚠️ 生产环境不允许 DROP COLUMN，只能 ADD + 标记废弃
⚠️ [其他约束]
```

### 食谱 3: [如: 添加新的后台任务/定时任务]

**参考已有实现**: `[填写]`

```
[填写步骤]
```

### 食谱 4: [填写常见任务]

```
[填写步骤]
```

## 通用变更影响

<!-- 影响全局的关键文件 — 改了波及面广 -->
<!-- 功能级的变更影响写在对应 features/[name]/ 中 -->

| 当你改了这个文件 | 影响范围 | 必须做的事 |
|-----------------|----------|-----------|
| [如: `src/models/user.ts`] | 认证、权限、所有用到 User 的序列化 | 重新生成类型 (`pnpm generate`)，检查 JWT payload |
| [如: `src/config/index.ts`] | 全局，所有读取配置的模块 | 同步更新 `.env.example`，通知运维更新部署配置 |
| [如: `package.json` 的 scripts] | CI/CD 流水线 | 检查 `.github/workflows/` 是否引用了改名的 script |
| [如: `src/shared/types/api.ts`] | 所有 API 端点 + 前端 | 前后端类型要同步，运行 `pnpm typecheck` |
| [填写] | [填写] | [填写] |

## 调查起点

<!-- 遇到问题时，从哪个文件开始排查 -->

| 问题类型 | 从这里开始查 | 排查思路 |
|----------|-------------|----------|
| [如: 接口返回 500] | `src/middleware/error-handler.ts` → 看日志格式 → 定位具体 service | 错误被全局捕获，先看 error handler 的日志输出 |
| [如: 权限/鉴权问题] | `src/auth/middleware.ts` → `src/auth/rbac.ts` | 先确认 token 是否有效，再查角色权限表 |
| [如: 数据不一致] | `src/models/` 对应 model → 查最近的 migration → 查写入点 | 先确认 schema 是否正确，再查写入逻辑 |
| [如: 性能问题] | `src/middleware/logger.ts`（看慢请求日志）→ 对应 service → 查 SQL | N+1 查询是常见原因，检查 ORM 的 eager loading |
| [如: 测试失败] | 看失败的 test 文件 → 检查对应的 fixture/mock → 检查最近改动 | fixture 在 `tests/fixtures/` 下，可能需要更新 |
| [填写] | [填写] | [填写] |

---

> 💡 新增高频任务或发现关键的变更联动时，请同步更新此文档
