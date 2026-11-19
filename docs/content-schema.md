# AURA 内容结构（除治疗页主体以外的所有页面）

配合 `docs/api-contract.md`。治疗页 `treatment.content` 的结构在契约 §3，本文末尾"治疗页补充"列出对它的扩展。种子由 `tools/aura-extract.mjs` 从原型抽取，字段名以本文为准；官网、管理端、后端不得自造字段。

## 0. 通用约定

- 文本叶子都是 `L10n = {"en":"…","zh":""}`；下文写 `L10n` 即此类型，`L10n(html)` 表示允许契约 §3 里的白名单标签。
- 媒体引用写成 `Media`：存储里是 `{"mediaId":N,"focus":"50% 45%"}`（种子里是 `{"mediaKey":"x.jpg","focus":"…"}`），公开接口返回时被替换成契约 §2 的 Media 对象。图片的 alt 在媒体库里（每个文件一份中英文 alt），内容里不再写 alt。
- 区块：每个区块对象带 `show`（缺省 true）。区块隐藏时官网整段不输出。官网必须容忍区块或字段缺失，不报错。
- 多行标题写成 `<br>` 分隔的 html（例：`Natural beauty,<br><em>refined.</em>`），官网把每一行包成一个 `ln` 动画行。标题里强调词用 `<em>`。
- **内部链接**：html 字段里的站内链接一律是不含子目录前缀的根相对路径（`/treatments/under-eye-hollows`、`/goals/facial-balancing`、`/about#who`），官网输出时统一补上 `baseURL`。外链保持完整地址。非链接用的 `#` 在种子里已被去掉。
- **预约动作**：原型里所有 `home.html#book` / `home.html?tx=…#book` 都是"打开预约抽屉"。内容里不存地址，只存按钮文字；需要预选项目的按钮带 `bookPreset`（字符串）：`"consultation"`（免费咨询）、`"aura-prime"`、或某个治疗的 `slug`。没有 `bookPreset` 即不预选。
- 站内页面路由表（官网路由 ↔ 原型文件）：`/`↔home；`/about`↔about；`/membership`↔aura-prime；`/facial-blueprint`；`/journal/faq`↔journal-faq；`/journal/botox-vs-xeomin`；`/goals/{slug}`↔`goal-{slug}`（slug：`skin-tightening`、`facial-balancing`、`wrinkles-jawline`、`facials-pores`、`glow-hydration`、`body-wellness`）；`/treatments/{slug}`↔原文件名。
- 原型顶部的 "Page prototype · …" 横幅、`[Copy to come]`、`[XXX-XXXX]`、`[Author]`、`[date]` 这类占位**不得出现在官网**。抽取时已把含方括号占位的字段置为空串并隐藏对应条目。

## 1. `site`（全站）

```
brand      {name:L10n, by:L10n, tagline:L10n}                 // AURA INSTITUTE / by sxy / Unveil Your Aura.
header     {searchPlaceholder:L10n, searchLabel:L10n, account:{show:false, label:L10n},
            bookLabel:L10n, mobileBookLabel:L10n, menuLabel:L10n}
nav        {dropdowns:{about:[{label:L10n, path:string}], membership:[{label:L10n, path:string}]}}
           // 类别本身、分组、治疗来自 /nav；Facial Blueprint / Membership / About 在 /nav 里是 link.type="page" 的类别；
           // 这里只补它们的下拉小菜单（About 的四个锚点、Membership 的 AURA Prime）。key 与 /nav 的类别 key 一致。
footer     {show, location:{title:L10n, lines:[L10n], mapUrl:string},
            hours:{title:L10n, lines:[L10n]},
            contact:{title:L10n, phone:{show, label:L10n, href:string}, email:{show, label:L10n, href:string},
                     instagram:{show, label:L10n, href:string}},
            legal:{text:L10n, links:[{label:L10n, href:string}]}}   // href 为空 = 只显示文字不做链接
floatBook  {show, label:L10n}                                   // 手机上的悬浮 Book Now
booking    见 §1.1
```

`phone`、`email` 在原型里是 `[XXX-XXXX]` 占位，种子里 `show=false`、文字为空，等运营在 CMS 填写后再打开。

### 1.1 `site.booking`（预约抽屉的文案；功能性文字如校验错误留在代码里用 `tx()`）

```
title        L10n                      // Book your visit
stepLabels   [L10n]×4                  // Choose a treatment / Pick a time / Your details / Review
consult      {title:L10n, text:L10n}   // 免费咨询卡片
searchPlaceholder L10n
viewAll      L10n
menu         [{title:L10n, items:[{treatmentSlug:string|null, title:L10n, blurb:L10n, price:L10n}]}]
times        [string]                  // 可选时间点，如 "9:00"
locationNote L10n
consentLabel L10n(html)
intakeNote   L10n
submitLabel  L10n                      // Request Appointment
done         {eyebrow:L10n, title:L10n, text:L10n}   // text 可用占位 {treatment} {date} {time}；title 可用 {firstName}
```

