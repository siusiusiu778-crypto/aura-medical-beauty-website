# AURA Institute 官网

AURA Institute 医美机构官网：Nuxt 4 + Vue 3（SSR），内容由 Vectra CMS 提供。正式站：<https://aurainstitute.com>（`www.` 跳转到裸域）。

## 给前端同事：先看这几条

1. **你可以直接改页面**：版式、样式、交互、新增模块都行。新增或调整模块时，**文案、图片、数字可以直接写死在前端页面里**，不用先去 CMS 建字段。
2. **写死的地方留一行标记** `CMS-TODO(区块名): 说明`，把它迁进 CMS（后端出数据）由负责人来做。
3. **已经从 CMS 读数据的页面**（首页、About、Membership、Facial Blueprint、Journal、目标页、治疗页）改版式没问题，但别把 CMS 的文字、图片改成写死。
4. 改动走分支和 PR；PR 的「check」通过后由负责人合并，**合并后自动发布到正式站**。
5. 你不需要、也不能碰服务器、接口、后端、Nginx。

详细规则见 [AGENTS.md](AGENTS.md)（Claude Code 会自动读取 [CLAUDE.md](CLAUDE.md)）。

## 快速开始

需要 Node 22 与 pnpm。

```bash
pnpm install
```

后端没接时用 mock 数据启动（读 `seed/aura-seed.json`）：

```bash
pnpm dev:mock
```

提交前确认：

```bash
pnpm typecheck
```

```bash
pnpm build
```

## 文档

| 文件 | 内容 |
|---|---|
| [docs/refactor-plan.md](docs/refactor-plan.md) | 整体方案、部署架构、换正式域名的步骤、实施记录 |
| [docs/api-contract.md](docs/api-contract.md) | 前后端接口约定（不要单方面修改） |
| [docs/content-schema.md](docs/content-schema.md) | CMS 内容结构（不要单方面修改） |
| [deploy/nginx/README.md](deploy/nginx/README.md) | 目标机器接入与发布的脱敏记录 |

## 目录

```
app/        页面、组件、样式、写死的图片（app/assets/img/）
server/     服务端路由（预览、缓存刷新、发布状态），别改
shared/     接口类型，别改
seed/ tools/  初始内容与抽取脚本
legacy/     原静态原型（验收后删除；GitHub Pages 上的旧原型地址跳转到这里）
```

## 注意

这是**公开仓库**：不要提交服务器地址、内网地址、密钥、未公开的客户信息。
