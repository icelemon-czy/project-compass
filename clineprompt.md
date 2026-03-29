# Cline 构建 L1 代码地图 — Prompt 模板

> 将以下 prompt 复制到 Cline 对话中使用。
> 使用前替换 `[项目配置文件]` 和 `[项目目录]` 为实际路径。

---

## Prompt

```markdown
# 任务：构建项目代码地图

## 背景
我需要为本项目构建 AI 上下文文档，参考模板在：
.ai/L1-codebase-map/

## 你的工作步骤

### Step 1: 收集原始信息（只用命令，不要逐文件阅读）
运行以下命令并记住输出：
- tree -L 2 -I 'node_modules|.git|dist|__pycache__|venv|.venv|build|target'
- cloc . --exclude-dir=node_modules,dist,venv,.venv,build,target --quiet
- cat [项目配置文件]
- 阅读项目根目录的 README.md（如果有）

### Step 2: 填写三个模板文件
按顺序读取模板 → 用 Step 1 的信息填写 → 写入对应位置：
1. overview.md → 保存到 [项目目录]/.ai/L1-codebase-map/overview.md
2. module-map.md → 同上
3. key-files.md → 同上

### 约束
- overview.md 控制在 100 行以内
- 不确定的地方写 [待确认：xxx]，不要编造
- 依赖图只画模块级别，不画文件级别
- 如果某个模块结构复杂看不清，在 key-files.md 中标注 [需要深入分析]
```

---

## 补充说明

### Sub-agent 的正确用法

主 agent（Cline）做 80% 的粗粒度探索，sub-agent 只在需要深入某个模块时才用：

```
主 Agent（Cline）
├── 阶段1：自己执行命令，填写 overview.md
├── 【可选 Sub-agent】：验证 overview.md 的准确性
│     "请阅读 overview.md，然后抽查 3-5 个关键路径确认描述是否准确"
├── 阶段2：自己执行命令，填写 module-map.md  
├── 【可选 Sub-agent】：分析一个复杂模块的内部依赖
│     "请深入分析 src/core/ 模块，搞清楚它暴露了哪些公开 API"
└── 阶段3：填写 key-files.md
```

### 用命令代替逐文件阅读

| 需要的信息 | 用命令获取（快+省 token） | 不要这样做（慢+贵） |
|-----------|------------------------|-------------------|
| 目录结构 | `tree -L 2` | 逐个 `ls` |
| 代码规模 | `cloc .` | 逐文件 `wc -l` |
| 依赖方向 | `grep -rn "import\|from"` | 逐文件读取全部内容 |
| 技术栈 | 读 `package.json` | 扫描所有文件后缀 |
| 入口文件 | `grep -rn "main\|bootstrap"` | 每个文件都读 |
