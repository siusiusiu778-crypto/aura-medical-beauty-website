/**
 * 预约抽屉的开关与预选项目。全站的 Book 按钮都调用 useBooking().open(...)，
 * 抽屉本身在 app.vue 里挂一次（BookDrawer）。
 *
 * 预选：`preset` 是契约里的 bookPreset（"consultation" | "aura-prime" | 治疗 slug）；`text` 是已经选好的项目名（治疗页首屏的下拉）。
 */
export interface BookRequest {
  preset?: string | null;
  text?: string | null;
  /** 已选项目所属治疗的 slug（治疗页首屏的下拉用），线索里记录意向治疗 */
  slug?: string | null;
}

export function useBooking() {
  const state = useState<{ open: boolean; request: BookRequest; nonce: number }>("booking", () => ({ open: false, request: {}, nonce: 0 }));
  return {
    state,
    open(request: BookRequest = {}) {
      state.value = { open: true, request, nonce: state.value.nonce + 1 };
    },
    close() {
      state.value = { ...state.value, open: false };
    }
  };
}
