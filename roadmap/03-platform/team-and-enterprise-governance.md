# Team And Enterprise Governance

> 级别：平台层
> 优先级：P1
> 一句话：让 Compass 能作为团队共享工程基础设施使用，而不仅是个人工作流工具。

## 要解决的问题

- 当前 Compass 已经把不少目录和模板视为公共接口，但缺少组织级治理能力。
- 在多人协作、合规要求或 release 审核场景下，现有文档还不足以构成可追责流程。
- 如果没有治理面，团队通常会通过 fork 和私有约定来补洞，长期会造成严重漂移。

## 为什么现在做

- 一旦进入多 Agent、cross-tool、pack 阶段，组织级规则和审计需求会自然出现。
- Governance 做得越晚，越容易和现有模板、workflow 发生冲突。
- 这也是把 Compass 从“好用方法”提升为“基础设施协议”的关键一步。

## 规划范围

- proposal、review、archive、release 的审计轨迹。
- rollback plan、风险确认、合规检查等 policy hook。
- 角色边界：谁能 approve、archive、skip validation。
- 为组织自定义规则提供插件或扩展点，而不是要求 fork 全仓库。

## 非目标

- 不在第一阶段建设完整 SaaS 管理后台。
- 不自己实现企业身份系统、权限平台或审批平台。
- 不要求所有团队必须采用同一套治理强度。

## 关键依赖

- 稳定的 workflow 状态机和结构化验证输出。
- 插件或 hook 的清晰边界。
- 对公共接口兼容性的更强约束。

## 里程碑建议

1. 先定义最小治理面：审计日志、approval points、policy hook 位置。
2. 再做组织自定义规则注入能力。
3. 最后补版本兼容、插件契约和治理模板。

## 开放问题

- 治理配置应该放在仓库内，还是允许组织级中心配置。
- 审计记录写 Markdown、YAML，还是独立结构化日志。
- 哪些策略属于核心 Compass，哪些只应由插件提供。

## 相关文档

- [平台层索引](README.md)
- [Cross-Tool Adapter Layer](../02-scale/cross-tool-adapter-layer.md)
- [路线图总索引](../README.md)
- [CHANGELOG](../../CHANGELOG.md)