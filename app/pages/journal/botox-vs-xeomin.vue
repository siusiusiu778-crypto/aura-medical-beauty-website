<template>
  <JournalArticleView :ctx="ctx" />
</template>

<script setup lang="ts">
definePageMeta({ pg: "journal" });
const ctx = await usePageContent("journal-botox-vs-xeomin");
usePageSeo(() => ({ ...seoFrom(ctx.page.value.seo, "Botox® vs Xeomin® | AURA Institute"), ogType: "article" as const }));
</script>
