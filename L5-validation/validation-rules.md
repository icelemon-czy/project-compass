# L5 验证规则参考

> 本文件定义 AI 执行 spec 验证时的规则和流程。
> 部署位置：`.ai/L5-validation/validation-rules.md`
>
> entrypoint 中的变更归档流程引用本文件。

## 验证类型

### 1. 结构验证（Spec 格式）

检查 L3 spec 是否符合格式规范：

- [ ] 每个 `### Requirement:` 至少有 1 个 `#### Scenario:`
- [ ] Scenario 使用 `- **WHEN** / - **THEN** / - **AND**` 格式
- [ ] Scenario 标题用 `####`（4 个 #），不是 `###`
- [ ] SHALL/MUST = 强制，SHOULD = 建议，MAY = 可选 — 使用正确
- [ ] 不包含实现细节（"用 Redis 缓存"是实现，"SHALL cache results"是需求）
- [ ] system.md 有 System Boundary 和 Cross-Cutting Requirements

### 2. 正向追溯（Spec → Code → Test）

对每条 SHALL/MUST Requirement 的每个 Scenario：

1. **定位实现** — 根据 L1 feature 文档找到对应的代码文件和函数/方法
2. **检查实现完整性** — WHEN 条件是否被处理，THEN 结果是否被产出
3. **定位测试** — 查找测试文件中是否有覆盖该 Scenario 的用例
4. **标注状态** — verified / untested / partial / unimplemented

> SHOULD 级别的 Requirement 也追溯，但允许 unimplemented 状态。
> MAY 级别的 Requirement 记录但不标记为问题。

### 3. 反向追溯（Code → Spec）

检查重要代码路径是否有 spec 覆盖：

1. **识别核心业务逻辑** — 从 L1 feature 文档中找到标记为核心的代码路径
2. **匹配 spec** — 是否有对应的 Requirement 描述了该行为
3. **标记缺口** — 有代码但无 spec → 标记为 `no-spec`，建议补写

> 不需要追溯所有代码。聚焦：public API、业务规则、数据变换、边界校验。
> 忽略：纯工具函数、胶水代码、框架生成代码。

### 4. 一致性检查

跨域 spec 之间的一致性：

- 同一概念是否在不同域中有矛盾的描述
- Cross-Cutting Requirements（system.md）是否被各域遵守
- 域间依赖是否在 spec 中有体现

### 5. 测试用例设计（Test Spec）

对 traceability 表中状态为 ⚠️ untested / ⚠️ partial / ❌ unimplemented 的 Scenario，展开具体测试用例。

**输入**：L3 Scenario 的 WHEN/THEN + 实现代码（如存在）

**输出**：`test-specs/<domain>.md`，包含：

| 用例类型 | 说明 | 必须程度 |
|---------|------|---------|
| happy path | 正常输入→预期输出 | 每个 Scenario 至少 1 个 |
| edge case | 边界值、特殊字符、空值、极端数据量 | SHALL/MUST 级别 |
| error path | 无效输入、权限不足、依赖不可用 | SHALL/MUST 级别 |
| boundary | 上下限、分页边界、超时阈值 | 按需 |

**规则**：
- 用例必须有**具体数据**，不能只写"valid input"
- Setup/Teardown 写清前置条件和清理操作
- 项目已有测试 → 只为缺口写，不重复已覆盖的
- 项目无测试 → 全量写
- 不涉及具体测试框架语法——用例设计是框架无关的

**两种场景的处理**：

| 场景 | test-specs 覆盖范围 | 后续动作 |
|------|-------------------|---------|
| 项目无测试 | 全量：每个 Scenario 展开所有用例类型 | AI 按 test-specs 生成测试代码到 codebase |
| 项目有测试 | 仅缺口：traceability 表中 ⚠️/❌ 的 Scenario | AI 按 test-specs 补写缺失测试 |

## 验证流程

### 单域验证（变更归档时）

```
1. 读取受影响域的 spec: specs/<domain>/spec.md
2. 读取对应的 L1 feature 文档
3. 逐条 Requirement 执行正向追溯
4. 对核心代码路径执行反向追溯
5. 更新 traceability/<domain>.md
6. 对 ⚠️/❌ 的 Scenario 生成/更新 test-specs/<domain>.md
7. 生成问题清单
```

### 全量验证（定期 / 手动触发）

```
1. 列出所有 specs/ 下的能力域
2. 对 system.md 执行结构验证
3. 对每个能力域执行单域验证
4. 执行跨域一致性检查
5. 汇总所有 test-specs/ 的完整性
6. 生成 reports/<date>-full.md
```

## 验证报告格式

```markdown
# 验证报告 — <date> (<scope>)

## 概要
- 能力域: N | Requirement: N | Scenario: N
- ✅ verified: N (%) | ⚠️ gap: N (%) | ❌ missing: N (%)

## 按域明细

### <domain>
| Requirement | Scenario | 状态 | 问题 |
|-------------|----------|------|------|

## 问题清单（按优先级）
1. **高** — [描述]
2. **中** — [描述]
3. **低** — [描述]

## 建议
- [ ] [建议的操作]
```
