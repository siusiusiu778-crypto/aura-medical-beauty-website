# AURA Institute 官网 — 给 Claude 的项目说明

完整的开发指引在 [AGENTS.md](AGENTS.md)，开始工作前先读它：

@AGENTS.md

## 对 Claude 的补充

- **允许写死内容**：新增或调整模块时，可以把文案、图片、数字直接写在前端代码里，不要为此反复追问或要求先建 CMS 字段；写死处按 AGENTS.md 留 `CMS-TODO` 标记，迁移进 CMS 由负责人完成。这与美窝新官网（要求代码里不放内容）的规则不同，不要沿用那边的习惯。
- 已经接了 CMS 的文字和图片（经 `usePageContent` 等取数的）不要改成写死。
- 用户说"发布""上线""部署"时，按 `.claude/skills/deploy/SKILL.md` 做，不要自己想办法登录服务器。
- 公开仓库：任何服务器地址、内网地址、凭据都不要写进文件或提交信息。
