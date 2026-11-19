# AURA Institute 官网重构方案（Nuxt SSR + Vectra CMS）

状态：Phase 0 核查完成，待开发　|　日期：2026-11-19

> 本仓库是公开仓库。本文不记录服务器地址、内网地址、凭据；这些以 `<占位>` 表示，实际值只在服务器与 Vectra 前端仓库的规范文档里。

## 0. 核查结论（决定了方案的几处关键选择）

| 项 | 核查结果 | 对方案的影响 |
|---|---|---|
| 目标机器 | CentOS 7，8 核 15G，磁盘余量 127G；Nginx 1.20（每个域名一个 `sites.d/*.conf`）；Docker 26 已装；**没有宿主机 Node**；机器上是多个 WordPress 站点，另有一个 Nuxt 容器 `uswoo-next`（`node:22-alpine`，host 网络，端口 3300，版本目录以只读方式挂进 `/app`，环境文件单独存放） | AURA 用同样的容器方式运行，端口取 3500（试启动 3501），目录与环境文件仿照 `uswoo-next` |
| 域名 | 机器上实际是 `overseasstudent.com`（配置文件 `www.overseasstudent.com.conf`，443 站点，证书覆盖该域名）。任务里写的 `oversesstudent.com` 是笔误 | 以 `overseasstudent.com` 为准 |
| 子目录名 | 任务里写的 `aura-institude`，英文应为 `aura-institute` | 主路径用 `aura-institute`；Nginx 同时接住 `/aura-institude` 并 301 到主路径。路径是环境变量，改名只改一处 |
| 该站点的 Nginx 配置 | 站点块里有**服务器级 `rewrite`**（如 `rewrite /. /index.php last;`），会在 location 匹配之前把几乎所有不存在的路径改写到 WordPress；还有一批正则 location（拦截特殊字符、按扩展名设缓存）。该文件今天还有人在改 | 只在该文件里加两行：一个放行 `if ($uri ~ ^/aura-institu[dt]e) { break; }`（与 uswoo.com 已有写法相同）和一个 `include` 指向我们自己的片段文件；片段里用 `location ^~ /aura-institute/`（`^~` 优先于正则）。改前备份、重新读最新内容、`nginx -t`、平滑重载、立即验证 WordPress 首页与后台不受影响，失败即还原 |
| 跳板与连通性 | 本机 → 跳板机 → 目标机器，SSH 密钥已通。目标机器能访问 `github.com` / `api.github.com`，**不能访问** uswoo.com 与跳板机的公网地址 | 发布沿用测试站的**拉取式**（Release 清单 + 服务器每分钟拉取）；一次性安装才需要经跳板 |
| 到 Vectra 的路径 | 目标机器经内网访问 Vectra 后端：`http://<Vectra 内网地址>:9924/portal_backend_v2/api/<前缀>`，带 `Host: <Vectra 后端主机名>`，已验证新官网公开接口可返回 | 按你的决定：在 198 的 Nginx 上做**同源内网反代**，`/aura-institute/api/` → Vectra 公开接口前缀，浏览器与服务端渲染都走它（服务端渲染也可直连内网地址）。同源，不需要跨域白名单；管理接口不在反代范围内 |
| 证书 | Let's Encrypt，`certbot renew` 每天 02:00 计划任务 | 不需要为 AURA 新签证书 |
| Vectra 后端仓库 | 真正的仓库是 GitHub 私有仓库 `ynliao99/portal_api`（`main`），后端目录 `portal_backend_v2`。本机 `~/Documents/Portal_API` 是空仓库加陈旧镜像，**不能用** | 已克隆到 `~/Projects/portal_api`；改既有后端文件仍从生产现拉 |
| 后端先例 | 新官网模块完整存在：`routes/uswoo_official.php`、控制器、`domain/`、`services/`、`repositories/`、`gateways/`、建表 SQL 与回滚、`bin/migrations/*_migrate.php`（默认只读，`--apply` 才执行）、`bin/*_seed_import.php`、配置类。签名密钥放系统凭据「内部密钥」（`internal.official_revalidate_<部署名>`、`internal.official_preview_secret`），本地配置文件只放非密钥。路由有加载顺序陷阱：固定段先于参数段，且必须先于 `uswoo_web` 的通用路由注册 | AURA 模块按同一结构写；密钥改放系统凭据，不放本地文件 |
| Vectra 前端先例 | `cms-kit/catalog.ts` 有两个目录（美窝房产CMS、留学生网小程序）；新官网页面是目录里的 `official*` 页面；另有 `src/views/tbts`（独立站点 CMS，自带媒体库）。前端 ChangeLog 在 `docs/CHANGELOG.md` | AURA 新增第三个目录与独立权限，视图放 `src/views/aura` |
| AURA 仓库现状（与旧 README 不一致） | 49 个 HTML、约 279 个媒体文件、61MB、2 个首页视频。仅剩 `tech-neck` 一页有 `[Copy to come]`，`[confirm]` 与 "SMILE" 字样已不存在。新增 `facial-blueprint`、`journal-faq`、`journal-botox-vs-xeomin`。导航含分组（如 Dermal Fillers / Wrinkle Relaxers）、标签（Signature、New）、一个顶层直链、搜索框（目前不起作用）、`My Account`（指向 `#`）、品牌 `AURA INSTITUTE by sxy`。页面里没有真正的预约表单，Book Now 只是跳到页内 `#book` | 治疗页模板化；预约表单、搜索是新增功能；`My Account` 在 CMS 里做显示开关，默认关；旧 README 与 `source/` 进 `legacy/` |

