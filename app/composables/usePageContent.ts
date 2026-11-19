import type { PageContent } from "~~/shared/types/api";

/**
 * 页面内容（home、about、membership、facial-blueprint、journal-*、site），来自 CMS「AURA 页面」。
 *
 *   const { c, ch, img, raw, list, on, page } = await usePageContent("home");
 *
 * 页面未发布或接口取不到时返回 503，不渲染空壳页面。
 * CMS 编辑预览时，用编辑器送来的（尚未保存的）内容代替已发布内容，见 useCmsEdit。
 */
export async function usePageContent(pageKey: string) {
  const api = useApi();
  // 必须在 await 之前取：之后拿不到 Nuxt 上下文
  const deps = useContentDeps();
  const edit = deps.edit;
  const { data, error } = await useAsyncData(`page:${pageKey}`, () => api<PageContent>(`/pages/${pageKey}`));
  if (error.value || !data.value) throw createError({ statusCode: 503, statusMessage: "Content unavailable", fatal: true });
  const payload = computed<Record<string, unknown>>(() => (edit.active.value && edit.overrides.value[pageKey]) || data.value?.content || {});
  return { ...useContentReader(payload, pageKey, deps), page: data as Ref<PageContent> };
}
