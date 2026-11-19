<template>
  <JournalFaqView :ctx="ctx" />
</template>

<script setup lang="ts">
definePageMeta({ pg: "faq" });
const ctx = await usePageContent("journal-faq");
usePageSeo(() => seoFrom(ctx.page.value.seo, "Journal & FAQ | AURA Institute"));
</script>
