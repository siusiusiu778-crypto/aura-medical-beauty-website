/** FAQ：同一时间只展开一条（原型 l3.js）。给 <details> 列表的容器 ref 用。 */
export function useOneOpen(container: Ref<HTMLElement | undefined>) {
  onMounted(() => {
    const root = container.value;
    if (!root) return;
    const onToggle = (event: Event) => {
      const target = event.target as HTMLDetailsElement;
      if (target.tagName !== "DETAILS" || !target.open) return;
      root.querySelectorAll<HTMLDetailsElement>("details").forEach(other => {
        if (other !== target) other.open = false;
      });
    };
    root.addEventListener("toggle", onToggle, true);
    onBeforeUnmount(() => root.removeEventListener("toggle", onToggle, true));
  });
}