## 1. 总体架构

```
浏览器 ─► https://overseasstudent.com/aura-institute/ ─► 目标机器 Nginx ─► AURA 容器（Nuxt SSR，:3500）
                                                                              │ 内网直连
Vectra「AURA」菜单 ─► Vectra 后端（新表 aura_*，公开接口 /aura/public/*）◄────┘
      └─ 保存内容 → 签名通知 /aura-institute/_site/revalidate
```

- 内容与媒体存 Vectra 自有库新表；访客读实时数据，缓存只是兜底。
- 子目录、域名全部来自环境变量：`NUXT_APP_BASE_URL`、`NUXT_PUBLIC_SITE_URL`、`NUXT_PUBLIC_DEPLOY_ENV`。换正式域名只改环境变量和 Nginx server 块。
- 这个子目录部署阶段全站 `noindex`（响应头与 meta 双保险）；别人域名根目录的 `robots.txt` 不动。

## 2. AURA 网站（本仓库，PR 合入 main）

分支 `refactor/nuxt-cms`，提 PR，用户回复"合并"后合入；合并即触发测试发布。

**目录**：`app/`（pages、components、composables、layouts、assets/css）、`server/routes/_site/`（revalidate、preview、lead、media、health）、`shared/types/`、`seed/`、`tools/`（抽取脚本）、`deploy/`（脱敏配置记录）、`legacy/`（原静态站，验收后删除）、`.github/workflows/`、`CLAUDE.md`、`.nvmrc`。

**页面**

| 页面 | 路由 | 数据 |
|---|---|---|
| 首页 | `/` | `pages/home` |
| 目标页 ×6 | `/goals/{slug}` | `goals/{slug}`（下挂有序治疗） |
| 治疗页 ×35 | `/treatments/{slug}` | `treatments/{slug}`，**一个 `TreatmentView`** |
| Facial Blueprint | `/facial-blueprint` | `pages/facial-blueprint` |
| 会员 AURA Prime | `/membership` | `pages/membership` |
| About | `/about` | `pages/about` |
| Journal & FAQ、Botox vs Xeomin | `/journal/faq`、`/journal/botox-vs-xeomin` | `pages/journal-faq`、`pages/journal-botox-vs-xeomin` |
| 全站 | 导航、页脚、浮动 Book Now、搜索 | `pages/site` + 类别与治疗列表 |

