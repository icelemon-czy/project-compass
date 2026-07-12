# 测试规范

> 适用于整个项目的测试规范。写测试前加载本文件。
> 更新方式：使用 `setup-testing` skill 引导填写或直接编辑。

## 测试框架

| 类型 | 框架 | 运行命令 |
|------|------|---------|
| 单元测试 | [填写，如 Jest / pytest / go test] | [填写，如 `npm test` / `pytest`] |
| 集成测试 | [填写，如 Supertest / pytest + httpx] | [填写] |
| E2E / UI 测试 | [填写，如 Playwright / Cypress] | [填写] |

## 测试文件约定

- **命名**: [填写，如 `*.test.ts` / `test_*.py` / `*_test.go`]
- **位置**: [填写，如 同目录 / `tests/` 目录 / `__tests__/` 目录]
- **测试命名模式**: [填写，如 `should_xxx_when_yyy` / `test_xxx` / `it('does xxx')`]

## 测试结构规范

### 单元测试

- **隔离策略**: [填写，如 mock 外部依赖 / 使用 DI 注入 fake]
- **Mock 工具**: [填写，如 `jest.mock()` / `unittest.mock.patch` / `gomock`]
- **断言风格**: [填写，如 `expect(x).toBe(y)` / `assert x == y` / `require.Equal`]
- **数据构造**: [填写，如 factory / fixture / inline 构造]

### 集成测试

- **数据库策略**: [填写，如 事务回滚 / 每次清库 / 内存数据库 / testcontainers]
- **外部服务**: [填写，如 mock server / VCR 录制 / 真实调用测试环境]
- **环境变量**: [填写，如 `.env.test` / 测试配置文件]

### UI / E2E 测试

- **选择器策略**: [填写，如 data-testid / aria-label / CSS selector]
- **等待机制**: [填写，如 显式等待 / auto-waiting / polling]
- **测试数据**: [填写，如 seed 数据 / API 创建 / fixture]
- **截图/视频**: [填写，如 失败时截图 / 全程录制]

## 覆盖率要求

- **最低覆盖率**: [填写，如 80% / 不强制 / 仅核心模块]
- **覆盖率工具**: [填写，如 `--coverage` / `coverage.py` / `go tool cover`]
- **排除路径**: [填写，如 `generated/` / `migrations/` / `*.d.ts`]

## 反模式

<!-- 写具体的、项目中实际要避免的测试反模式 -->

- ❌ [填写，如 测试中直接操作数据库而不走 service 层]
- ❌ [填写，如 用 `sleep()` 等待异步操作而不用显式等待]
- ❌ [填写，如 测试之间共享可变状态]
