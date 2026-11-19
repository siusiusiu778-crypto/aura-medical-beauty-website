import type { Media } from "~~/shared/types/api";

type Leaf = string | { en?: string; zh?: string };

function dig(source: unknown, path: string): unknown {
  let node = source;
  for (const key of path.split(".")) {
    if (node === null || typeof node !== "object") return undefined;
    node = (node as Record<string, unknown>)[key];
  }
  return node;
}

/**
 * 注意：useContentDeps() 要在页面 setup 里、第一个 await 之前调用（之后拿不到 Nuxt 上下文），再传给 useContentReader。
 *
 * 内容读取器：页面、治疗、目标页共用。所有访客看到的文字和图片都经过这里，代码里不放默认内容。
 *
 *   c("hero.lede")          纯文字（en，缺了回退 zh）
 *   ch("hero.title")        给 v-html：转义后只还原白名单标记
 *   img("hero.image")       图片地址（媒体库引用解析后的 url）
 *   media("hero.image")     完整媒体对象（alt、focus、视频海报）
 *   raw<T>("x.y")           其他原始值
 *   list("how.cards")       列表下标，配合 v-for
 *   on("how")               区块是否展示（how.show 不为 false）
 *
 * 字段没填时返回空串（列表为空数组），页面对应位置留空。
 * CMS 编辑预览时，c()/ch() 返回的文字末尾带不可见标记、img() 带 #cms= 片段，用于点页面定位字段；
 * 所以不要拿它们的返回值做相等比较或拼进别的地址，需要原始值用 raw()。
 */
export function useContentDeps() {
  return { edit: useCmsEdit(), base: useRuntimeConfig().app.baseURL.replace(/\/$/, "") };
}

export function useContentReader(payload: ComputedRef<Record<string, unknown>> | Ref<Record<string, unknown>>, refPrefix: string, deps: ReturnType<typeof useContentDeps>) {
  const { edit, base } = deps;
  const ref = (path: string) => `${refPrefix}:${path}`;

  function c(path: string): string {
    const leaf = dig(payload.value, path) as Leaf | undefined;
    const text = typeof leaf === "string" ? leaf : !leaf || typeof leaf !== "object" ? "" : leaf.en || leaf.zh || "";
    return text && edit.active.value ? text + cmsMark(ref(path)) : text;
  }
  // 内容里的站内链接写成 /treatments/x 这样的路径：v-html 里的 <a> 不经过 NuxtLink，这里补上站点前缀（子目录部署时）
  const ch = (path: string) => richHtml(c(path)).replace(/href="\/(?!\/)/g, `href="${base}/`);

  function media(path: string): Media | null {
    const leaf = dig(payload.value, path) as Media | null | undefined;
    return leaf && typeof leaf === "object" && leaf.url ? leaf : null;
  }
  function img(path: string): string {
    const url = media(path)?.url || "";
    return url && edit.active.value ? url + cmsImageMark(ref(path)) : url;
  }
  /** 图片的替代文字（媒体库里填的 alt），没填为空串 */
  function alt(path: string): string {
    const text = media(path)?.alt;
    return text ? text.en || text.zh || "" : "";
  }
  /** CSS object-position；没设置为 undefined */
  const focus = (path: string): string | undefined => media(path)?.focus || undefined;

  function raw<T>(path: string): T | undefined {
    const leaf = dig(payload.value, path);
    return leaf === undefined || leaf === null || leaf === "" ? undefined : (leaf as T);
  }
  function list(path: string): number[] {
    const leaf = dig(payload.value, path);
    return Array.isArray(leaf) ? leaf.map((_, index) => index) : [];
  }
  const on = (path: string) => raw<boolean>(`${path}.show`) !== false;

  return { c, ch, img, media, alt, focus, raw, list, on };
}