预约抽屉只提交线索（`POST /leads`），日期与时间并入 `message`（如 `Preferred: Tue, Nov 25 · 10:30`），不含任何"已预订"表述。

## 2. `home`

```
hero     {show, images:[Media, Media], eyebrow:L10n, title:L10n(html), lede:L10n, cta:{label:L10n}}
results  {show, eyebrow:L10n, title:L10n(html),
          items:[{goal:"skin-tightening"|…, name:L10n, image:Media, bullets:[L10n]}]}      // 6 张目标卡片，点击进 /goals/{goal}
season   {show, badge:L10n, image:Media, label:L10n, title:L10n(html),
          main:{title:L10n, text:L10n}, facts:[{label:L10n, value:L10n}], note:L10n, cta:{label:L10n}}
stars    {show, label:L10n, title:L10n(html), items:[{treatment:slug, image:Media, name:L10n, effect:L10n}]}   // Most loved，6 项
about    {show, image:Media, label:L10n, title:L10n(html), text:L10n, link:{label:L10n, path:"/about"}, values:[L10n]}
experience {show, label:L10n, title:L10n(html), steps:[{title:L10n, text:L10n}], cta:{label:L10n, bookPreset:"consultation"}}
```

区块序号、交替底色由代码按 `show` 计算，不放进内容。`season`（假日专题）是时效内容，运营下线时把 `season.show` 设为 false。

## 3. `about`

```
hero     {show, image:Media, eyebrow:L10n, title:L10n(html), lede:L10n, cta:{label:L10n}}
intro    {show, eyebrow:L10n, text:L10n(html)}
who      {show, eyebrow:L10n, title:L10n(html), text:L10n, image:Media}                 // 锚点 #who
standards {show, eyebrow:L10n, title:L10n(html), items:[{title:L10n, text:L10n}]}       // 锚点 #standards，6 项，序号由代码生成
technology {show, eyebrow:L10n, title:L10n(html), text:L10n, image:Media,
            table:{head:[L10n, L10n], rows:[[L10n, L10n]]}, note:L10n}                 // 锚点 #technology
aesthetic {show, eyebrow:L10n, title:L10n(html), text:L10n, link:{label:L10n, path:"/facial-blueprint"},
           images:[Media, Media, Media], quote:L10n}                                   // 锚点 #aesthetic
closing  {show, image:Media, title:L10n(html), text:L10n, cta:{label:L10n}}
```

## 4. `membership`（AURA Prime）

```
hero     {show, image:Media, tag:{kicker:L10n, line:L10n}, titleLines:[L10n, L10n(html)],   // "AURA" / "<em>Prime</em>"
          kicker:L10n, tagline:L10n(html), join:{label:L10n, bookPreset:"aura-prime"},
          talk:{lead:L10n, linkLabel:L10n}, lede:L10n,
          price:{amount:L10n, unit:L10n, note:L10n}, chips:[L10n]}
included {show, eyebrow:L10n, title:L10n(html), intro:L10n, tagline:L10n,
          cards:[{number:L10n, caption:L10n, label:L10n, title:L10n, text:L10n, link:{label:L10n, path:string}}],
          foot:{note:L10n, link:{label:L10n, bookPreset:"aura-prime"}}}
faq      {show, eyebrow:L10n, title:L10n(html), image:Media, items:[{q:L10n, a:L10n(html)}]}
closing  {show, image:Media, title:L10n(html), text:L10n, cta:{label:L10n, bookPreset:"aura-prime"}}
talkDialog {show, eyebrow:L10n, title:L10n(html), lead:L10n,
            rows:[{label:L10n, html:L10n(html), show}],                                  // Call / Email / Visit / Hours / Social；Call、Email 为占位时 show=false
            consult:{eyebrow:L10n, title:L10n(html), bullets:[L10n], cta:L10n, fine:L10n}}
```

## 5. `facial-blueprint`

```
hero   {show, eyebrow:L10n, title:L10n(html), lede:L10n, cta:{label:L10n},
        map:{stepIntro:L10n, label:L10n, caption:L10n, kicker:L10n,
             modes:[{key:"thirds"|"fifths"|"profile"|"lips"|"contour", name:L10n, sub:L10n, caption:L10n, view:"front"|"side"}],
             front:Media, side:Media}}
steps  {show, eyebrow:L10n, title:L10n(html), items:[{title:L10n, text:L10n}]}              // 序号由代码生成
aesthetic {show, eyebrow:L10n, title:L10n(html), intro:L10n(html),
           rows:[{image:Media, dots:"scale"|"line"|null, name:L10n, title:L10n, text:L10n}]}   // 序号由代码生成
reviews {show:false, eyebrow:L10n, title:L10n(html), items:[{rating:5, quote:L10n, name:L10n, sample:true}], cta:{label:L10n}}
faq    {show, eyebrow:L10n, title:L10n(html), items:[{q:L10n, a:L10n(html)}]}
closing {show, image:Media, title:L10n(html), text:L10n, cta:{label:L10n}}
```

