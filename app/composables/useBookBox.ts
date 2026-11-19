/**
 * 治疗页首屏的预约下拉（选项目 + Continue to Booking）。移植自原型 l3.js：
 * 选中后胶囊里显示所选项（带 " · " 的取后半段），点 Continue 打开预约抽屉并预选该项目；
 * 点列表以外的地方收起；列表放不下时向上展开。
 */
export function useBookBox(options: () => string[], consultFallback: () => string, slug: () => string | null = () => null) {
  const book = useBooking();
  const picked = ref(-1);
  const el = ref<HTMLDetailsElement>();
  const up = ref(false);

  const shown = (label: string) => {
    if (picked.value < 0) return label;
    const text = options()[picked.value] ?? label;
    return text.includes(" · ") ? text.split(" · ").slice(1).join(" · ") : text;
  };
  function pick(index: number, event: Event) {
    picked.value = index;
    event.preventDefault();
    if (el.value) el.value.open = false;
  }
  function onToggle() {
    const details = el.value;
    if (!details?.open) return;
    up.value = false;
    const list = details.querySelector<HTMLElement>(".bbopts");
    if (!list) return;
    const rect = details.getBoundingClientRect();
    const height = list.offsetHeight + 16;
    if (rect.bottom + height > innerHeight && rect.top - height > 0) up.value = true;
  }
  function proceed() {
    const text = options()[picked.value < 0 ? 0 : picked.value] ?? "";
    const consult = !text || /^complimentary consultation$/i.test(text);
    book.open({ text: consult ? consultFallback() : text, slug: consult ? null : slug() });
  }
  onMounted(() => {
    const onClick = (event: MouseEvent) => {
      if (el.value?.open && !el.value.contains(event.target as Node)) el.value.open = false;
    };
    document.addEventListener("click", onClick);
    onBeforeUnmount(() => document.removeEventListener("click", onClick));
  });
  return { picked, el, up, shown, pick, onToggle, proceed };
}
