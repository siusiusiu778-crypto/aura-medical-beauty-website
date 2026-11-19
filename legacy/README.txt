AURA Institute 网站原型 · 2026-11-03（导航与页面结构重构后）

打开方式
  site/home.html   首页（从这里开始浏览，所有导航和卡片都能点）
  site/index.html  全部页面目录

结构（两条独立路径，互不链接）
  路径 A·顶部导航（按治疗类型）：Injectables / Skin Tightening & Lifting / Skin / Wellness & Longevity / Body / Membership / About
    分类名本身不是链接，只展开下拉菜单（桌面 hover/点击，移动端点击展开为手风琴）；下拉菜单里每一项都直接链接到对应的三级治疗页面。
    共享导航组件：site/nav.html（标记）+ site/nav.css（样式）+ site/nav.js（抓取 nav.html 注入 #site-header，处理下拉/手风琴/Esc）。
  路径 B·首页"Start with your goal"卡片（按改善目标，二级页面，仅此处可达）：
    goal-skin-tightening.html / goal-facial-balancing.html / goal-wrinkles-jawline.html /
    goal-facials-pores.html / goal-glow-hydration.html / goal-body-wellness.html
    每个目标页列出该目标下的全部治疗项目，点击条目进入对应三级页面。

  已删除的旧二级分类页（face-design.html、skin-tightening.html、skin-glow.html、wellness.html、body-shape.html）
  上线时请在服务器层配置 301 重定向（Netlify/Vercel 等可直接用 _redirects 文件，已放在 site/_redirects）：
    /face-design      -> /goal-facial-balancing
    /skin-tightening  -> /goal-skin-tightening
    /skin-glow        -> /goal-glow-hydration
    /wellness         -> /goal-body-wellness
    /body-shape       -> /goal-body-wellness

  三级页面：共 35 个治疗页，模板统一为 Thermage® FLX 的结构（图左文右 + 预约框 → 原理 → 适合人群 → 技术 → 一览 → FAQ → 结尾横幅）。
    已有完整文案：Thermage® FLX、EMFACE®、Botox & Xeomin、Rejuran®(原 glow-booster，已改名)、Gold Skin Analysis、Body Sculpt、NAD+ IV Drip
    待补文案的占位页（28 个，<meta name="robots" content="noindex">，首屏文案已填，其余区块为"[Copy to come]"）：
    chin-balance / defined-jawline / under-eye-hollows / temples / lip-volume / nose-profile / sculptra / radiesse /
    botox-brow-lift / jaw-slimming / kybella / facial-harmonization / lower-face-lift / exion /
    hydrafacial / signature-facial / barrier-recovery-facial / gold-rf-microneedling /
    bbl-photofacial / skinvive / under-eye-brightening / neck-hydration / tech-neck / scalp-hair /
    fat-dissolving / trap-tox / stretch-mark-repair / exomind

说明
  [confirm] = 时长等信息待确认；"[Copy to come]" = 占位文案，上线前需替换
  图片为占位图，首页视频/海报含 THE SMILE INSTITUTE 字样，上线前必须更换素材
  source/ 是旧版生成脚本（python3，对应改版前的首页版本，本次重构未使用，仅作历史参考）
