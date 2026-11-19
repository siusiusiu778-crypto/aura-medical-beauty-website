# AURA Institute 官网 — 给 Claude 的项目说明

Nuxt 4 + Vue 3（SSR、TypeScript 严格模式、pnpm、Node 22）。这是**公开仓库**：不要提交服务器地址、内网地址、凭据、未公开的客户信息。

接口与内容约定见 `docs/api-contract.md`、`docs/content-schema.md`；整体方案见 `docs/refactor-plan.md`。

## 最重要的一条规则：代码里不放内容

访客看到的所有文案、图片、数字、SEO 标题都来自 CMS（Vectra →「AURA」菜单），**代码里不允许写默认文案或默认图片**。

```ts
const ctx = await usePageContent("about");            // 页面键见 docs/api-contract.md §6
const { c, ch, img, alt, focus, raw, list, on } = ctx;
c("hero.eyebrow")      // 纯文字（en，缺了回退 zh）
ch("hero.title")       // 给 v-html 用：转义后只还原白名单标记（em b strong br a span ul ol li p、实体）
img("hero.image")      // 图片地址（媒体库引用解析后的 url）
alt("hero.image")      // 媒体库里填的替代文字
focus("hero.image")    // CSS object-position
raw<string>("x.y")     // 其他原始值（链接、slug、数字）
list("how.cards")      // 列表下标，配合 v-for
on("how")              // 区块是否展示（how.show 不为 false）
```

治疗页、目标页用 `useTreatment(slug)`、`useGoal(slug)`，读取方式相同。全站内容（页脚、站点名称、预约抽屉文案）用 `await useSite()`，导航用 `useNav()`。

- **每个区块都要能在 CMS 里隐藏**：每个 `<section>` 写成 `<section v-if="on('区块键')">`，并容忍区块或字段缺失。
- **CMS 实时预览依赖这些函数**：编辑器把官网内嵌进去预览时，`c()` / `ch()` 返回的文字末尾带不可见标记、`img()` 的地址带 `#cms=` 片段，点页面内容才能定位字段（见 `app/composables/useCmsEdit.ts`）。所以页面上的文字和图片一定要经过这几个函数直接输出；**不要拿返回值做相等比较、当 `key`、拼进别的地址**，需要原始值用 `raw()`。预览通道的消息标识沿用美窝新官网（`uswoo-cms` / `uswoo-site`），以便 Vectra 编辑器复用同一套实现。
- `useContentDeps()` 必须在页面 setup 里、第一个 `await` 之前调用（之后拿不到 Nuxt 上下文）；`useTreatment` / `useGoal` / `usePageContent` 已经做了。
- 需要新的文字或图片时：**先**在 CMS 里加字段并填好，**再**发布读取它的代码。字段没填时页面上是空的，不会有兜底。
- 只有功能性界面文字留在代码里：表单校验与提交状态、无障碍标签、面包屑的 "Home"、"Learn More" 这类固定标签。写法是 `tx("English")`（首发只有英文站，`tx` 原样返回；以后开 `/zh` 时在这里接词典）。拿不准算内容还是界面文字时，按内容处理，放进 CMS。
- **预约**：所有 Book 按钮调用 `useBooking().open({ preset?, text?, slug? })`，抽屉（`BookDrawer`）在 `app.vue` 里挂一次，提交到 `POST /leads`。内容里不存预约地址。
- **客户评价**：`sample: true` 的评价一律不输出（美国 FTC 规定不得把示意评价当真实评价发布）。
- 脸部比例图（`facial-blueprint`）的 SVG 点线是代码资产，在 `app/assets/fragments/`，动画逻辑在 `BlueprintView.vue`。

## 子目录与站内链接

- 部署在子目录（例如 `/aura-institute/`），由 `NUXT_APP_BASE_URL` 决定，构建和运行都要设置。**所有站内链接用 `NuxtLink`**，不写死 `/`；内容里的 html 链接写成不含前缀的根相对路径（`/treatments/xxx`），`ch()` 输出时统一补前缀。
- 换正式域名：改环境变量与 Nginx，不改代码。见 `docs/refactor-plan.md` 第 7 节。

## 样式

- 原型的 CSS 由 `pnpm scope-css` 从 `legacy/site/` 生成到 `app/assets/css/`：每个页面类型限定在 `.pg-<页面>` 下（页面类型在各页面里用 `definePageMeta({ pg })` 声明，`app.vue` 把它放到根元素上），导航与页脚在 `chrome.css`，预约抽屉在 `drawer.css`。**生成物不要手改**；补充样式写在 `chrome.extra.css`（全站）。
- 删除 `legacy/` 之后 `scope-css` 不能再运行，生成物就成了唯一来源，到那时可以直接手改。

## 服务端

- 数据只读公开接口 `/aura/public/*`，用 `useApi()`；类型在 `shared/types/api.ts`，跟着后端的实际返回走，不要单方面修改，接口变化先改 `docs/api-contract.md`。
- 服务端渲染直连 Vectra 内网（`NUXT_API_BASE_SERVER` + `NUXT_API_HOST_HEADER`），浏览器端走同源反代 `NUXT_PUBLIC_API_BASE`。
- `/_site/revalidate`：Vectra 保存内容后签名通知，清空页面缓存；`/_site/preview/{entity}/{id}`：草稿预览（不缓存、noindex）。
- 页面输出不能包含访客相关内容（整页会被缓存，`swr: 600`）。

## 本地开发

```bash
pnpm install
```

没有后端时用 mock（读 `seed/aura-seed.json`，图片读 `legacy/site/`）：

```bash
pnpm dev:mock
```

提交前：`pnpm typecheck` 和 `pnpm build` 都要通过。

注释用简体中文，说明"为什么"。