- **脸部比例图（`hero.map`）的 SVG 点线是代码资产**，不进 CMS：抽取工具把原型里的 `<svg class="fbsvg">…</svg>` 存到 `seed/fragments/facial-blueprint-map.svg.html`（两处 `<image href>` 换成 `{{front}}` / `{{side}}` 占位，官网用 `hero.map.front/side` 的地址替换），三张图上的圆点 SVG 存到 `seed/fragments/facial-blueprint-dots-scale.svg.html`、`…-dots-line.svg.html`。动画脚本（五种比例轮播）在代码里，文字取自 `hero.map.modes`。
- **客户评价**：原型里的三条是版面示意（带 "Sample" 标签），按美国 FTC 规定不得当作真实评价发布。种子里 `reviews.show=false` 且每条 `sample:true`；只有换成真实客户、取得同意的评价并把 `sample` 去掉后才允许打开。官网在 `sample:true` 时不输出该条。

## 6. `journal-faq`

```
hero   {show, title:L10n(html), lede:L10n}
tabs   [{key:"all"|"edu"|"faq", label:L10n}]                                                   // 筛选条，第一项 key="all"
sections [{key:"edu"|"faq", title:L10n, lede:L10n,
           items:[{title:L10n, excerpt:L10n, image:Media,
                   tags:[L10n], link:{type:"journal"|"none", target:string}}]}]           // link.type="none"：文章还没写，渲染为不可点
closing {show, eyebrow:L10n, title:L10n(html), text:L10n, cta:{label:L10n}}
```

## 7. `journal-botox-vs-xeomin`

```
header  {show, eyebrow:L10n, title:L10n(html), byline:[{label:L10n, show}], image:Media}   // byline 含 [Author]、[Provider name]、[date] 占位项 show=false
toc     {title:L10n, cta:{label:L10n, path:"/treatments/botox-xeomin"}}                    // 目录项由 body 里 h2 的 id 生成
body    [{type:"p"|"h2"|"callout", id:string?, label:L10n?, text:L10n(html)}]              // callout 的 label 是 "Provider note" / "Medical disclaimer"
related {show, eyebrow:L10n, title:L10n(html), items:[{treatment:slug, image:Media, title:L10n, text:L10n, meta:L10n}]}
more    {show, eyebrow:L10n, title:L10n(html), items:[{image:Media, title:L10n, text:L10n, meta:L10n, link:{type:"journal"|"none", target:string}}]}
closing {show, eyebrow:L10n, title:L10n(html), text:L10n, cta:{label:L10n}}
```

## 8. 目标页 `goal.content`（`goals/{slug}`，6 个）

```
hero    {eyebrow:L10n, title:L10n(html), lede:L10n}
groups  [{key:string, label:L10n}]                  // 筛选条（"All" 由代码加）；没有分组的目标页为空数组
items   [{treatment:slug, group:string|null, image:Media, title:L10n, text:L10n, tags:[L10n]}]   // 顺序即展示顺序
closing {show, eyebrow:L10n, title:L10n(html), text:L10n, cta:{label:L10n}}
```

目标的 `name` / `summary` / `card` 是目标实体自己的字段（契约 §4）。`items` 里的 `treatment` 必须是已存在的治疗 slug；管理端 `treatmentIds` 与这里的顺序同步由管理端保存时负责。

## 9. 页面 SEO

每个页面与治疗/目标的 `seo` 是 `{title, description, keywords, ogMediaId, noindex}`。种子里 `title` 取原型 `<title>`，`description` 取 `meta description`（没有则空，由官网用首段文字兜底）。

## 10. 治疗页补充（已同步写入契约 §3）

治疗页 49 个原型里 35 个是同一套模板，差异如下，已并入 `treatment.content`：

- `how` 增加 `tagline`（"Know first. Then treat." 一类的小句）；卡片的 `zone` 对应原型的 `data-zone`。
- `tech.anchor`：第三区块锚点 id，`"tech"`（Thermage、EMFACE、Exion）或 `"treatment"`（其余）；区块标题文字不同（The technology / Your treatment）已在 `eyebrow`/`title` 里。
- 新增 `grid`（Gold Skin Analysis 用"六件事"列表代替"适合人群"）：`{show, eyebrow, title, items:[{title,text}], foot:L10n(html)}`；使用 `grid` 的页面 `fit.show=false`。
- 新增 `listing`：`{blurb:L10n, price:L10n, tags:[L10n]}`，用于预约抽屉与目标页行的小字（目标页行文字以目标 `items[].text` 为准）。
- `fit.pairNote` 即原型的 "Pairs well"；`how.note` 即 FDA 声明一行；`hero.bookbox.options[0]` 为免费咨询或首选项。
- `tech-neck` 是占位页：`copyComplete=false`，只有 `hero` 与 `closing`，`how`、`fit`、`tech`、`faq` 的 `show=false`。
