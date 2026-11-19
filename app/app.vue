<template>
  <div class="aura" :class="`pg-${pg}`">
    <SiteHeader />
    <NuxtPage :page-key="pageKey" />
    <SiteFooter />
    <button v-if="on('floatBook') && c('floatBook.label')" type="button" class="floatbook" @click="book.open()">{{ c("floatBook.label") }}</button>
    <BookDrawer />
    <BackToTop />
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const route = useRoute();
const book = useBooking();

// 页面类型决定样式作用域（.pg-<页面>），在各页面里用 definePageMeta({ pg }) 声明
// 草稿预览页按预览的内容类型覆盖（见 pages/_site/preview）
const pgOverride = useState("pg-override", () => "");
const pg = computed(() => pgOverride.value || String(route.meta.pg ?? "home"));

// CMS 可视化编辑预览时，区块显隐变化后让页面整体重新挂载（见 useCmsEdit）；平时就是按路由区分
const { epoch } = useCmsEdit();
const pageKey = (r: { fullPath: string }) => `${r.fullPath}#${epoch.value}`;

// 站点名称、favicon、全站内容来自 CMS「site」页面
const { c, img, on } = await useSite();

useHead({
  link: () => (img("brand.favicon") ? [{ rel: "icon" as const, href: img("brand.favicon"), key: "favicon" }] : []),
  // 子目录测试阶段整站不被收录；正式站由各页面自己决定
  meta: () => (config.public.deployEnv === "production" ? [] : [{ name: "robots", content: "noindex, nofollow" }])
});
</script>
