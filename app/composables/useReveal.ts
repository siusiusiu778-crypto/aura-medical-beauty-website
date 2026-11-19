/**
 * 滚动出现：原型里每个页面各自的小脚本（给 .rv / .rv-img / .big 加上 .in）。
 * 页面挂载后调用一次；偏好减少动效或没有 IntersectionObserver 时直接全部显示。
 */
export function useReveal(options: { threshold?: number; rootMargin?: string; selector?: string } = {}) {
  const { threshold = 0, rootMargin = "0px 0px 12% 0px", selector = ".rv,.rv-x,.rv-img,.big" } = options;
  onMounted(() => {
    const els = [...document.querySelectorAll(selector)];
    if (matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) {
      els.forEach(el => el.classList.add("in"));
      return;
    }
    const io = new IntersectionObserver(
      entries =>
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        }),
      { threshold, rootMargin }
    );
    els.forEach(el => io.observe(el));
    onBeforeUnmount(() => io.disconnect());
  });
}
