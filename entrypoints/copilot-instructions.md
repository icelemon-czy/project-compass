# AI 导航指令（GitHub Copilot 版）

> 复制本文件到项目的 `.github/copilot-instructions.md`

你有一套项目文档在 `.ai/` 下，按以下流程工作：

## 每次对话启动时（自动）

读取以下 3 个文件，建立基础认知：

1. `.ai/L1-codebase-map/overview.md` — 项目功能索引（< 60 行）
2. `.ai/L2-rules/global.md` — 全局编码规则与反模式
3. `.ai/L4-session/active-session.md` — 上次进度与下一步动作

## 收到任务后（按需导航）

1. **查索引** — 在 overview.md 的功能索引表中匹配任务涉及的功能
2. **读功能文档** — 读取 `.ai/L1-codebase-map/features/[功能名]/README.md`
   - 按需深入：各层 `.md` 文件（文件名反映实际架构层，如 handler.md / service.md / repo.md）
3. **读模块规则** — 读取 `.ai/L2-rules/[模块名].md`（编码约束 + 合约）
4. **做通用任务时** — 查 `.ai/L1-codebase-map/key-files.md`（任务食谱）
5. **跨模块修改时** — 查 `.ai/L1-codebase-map/module-map.md`（变更联动表）
6. **理解运行时结构时** — 查 `.ai/L1-codebase-map/architecture.md`（请求生命周期 + 启动顺序 + 运行时协作）
7. **改底层基础设施时** — 查 `.ai/L1-codebase-map/infrastructure/README.md`（框架基类、配置、插件、构建流程、测试基础设施等）
8. **创建新文件时** — 查 `.ai/L2-rules/templates.md`（标准代码模板）

## 任务管理

- 查看任务 → `.ai/L3-tasks/board.md`
- 创建任务 → 复制 `.ai/L3-tasks/_task-template.md`
- 写计划 + 提验收问题 → 等人类确认后再执行
- 参考历史决策 → `.ai/L3-tasks/decision-log.md`

## 对话结束时

更新 `.ai/L4-session/active-session.md`：
- 当前做到哪一步
- 涉及文件的状态
- 测试运行结果
- 下一步具体动作

同步 `.ai/L3-tasks/board.md` 任务状态：
- 任务进展有变化 → 更新 board.md 状态和测试列
- 代码完成 + 测试全部通过 → 状态改为 ✅ review，将任务文件移入 `L3-tasks/review/`

## 关键约束

- 修改代码前先查 overview.md 定位功能，不要盲目 grep
- 注意 overview.md 的「雷区清单」，不要碰标记的文件/配置
- 遵守 global.md 的所有规则，特别是「反模式清单」
- 跨模块修改前先查 module-map.md 的「变更联动表」
- 做了重要架构决策 → 记录到 decision-log.md
