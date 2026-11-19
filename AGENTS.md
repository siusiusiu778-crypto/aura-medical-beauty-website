# AURA Institute 官网 — 前端开发指引（给 AI Agent 与前端同事）

Nuxt 4 + Vue 3（SSR、TypeScript 严格模式、pnpm、Node 22）。**公开仓库**：不要提交服务器地址、内网地址、凭据、未公开的客户信息。

你是**只负责前端**的开发者。你可以放手改页面的版式、样式、交互和内容呈现；后端、服务器、CMS 数据结构由负责人处理。下面说清楚哪些能做、哪些不能做、怎么交接。

## 和美窝新官网的规则不同：现在允许写死内容

美窝新官网要求"代码里不放内容"。**AURA 不这样要求**：

- 你调整或新增一个模块时，可以**直接把文案、图片、数字、链接写死在页面或组件里**，不必先去 CMS 建字段，也不必等后端。
- 把写死的内容**迁进 CMS（后端出数据）由负责人来做**，你不需要考虑、也不需要等。
- 想怎么做版式、动效、交互、新模块都可以，不用为了"可配置"而把代码写复杂。

唯一要做的交接动作：**给写死的内容留标记**（见下节），负责人才能找得到、迁得走。

## 写死内容的约定

1. **标记**：每处写死的内容旁边写一行注释，格式固定，方便全局搜索：
   - Vue 模板：`<!-- CMS-TODO(区块名): 一句话说明，例如 首页 Journal 三张卡片的标题和图片 -->`
   - TS/JS：`// CMS-TODO(区块名): …`
   - 一个模块里内容很多时，在模块开头标一处即可，写清楚包含哪些字段。
   - 负责人用 `grep -rn "CMS-TODO" app` 汇总待迁移清单。
2. **图片**：放在 `app/assets/img/<模块名>/`，在模板里用 `~/assets/img/...` 引用（构建时生成带哈希的文件，路径前缀由运行时的子目录设置自动补上，换域名不会坏；小于约 4KB 的图会被直接内联）。
   - 不要放进 `public/`（那里的路径不会自动带子目录前缀）。
   - 压缩后再提交：宽度不超过 2000px、单张尽量 300KB 以内，优先 `.webp` 或 `.jpg`；视频不要进仓库，把地址告诉负责人上传到媒体库。
   - 必须写 `alt`；纯装饰图写空 `alt=""`。
   - 图片需要有使用授权；**不要提交真实客户的术前术后照片**，除非负责人确认过书面同意。
3. **文案**：写英文（站点目前只有英文）；医美功效、价格、时长、"FDA 批准"这类表述**不要凭空编写**，没有依据时先留占位并标 `CMS-TODO` 告诉负责人，不要写成事实。
4. **新增页面**：放在 `app/pages/`，在页面里用 `definePageMeta({ pg: '页面名' })` 声明样式作用域；SEO 调用一次 `usePageSeo()`。新页面没有 CMS 数据时，标题和描述也写死并标 `CMS-TODO`。
5. **站内链接**一律用 `NuxtLink`，不写死 `/`（站点部署在子目录，换正式域名时前缀会变）。

## 已经由 CMS 驱动的页面和模块：改版式可以，别拆掉数据绑定

现有的首页、About、Membership、Facial Blueprint、Journal、目标页、治疗页，**文字和图片是从 CMS 读的**（页面里通过 `usePageContent` / `useTreatment` / `useGoal` / `useSite` 取数）。改这些页面时：

- 改版式、样式、动效、区块顺序都可以。
- **不要把已经接了 CMS 的文字、图片改成写死**——那样运营在 CMS 里改的内容就不生效了。
- 要在这类页面里**加一块新内容**：直接写死并标 `CMS-TODO` 即可，不需要先动 CMS。
- 要在 CMS 驱动的区块里**加一个新字段**：同样先写死并标 `CMS-TODO`，说明想要的字段名，由负责人加进 CMS 和后端后再把代码改成读 CMS。

读取 CMS 的写法（改版式时会用到）：

