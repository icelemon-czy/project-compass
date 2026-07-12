# Compass Harness TODO

> 当前状态：Phase 1、Phase 2（含 `.compass-harness/` 中心化安装结构）已于 2026-07-12 完成。
>
> 目标：将 Project Compass 演进为 **Compass Harness**——一套面向可靠 AI 辅助软件开发的上下文、代理、流程与验证系统。

## 产品定位

- **项目名称**：Compass Harness
- **产品类别**：AI Engineering System
- **英文定位**：An open AI engineering harness for context, agents, skills, specs, workflows, and verification.
- **中文定位**：面向可靠 AI 辅助软件开发的上下文、代理、流程与验证系统。
- **CLI 名称**：`compass`

## 实施原则

- 品牌改名与架构重构分开提交。
- 第一阶段不修改现有公共接口。
- `compass`、Skill 名称和 L1–L5 语义结构保持兼容；目标项目中的上下文从 `.ai/` 迁入 `.compass-harness/context/`。
- 模板内容只维护一份权威源文件，由适配器生成不同 AI 工具需要的文件。
- 历史 Changelog 中的旧项目名称保留，当前文档统一使用新名称。

## 目标平台

Compass Harness 后续只支持以下三个 AI 开发工具：

- **Codex**
- **Claude Code**
- **OpenCode**

Phase 2 将停止维护 GitHub Copilot 和 Cline 适配。这里的“移除 GitHub”仅指 Copilot 相关的 builders、entrypoints 和 Skill 适配；`.github/workflows/` 中的 GitHub Actions CI 保留。

### 三平台共享策略

- 目标项目的 `.compass-harness/` 保存上下文、Skills、Subagent 角色和安装元数据，是唯一可编辑权威目录。
- 根 `AGENTS.md` 作为 Codex 与 OpenCode 共享的薄入口，只导航到 `.compass-harness/`。
- Codex/OpenCode 的 `.agents/skills/` 与 Claude Code 的 `.claude/skills/` 是生成镜像，不作为权威源手工修改。
- Subagent 权威角色保存在 `.compass-harness/subagents/`，按选择分别生成：
  - Codex：`.codex/agents/*.toml`
  - Claude Code：`.claude/agents/*.md`
  - OpenCode：`.opencode/agents/*.md`
- `CLAUDE.md` 作为 Claude Code 的薄入口，只导航到 `.compass-harness/`。
- `opencode.json` 只保存 OpenCode 特有的权限和 instructions 配置，不复制项目知识正文。

## 第一阶段：品牌改名

### 任务

- [x] 将 `README.md` 的显示名称改为 Compass Harness。
- [x] 将 `README.zh.md` 的显示名称改为 Compass Harness。
- [x] 更新 `slides.md` 中的品牌名称和定位。
- [x] 更新 `WORKFLOW-ANALYSIS.md` 中的当前品牌名称。
- [x] 更新 `roadmap/README.md` 和各路线图中的当前品牌名称。
- [x] 更新 `compass` CLI 的注释、Banner 和帮助文本。
- [x] 在中英文 README 中加入统一的产品定位。
- [x] 将版本升级为 `0.4.0`。
- [x] 在 `CHANGELOG.md` 中记录品牌变化和兼容性说明。

### 本阶段不修改

- [x] CLI 仍使用 `compass`。
- [x] 项目上下文目录仍使用 `.ai/`。
- [x] Skill 名称保持不变。
- [x] L1–L5 目录结构保持不变。
- [x] 未自动重命名 GitHub 仓库、本地目录或远端地址。

### 验收标准

```bash
rg "Project Compass|project-compass"
bash -n compass
git diff --check
git status --short
```

- 当前产品文档和 CLI 展示统一使用 Compass Harness。
- `Project Compass` 仅允许存在于历史记录或明确的迁移说明中。
- CLI 语法检查通过。
- Git diff 不包含空白错误。

## 第二阶段：迁移现有 Skill 并建立新增能力模板

