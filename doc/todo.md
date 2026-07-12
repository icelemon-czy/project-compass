# Compass Harness TODO

> 当前状态：Phase 1 已于 2026-07-12 完成；Phase 2 尚未开始。
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
- `.ai/`、`compass`、Skill 名称和 L1–L5 结构暂时保持兼容。
- 模板内容只维护一份权威源文件，由适配器生成不同 AI 工具需要的文件。
- 历史 Changelog 中的旧项目名称保留，当前文档统一使用新名称。

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

## 第二阶段：专业 AI 系统模板

### 目标结构

```text
templates/
└── professional-ai-system/
    ├── manifest.yaml
    ├── global/
    │   └── AGENTS.md
    ├── project/
    │   ├── AGENTS.md
    │   └── context/
    │       ├── L1-codebase-map/
    │       ├── L2-rules/
    │       ├── L3-specs/
    │       ├── L4-session/
    │       └── L5-validation/
    ├── subagents/
    │   ├── _agent-template.toml
    │   ├── codebase-explorer.toml
    │   ├── impact-analyst.toml
    │   ├── test-reviewer.toml
    │   └── spec-validator.toml
    ├── skills/
    │   ├── _skill-template/
    │   ├── new-change/
    │   ├── continue-change/
    │   ├── fix-bug/
    │   ├── review-tests/
    │   └── archive-change/
    └── adapters/
        ├── codex/
        ├── claude/
        ├── copilot/
        └── cline/
```

### 任务

- [ ] 定义 `manifest.yaml` 的版本、组件和适配器字段。
- [ ] 创建全局 `AGENTS.md` 模板，只包含跨项目通用原则。
- [ ] 创建项目 `AGENTS.md` 模板，作为 `.ai/` 上下文导航入口。
- [ ] 创建通用 Subagent TOML 模板。
- [ ] 创建第一批只读 Subagent：Explorer、Impact Analyst、Test Reviewer、Spec Validator。
- [ ] 创建标准 Skill 模板，明确触发条件、输入、步骤、Subagent 编排、输出和验收规则。
- [ ] 将 Codex Skill 的权威源迁移到 `.agents/skills/` 对应模板。
- [ ] 由适配器生成 `.github/skills/` 等工具专用产物，避免双重维护。
- [ ] 定义模板升级和项目自定义内容的合并策略。

### 安装后的目标结构

```text
AGENTS.md
.ai/
.codex/agents/
.agents/skills/
.github/skills/
CLAUDE.md
```

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
3. `feat(templates): add professional AI system template`
4. `refactor(skills): establish canonical cross-tool skill source`
5. `feat(agents): add project-scoped custom subagents`
6. `feat(cli): implement doctor and validate`
7. `feat(cli): implement generate and upgrade`

## 完成定义

- 新项目可以通过一个命令安装 Compass Harness。
- Codex、Claude、Copilot 和 Cline 使用同一套权威规则与工作流。
- 项目上下文、Subagents 和 Skills 可以独立升级并进行版本检查。
- Agent 不依赖人工提醒即可找到适当上下文和工作流。
- 所有“完成”结论都有测试、验证报告或追溯证据支持。
