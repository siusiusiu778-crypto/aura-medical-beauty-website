import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

/**
 * 开发用 mock：NUXT_MOCK_API=1 时按 docs/api-contract.md 的形状，从 seed/aura-seed.json 返回公开接口，
 * 让没有后端也能 pnpm dev:mock 看全站。mediaKey 解析成本进程的 /_mock/media/<文件名>（读 legacy/site）。
 * 正式环境（没设该变量）这个入口不存在。
 */
type Json = Record<string, unknown>;

let cache: Json | null = null;
let mediaIndex: Map<string, Json> | null = null;
function seed(): Json {
  if (!cache) {
    cache = JSON.parse(readFileSync(resolve(process.cwd(), "seed/aura-seed.json"), "utf8"));
    mediaIndex = new Map(((cache!.media as Json[]) ?? []).map(item => [String(item.key), item]));
  }
  return cache!;
}

/** 递归把 {mediaKey, focus} 换成契约里的 Media 对象 */
function resolveMedia(node: unknown): unknown {
  if (Array.isArray(node)) return node.map(resolveMedia);
  if (node && typeof node === "object") {
    const obj = node as Json;
    if (typeof obj.mediaKey === "string") {
      const key = obj.mediaKey;
      const meta = mediaIndex?.get(key) ?? {};
      return {
        id: 0,
        url: `${useRuntimeConfig().app.baseURL}_mock/media/${key}`,
        kind: /\.(mp4|webm)$/i.test(key) ? "video" : "image",
        // 引用上带 alt 时覆盖媒体库里的（同一张图在不同位置的替代文字不同）
        alt: (obj.alt as Json | undefined) ?? meta.alt ?? { en: "", zh: "" },
        width: null,
        height: null,
        posterUrl: null,
        focus: obj.focus ?? null
      };
    }
    return Object.fromEntries(Object.entries(obj).map(([k, v]) => [k, resolveMedia(v)]));
  }
  return node;
}

const ok = (data: unknown) => ({ status: "success", data, message: "" });
const media = (value: unknown) => (value ? resolveMedia(value) : null);
const seoOf = (seo: unknown) => resolveMedia({ title: { en: "", zh: "" }, description: { en: "", zh: "" }, keywords: { en: "", zh: "" }, ogImage: null, noindex: false, ...((seo as Json) ?? {}) });

export default defineEventHandler(event => {
  if (process.env.NUXT_MOCK_API !== "1") throw createError({ statusCode: 404 });
  if (!existsSync(resolve(process.cwd(), "seed/aura-seed.json"))) throw createError({ statusCode: 503, statusMessage: "seed/aura-seed.json missing" });
  const path = String(getRouterParam(event, "path") ?? "");
  const data = seed();
  const categories = (data.categories as Json[]).filter(cat => cat.isOnline !== false);
  const treatments = data.treatments as Json[];
  const goals = data.goals as Json[];
  const pages = data.pages as Record<string, Json>;
  const fail = (code: number, key: string) => {
    setResponseStatus(event, code);
    return { status: "error", message: key, error_key: key, code };
  };

  // 草稿预览：mock 里不校验签名，按页面键 / slug 返回与详情接口同形的数据
  if (path.startsWith("preview/")) {
    const [, entity, id] = path.split("/");
    const target = entity === "page" ? `pages/${id}` : `${entity}s/${id}`;
    return $fetch(`/_mock/aura/${target}`);
  }
  if (path === "nav") {
    return ok({
      categories: categories.map(cat => {
        const mine = treatments.filter(t => t.categoryKey === cat.key).sort((a, b) => Number(a.groupSort ?? 0) - Number(b.groupSort ?? 0));
        const groups: { name: unknown; treatments: unknown[] }[] = [];
        for (const t of mine) {
          const name = (t.group as Json | null) ?? null;
          const label = name ? JSON.stringify(name) : "";
          let group = groups.find(g => (g.name ? JSON.stringify(g.name) : "") === label);
          if (!group) groups.push((group = { name, treatments: [] }));
          group.treatments.push({ slug: t.slug, name: t.name });
        }
        return {
          key: cat.key,
          name: cat.name,
          tag: cat.tag ?? null,
          link: cat.linkType === "none" ? null : { type: cat.linkType, target: cat.linkTarget },
          groups: cat.linkType === "none" ? groups : []
        };
      })
    });
  }
  if (path.startsWith("pages/")) {
    const page = pages[path.slice(6)];
    if (!page) return fail(404, "not_found");
    return ok({ key: path.slice(6), content: resolveMedia(page.content), seo: seoOf(page.seo), updatedAt: "2026-11-19T00:00:00Z" });
  }
  if (path === "treatments") {
    return ok(treatments.map(t => ({ slug: t.slug, name: t.name, category: t.categoryKey, group: t.group ?? null, summary: t.summary, card: media(t.cardMedia), copyComplete: t.copyComplete !== false })));
  }
  if (path.startsWith("treatments/")) {
    const t = treatments.find(item => item.slug === path.slice(11));
    if (!t) return fail(404, "not_found");
    const cat = (data.categories as Json[]).find(c => c.key === t.categoryKey) as Json;
    const related = treatments.filter(x => x.categoryKey === t.categoryKey && x.slug !== t.slug).slice(0, 3).map(x => ({ slug: x.slug, name: x.name, card: media(x.cardMedia) }));
    return ok({
      slug: t.slug,
      name: t.name,
      category: { key: cat.key, name: cat.name },
      group: t.group ?? null,
      summary: t.summary,
      card: media(t.cardMedia),
      content: resolveMedia(t.content),
      seo: seoOf({ ...(t.seo as Json), noindex: t.copyComplete === false || (t.seo as Json)?.noindex }),
      copyComplete: t.copyComplete !== false,
      updatedAt: "2026-11-19T00:00:00Z",
      related
    });
  }
  if (path === "goals") return ok(goals.map(g => ({ slug: g.slug, name: g.name, summary: g.summary, card: media(g.cardMedia) })));
  if (path.startsWith("goals/")) {
    const g = goals.find(item => item.slug === path.slice(6));
    if (!g) return fail(404, "not_found");
    const items = (((g.content as Json).items as Json[]) ?? []).map(item => treatments.find(t => t.slug === item.treatment)).filter(Boolean) as Json[];
    return ok({
      slug: g.slug,
      name: g.name,
      summary: g.summary,
      card: media(g.cardMedia),
      content: resolveMedia(g.content),
      seo: seoOf(g.seo),
      treatments: items.map(t => ({ slug: t.slug, name: t.name, summary: t.summary, card: media(t.cardMedia) })),
      updatedAt: "2026-11-19T00:00:00Z"
    });
  }
  if (path === "sitemap") {
    return ok({
      pages: Object.keys(pages).map(key => ({ key, updatedAt: null, noindex: false })),
      treatments: treatments.map(t => ({ slug: t.slug, updatedAt: null, noindex: t.copyComplete === false })),
      goals: goals.map(g => ({ slug: g.slug, updatedAt: null }))
    });
  }
  return fail(404, "not_found");
});
