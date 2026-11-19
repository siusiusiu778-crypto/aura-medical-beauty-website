/**
 * 两条横线之间的标签行（治疗页首屏、AURA Prime）：始终一行。字号与间距一起缩小去适应行宽，空间够了再放回设计尺寸。
 * 移植自原型 nav.js 的 fitChips。
 */
export function useFitChips(selector = ".thero2 .chips, .pr .chips") {
  onMounted(() => {
    const fit = () => {
      document.querySelectorAll<HTMLElement>(selector).forEach(row => {
        const spans = [...row.children] as HTMLElement[];
        spans.forEach(s => {
          s.style.fontSize = "";
          s.style.paddingLeft = "";
          s.style.paddingRight = "";
          s.style.letterSpacing = "";
        });
        const avail = row.clientWidth;
        if (!avail) return;
        if (row.scrollWidth > avail + 0.5) spans.forEach(s => (s.style.letterSpacing = ".07em"));
        for (let k = 0; k < 3; k += 1) {
          const need = row.scrollWidth;
          if (need <= avail + 0.5) break;
          const r = avail / need;
          spans.forEach((s, i) => {
            const cs = getComputedStyle(s);
            s.style.fontSize = `${Math.max(7, parseFloat(cs.fontSize) * r)}px`;
            if (i > 0) s.style.paddingLeft = `${parseFloat(cs.paddingLeft) * r}px`;
            s.style.paddingRight = `${parseFloat(cs.paddingRight) * r}px`;
          });
        }
      });
    };
    let timer: ReturnType<typeof setTimeout>;
    const onResize = () => {
      clearTimeout(timer);
      timer = setTimeout(fit, 60);
    };
    fit();
    window.addEventListener("resize", onResize);
    document.fonts?.ready.then(fit);
    onBeforeUnmount(() => window.removeEventListener("resize", onResize));
  });
}
