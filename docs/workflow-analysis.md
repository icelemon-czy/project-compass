# Compass Workflow Analysis

> 当前设计结论：减少用户要理解的入口和 handoff，同时保留 SDD、TDD、review 与追溯的不变量。

## 一、设计判断

### First Principles

Skill 应对应用户能够独立表达的目标，而不是内部流水线步骤。

- “实现这个需求”“修复这个 bug”“解释这段架构”是用户目标。
- “继续 change”“同步 context”“review 后归档”通常只是上一个目标的内部状态或后置条件。
- 用户注意力是稀缺资源；Agent token 和内部迭代不是用户要管理的资源。

### Occam's Razor

- 不为同一状态机创建多个入口。
- 不用多个 Subagent role 表达同一种只读 SDD 审查能力。
- 不复制 review、doc-sync 或 archive 规则。
- 不因 Spec 存在就强迫所有代码修改走 SDD；只有可观察契约变化才创建 L3 change。

## 二、当前 Skill 全景

安装包包含 9 个 Skill，其中 7 个核心用户入口；`ralph-loop` 和 `skill-creator` 是显式可选 meta capability。

| Skill | 用户目标 | 说明 |
|:------|:---------|:-----|
| `/init-project` | 从零创建项目 | 吸收 Git 初始化和初始测试规范 |
| `/build-context` | 为已有项目构建、重建或修复 context | 独立保留；也负责定向更新 L2 testing rules |
| `/brainstorm` | 澄清 idea、比较方案并收敛 design | 可选前置；内部复用 ask-codebase，确认实施后进入 develop |
| `/develop` | 开发功能、调整行为或重构代码 | 内部完成 SDD/TDD/review/doc-sync/archive，并可恢复已有 change |
| `/fix-bug` | 定位并修复行为异常 | 自动分诊 code/test/spec，并复用 review/closeout |
| `/audit-tests` | 专项审计测试是否可信 | 只在用户明确要求检查覆盖、断言、mock、skip 或 false pass 时使用 |
| `/ask-codebase` | 定位、解释、影响分析或查询 change 状态 | 只读；吸收原 check-changes |
| `/ralph-loop` | 显式持续迭代到客观终点 | 可选外层执行模式，不是默认 workflow |
| `/skill-creator` | 创建、更新或精简 project-local Skill | 可选 authoring workflow，不归入普通 develop |

Commit/push 是 Agent 的通用能力，不属于 Compass 生命周期。只有用户明确要求时执行。

## 三、合并记录

| 原 Skill | 当前归属 | 原因 |
|:---------|:---------|:-----|
| `/git-init` | `/init-project` | 新项目初始化阶段；单独 git init 不需要 Compass 专用流程 |
| `/setup-testing` | `/init-project` + `/build-context` | testing.md 是 L2 构建/修复的一部分 |
| `/new-change` | `/develop` create path | 同一 change 生命周期 |
| `/continue-change` | `/develop` resume path | resume 是状态，不是新目标 |
| `/archive-change` | `/develop` closeout | 通过 review 后的自动后置条件 |
| `/check-changes` | `/ask-codebase` change-status path | 本质是只读状态问答 |
| `/update-ai` | 所有 code-changing workflow 的 doc-sync postcondition | 服务变更，不是用户目标；不能并入 build-context |
| `/git-commit` | Agent 通用能力 | 不应污染 change lifecycle，也不能默认产生外部副作用 |

`/audit-tests` 没有并入 `/develop` 或 `/ask-codebase`：它不是普通 code review 或代码问答，而是对测试可信度的专项审计，有独立的证据协议和 verdict。默认只向用户返回结果，不写 L5 report；只有用户明确要求保存时才落盘。

普通 code review 是 Agent 的通用能力，不新增 Compass Skill。用户可以直接要求 review diff、PR 或文件；`/develop` 也会在交付前内部完成必要 review。

`/brainstorm` 保持独立，因为“先帮我想清楚”是可单独表达的用户目标。它不是 `/develop` 的 mandatory gate：明确需求直接实施；尚未定型的 idea 才先读取 `/ask-codebase` 证据、讨论 material choice，并在用户要求实施时由 Agent 自动接入 `/develop`。

`/skill-creator` 保持为可选 meta capability：Skill authoring 有独立的 trigger、resource、validation 和 forward-test contract，不应伪装成普通 product change；概念尚未明确时可以先经过 `/brainstorm`，随后自动接续创建。

## 四、正常用户体验

