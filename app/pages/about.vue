<template>
  <AboutView :ctx="ctx" />
</template>

<script setup lang="ts">
definePageMeta({ pg: "about" });
const ctx = await usePageContent("about");
usePageSeo(() => seoFrom(ctx.page.value.seo, "About | AURA Institute"));
</script>
