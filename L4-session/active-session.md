# 当前会话状态

> ⚡ 每次对话必读 + 对话结束时更新
> 这是 AI 的"短期工作记忆"，让它知道"上一步做到哪了、下一步该做什么"

## 最后更新

- **时间**: [YYYY-MM-DD HH:mm]
- **对话主题**: [简述上次对话在做什么]

## 当前工作焦点

**正在做**: [具体到函数级别，如: 将 `UserService.authenticate()` 从 `auth.ts` 迁移到 `auth/service.ts`]

**当前步骤**: [如: current-plan.md 步骤 3 — 迁移认证逻辑，已完成 3/8 处调用方更新]

**涉及文件**:
- `[文件路径]` — [具体状态，如: API 签名已改，旧方法标记 @deprecated]
- `[文件路径]` — [如: 已修改，但调用者还没更新]
- `[文件路径]` — [如: 待修改]

## 已完成（本轮）

- [x] [具体描述，如: 将 `authenticate()` 移到新文件，签名不变]
- [x] [如: 更新了 `routes/auth.ts` 的 import 路径]

## 下一步具体动作

<!-- 具体到可以直接执行的操作，不写"继续重构" -->

1. [ ] [如: 打开 `src/controllers/user.ts`，将第 45 行的 `auth.validate()` 改为 `authService.validate()`]
2. [ ] [如: 运行 `pnpm test -- auth` 确认迁移没有 break]
3. [ ] [如: 更新 `module-map.md` 的 Auth 模块公开 API 清单]

## 测试状态

<!-- 当前代码的测试情况 -->

- ✅ [如: `pnpm test -- auth` — 12/12 通过]
- ❌ [如: `pnpm test -- user` — 3 个失败（因为 import 路径还没更新）]
- ⏳ [如: `pnpm test -- integration` — 还没跑]

## 阻塞 / 待确认

- [如: `src/legacy/auth-v1.ts` 有一处调用方式看不懂，需要确认是否还在用]

## 上下文备注

> AI 在下次对话中需要知道的重要信息

- [如: 发现 `auth/token.ts` 有硬编码的 secret fallback，需要单独处理]
- [如: `config.ts` 第 23 行有一个未文档化的 `LEGACY_MODE` 开关，暂时不要动]

---

## 会话历史摘要

| 日期 | 主题 | 成果 |
|------|------|------|
| YYYY-MM-DD | [填写] | [填写] |
| YYYY-MM-DD | [填写] | [填写] |