```text
用户：未定型 idea ─→ `brainstorm` ─→ 读取 `ask-codebase` 证据 ─→ design direction
                                                               ↓ 用户要求实施
用户：明确目标 ───────────────────────────────────────────────→ `develop`
                                                               ↓
                                                SDD path 或 lightweight path
  ↓
需要 SDD：proposal + delta Spec + 必要业务决策
  ↓
Scenario → 红灯测试 → 最小实现 → 绿灯
  ↓
Main Agent 运行测试；sdd-reviewer 只读 verify
  ├─ CLI worker enabled：implementation 由 hook 交给 `claude` CLI
  ├─ 技术问题：Main Agent 修复并重新验证
  └─ 产品歧义：只在此时询问用户
  ↓
doc-sync L1/L2 → L5 verified → delta 合并 → archive
  ↓
一次性交付
```

用户不再被要求依次运行 review、archive、update 或 commit Skill。

## 五、Change 的轻重分流

### SDD path

命中任一项时使用：

- 可观察业务行为变化
- API、schema、权限或兼容性变化
- 数据迁移或跨模块契约变化
- 需要新增/修改/删除 Requirement

保留 proposal、delta Spec、Scenario、TDD、review 和 archive。

### Lightweight path

适用于内部重构、机械迁移、文档或不改变外部契约的配置调整：

- 不创建 proposal 或 delta Spec。
- 仍读取相关规则、运行真实检查并执行 doc-sync。
- 一旦发现契约变化，升级到 SDD path。

这解决了“加上 Spec 后所有事情都变 heavy”的根因：不是删除 Spec，而是只在 Spec 能表达真实产品契约时使用它。

## 六、Subagent 设计

### 角色

默认只有一个内部只读角色：`sdd-reviewer`。

- `mode=plan`：检查影响面、行为歧义、delta Spec 和验证面。
- `mode=verify`：按 Scenario 检查 THEN/assertion、真实生产调用、mock、skip、边界和 false pass。

原 `impact-analyst`、`spec-validator`、`test-reviewer` 合并到这个角色。`codebase-explorer` 只为大型只读调查保留为可选角色。

### Ownership

- Main Agent：状态机 owner、最终 verifier；未启用 CLI worker 时也是 implementation writer。
- Subagent：只读证据提供者，不写 Spec、代码、报告、状态或 archive。
- CLI worker：仅当安装判定 `enabled` 时，由 hook 调用 Claude Code CLI 写 implementation；失败是 blocker，不能悄悄改回本地实现。
- 角色不可用或冲突：Main Agent 静默按同一 validation protocol inline fallback，不把安装工作交给用户。

每个已选平台默认生成 `sdd-reviewer`。用户无需知道它是否被调用，也无需选择下一步。

## 七、CLI worker

Implementation 的执行替换不是新 Skill，也不是新 Subagent。Canonical source 在 `compass/hooks/cli-worker/`，和 Skill / agent 一样按平台迁移。

- 安装时判定本机 `claude` 是否可调用，结论写入 `.compass/context/cli-worker.md`。不为这个再问用户。
- `enabled` 时，Codex / Cursor / OpenCode 安装 native hook；planner 正要执行的那次 tool call 由 hook 直接 pass 给 `claude` CLI 做同一件动作。
- `disabled` 不装 hook，planner 自己写代码。
- Claude Code 不装这只 hook，避免 `claude` 套 `claude`。
- Skill 只定义用户目标；`AGENTS.md` 不承担触发。X 是平台 pending tool call。verify / doc-sync / archive 仍在 planner Main Agent。

## 八、质量不变量

入口合并不等于检查缩水：

1. 只有行为契约变化才创建 Spec，但创建后每个 Requirement 必须有可观察 Scenario。
2. Scenario 必须先映射为能观察到预期失败的测试，再写实现。
3. 写代码前读取真实 L2 规则，完成后逐条检查。
4. 绿灯不是通过证明；必须检查具体 assertion 和真实生产调用链。
5. weak assertion、mock 被测主体、skip/only、吞异常、空 snapshot 和 false pass 都是阻塞项。
6. 技术 review finding 自动修复并重新验证；产品语义冲突才打扰用户。
7. L1/L2 按实际 diff 自动同步；L3 由 change 合并；L5 只记录实际核实的证据。
8. 只有 review `PASS` 才能自动 archive。
9. Commit/push 只在用户明确要求时发生。

## 九、人工门槛

固定的流程确认被移除。只保留两类真实门槛：

| 门槛 | 何时出现 |
|:-----|:---------|
| 产品决策 | 不同答案会改变范围、行为、兼容性、迁移或主要成本 |
| 权限/外部副作用 | 需要新增权限、访问外部系统、部署、发布或 push |

技术选型、内部 review、context sync 和 archive 不因“流程到了这一步”而要求用户确认。
