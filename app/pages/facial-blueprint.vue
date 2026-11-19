<template>
  <BlueprintView :ctx="ctx" />
</template>

<script setup lang="ts">
definePageMeta({ pg: "blueprint" });
const ctx = await usePageContent("facial-blueprint");
usePageSeo(() => seoFrom(ctx.page.value.seo, "Facial Blueprint | AURA Institute"));
</script>
