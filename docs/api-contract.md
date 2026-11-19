# AURA 接口与内容约定（后端、Vectra 前端、官网三方共用）

本文是三方并行开发的唯一接口依据。任何一方要改，先改本文再改代码。

## 1. 通用

- 响应信封：成功 `{"status":"success","data":…,"message":""}`；失败 `{"status":"error","message":"…","error_key":"…","code":<http>}`，HTTP 状态码与 `code` 一致。
- 双语文本 `L10n = {"en":"…","zh":"…"}`，`zh` 可为空串。官网英文站取 `en`，`zh` 为空时回退 `en`。
- 乐观锁：所有更新带 `updatedAt`（字符串，原样回传）；不一致返回 409，`error_key = "aura.conflict"`。
- 状态：`draft | published | offline`（页面只有 `draft | published`）。公开接口只返回 `published` 且未删除；页面未发布返回 503，`error_key = "aura.page_unpublished"`。
- 时间一律 ISO 8601 UTC 字符串。

错误 key 必须是「模块.原因」小写点分（见 Vectra 前端 `docs/standards/api-error-keys.md`），后端在 `resources/api_errors/keys.php` 注册，前端语言包同步。AURA 约定的 key：`aura.conflict`（409）、`aura.slug_taken`（409）、`aura.page_unpublished`（503）、`aura.not_found`（404）、`aura.lead_invalid`（422）、`aura.lead_rate_limited`（429）、`aura.category_in_use`（409）、`aura.media_in_use`（409）、`aura.unsupported_media`（415）。

## 2. 媒体引用与 Media 对象

存储里内容 JSON 用引用：`{"mediaId": 123, "focus": "50% 45%"}`（`focus` 可选，对应 CSS `object-position`）。
公开接口返回前，后端把所有 `mediaId` 引用替换为：

```json
{"id":123,"url":"https://cdn…/x.jpg","kind":"image","alt":{"en":"","zh":""},"width":1200,"height":800,"posterUrl":null,"focus":"50% 45%"}
```

找不到或已删除的媒体解析为 `null`。存储里没有图片的字段写作 `{"mediaId": null}`（管理端编辑器按这个形状识别图片字段）。`kind` 为 `image | video`；视频的 `posterUrl` 是海报图地址。
种子文件里用 `{"mediaKey":"thermage-hero.jpg","focus":"…"}`，导入脚本上传媒体后换成 `mediaId`。

## 3. 内容 JSON 的通用规则

- 任何内容 JSON 的文本叶子都是 `L10n`；列表是数组；每个区块是一个对象并带 `"show": true|false`（缺省视为 true；官网用 `on('区块键')` 判断）。
- 允许 HTML 的字段（官网用 `ch()` 输出）只允许这些标签：`em`、`b`、`strong`、`br`、`a[href]`、`span`、`ul`、`ol`、`li`、`p`，`&shy;` 实体保留。后端保存时做白名单清洗（参考 `UswooOfficialHtmlSanitizer`）。
- 内容 JSON 大小上限 512KB。后端对内容只做大小、JSON 合法性、HTML 清洗与媒体引用解析，**不校验字段结构**；字段结构由 `docs/content-schema.md` 约定，管理端用通用的结构化编辑器编辑。

### 治疗页内容结构 `treatment.content`

```
hero    {show, image:Media, kicker:L10n?, title:L10n(html), lede:L10n, chips:[L10n],
         bookbox:{show, label:L10n, options:[L10n], cta:L10n}, learnMore:L10n}
how     {show, eyebrow:L10n, title:L10n(html), intro:L10n(html), tagline:L10n?,
         cards:[{image:Media, title:L10n, text:L10n, zone:L10n?}], note:L10n?}
fit     {show, eyebrow:L10n, title:L10n(html), yes:{title:L10n, items:[L10n]}, no:{title:L10n, items:[L10n]},
         image:Media, pairNote:{label:L10n, html:L10n}?}
grid    {show, eyebrow:L10n, title:L10n(html), items:[{title:L10n, text:L10n}], foot:L10n(html)}   // 可选；用它时 fit.show=false（Gold Skin Analysis）
tech    {show, anchor:"tech"|"treatment", eyebrow:L10n, title:L10n(html), image:Media, steps:[{title:L10n, text:L10n(html)}]}
faq     {show, eyebrow:L10n, title:L10n(html), items:[{q:L10n, a:L10n(html)}]}
closing {show, image:Media, title:L10n(html), text:L10n, cta:L10n}
listing {blurb:L10n, price:L10n, tags:[L10n]}      // 预约抽屉与目标页行的小字
```

