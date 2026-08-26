# Project Documentation

Compass 把目标项目自己的 README 和 `doc/` 作为 project knowledge。README 讲项目为何存在并提供导航；`doc/` 讲各 feature 的 design；源码、配置和测试用来验证实现事实，不另建一套 Compass context。

## Structure

```text
README.md
doc/
├── <feature>_design.md
└── todo.md                 # optional
```

| Artifact | Responsibility |
|:---------|:---------------|
| `README.md` | 项目目的、Document map、必要的项目入口；不展开 feature design |
| `doc/<feature>_design.md` | 一个有独立目的和行为边界的 feature design |
| `doc/todo.md` | 可选的当前工作清单；不保存永久 design 或已完成历史 |

Feature boundary 按用户目的、observable behavior 和 ownership 判断，不按源码目录机械拆分。两个部分能独立解释、独立变化或各自拥有 source of truth 时拆成两份；同一 flow 的内部 layer 留在一份 design。文档过大不是唯一拆分理由，先判断是否真的存在两个 feature。

## Content

每份 design 从 big picture 展开，只写理解和维护该 feature 所需的内容：目的与 non-goal、user-visible behavior、system boundary、主要 flow、依赖或 data、重要 decision、failure/compatibility、验证方式。简单 feature 不必凑齐固定 heading；file listing、field 和 optional parameter 只在它们影响 design 时出现。

Source of truth 按问题类型判断：

- 用户确认的行为和已有产品文档决定 intended behavior。
- 源码、配置、测试和运行结果证明 current implementation。
- Git history 解释 change，不单独证明当前意图。
- 三者冲突时明确记录 conflict；不要把当前代码自动改写成产品需求。

同一 fact 只维护一处。README 和其他 design 只 refer canonical document，不 copy 整段说明。

## Maintenance

- 新 feature：创建对应 design，并在 README Document map 添加一行。
- 行为、boundary、flow、dependency 或重要 decision 变化：更新原 design。
- rename、split 或 merge：同步文件、Document map 和 current reference；先确认没有丢失仍有效的事实。
- feature 删除：确认实现与 current reference 都已移除后，再删除或保留为明确的 historical record。
- 纯内部修改没有改变 design fact 时，不制造文档 churn。

普通代码工作在完成前同步实际变化影响的 design。