Phase 2 包含两类产物：项目原有的 13 个 Skill 迁移到新的跨工具权威目录，作为真实 Skill 继续维护；AGENTS、Subagent 和三平台配置等新增能力只提供模板，不在本仓库安装为真实实例。

### 实施原则

- **保留现有资产**：原有 13 个 Skill 不丢弃，迁移到 `.agents/skills/` 权威目录。
- **新增能力模板化**：AGENTS、Subagent 和平台配置只提供模板，不提前安装完整运行系统。
- **不伪造验证**：不把主观 AI 输出、跨平台行为一致性或一次演示结果写成可重复验收标准。
- **不生成实例**：只提供 Subagent 角色模板和平台格式示例，不创建 `.codex/agents/`、`.claude/agents/` 或 `.opencode/agents/` 实例。
- **保留最小结构**：模板只规定必要字段和职责边界，不强制项目完整填写 L1–L5。
- **单一权威源**：本模板仓库在 `.agents/skills/` 维护原始 Skill；安装到目标项目后统一进入 `.compass-harness/skills/`。平台原生目录只保存生成的发现层。

### 内容边界

Phase 2 交付以下内容：

- `.agents/skills/` 中迁移后的 13 个现有 Skill。
- 通用工作原则 `AGENTS.md` 模板。
- 项目级 `AGENTS.md` 和最小 `.compass-harness/context/` 上下文模板。
- 供未来新建 Skill 使用的通用 `SKILL.md` 模板。
- 通用 Subagent 角色模板，以及 Explorer、Impact Analyst、Test Reviewer、Spec Validator 四个角色示例。
- Codex、Claude Code、OpenCode 的格式适配模板。
- 模板 manifest、占位符规范和静态检查规则。

以下内容不属于 Phase 2：

- 不重新设计 13 个现有 Skill 的完整业务流程；Phase 2 只做迁移和跨工具格式整理。
- 不实现真实变更闭环或跨平台行为一致性测试。
- 不调用、生成或安装真实 Subagent。
- 不生成具体项目的技术栈、代码地图、Spec、会话状态和验证报告。

### 模板仓库目录

本仓库保留可直接开发和验证的 Skill 权威源；其余新增能力集中放入模板目录：

```text
.agents/skills/                       # 从 .github/skills/ 迁移的 13 个真实 Skill

templates/compass-harness/
├── manifest.yaml
├── agent-rules/
│   ├── AGENTS.global.md
│   └── AGENTS.project.md
├── context/
│   ├── L1-codebase-map/
│   ├── L2-rules/
│   ├── L3-specs/
│   ├── L4-session/
│   └── L5-validation/
├── skills/
│   └── _skill-template/
├── subagents/
│   ├── _subagent-template.md
│   └── examples/
└── adapters/
    ├── codex/
    ├── claude-code/
    └── opencode/
```

### 目标项目安装目录

Compass Harness 安装到其他项目时，所有可编辑内容集中在 `.compass-harness/`；工具原生路径只作为生成的薄适配层：

```text
.compass-harness/
├── manifest.yaml
├── config.yaml
├── rules/                           # 跨平台共享规则与项目导航
├── context/                         # L1–L5 项目上下文
├── skills/                          # 13 个 Skill 的安装后权威源
└── subagents/                       # 通用角色定义与所选角色

AGENTS.md                            # Codex/OpenCode 薄入口
CLAUDE.md                            # Claude Code 薄入口
.agents/skills/                      # Codex/OpenCode 生成镜像
.claude/skills/                      # Claude Code 生成镜像
.codex/agents/                       # 可选生成适配
.claude/agents/                      # 可选生成适配
.opencode/agents/                    # 可选生成适配
```

`.compass-harness/` 之外的生成文件不得承载唯一项目知识；删除后应能由 Phase 3 CLI 从权威目录重建。

### Phase 2A：迁移现有 13 个 Skill