其他页面（首页、About、Membership、Facial Blueprint、Journal、目标页、`site`）的内容结构由 `docs/content-schema.md` 约定，该文件由种子抽取工具的作者维护。html 字段里的站内链接是不含子目录前缀的根相对路径，官网输出时补 `baseURL`。

## 4. 公开接口 `/aura/public/*`（匿名，GET 带短缓存头）

后端真实路径：`/portal_backend_v2/api/aura/public/*`。198 上同源反代：`/aura-institute/api/*` → 上述路径（只转发 GET 与 `POST leads`）。

| 方法与路径 | 返回 `data` |
|---|---|
| `GET /nav` | `{"categories":[{"key","name":L10n,"tag":L10n\|null,"link":{"type":"none"\|"page"\|"treatment","target":"…"}\|null,"groups":[{"name":L10n\|null,"treatments":[{"slug","name":L10n}]}]}]}`；只含已发布治疗，按 `sort`、`groupSort` 排序 |
| `GET /pages/{key}` | `{"key","content":{…},"seo":{"title":L10n,"description":L10n,"keywords":L10n,"ogImage":Media\|null,"noindex":bool},"updatedAt"}`；页面键见 §6 |
| `GET /treatments` | `[{"slug","name":L10n,"category":"key","group":L10n\|null,"summary":L10n,"card":Media\|null,"copyComplete":bool}]` |
| `GET /treatments/{slug}` | `{"slug","name","category":{"key","name":L10n},"group","summary","card","content":{…},"seo":{…},"copyComplete","updatedAt","related":[{"slug","name","card"}]}`；404 `aura.not_found` |
| `GET /goals` | `[{"slug","name":L10n,"summary":L10n,"card":Media\|null}]` |
| `GET /goals/{slug}` | `{"slug","name","summary","card","content":{…},"seo":{…},"treatments":[{"slug","name","summary","card"}],"updatedAt"}` |
| `GET /sitemap` | `{"pages":[{"key","updatedAt","noindex"}],"treatments":[{"slug","updatedAt","noindex"}],"goals":[{"slug","updatedAt"}]}` |
| `GET /preview/{entity}/{id}?exp=&sig=` | 与对应详情接口同形，但不要求已发布；签名机制照 `uswoo_official` 的预览（密钥取系统凭据 `internal.aura_preview_secret`）；`entity` ∈ `page|treatment|goal` |
| `POST /leads` | 见下 |

`noindex` 对治疗为：`copyComplete = false` 或 SEO 里手动设了 `noindex`。

**线索** `POST /leads` 请求体：

```json
{"name":"…","email":"…","phone":"","treatment":"thermage-flx","message":"","pageUrl":"/aura-institute/treatments/thermage-flx","env":"staging","website":"","startedAt":1760000000000}
```

`website` 是蜜罐，非空则静默丢弃（仍返回成功）；`startedAt` 是表单首次渲染的毫秒时间戳，距提交少于 3 秒按垃圾处理；同一 IP 10 分钟最多 5 条。成功 201：`{"id":123}`。错误：`aura.lead_invalid`（422）、`aura.lead_rate_limited`（429）。`env` 为 `staging` 时线索标记为测试。

## 5. 缓存刷新（Vectra 后端 → 官网）

`POST {站点}/_site/revalidate`（路径随 `baseURL` 带前缀），机制与 uswoo-website 的 `revalidate.post.ts` 完全一致（HMAC-SHA256 签名头、时间戳 5 分钟内有效，密钥为系统凭据 `internal.aura_revalidate_<部署名>`）。请求体 `{"tags":[…],"timestamp":<ms>}`，标签：

| 标签 | 官网清除的页面 |
|---|---|
| `page:{key}` | 对应页面（首页 `home` 时含 `/`） |
| `treatment:{slug}` | `/treatments/{slug}`，以及 `treatments`、`nav` 涉及的页面 |
| `treatments` | 所有治疗页与首页、目标页 |
| `goal:{slug}` / `goals` | 对应目标页 / 全部目标页与首页 |
| `nav`、`site` | 全站 |

## 6. 页面键

`site`（站点名称、logo、favicon、导航之外的全站内容、页脚、浮动 Book Now、搜索占位、`account.show`）、`home`、`about`、`membership`、`facial-blueprint`、`journal-faq`、`journal-botox-vs-xeomin`。

官网路由：`/`、`/about`、`/membership`、`/facial-blueprint`、`/journal/faq`、`/journal/botox-vs-xeomin`、`/goals/{slug}`、`/treatments/{slug}`。

