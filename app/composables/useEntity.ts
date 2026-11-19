import type { GoalDetail, PageContent, TreatmentDetail } from "~~/shared/types/api";

type Deps = ReturnType<typeof useContentDeps>;

/** 内容读取器 + 实体：内容来自 entity.content，CMS 编辑预览时优先用编辑器送来的内容（按 key） */
export function buildCtx<T extends { content: Record<string, unknown> }>(entity: Ref<T>, key: string, deps: Deps) {
  const payload = computed<Record<string, unknown>>(() => (deps.edit.active.value && deps.edit.overrides.value[key]) || entity.value.content || {});
  return { ...useContentReader(payload, key, deps), entity };
}

/** 治疗页：/treatments/{slug}。不存在或未发布返回真实的 404。 */
export async function useTreatment(slug: string) {
  const api = useApi();
  const deps = useContentDeps();
  const { data, error } = await useAsyncData(`treatment:${slug}`, () => orNull(api<TreatmentDetail>(`/treatments/${slug}`)));
  if (error.value) throw createError({ statusCode: 503, statusMessage: "Content unavailable", fatal: true });
  if (!data.value) throw createError({ statusCode: 404, statusMessage: "Not found", fatal: true });
  return buildCtx(data as Ref<TreatmentDetail>, `treatment:${slug}`, deps);
}

/** 目标页：/goals/{slug} */
export async function useGoal(slug: string) {
  const api = useApi();
  const deps = useContentDeps();
  const { data, error } = await useAsyncData(`goal:${slug}`, () => orNull(api<GoalDetail>(`/goals/${slug}`)));
  if (error.value) throw createError({ statusCode: 503, statusMessage: "Content unavailable", fatal: true });
  if (!data.value) throw createError({ statusCode: 404, statusMessage: "Not found", fatal: true });
  return buildCtx(data as Ref<GoalDetail>, `goal:${slug}`, deps);
}

/** 页面（预览用）：已经取到 PageContent 时直接建读取器；key 是页面键 */
export function buildPageCtx(page: Ref<PageContent>, key: string, deps: Deps) {
  const payload = computed<Record<string, unknown>>(() => (deps.edit.active.value && deps.edit.overrides.value[key]) || page.value.content || {});
  return { ...useContentReader(payload, key, deps), page };
}
