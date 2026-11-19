import type { NavCategory, TreatmentSummary } from "~~/shared/types/api";

/** 全站通用内容（页脚、站点名称、按钮文字等）：CMS「AURA 页面 → site」。同一页面多处调用只请求一次。 */
export function useSite() {
  return usePageContent("site");
}

/** 导航：类别 → 分组 → 治疗，来自 /nav，加一个治疗会自动出现在下拉里 */
export async function useNav() {
  const api = useApi();
  const { data } = await useAsyncData("nav", () => api<{ categories: NavCategory[] }>("/nav"));
  return computed(() => data.value?.categories ?? []);
}

/** 全部治疗（搜索框按名称过滤用），浏览器端首次聚焦搜索框时才请求 */
export function useTreatmentIndex() {
  const api = useApi();
  const items = useState<TreatmentSummary[]>("treatment-index", () => []);
  let loading = false;
  async function load() {
    if (items.value.length || loading) return;
    loading = true;
    try {
      items.value = await api<TreatmentSummary[]>("/treatments");
    } finally {
      loading = false;
    }
  }
  return { items, load };
}