- [x] 将 `.github/skills/` 中现有 13 个 Skill 迁移到 `.agents/skills/`。
- [x] 保留原有 Skill 名称和主要工作流，避免迁移阶段同时进行大规模功能重写。
- [x] 将权威 `SKILL.md` frontmatter 整理为跨工具格式；平台专用字段不进入权威源。
- [x] 修正 Skill 中已失效的 Copilot/Cline 路径引用，并统一指向 Compass Harness 当前目录。
- [x] 检查 Skill 之间的名称引用和相对文件引用，避免迁移后断链。
- [x] 更新 `.github/workflows/validate.yml`，将 Skill 静态检查目标切换到 `.agents/skills/`。
- [x] 在确认新目录完整后，移除旧 `.github/skills/`，不长期维护两份 Skill。

### Phase 2B：定义模板契约并编写基础模板

- [x] 创建 `templates/compass-harness/manifest.yaml`，定义模板版本、组件、源文件、适配器和安装目标。
- [x] 定义统一占位符格式，例如 `{{PROJECT_NAME}}`、`{{TEST_COMMAND}}`、`{{SOURCE_ROOT}}`。
- [x] 明确哪些字段必填、哪些可选，以及未填写占位符的处理方式。
- [x] 定义模板文件命名规则和相对引用规则。
- [x] 编写全局 `AGENTS.md` 模板：只包含跨项目原则、权限边界和基本完成条件。
- [x] 编写项目 `AGENTS.md` 模板：只负责导航项目上下文，不复制 L1–L5 正文。
- [x] 整理 L1–L5 的空白模板；标注最小必填内容，不要求全部启用。
- [x] 编写 `_skill-template/SKILL.md`，包含触发描述、前置条件、步骤、允许写入、失败条件、输出和完成定义。
- [x] `_skill-template` 只用于以后创建新 Skill，不复制 `.agents/skills/` 中现有 Skill 的正文。

### Phase 2C：编写 Subagent 角色模板

本阶段只写角色定义，不创建或运行真实 Subagent。

- [x] 编写 `_subagent-template.md`，包含角色目标、输入、只读/写入权限、禁止事项和输出契约。
- [x] 编写 Codebase Explorer 示例模板。
- [x] 编写 Impact Analyst 示例模板。
- [x] 编写 Test Reviewer 示例模板。
- [x] 编写 Spec Validator 示例模板。
- [x] 示例模板只表达职责和输出结构，不声称已经验证其推理质量。

### Phase 2D：编写三平台适配模板

- [x] Codex：提供 `AGENTS.md`、`.agents/skills/` 和 `.codex/agents/*.toml` 的目标格式示例。
- [x] Claude Code：提供 `CLAUDE.md`、`.claude/skills/` 和 `.claude/agents/*.md` 的目标格式示例。
- [x] OpenCode：提供 `AGENTS.md`、`.agents/skills/`、`opencode.json` 和 `.opencode/agents/*.md` 的目标格式示例。
- [x] 适配模板引用同一份角色和 Skill 权威模板，不复制通用正文。
- [x] Phase 2 不将这些模板安装到仓库根目录；安装和生成留给 Phase 3 CLI。

### Phase 2E：静态检查与旧平台清理

Phase 2 只做能够客观重复执行的静态检查：

- [x] 检查 `manifest.yaml` 能被解析，且声明的源文件全部存在。
- [x] 检查 `.agents/skills/` 中 13 个现有 Skill 的 frontmatter、目录名和内部引用。
- [x] 检查新建 Skill 模板的 frontmatter 和必填章节。
- [x] 检查 Subagent 模板包含角色、权限、禁止事项和输出契约。
- [x] 检查模板中的相对引用无断链。
- [x] 检查所有占位符已登记；示例文件不得残留未登记占位符。
- [x] 检查三个适配器模板均引用权威源，不维护重复的通用正文。
- [x] CI 只执行以上静态检查，不声称验证 AI 行为。

静态检查通过后清理旧平台：

