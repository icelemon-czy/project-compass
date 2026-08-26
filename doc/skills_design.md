# Skills

这是 `compass/skills/` 的 design。下表是 canonical Skill inventory；每个 Skill 都读目标仓库的 README 和 `doc/`。

| Skill | 做什么 |
|:------|:-------|
| `brainstorm` | 澄清尚未定型的 idea，比较 alternatives，收敛 design direction |
| `ralph-loop` | 对有客观完成条件的任务持续迭代，直到验证通过或真实阻塞 |
| `skill-creator` | 创建、更新或精简 project-local Skill |
| `build-docs` | 首次建立或整体重整 README 和 feature design |
| `maintain-docs` | 合并文档 review 与 update，按 intent 只读检查或增量修复 |

安装时从 `.compass/skills/<skill>/` 完整复制到各已选平台的 project-level directory。装完 staging 删除，之后以平台 native copy 为准。用户自建同名 Skill 内容不同则不覆盖。

| Platform | Skill dest |
|:---------|:-----------|
| Codex | `.agents/skills/<skill>/` |
| Cursor | `.cursor/skills/<skill>/` |
| OpenCode | `.opencode/skills/<skill>/` |
| Claude Code | `.claude/skills/<skill>/` |

编排见 [install_instruction.md](install_instruction.md)。平台 dest 见 [platforms_design.md](platforms_design.md)。
