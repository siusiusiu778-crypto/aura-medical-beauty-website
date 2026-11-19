<template>
  <MembershipView :ctx="ctx" />
</template>

<script setup lang="ts">
definePageMeta({ pg: "membership" });
const ctx = await usePageContent("membership");
usePageSeo(() => seoFrom(ctx.page.value.seo, "AURA Prime Membership | AURA Institute"));
</script>