- 导航由「类别 → 分组 → 治疗」生成；分组与标签可在 CMS 设置。搜索在浏览器端过滤治疗名称。
- 所有链接走 `NuxtLink`，不写死 `/`；响应与静态资源前缀由 `baseURL` 处理。
- 现有 6 份 CSS 限定在 `.pg-<页面>` 下复用；用 Playwright 对原型与新页面在桌面和手机宽度下截图对比。
- 预约表单：放在每页结尾的 `#book` 区块，浏览器直接 POST 到同源反代 `/aura-institute/api/leads`（由 198 Nginx 转到 Vectra）；蜜罐、提交间隔校验、后端按 IP 限流；来源标记 `staging` / `production`。
- 内容缺失处留空，不写默认文案；`copy_complete=false` 的页面自动 `noindex`，没有文案的区块隐藏。

## 3. Vectra 后端（`portal_api`，推 `main`，按 `docs/standards/backend-deployment.md` 上传）

模块 `aura_site`，文件仿 `uswoo_official`：`routes/aura.php`、`controllers/AuraSiteController.php`、`domain/aura_site/`、`services/aura_site/`、`repositories/aura_site/`、`gateways/AuraRevalidateGateway.php`、`settings/AuraSiteConfig.php`、`migrations/<日期>_aura_site.sql` 与回滚、`bin/migrations/aura_site_migrate.php`（默认只读）、`bin/aura_seed_import.php`（可重复）、`tests/`。

| 表 | 内容 |
|---|---|
| `aura_page` | 页面键 `site`、`home`、`about`、`membership`、`facial-blueprint`、`journal-faq`、`journal-botox-vs-xeomin`；结构化 JSON（`{en, zh}`，区块带 `show`）；草稿/已发布；历史版本 |
| `aura_category` | 导航类别（名称、排序、是否直链、标签） |
| `aura_treatment` | 35 个治疗：slug、类别、分组、名称、各区块 JSON、`copy_complete`、SEO、上线 |
| `aura_goal`、`aura_goal_treatment` | 6 个目标页与有序治疗 |
| `aura_media`、`aura_media_folder` | 媒体库 |
| `aura_lead` | 预约咨询与状态流转 |
| `aura_history` | 历史版本 |

通用列：`created_at`、`updated_at`（乐观锁）、`updated_by`、`deleted_at`。不改任何现有表，只新增，可重复执行。

**公开接口** `/aura/public/*`（对外经 198 反代暴露为 `/aura-institute/api/*`，只转发 GET 与 `POST leads`）：`site`、`pages/{key}`、`treatments`、`treatments/{slug}`、`goals`、`goals/{slug}`、`sitemap`、`preview/{entity}/{id}`、`POST leads`。匿名只读、统一信封、短缓存。
**管理接口** `/aura/admin/*`：能力描述、页面、类别、治疗、目标、媒体、咨询；需登录、乐观锁、历史恢复、审计。

**媒体库**：沿用 `uswoo_web_media` 的 OSS + CDN 与中英文 alt；新增文件夹、批量上传、视频与海报、原位替换（编号不变）、被引用反查；权限独立。约 279 个文件由种子脚本批量进库。
**权限**：「CMS管理权限」新增网站"AURA Institute"，键 `aura_*`：全局管理员、内容编辑、发布与下线、媒体、咨询处理。
**刷新通知**：`revalidate_targets` 放本地配置文件（非密钥），签名密钥放系统凭据 `internal.aura_revalidate_<部署名>`，与容器环境文件里的 `NUXT_REVALIDATE_SECRET` 同值。签名头与状态码读取一次做对。
**种子**：从 49 个 HTML 抽取 → `seed/` → `aura_seed_import.php`；图片进媒体库；`tech-neck` 标记为未完成。

## 4. Vectra 前端（`uswoo_portal`，推 `main`）

