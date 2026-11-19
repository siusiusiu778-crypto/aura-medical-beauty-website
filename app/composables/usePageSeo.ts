import type { Seo } from "~~/shared/types/api";

interface PageSeo {
  title: string;
  description?: string;
  keywords?: string;
  image?: string | null;
  noindex?: boolean;
  ogType?: "website" | "article";
  jsonLd?: Record<string, unknown>[];
}

/** 站内路径 → 绝对地址（canonical、结构化数据以 NUXT_PUBLIC_SITE_URL 为准，含子目录前缀） */
export function useAbsoluteUrl() {
  const config = useRuntimeConfig();
  const site = String(config.public.siteUrl).replace(/\/$/, "");
  const base = String(config.app.baseURL).replace(/\/$/, "");
  return (path: string) => (/^https?:\/\//.test(path) ? path : site + base + (path.startsWith("/") ? path : `/${path}`));
}

/** 把接口返回的 seo 字段整理成页面用的 PageSeo；标题缺了用 fallbackTitle */
export function seoFrom(seo: Seo | undefined, fallbackTitle: string, extra: Partial<PageSeo> = {}): PageSeo {
  const pick = (value?: { en?: string; zh?: string }) => value?.en || value?.zh || "";
  return {
    title: pick(seo?.title) || fallbackTitle,
    description: pick(seo?.description) || undefined,
    keywords: pick(seo?.keywords) || undefined,
    image: seo?.ogImage?.url ?? null,
    noindex: Boolean(seo?.noindex),
    ...extra
  };
}

/**
 * 每个页面调用一次：title、description、keywords、Open Graph、Twitter 卡片、canonical、robots、结构化数据。
 * 子目录测试阶段整站 noindex（app.vue 输出）；正式环境下个别页面（文案未完成的治疗页）单独 noindex。
 */
export function usePageSeo(input: PageSeo | (() => PageSeo)) {
  const seo = computed(() => (typeof input === "function" ? input() : input));
  const config = useRuntimeConfig();
  const route = useRoute();
  const absolute = useAbsoluteUrl();
  const production = config.public.deployEnv === "production";
  const canonical = computed(() => absolute(route.path));
  const image = computed(() => (seo.value.image ? absolute(seo.value.image) : undefined));

  useSeoMeta({
    title: () => seo.value.title,
    description: () => seo.value.description || undefined,
    ogTitle: () => seo.value.title,
    ogDescription: () => seo.value.description || undefined,
    ogType: () => seo.value.ogType ?? "website",
    ogUrl: () => canonical.value,
    ogImage: () => image.value,
    twitterCard: "summary_large_image",
    twitterTitle: () => seo.value.title,
    twitterDescription: () => seo.value.description || undefined,
    twitterImage: () => image.value
  });

  useHead({
    link: () => [{ rel: "canonical", href: canonical.value, key: "canonical" }],
    meta: () => [
      ...(production && seo.value.noindex ? [{ name: "robots", content: "noindex, follow", key: "robots" }] : []),
      ...(seo.value.keywords ? [{ name: "keywords", content: seo.value.keywords, key: "keywords" }] : [])
    ],
    script: () => (seo.value.jsonLd ?? []).map((item, index) => ({ type: "application/ld+json", key: `ld-${index}`, innerHTML: JSON.stringify({ "@context": "https://schema.org", ...item }) }))
  });
}