```ts
const ctx = await usePageContent("about");            // 页面键：site、home、about、membership、facial-blueprint、journal-faq、journal-botox-vs-xeomin
const { c, ch, img, alt, focus, raw, list, on } = ctx;
c("hero.eyebrow")      // 纯文字
ch("hero.title")       // 给 v-html 用，只保留白名单标记（em b strong br a span ul ol li p）
img("hero.image")      // 图片地址
alt("hero.image")      // 替代文字
focus("hero.image")    // CSS object-position
raw<string>("x.y")     // 链接、slug、数字等原始值
list("how.cards")      // 列表，配合 v-for
on("how")              // 区块是否展示（CMS 里 how.show 不为 false）
```

治疗页、目标页用 `useTreatment(slug)`、`useGoal(slug)`，全站内容用 `await useSite()`，导航用 `useNav()`。

**CMS 实时预览依赖这些函数**：`c()` / `ch()` 返回的文字末尾带不可见标记，`img()` 的地址带 `#cms=` 片段，CMS 编辑器点页面内容才能定位字段。所以经过它们输出的文字和图片，**不要拿返回值做相等比较、当 `key`、拼进别的地址**；需要原始值用 `raw()`。`<section>` 写成 `<section v-if="on('区块键')">` 并容忍字段缺失。

字段结构见 `docs/content-schema.md`，接口见 `docs/api-contract.md`，**这两份文件不要单方面修改**，需要变化时告诉负责人。

## 不要做的事

- 不要登录服务器，不要改服务器配置、Nginx、证书、计划任务。
- 不要改接口与后端；`server/` 下的服务端路由、`shared/types/api.ts`、`deploy/`、`.github/workflows/` 不要改，除非负责人同意。
- 不要自己合并 PR 或改发布流程；域名、证书、Nginx 由负责人管理（见 `docs/refactor-plan.md`）。
- 不要把密钥、`.env`、服务器地址、内网地址写进代码或文档。提交前自查：`git diff | grep -nE 'sk-|ghp_|AKIA|BEGIN [A-Z ]*PRIVATE KEY|172\.|192\.168'`。
- 不要在页面输出里放访客相关的内容（整页会被缓存 10 分钟）。
- 不要手改 `app/assets/css/` 里由 `pnpm scope-css` 生成的文件（`legacy/` 删除前）；补充样式写在同目录的 `*.extra.css` 里；新模块的样式可以新建自己的 CSS 文件或在组件里写 `<style>`，选择器限定在 `.pg-<页面>` 下。

## 目录

```
app/pages/        路由页面            app/components/   组件（views/ 里是各页面的主体）
app/composables/  取数与通用逻辑      app/assets/css/   样式    app/assets/img/  写死的图片
server/           服务端路由（别改）   shared/types/     接口类型（别改）
seed/ tools/      初始内容与抽取脚本   docs/             方案、接口、内容结构
legacy/           原静态原型（验收后删除）
```

## 本地开发

```bash
pnpm install
```

后端没接时用 mock（读 `seed/aura-seed.json`，图片读 `legacy/site/`）：

```bash
pnpm dev:mock
```

写完提交前，这两个都要通过：

```bash
pnpm typecheck
```

```bash
pnpm build
```

服务端渲染要求：`window`、`document` 只能在 `onMounted` 里用；新写的交互组件在服务端渲染时不能报错。

## 提交与发布

改动走分支和 PR，不要直接推 `main`：

```bash
git switch -c <分支名>
```

```bash
git add <改动的文件>
```

```bash
git commit -m "<一句话说清楚改了什么>"
```

```bash
git push -u origin <分支名>
```

```bash
gh pr create --fill
```

- PR 上会自动跑「check」（类型检查 + 构建），通过后由负责人合并。**用户说"发布""部署"时，按 `.claude/skills/deploy/SKILL.md` 做。**
- 合并到 `main` 会自动构建并**发布到正式站** `https://aurainstitute.com`，所以合并要谨慎；发布成功后可看 `https://aurainstitute.com/_deploy/status.json`。
- 发布失败时旧版本继续运行，不受影响；看 Actions 日志修复后重新合并。

注释用简体中文，说明"为什么"。

## 给负责人：把写死内容迁进 CMS

1. `grep -rn "CMS-TODO" app` 得到清单。
2. 在 `docs/content-schema.md` 里为该区块定义字段，后端加字段与种子，Vectra 前端编辑器登记。
3. 先在 CMS 里填好内容，再把代码从写死改成 `c()` / `img()` 读取，并删除 `CMS-TODO` 标记与 `app/assets/img/` 里已迁走的图片。
