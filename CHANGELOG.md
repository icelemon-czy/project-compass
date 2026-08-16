# Changelog

Compass 将 `compass/` 及其中的 `AGENTS.md`、`context/`、`skills/`、`subagents/`、`hooks/` 和 `platforms/` 视为模板公共接口；安装说明在 `doc/install_instruction.md`。fork 使用者请按本文件判断是否需要 rebase。

版本号采用 [Semantic Versioning](https://semver.org/)：

- **MAJOR** — 安装契约、hook 契约或项目知识约定的不兼容变更
- **MINOR** — 新增平台或可选能力
- **PATCH** — 措辞修订、拼写、语义不变的澄清

## [Unreleased]

## [0.6.0] — 2026-08-16

项目知识在目标仓库自己的 README 和 `doc/`。安装器留下平台规则、三个 Skill（`brainstorm`、`ralph-loop`、`skill-creator`）、可选 CLI worker hook，以及 `.compass/context/` 下的 `cli-worker.md` 与 README。

### Removed

- 删除 `/develop`、`/fix-bug`、`/ask-codebase`、`/build-context`、`/init-project`、`/audit-tests`。
- 删除 L1–L5 context 模板、`doc-sync.md` 和默认 `sdd-reviewer`。

### Changed

- 安装包保留 `/brainstorm`、`/ralph-loop`、`/skill-creator`；它们读目标仓库 README 和 `doc/`。安装时复制到各已选平台的 project-level Skill directory。
- 项目知识约定改为目标仓库的 README 和 `doc/`（`doc/<feature>_design.md` 每模块一份；`doc/todo.md` 可选）。安装器不覆盖、不编造。
- `AGENTS.md` 写入该约定；`.compass/context/` 留下 `cli-worker.md` 与目录 README。
- CLI worker 锁文件改为 `.compass/context/cli-worker.lock`。
- 根 README 只说明 Compass 是什么，并 refer 到 `doc/` 下各模板部件的 design；安装说明在 `doc/install_instruction.md`。`compass/` 只承载模板副本。
- `compass/templates/` 提供目标仓库的 README 骨架（Document map 指向 `doc/<feature>_design.md`）；安装时缺失则复制，已有则按模版整理结构。
- 删除维护者目录 `docs/`。Compass 自己的 design 放在 `doc/`。
- 新增根 `LICENSE`（MIT）。

## [0.5.0] — 2026-08-16

### Added

- 新增 Cursor platform installer：根 `AGENTS.md`、`.cursor/skills/`、只读 `.cursor/agents/sdd-reviewer.md`。
- Installation 会在本机判定 Claude Code CLI 是否可调用，并把结果写入 `.compass/context/cli-worker.md`。
- Planner platform（Codex / Cursor / OpenCode）在 `enabled` 时从 `compass/hooks/cli-worker/` 迁移 native hook，拦截 implementation 并改为调用 `claude` CLI 做同一件工作。Claude Code 不安装该 hook。
- Installation 会在 repository-local `.git/info/exclude` 中维护 Compass 受管区块，写入 `/.compass/` 以及已选 platform 的 `AGENTS.md` / `CLAUDE.md`、Compass Skill、generated Subagent 和已安装 hook 精确 path，不修改 shared `.gitignore` 或 tracked-file index flag。
- 新增 `/skill-creator` Skill，用于创建、更新、rename、merge、split 或验证 project-local Skill，并优先复用现有能力、同步 canonical inventory 与执行 trigger boundary 验证。
- 新增 `/brainstorm` Skill，将尚未定型的 idea 与现有 codebase facts 结合，比较真实 alternatives 并收敛 design direction；用户要求实施时在同一任务中进入 `/develop`。
- 新增 `/ralph-loop` Skill，以可验证完成条件驱动持续改进，并在平台支持时复用原生 goal/continuation 能力。
- Ralph Loop 可把单轮工作路由到现有 Compass Workflow，同时保留 Proposal、Review、权限和验证边界。
- 新增统一 `/develop` Skill，从用户目标自动推进 plan、TDD、review、context sync 和 archive。
- 新增内置只读 `sdd-reviewer`，用 `plan` / `verify` 两种模式合并影响、Spec 和测试审查；Main Agent 保持状态机 owner。

### Changed

- 将 L1/L2 上下文同步收口为代码变更 workflow 的自动收尾步骤，由 `doc-sync.md` 提供唯一规则；用户无需额外触发同步。
- `/build-context` 保持为已有代码库首次构建或完整重建上下文的独立入口。
- 将原 `/build-ai` 重命名为 `/build-context`，原 `/change` 重命名为 `/develop`，并缩短全部 Skill descriptions、补充互斥触发边界。
- 只有外部契约变化才走 SDD；内部重构等走 lightweight path，不再为所有修改创建 Spec。
- 每个已选平台默认生成只读 `sdd-reviewer`；角色不可用时 Main Agent 使用同一协议 inline fallback。
- 将 `/review-tests` 重命名为 `/audit-tests`，明确它只负责专项测试可信度审计；默认返回结果而不写入 L5 report。
- 普通 code review 保持为 Agent 通用能力，不新增 Compass Skill；正常开发已在 `/develop` 内部完成必要 review。
- 支持平台现为 Codex、Cursor、Claude Code 与 OpenCode。

### Removed

- 移除独立的 `/update-ai`；同步成为代码变更的自动后置条件。
- 将 `/new-change`、`/continue-change` 和 `/archive-change` 合并为 `/develop`。
- 将 `/check-changes` 合并到 `/ask-codebase`，将 `/git-init` 合并到 `/init-project`，将 `/setup-testing` 合并到 `/build-context`。
- 移除 `/git-commit`；commit/push 继续由 Agent 通用能力在用户明确要求时执行。
- 将 `impact-analyst`、`spec-validator`、`test-reviewer` 合并为 `sdd-reviewer`。
- 当前安装包从 13 个 Skill 收敛为 9 个（7 个核心入口 + 可选 `/ralph-loop`、`/skill-creator`）。

### Compatibility

- Skill 名称和 L1–L5 语义结构保持不变。
- CLI worker 默认关闭，除非安装时探测到可调用的 `claude`。
- Hook 是新的一类受管 artifact；不修改 `.codex/config.toml` 或 `opencode.json`。

## [0.4.0] — 2026-07-12

### Changed

- 产品名称收敛为 **Compass（罗盘）**。
- 明确产品定位为可以直接复制到目标项目 `.compass/` 的 AI 辅助开发工具包。
- 将源码安装包目录统一为 `compass/`，目标项目目录统一为 `.compass/`，不保留旧名称的别名或软链接。
- 将当前支持平台收敛为 Codex、Claude Code 与 OpenCode。
- 将可复制运行资产收口到唯一 `compass/`；根目录只保留说明和维护文档。
- 将原有 13 个 Skill 收口到 `compass/skills/` 唯一权威目录；不保留 Skill 复制目录或软链接。
- 将 L1–L5 空白上下文直接收口到 `compass/context/`，安装后在原地填写为目标项目 `.compass/context/`。
- 将四个可选的具体 Subagent 角色与三平台安装器及模板收口到 `compass/`；每个角色声明适用的委派条件，默认不生成真实 Subagent 实例。
- 将安装包中的适配目录统一命名为 `platforms/`，按 Codex、Claude Code、OpenCode 分组。
- 将总 `compass/INSTALL.md` 收敛为平台无关编排器，平台差异由各自的 `platforms/<platform>/INSTALL.md` 封装。
- 将 TODO、工作流分析和路线图保留在仅供维护者使用的 `docs/`。

### Added

- 新增 `compass/INSTALL.md`，作为供 Agent 执行的非破坏安装、迁移、验证和移除契约。
- 新增带稳定标记区块的 `compass/AGENTS.md`，允许安装 Agent 与现有项目规则安全合并。
- 为 Codex、Claude Code 和 OpenCode 分别新增平台安装、验证、结果回传与移除契约。
- 恢复 `build-ai` 的 Skill-local references，将 L1 发现、L1 深入分析、L2 规则、L3 Spec、L5 验证、结构准备和入口边界作为按需加载的详细流程。

### Removed

- 移除 GitHub Copilot 与 Cline 的 builders、entrypoints 和当前支持说明。
- 移除旧 `.github/skills/`、嵌套模板目录、通用 Skill 脚手架和 Claude builder prompts。
- 移除已放弃的 manifest、installed manifest、config 和 Bash `compass` CLI。
- 移除 AGENTS global/project 分层与重复平台 AGENTS 模板。
- 移除没有产品价值的仓库静态测试与仅服务于它的 GitHub Actions CI。
- 移除 Codex 旧式 `[agents.<id>]` 注册模板和会重复加载根 `AGENTS.md` 的 OpenCode 配置模板。

### Compatibility

- 13 个 Skill 名称和 L1–L5 语义结构保持不变。
- 安装方式改为仅复制 `compass/` 后让 Agent 执行 `.compass/INSTALL.md`，不提供 Bash 安装脚本或全局安装。
- 旧 `.ai/` 由安装 Agent 非破坏迁移到 `.compass/context/`，验证前不删除原目录。
- `.github/skills/`、旧嵌套模板目录、根目录 `L1-*` 至 `L5-*`、`.ai/` 和旧 `entrypoints/` 属于已迁移或移除的旧接口。
- 本次版本不自动重命名 GitHub 仓库、本地目录或 Git remote。

## [0.3.0] — 2026-04-18

### BREAKING
- **`/spec-fix` 改名为 `/fix-bug`**，并内置 5 类分诊（代码 / 测试 / 虚假通过 / Spec 歧义 / Spec 缺失）。fork 用户需要把对 `/spec-fix` 的引用替换为 `/fix-bug`。
- **proposal.md 模板新增必填字段**：`parent-change`、`depth`。旧模板生成的 proposal 可留空，但新 skill 期望这两个字段存在。

### Added
- `/review-tests` Step 0：**强制执行项目测试套件**。红灯直接转 `/fix-bug`，不得在失败状态下走审查。
- `/review-tests` Step 3：**7 条虚假通过反模式清单**（断言缺失 / 断言太弱 / Happy path only / Mock 了要测的东西 / Assertion 绕开 spec THEN / 条件永真 / 吞异常）。项目可在 `L2-rules/testing.md` 追加第 8+ 条。
- `/fix-bug` Step 3C：**递归环检测**，`depth >= 2` 时不再创建嵌套 fix 变更。
- `/new-change` Step 7：**强制读取 L2 rules** 并在输出中列出本次要遵守的关键规则。
- `/continue-change` Step 2a：**L4 session 漂移检查**，session 与 git/tasks 不一致时必须先对齐再续写。
- `/update-ai` Step 2：明确标注 `git diff` 是启发式，Step 3 必须由用户逐条确认。
- `/archive-change` Step 3：MODIFIED 区段合并示例（整块替换规则）。
- `/build-ai`：明确对 `builders/*.md` 的版本依赖，缺失时停止而不是自造。
- `proposal.md` 模板：允许状态转移表 + append-only 转移日志。
- `README` / `README.zh`：专门的 Skill 章节，含 skill 发现机制说明（Claude Code 原生、Copilot 指令驱动）。
- `VERSION` + 本 `CHANGELOG.md`。
- `.github/workflows/validate.yml`：最小 CI（SKILL.md 单 front-matter 校验、无 `13 skills` 字样残留）。
- `L5-validation/traceability/_example.md`：一个填好的追溯示例。

### Changed
- 统一使用 **12 skills** 口径（之前文档错误标注为 13）。
- "唯一人工门槛" 措辞更正为 **两个关键人工门槛（Proposal + Review）+ 少量轻确认**。
- README 中 skill 流程图改为 mermaid，避免 ASCII 在中英混排下对齐错位。

### Fixed
- **P0**：`.github/skills/fix-bug/SKILL.md` 与 `.github/skills/review-tests/SKILL.md` 末尾残留旧版本 front-matter + 正文，YAML 解析会被污染。已移除。

## [0.2.0] — 2026-04-17
- 首版 `/spec-fix`、`/review-tests`（静态审查）、`/archive-change`。

## [0.1.0] — 2026-04
- 初始 5 层架构 + builder prompts。