- `cms-kit/catalog.ts` 新增 AURA 目录（基础路径 `/aura`）：概览、页面、治疗、目标页、类别与导航、媒体库、预约咨询、权限。
- 视图在 `src/views/aura/*`，API 封装在 `src/api/aura.ts`，路由模块 `src/router/modules/aura.ts`。
- 页面编辑器内嵌 AURA 官网做**实时预览**（沿用 `useCmsEdit` 协议，`NUXT_PUBLIC_CMS_ORIGINS` 登记 Vectra 网址）。
- 约束：五种语言文案（繁体手写）、契约测试、前后端各写 ChangeLog；前端仓库不运行 `pnpm build` / `dev`。

## 5. 部署（目标机器，经跳板一次性安装，之后全自动）

**目录**（仿 `uswoo-next`）：`/home/aura-web/{releases,current,status,logs,acme?}`、环境文件 `/home/aura-web/aura.env`（权限 600，不进仓库）。
**容器**：`node:22-alpine`，host 网络监听回环端口 3500，限内存 768m / CPU 1.5，版本目录只读挂载。
**拉取式发布**（沿用测试站机制，脚本仓库里只留脱敏记录）：

1. 推 `main` → GitHub Actions：类型检查、构建、打包 `output-<sha>.tgz` 与 `manifest.json` → 上传 Release「staging」。
2. 目标机器每分钟一次拉取脚本：核对 sha256 → 解压 → 备用端口 3501 试启动并检查 `/aura-institute/` 返回 200 → 通过才切换 → 写 `status.json`；失败保留旧版本；保留最近 5 个版本。
3. Actions 读取 `https://overseasstudent.com/aura-institute/_deploy/status.json`，切换成功才算成功。
4. 回退：`gh workflow run deploy-staging.yml -f ref=<提交号>`。

**Nginx**（只动目标站点文件两行，其余放在我们自己的片段里）：

- 放行：`if ($uri ~ ^/aura-institu[dt]e) { break; }` 放在站点块最前，避免被服务器级 `rewrite` 改写到 WordPress。
- 接口反代（在同一片段里）：`location ^~ /aura-institute/api/` → `proxy_pass http://<Vectra 内网地址>:9924/portal_backend_v2/api/aura/public/;`，`Host` 设为 Vectra 后端主机名，只允许 GET、POST、OPTIONS，限制请求体 1m，超时 5s/30s；该 location 必须排在 `/aura-institute/` 之前（更长前缀优先，同为 `^~`）。
- 片段：`location ^~ /aura-institute/` → `proxy_pass http://127.0.0.1:3500`（不剥离前缀）；`/aura-institute` 与 `/aura-institude` 均 301 到 `/aura-institute/`；`X-Robots-Tag: noindex, nofollow`；`/_deploy/status.json` 放行。
- 验证：`curl --resolve` 对比改前改后 WordPress 首页、`/wp-admin/`、一个静态资源的状态码与响应头不变。

## 6. 实施顺序

| 阶段 | 内容 | 合入 / 发布 | 验收 |
|---|---|---|---|
| 1 | 后端：表、接口、权限、媒体库、种子脚本、测试、ChangeLog | 推 `portal_api` `main`；逐文件上传，权限门禁；先 dry-run 迁移再 `--apply`；导入种子 | 公开接口返回种子数据，管理接口能读写 |
| 2 | 前端：AURA 目录、各管理页、媒体库、实时预览、五语言、测试 | 推 `uswoo_portal` `main` | 能登录编辑并保存、预览生效 |
| 3 | AURA 站：Nuxt 工程、模板、发布流程、截图对比 | PR 到 `main`，等"合并" | `pnpm typecheck`、`pnpm build` 通过，视觉对比通过 |
| 4 | 目标机器一次性安装、首次发布、Nginx 接入 | 经跳板，逐步验证 | 首页、治疗页、预约表单、预览、保存即刷新、WordPress 站点不受影响 |
| 5 | 补文案补素材，换正式域名 | 后续 | 另行安排 |

第 1、2 步先于第 3 步："先在 CMS 里有字段，再发布读取它的代码"。

