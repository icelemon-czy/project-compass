<!-- compass:start -->
## Language Style

维护任何 agent-facing document 时，动词使用中文，核心名词使用 English。

## Documentation Style

维护任何 document 时逐层递进：先给 big picture（目标和主线 flow），再展开细节。

- overview 层（开头段落、table、diagram）凸显目的和数据流，不堆 optional 参数、路径或 field-level 细节；细节放到对应展开层或 referenced document。
- 分层放置：entry document 放主体和导航，detail document 放展开。
- 同一 fact 只维护一处，其余位置用引用指向，避免多处 copy 漂移。

## Developing Principles

### Design

- First Principles Thinking：从最基础的事实、约束和目标出发重新推导 design。
- Occam's Razor：如无必要，勿增 abstraction、entity、schema、dependency 或 layer。

### Implementation

- 先确认 source of truth，再开始 implementation；当 source of truth 与 implementation 冲突时，先标记 conflict 并向 user 说明。
- 不要修改 source of truth 或 design artifact，除非 user 明确要求，或本次改动已经改变了对应行为。
- 保持现有 code structure、design style 和 layer boundary；优先沿用已有 module、helper、pattern，不为了局部便利新增 layer。
- 抽离 code 中的 config：将可变环境、路径、selector、timeout、feature flag、prompt 参数等放到已有 config boundary。

### Testing

生成或修订 test 时：

- 先读取相关 source of truth 和测试命令（优先 README / design，其次项目配置）。
- 测试 behavior 和 user-visible contract，避免 overfit implementation detail。
- 避免把 test 绑定到 brittle selector、临时 copy、内部 helper 调用顺序、mock 的无关字段或当前代码的 bug。
- 使用最小必要 fixture 和 assertion；每个 assertion 都应对应真实 requirement、risk 或 regression。
- 当 source of truth 与 implementation 冲突时，只在 test 中固化已确认 behavior。

## Review Rule

进行 review 时，先从 high-level requirement 和 source of truth 判断 implementation / test 是否 overfit 当前 case，并检查是否缺少 anti-overfit test。

每个问题按以下结构返回：

- 问题：指出具体 defect、risk、regression、overfit implementation、overfit test 或 missing anti-overfit test，并引用 file/line。
- 白话解释：说明问题上下文、为什么会影响 user 或维护者。
- 当前状态：说明代码现在怎么做、test 现在覆盖了什么、缺口在哪里。
- 解决方案：给出最小可行修复；必要时补充从 high-level requirement 出发的 anti-overfit test，避免只绑定当前 fixture、mock、copy、selector 或 implementation detail。

<!-- compass:end -->
