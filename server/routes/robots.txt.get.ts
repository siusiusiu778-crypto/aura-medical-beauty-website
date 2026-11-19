/** 正式站允许收录并指向站点地图；其余环境（子目录测试阶段）整站禁止抓取。 */
export default defineEventHandler(event => {
  const config = useRuntimeConfig(event);
  setHeader(event, "content-type", "text/plain; charset=utf-8");
  if (config.public.deployEnv !== "production") return "User-agent: *\nDisallow: /\n";
  const base = String(config.app.baseURL).replace(/\/$/, "");
  const site = String(config.public.siteUrl).replace(/\/$/, "");
  return `User-agent: *\nAllow: /\nDisallow: ${base}/_site/\n\nSitemap: ${site}${base}/sitemap.xml\n`;
});
