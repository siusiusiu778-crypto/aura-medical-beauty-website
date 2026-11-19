import type { SitemapData } from "~~/shared/types/api";

const xml = (text: string) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/** 站点地图：静态页、目标页、治疗页。哪些可收录由后端 /sitemap 决定；文案未完成（noindex）的页面不列入。 */
export default defineEventHandler(async event => {
  const config = useRuntimeConfig(event);
  const site = String(config.public.siteUrl).replace(/\/$/, "") + String(config.app.baseURL).replace(/\/$/, "");
  const data = await publicApi<SitemapData>(event, "/sitemap");

  const entries: { path: string; lastmod: string | null }[] = [
    ...data.pages.filter(page => !page.noindex && page.key in PAGE_PATHS).map(page => ({ path: pagePath(page.key), lastmod: page.updatedAt })),
    ...data.goals.map(goal => ({ path: `/goals/${goal.slug}`, lastmod: goal.updatedAt })),
    ...data.treatments.filter(item => !item.noindex).map(item => ({ path: `/treatments/${item.slug}`, lastmod: item.updatedAt }))
  ];
  const urls = entries.map(entry => {
    const loc = site + (entry.path === "/" ? "/" : entry.path);
    return `<url><loc>${xml(loc)}</loc>${entry.lastmod ? `<lastmod>${xml(entry.lastmod.slice(0, 10))}</lastmod>` : ""}</url>`;
  });
  setHeader(event, "content-type", "application/xml; charset=utf-8");
  setHeader(event, "cache-control", "public, max-age=600");
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.join("\n")}\n</urlset>\n`;
});
