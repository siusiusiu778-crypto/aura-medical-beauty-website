<template>
  <GoalView :ctx="ctx" />
</template>

<script setup lang="ts">
definePageMeta({ pg: "goal" });

const route = useRoute();
const ctx = await useGoal(String(route.params.slug));
const { entity } = ctx;
const { bi } = useTx();

usePageSeo(() => seoFrom(entity.value.seo, `${bi(entity.value.name)} | AURA Institute`));
</script>