## 7. 管理接口 `/aura/admin/*`（需登录，Vectra 前端使用）

列表统一返回 `{"items":[…],"total":N,"page":1,"pageSize":20}`，参数 `page`、`pageSize`、`q`。写接口幂等键沿用现有 `Idempotency-Key` 约定。

| 资源 | 接口 |
|---|---|
| 能力 | `GET /capabilities` → `{"permissions":{"admin":bool,"edit":bool,"publish":bool,"media":bool,"leads":bool},"pageKeys":[…],"statuses":[…],"leadStatuses":["new","contacted","closed","spam"],"siteOrigins":{"staging":"…","production":"…"}}` |
| 概览 | `GET /overview` → 各资源数量、未处理线索数、未完成文案的治疗数 |
| 页面 | `GET /pages`；`GET /pages/{key}`；`PUT /pages/{key}` `{content,seo,updatedAt}`；`POST /pages/{key}/transitions/{publish\|unpublish}`；`GET /pages/{key}/history`；`POST /pages/{key}/history/{historyId}/restore`；`POST /pages/{key}/preview-link` |
| 类别 | `GET /categories`；`POST /categories`；`PUT /categories/{id}`；`DELETE /categories/{id}`（有治疗时 409 `aura.category_in_use`）；`POST /categories/reorder` `{ids:[…]}` |
| 治疗 | `GET /treatments?categoryId&status&copyComplete`；`POST`；`GET /treatments/{id}`；`PUT /treatments/{id}`；`DELETE`（归档，可恢复）；`POST /treatments/{id}/transitions/{publish\|unpublish}`；`GET …/history`；`POST …/history/{historyId}/restore`；`POST …/preview-link`；`POST /treatments/reorder` `{items:[{id,sort,groupSort}]}` |
| 目标 | 与治疗同形；`PUT` 里带 `treatmentIds:[…]`（有序） |
| 媒体 | `GET /media?folderId&kind&q`；`POST /media`（multipart：`file`，可选 `folderId`、`poster`）；`PUT /media/{id}` `{name,alt,folderId,posterMediaId,updatedAt}`（视频的海报指向另一条图片媒体）；`POST /media/{id}/replace`（multipart `file`，编号与引用不变）；`DELETE /media/{id}`（被引用时 409 `aura.media_in_use`）；`GET /media/{id}/usage`；`GET/POST/PUT/DELETE /media/folders` |
| 线索 | `GET /leads?status&env`；`PUT /leads/{id}` `{status,note}` |

管理端实体字段：

- 治疗：`{id,slug,name:L10n,categoryId,group:L10n|null,groupSort,summary:L10n,cardMediaId,content,seo,copyComplete,status,sort,updatedAt,updatedByName}`；`seo` 为 `{title:L10n,description:L10n,keywords:L10n,ogMediaId,noindex}`。`slug` 创建后不可改（改会破坏链接）。
- 目标：`{id,slug,name,summary,cardMediaId,content,seo,treatmentIds,status,sort,updatedAt,…}`。
- 类别：`{id,key,name:L10n,tag:L10n|null,linkType:"none"|"page"|"treatment",linkTarget,sort,isOnline}`。
- 页面：`{key,content,seo,status,updatedAt,updatedByName}`。
- 媒体：`{id,url,thumbUrl,kind,name,alt:L10n,width,height,sizeBytes,mime,folderId,posterMediaId,createdAt,updatedAt}`。
- 线索：`{id,name,email,phone,treatmentSlug,message,pageUrl,env,status,note,createdAt,updatedAt}`。
- 管理端读取内容时 `mediaId` 引用**保持原样**（不解析），另附 `mediaIndex:{"<id>":Media}` 供编辑器显示缩略图。

## 8. 权限键

`aura_admin`（全局，含全部；与 TBTS 一样，显式授予的 `all` 同样放行，`superAdmin` 不放行）、`aura_edit`（内容读写）、`aura_publish`（发布与下线）、`aura_media`（媒体上传、替换、删除）、`aura_leads`（线索处理）。接入方式照 `uswoo_official_*`：后端 `AuraAccess`、前端 `access.ts`、超级管理员「CMS管理权限」面板新增网站"AURA Institute"。

## 9. 种子文件 `seed/aura-seed.json`