- [x] 移除 `builders/copilot/` 和 `builders/cline/`。
- [x] 移除 `entrypoints/copilot-instructions.md` 和 `entrypoints/clinerules.md`。
- [x] 确认旧 `.github/skills/` 已完成迁移并删除，不再作为 Skill 权威源。
- [x] 保留 `.github/workflows/` 中的 GitHub Actions CI。
- [x] 清理 README、工作流文档和路线图中的 Copilot/Cline 当前支持说明。
- [x] 保留 Changelog 和多 Agent 调研中的 Copilot/Cline 历史记录。

### Phase 2F：中心化目标项目安装结构

- [x] 将目标项目的权威安装根目录定义为 `.compass-harness/`。
- [x] 将上下文安装目标从 `.ai/` 改为 `.compass-harness/context/`。
- [x] 将安装后的 Skill 权威目录定义为 `.compass-harness/skills/`。
- [x] 将通用 Subagent 角色权威目录定义为 `.compass-harness/subagents/`。
- [x] 将 `AGENTS.md`、`CLAUDE.md` 和各工具私有目录明确为可重建的薄适配层。
- [x] 更新 manifest、13 个 Skill、上下文模板、适配器、CLI 与当前文档中的路径。
- [x] 静态检查禁止当前模板和 Skill 继续依赖 `.ai/`，并验证 `.compass-harness/` 安装契约。

### Phase 2 完成定义

- 本仓库 `.agents/skills/` 包含迁移后的 13 个原始 Skill；目标项目将其安装到 `.compass-harness/skills/`。
- `templates/compass-harness/` 目录结构完整，manifest 与实际文件一致。
- 目标项目所有可编辑的 Harness 内容位于 `.compass-harness/`，平台原生文件均可由其重建。
- 全局/项目 AGENTS、Skill、Subagent 和三平台适配模板均已提供。
- 四个 Subagent 仅作为角色示例存在，仓库根目录没有生成真实 Subagent 配置。
- Phase 2 的验收仅包含可重复执行的静态检查，没有跨平台行为或推理质量承诺。
- Copilot 与 Cline 当前模板已移除，GitHub Actions CI 继续可用。

## 第三阶段：CLI 执行层

### 目标命令

```text
compass init
compass generate
compass doctor
compass validate
compass upgrade
```

### 任务

- [ ] `compass init`：选择模板并初始化新项目或现有项目。
- [ ] `compass generate`：从权威模板生成各 AI 工具适配文件。
- [ ] `compass doctor`：检查 AGENTS、Subagents、Skills、适配器和 L1–L5 完整性。
- [ ] `compass validate`：检查变更状态机、Spec、测试、会话状态和追溯关系。
- [ ] `compass upgrade`：升级模板，同时保留项目自定义内容。
- [ ] 消除 CLI 中对 GNU `grep -P` 和 `find -printf` 的依赖。
- [ ] 为 macOS、Linux 和 CI 建立 CLI 测试夹具。
- [ ] 将结构检查和 CLI 测试接入 GitHub Actions。

## 推荐提交顺序

1. `docs: add Compass Harness transition plan`
2. `docs: rename Project Compass to Compass Harness`
3. `refactor(skills): migrate existing skills to the cross-tool source`
4. `feat(templates): define Compass Harness manifest and placeholders`
5. `feat(templates): add AGENTS and context templates`
6. `feat(templates): add Skill and Subagent role templates`
7. `feat(adapters): add Codex, Claude Code, and OpenCode templates`
8. `test(templates): add deterministic static validation`
9. `chore(platforms): remove Copilot and Cline templates`
10. `feat(cli): implement doctor and validate`
11. `feat(cli): implement generate and upgrade`

## 完成定义

- 新项目可以通过一个命令将 Compass Harness 安装到 `.compass-harness/`。
- Codex、Claude Code 和 OpenCode 使用同一套权威规则与工作流。
- 项目上下文、Subagents 和 Skills 可以独立升级并进行版本检查。
- Agent 不依赖人工提醒即可找到适当上下文和工作流。
- 所有“完成”结论都有测试、验证报告或追溯证据支持。
