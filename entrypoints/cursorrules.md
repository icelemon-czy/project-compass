# AI 导航指令（Cursor 版）

> 复制本文件到项目根目录，重命名为 `.cursorrules`
>
> 也可以放入 `.cursor/rules/project-compass.md` 并在 frontmatter 中设置：
> ```yaml
> ---
> description: "Project context navigation via .ai/ docs"
> alwaysApply: true
> ---
> ```

你有一套项目文档在 `.ai/` 下，按以下流程工作：

## 每次对话启动时（自动）

读取以下 3 个文件，建立基础认知：

1. `.ai/L1-codebase-map/overview.md` — 项目功能索引（< 60 行）
2. `.ai/L2-rules/global.md` — 全局编码规则与反模式
3. `.ai/L4-session/active-session.md` — 上次进度与下一步动作

## 收到任务后（按需导航）

1. **查索引** — 在 overview.md 的功能索引表中匹配任务涉及的功能
2. **读功能文档** — 读取 `.ai/L1-codebase-map/features/[功能名]/README.md`
   - 按需深入：`entry.md`（入口层）/ `logic.md`（逻辑层）/ `data.md`（数据层）
3. **读模块规则** — 读取 `.ai/L2-rules/[模块名].md`（编码约束 + 合约）
4. **做通用任务时** — 查 `.ai/L1-codebase-map/key-files.md`（任务食谱）
5. **跨模块修改时** — 查 `.ai/L1-codebase-map/module-map.md`（变更联动表）
6. **创建新文件时** — 查 `.ai/L2-rules/templates.md`（标准代码模板）

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

## 关键约束

- 修改代码前先查 overview.md 定位功能，不要盲目 grep
- 注意 overview.md 的「雷区清单」，不要碰标记的文件/配置
- 遵守 global.md 的所有规则，特别是「反模式清单」
- 跨模块修改前先查 module-map.md 的「变更联动表」
- 做了重要架构决策 → 记录到 decision-log.md