```json
{"categories":[…管理端字段，无 id…],
 "treatments":[{…管理端字段，无 id；categoryKey 代替 categoryId；cardMedia 为 {"mediaKey":…}；content 内图片用 mediaKey}],
 "goals":[{…；treatmentSlugs 代替 treatmentIds}],
 "pages":{"home":{content,seo}, …},
 "media":[{"key":"thermage-hero.jpg","alt":{"en":"…","zh":""},"name":"…"}],
 "mediaDir":"legacy/site"}
```

`media` 数组按文件名给出每个媒体的中英文 alt（同一文件在多处使用时取第一处），导入时写入媒体库的 alt。导入脚本 `bin/aura_seed_import.php --file=… --media-dir=… [--apply]`：默认只读（只打印将创建/更新什么）；`--apply` 才写入；按 `slug` / `key` / 文件名 SHA-256 去重，可重复执行；内容已被人工改过（`updated_by` 非空）的行默认跳过，`--force-content` 才覆盖。

## 10. 实时预览协议（Vectra 编辑器 ↔ 官网）

与 uswoo 新官网同一套，`window.postMessage`，官网只在被内嵌、网址带 `?cms-edit`、上层来源在 `NUXT_PUBLIC_CMS_ORIGINS` 里时启用。

- `capabilities.siteOrigins` 是**站点根地址（含子目录前缀）**，如 `https://overseasstudent.com/aura-institute`；消息的 `targetOrigin` 取其 `origin`。
- 预览地址 = 站点根地址 + 路由路径 + `?cms-edit`。路由路径：页面键 `home`→`/`，`about`→`/about`，`membership`→`/membership`，`facial-blueprint`→`/facial-blueprint`，`journal-faq`→`/journal/faq`，`journal-botox-vs-xeomin`→`/journal/botox-vs-xeomin`；治疗→`/treatments/{slug}`；目标→`/goals/{slug}`。`site` 页面用首页预览。
- 编辑器 → 官网：`{source:"uswoo-cms", type:"content", key, payload}`、`{source:"uswoo-cms", type:"focus", ref}`。官网 → 编辑器：`{source:"uswoo-site", type:"ready", path}`、`{source:"uswoo-site", type:"select", ref}`。
- 内容键 `key`：页面用页面键；治疗 `treatment/{slug}`；目标 `goal/{slug}`。`ref = "{key}:{字段路径}"`，字段路径用 `.` 连接（列表下标是数字，如 `how.cards.0.title`），按**第一个冒号**切分。
- `payload` 是**已解析媒体**的内容 JSON：编辑器先把所有 `{mediaId, focus}` 替换为 §2 的 Media 对象（用管理端的 `mediaIndex`），再发给官网；官网用它盖掉接口返回的该键内容。治疗与目标只发 `content`，名称、摘要等不在其中。

## 11. 后端实现说明（后端分支补充，2026-11-18；与上文不一致处以本节为准）

**响应与错误**
- Vectra 的统一出口会**删掉所有值为 `null` 的字段**（含嵌套）。所以文中标 `|null` 的字段（`card`、`group`、`tag`、`link`、`ogImage`、`posterUrl`、`focus`、`cardMediaId`、`publishedAt`、线索的 `phone` 空串除外）为空时**整个字段不出现**，官网与编辑器一律按「缺省 = null」处理。内容数组里被解析成 `null` 的元素（媒体已删除）也会被删掉，后面的元素会前移；所以内容里**不要用下标定位图片列表之外的东西**。
- 失败响应的 `code` 等于 HTTP 状态码；`error_key` 见 §1 的 key 之外再加：`aura.forbidden`（403，无权进入）、`aura.permission_forbidden`（403，进入但无此操作权限）、`aura.validation_detail`（400，`{detail}`）、`aura.idempotency_key_required`（400）、`aura.media_too_large`（413）、`aura.media_duplicate`（409）、`aura.folder_not_empty`（409）、`aura.upload_failed`（502）、`aura.preview_unavailable`（400）。`aura.lead_invalid` 的译文带 `{detail}`。
- 所有**写**请求（POST/PUT/DELETE，含 multipart）必须带 `Idempotency-Key` 请求头（16–100 位，`[A-Za-z0-9_-]`），否则 400。DELETE 与归档成功返回 `data: []`。
- 管理端 `updatedAt` 是**原样的数据库时间字符串**（形如 `2026-11-18 10:00:00.123`，用作乐观锁令牌，不要解析、不要改格式）；公开接口与管理端的 `createdAt` / `publishedAt` 是 ISO 8601。

