<template>
  <HomeView :ctx="ctx" />
</template>

<script setup lang="ts">
definePageMeta({ pg: "home" });
const absolute = useAbsoluteUrl();
const ctx = await usePageContent("home");
usePageSeo(() => ({
  ...seoFrom(ctx.page.value.seo, "AURA Institute"),
  jsonLd: [{ "@type": "MedicalBusiness", name: "AURA Institute", url: absolute("/") }]
}));
</script>
