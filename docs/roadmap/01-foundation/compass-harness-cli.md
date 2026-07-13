# Compass Harness CLI

> 级别：基础层
> 优先级：P1
> 一句话：把 Compass Harness 从一套文档和 prompt，升级为可执行的 workflow harness。

## 要解决的问题

- 当前安装由 Agent 按 `harness/INSTALL.md` 执行；只有真实使用证明需要自动化后，才考虑统一 CLI。
- 文档结构漂移、状态机错误、字段缺失、目录不一致等问题缺少统一检查入口。
- 新用户接入 Compass 时，需要手动建立 `.compass-harness/` 权威目录并渲染平台适配模板。

## 为什么现在做

- 这是后续 Workflow Macros、Cross-Tool Adapter、Governance 的共同底座。
- 如果没有执行层，Compass 很容易继续停留在“写得很完整，但运行不稳定”的状态。
- 当前仓库已经明确模板源与目标项目 `.compass-harness/` 安装契约，适合继续实现 CLI。

## 规划范围

- `compass doctor`：检查目录结构、缺失文件、公共接口漂移。
- `compass validate`：检查 change 状态、task 结构、session 对齐、文档引用一致性。
- `compass generate`：从 `.compass-harness/` 生成或刷新 AGENTS、tool-specific Skill 镜像、Subagent 适配和基础索引文件。
- `compass check-api`：验证模板字段、目录约定和版本兼容性。

## 非目标

- 不在第一阶段做成重型云端控制平面。
- 不试图替代项目本身的测试框架、构建系统或 OpenSpec CLI。
- 不要求所有 Compass 流程都只能通过 CLI 运行。

## 关键依赖

- 以 `harness/skills/` 为唯一源，并保持 `harness/INSTALL.md` 的非破坏安装契约。
- 给现有 workflow 状态机一个机器可检查的表示。
- 约定 CLI 与文档目录之间的版本关系。

## 里程碑建议

1. 先做 `doctor` 和 `validate`，覆盖结构与状态检查。
2. 再做 `generate`，统一生成入口文件和技能骨架。
3. 最后接 CI 和升级检查，让公共接口变更更可控。

## 开放问题

- CLI 用 Node.js 还是保持尽量无运行时依赖。
- 是否真的需要 manifest，还是继续由 `harness/INSTALL.md` 作为唯一安装契约。
- 是否需要显式的 `compass upgrade` 命令。

## 相关文档

- [基础层索引](README.md)
- [路线图总索引](../README.md)
- [根 README](../../../README.md)
- [工作流分析](../../workflow-analysis.md)
