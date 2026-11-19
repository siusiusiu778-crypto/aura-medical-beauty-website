# AURA 部署记录（脱敏）

目标：`https://aurainstitute.com`（正式站，2026-11-19 上线；`www.` 跳转到裸域）。此前的测试地址 `<原域名>/aura-institute/` 已撤除，原域名配置已还原。本目录是变更记录与脚本模板，**不是部署源**；真实地址、主机名、目录、密钥只在服务器上。公开仓库，不得写入任何内网地址、凭据或未公开的客户信息。

| 文件 | 对应服务器上的 | 说明 |
|---|---|---|
| `../staging/pull-release.sh`（见 `deploy/staging/`） | `<目录>/bin/pull-release.sh`，root 计划任务每分钟一次 | 拉取式发布：读 Release「staging」→ 校验 → 备用端口试启动 → 切换 → 写 `status.json` |
| `aurainstitute.com.conf` | `<nginx 目录>/sites.d/aurainstitute.com.conf` | 正式域名站点：80 验证与跳转、443（www 跳转、同源接口反代 `/api/`、应用转发） |
| `overseasstudent.com.patch.md` | （已撤除）原站点文件里 `AURA-BEGIN…AURA-END` 四行 | 测试阶段的接入、撤除、基线核对规程，留作记录 |
| `wp-baseline.sh` | 临时运行 | 接入前后对比原站点的状态码与响应头 |

## 一次性安装顺序（经跳板，之后日常发布不再需要）

1. 建目录 `<目录>`（`/home/aura-web`）及 `releases/`、`status/`、`logs/`、`bin/`；安装 `pull-release.sh`（root，755）。
2. 写环境文件 `<目录>/aura.env`（root，600，不进仓库），键如下（值只在服务器上）：

   | 键 | 作用 |
   |---|---|
   | `NUXT_APP_BASE_URL` | 根路径部署为 `/`（构建与运行必须一致） |
   | `NUXT_PUBLIC_SITE_URL` | 站点的对外根地址，用于 canonical、站点地图 |
   | `NUXT_PUBLIC_DEPLOY_ENV` | `staging`（不收录、表单标记测试）/ `production` |
   | `NUXT_PUBLIC_API_BASE` | 浏览器端接口基址，同源：`/api` |
   | `NUXT_API_BASE_SERVER` | 服务端渲染直连 Vectra：`http://<Vectra 内网地址>:9924/portal_backend_v2/api/aura/public` |
   | `NUXT_API_HOST_HEADER` | 直连时带的 `Host`：`<Vectra 后端主机名>` |
   | `NUXT_REVALIDATE_SECRET` | 与 Vectra 系统凭据 `internal.aura_revalidate_<部署名>` 同值 |
   | `NUXT_PREVIEW_SECRET` | 与 Vectra 系统凭据 `internal.aura_preview_secret` 同值 |
   | `NUXT_PUBLIC_CMS_ORIGINS` | 允许内嵌预览的 Vectra 网址（逗号分隔） |
   | `NUXT_STATUS_FILE` | `/status/status.json`（容器内只读挂载） |

3. 接入 Nginx：新建 `sites.d/aurainstitute.com.conf`（先只放 80 端口块，用 certbot webroot 签证书，再追加 443 块），`nginx -t` 通过后平滑重载。
4. 计划任务：`* * * * * <目录>/bin/pull-release.sh <目录> >/dev/null 2>&1`；第一次合并 `main` 后约 1 分钟内应出现第一个版本。
5. Vectra 侧登记：`revalidate_targets` 加 `https://<域名>/_site/revalidate`；系统凭据「内部密钥」加对应两个密钥。

## 端口与目录约定

- 应用容器 `aura-institute`：`127.0.0.1:3500`；试启动 `aura-institute-try`：`127.0.0.1:3501`。机器上已有的 Nuxt 容器占用 3300，不要冲突。
- 版本目录只读挂载为容器内 `/app`；`<目录>/status` 只读挂载为 `/status`。
- Docker 镜像 `node:22-alpine`（机器上已有）。

## 不要做的事

- 不改原站点文件里 AURA 四行以外的任何内容，不改 `nginx.conf`，不改 WordPress 目录与证书。
- 不把 `aura.env`、密钥或真实地址提交进仓库。
- 发布失败时旧版本继续运行；排查看 `<目录>/logs/pull.log` 与 `status/status.json`。
