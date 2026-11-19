// AURA Institute 官网：Nuxt 4 + SSR。内容来自 Vectra 的 AURA CMS，接口与内容约定见 docs/api-contract.md。
// 子目录部署：NUXT_APP_BASE_URL（构建与运行都要设置，例如 /aura-institute/），换正式域名时改成 / 即可。
const mock = process.env.NUXT_MOCK_API === "1";

export default defineNuxtConfig({
  compatibilityDate: "2026-07-01",
  devtools: { enabled: false },

  // components/views/ 下的页面视图不加目录前缀，直接叫 TreatmentView、HomeView……
  components: [{ path: "~/components", pathPrefix: false }],

  css: ["~/assets/css/base.css", "~/assets/css/chrome.css", "~/assets/css/drawer.css", "~/assets/css/chrome.extra.css"],

  runtimeConfig: {
    // 服务端渲染直连 Vectra 后端的内网基址与 Host 头（与浏览器端同一组公开接口）；留空则回退到 public.apiBase
    apiBaseServer: "",
    apiHostHeader: "",
    revalidateSecret: "",
    previewSecret: "",
    public: {
      siteUrl: "https://overseasstudent.com",
      // 浏览器端接口基址：198 上的同源反代
      apiBase: mock ? "/_mock/aura" : "/aura-institute/api",
      deployEnv: "staging",
      // 允许内嵌本站做可视化编辑预览的 CMS 网址（逗号分隔，NUXT_PUBLIC_CMS_ORIGINS）。留空则不开放。
      cmsOrigins: ""
    }
  },

  app: {
    baseURL: process.env.NUXT_APP_BASE_URL || "/",
    head: {
      htmlAttrs: { lang: "en" },
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1, viewport-fit=cover" }
      ],
      link: [
        { rel: "preconnect", href: "https://fonts.googleapis.com" },
        { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "" },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Hanken+Grotesk:wght@300;400;500;600&family=Tenor+Sans&display=swap"
        }
      ]
    }
  },

  typescript: { strict: true },

  // 页面缓存放进程内存：整页输出不含访客相关内容，可以缓存。时长只是兜底，
  // CMS 保存内容后后端会通知 /_site/revalidate 立即清空。
  $production: {
    routeRules: {
      "/**": { swr: 600 },
      "/_site/**": { swr: false, cache: false },
      "/_deploy/**": { swr: false, cache: false },
      "/_mock/**": { swr: false, cache: false },
      "/sitemap.xml": { swr: false, cache: false },
      "/robots.txt": { swr: false, cache: false }
    }
  }
});