## 7. 换正式域名：如何不影响原域名 `overseasstudent.com`

原则：**所有 AURA 相关的东西都能一次性撤掉，撤完后 `overseasstudent.com` 的配置与改前完全一致**。为此接入时就做到：

1. **配置隔离**：对原站点文件的改动固定为两行（放行 `if … break` 与一行 `include`），都带统一标记注释 `# AURA-BEGIN` / `# AURA-END`；其余全部在我们自己的片段文件 `aura-institute.location.conf` 里。
2. **目录隔离**：容器、版本目录、环境文件、日志都在 `/home/aura-web`，不放进 `/data/sites/www.overseasstudent.com`（不碰 WordPress 目录）。
3. **不占共享资源**：不改 `nginx.conf` 全局、不新增证书、不改 WordPress 的缓存区与计划任务。

**切换步骤（顺序固定）**

| 步骤 | 做什么 | 目的 |
|---|---|---|
| 1 | 新域名准备：DNS 指向、证书（沿用 `certbot`）、`sites.d/<新域名>.conf` 新建，`location /` 转发到同一个容器；容器环境变量改 `NUXT_APP_BASE_URL=/`、`NUXT_PUBLIC_SITE_URL=https://<新域名>`、`NUXT_PUBLIC_DEPLOY_ENV=production`，放开收录 | 新域名先独立跑通，旧入口不动 |
| 2 | Vectra 侧登记新部署：`revalidate_targets` 加新地址与新签名密钥，`preview_bases` 与 `NUXT_PUBLIC_CMS_ORIGINS` 加新域名 | 保存即刷新、预览、实时编辑在新域名生效 |
| 3 | 新域名验收：首页、治疗页、预约表单（来源标记 `production`）、sitemap、robots、保存即刷新 | 通过后才动旧入口 |
| 4 | 旧入口过渡：`overseasstudent.com/aura-institute/` 改为 301 到新域名同路径，保留 30 天 | 已分享出去的测试链接不失效，也不再有内容留在原域名 |
| 5 | 过渡期满撤除：删除原站点文件里 `AURA-BEGIN…AURA-END` 两处，删除 `aura-institute.location.conf`，`nginx -t` 后平滑重载 | **原域名恢复到接入前的配置** |
| 6 | 清理与核对：旧部署从 Vectra 的 `revalidate_targets` 移除、系统凭据里旧部署密钥删除；`diff` 原站点文件与接入前备份应只剩无关的他人改动；用 `curl --resolve` 对比 WordPress 首页、`/wp-admin/`、静态资源状态码与响应头 | 证明原域名不受影响 |

**接入前必须做的基线**：备份原站点文件（带时间戳），并记录 WordPress 首页、`/wp-admin/`、一个静态资源、一个不存在路径的状态码与关键响应头，作为第 6 步的对照。

**回滚**：任意一步出问题，把步骤 1 之前备份的配置放回、`nginx -t`、平滑重载即可；AURA 容器停掉不影响任何其他站点。

**SEO 防污染**：子目录阶段全站 `noindex`，所以不会有旧域名的收录需要迁移；canonical 一律指向 `NUXT_PUBLIC_SITE_URL`（正式域名确定后再改），不在原域名上留任何指向它的 canonical。

## 8. 风险

1. 目标站点 Nginx 文件有人在改；每次修改前重新读取、备份，改动限于两行加一个片段。
2. 服务器级 `rewrite` 与正则 location 的优先级是最大的接入风险，靠 `if … break` 与 `^~` 解决，验证清单见第 5 节。
3. 目标机器与 Vectra 同在内网，但 uswoo.com 公网地址不通，所以接口地址必须用内网基址（已验证）。
4. 本仓库公开：仓库里不放地址、凭据、未公开客户信息；`deploy/` 只放脱敏记录。
5. 子目录阶段全站 `noindex`；上线正式域名前再按 `site/_redirects` 在 Nginx 配 301。
6. 测试与以后正式站共用同一份 CMS 内容。