**公开接口**
- `GET /pages/{key}`：未发布或还没建过 → 503 `aura.page_unpublished`；页面键不在 §6 里 → 404 `aura.not_found`。
- `GET /preview/{entity}/{id}?exp=<unix秒>&sig=<十六进制>`：`sig = HMAC-SHA256("{entity}:{id}:{exp}", aura_preview_secret)`；`page` 的 `id` 是页面行的数字 id（见预览链接）。签名无效、过期、内容不存在一律 404 `aura.not_found`。响应带 `Cache-Control: no-store` 与 `X-Robots-Tag: noindex, nofollow`。
- `POST /leads` 成功 201 `{id}`；蜜罐非空 → 201 `{id: 0}`（没落库）；`startedAt` 距提交不足 3 秒 → 落库为 `status: spam`（仍返回 201，不通知）；限流先于落库判断。`phone` 只允许数字与 `+()-.` 和空格。
- 缓存头：除站点地图（300 秒）外，GET 为 `public, max-age=30, stale-while-revalidate=120`。

**刷新通知（§5）**：签名头名与美窝新官网一致，是 **`X-USWOO-Revalidate-Signature`**（对原始请求体的 HMAC-SHA256，十六进制）；官网一侧直接复用 uswoo-website 的 `revalidate.post.ts`（只把读取的环境变量名保持为 `NUXT_REVALIDATE_SECRET`）。发布与**下线**、归档、媒体替换、媒体 alt 变化都会通知。治疗的标签一律是 `treatment:{slug}`、`treatments`、`nav`；类别变更是 `nav`、`treatments`；页面 `site` 同时发 `site`。

**管理接口细节**
- 能力 `GET /capabilities`（不要求有权限）返回 §7 的字段，另加 `canEnter`、`pageStatuses`、`linkTypes`、`mediaKinds`、`previewReady`、`previewEnvs`；`siteOrigins` 是对象 `{env: 站点根地址}`。
- 页面 `GET /pages/{key}`：页面还没建过时返回 `exists: false`、空 `content`、`updatedAt: ""`，第一次 `PUT`（不带 `updatedAt`）才建行。`GET /pages` 返回 `{items:[{key, exists, status, updatedByName, updatedAt}]}`。
- 预览链接 `POST …/preview-link` 返回 `{links:{<env>: "<站点根地址>/_site/preview/<entity>/<id>?exp=…&sig=…">}, expiresAt}`；官网的预览路由是 `/_site/preview/[entity]/[id]`（`entity` ∈ `page|treatment|goal`）。有效期 30 分钟。
- 治疗 / 目标：`transitions/publish` 要求 `aura_publish` 且发布前有「英文名称、类别、内容」；`transitions/unpublish` 把状态置为 `offline`；`DELETE` 是归档（slug 仍被占用），已发布的内容归档要 `aura_publish`；`slug` 与类别 `key` 创建后不可改（传不同值 → 400）。目标页另有 `POST /goals/reorder {items:[{id,sort}]}`。列表项带 `card`（Media）用于缩略图，不带 `content`。
- 类别：`POST /categories/reorder {ids:[…]}` 按顺序把 `sort` 设为 10、20、30…；`PUT` 与 `DELETE` 需带 `updatedAt`。
- 媒体：`GET /media?folderId=<数字|root>&kind=&q=&page=&pageSize=`（`root` 只看没进文件夹的）；`POST /media` 的 multipart 字段 `file`、可选 `poster`（视频海报图）、`folderId`、`name`、`altEn`/`altZh`（或 `alt` 对象）、`width`/`height`（视频，后端不解析视频尺寸）、`posterMediaId`；内容已在库里时复用那条（响应带 `created: false`）；`POST /media/{id}/replace` 的 multipart 字段 `file` 与 `updatedAt`，类型必须与原来一致；`PUT /media/{id}` 可改 `name`、`alt`、`folderId`、`posterMediaId`；`GET /media/{id}/usage` 返回 `{items:[{type:page|treatment|goal|media, id, key, name, field}], referenceCount}`；`thumbUrl` 对图片就是原图地址，对视频是海报地址。文件夹：`{name, parentId?, sort?, updatedAt}`，只能删空文件夹。
- 权限分层：任何 AURA 权限都能进入后台、读内容、浏览媒体库；改名 / alt / 移动 / 文件夹维护要 `aura_media` 或 `aura_edit`；上传、替换、删除要 `aura_media`；**预约线索只有 `aura_leads` 能读与处理**（`/overview` 里的线索数量对其他人省略）。
- 线索 `status` 取值 `new | contacted | closed | spam`；`env` 取 `production | staging`；`GET /leads?status=&env=&q=`。

