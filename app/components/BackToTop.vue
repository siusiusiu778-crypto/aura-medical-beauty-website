<template>
  <button type="button" class="totop" :class="{ on: shown }" aria-label="Back to top" @click="top">
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M8 13V3M3.5 7.5 8 3l4.5 4.5" /></svg>
  </button>
</template>

<script setup lang="ts">
/** 返回顶部：首屏之后出现（样式 .totop 在 chrome.css）。移植自原型 nav.js。 */
const shown = ref(false);
function top() {
  window.scrollTo({ top: 0, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
}
onMounted(() => {
  let tick = false;
  const update = () => {
    tick = false;
    shown.value = window.scrollY > window.innerHeight * 0.8;
  };
  const onScroll = () => {
    if (!tick) {
      tick = true;
      requestAnimationFrame(update);
    }
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  update();
  onBeforeUnmount(() => window.removeEventListener("scroll", onScroll));
});
</script>
