# Templates

这是 `compass/templates/` 的 design。

这里只有一份目标仓库的根 README 骨架：先写目的，再用 Document map 标出 `doc/<feature>_design.md` 这一层，并说明 `doc/todo.md` 只用于可选的当前工作。不提供单独的 feature design 文件。

安装时：根 README 不存在则复制本模版；已存在则按本模版整理结构（目的 + Document map），保留原有事实，不编造 `doc/` 下的 feature design。结果进 Git，不写进 local exclude。`.compass/templates/` 是 staging，装完删除。

完整文档边界见 [documentation_design.md](documentation_design.md)。
