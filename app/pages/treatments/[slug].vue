<template>
  <TreatmentView :ctx="ctx" />
</template>

<script setup lang="ts">
definePageMeta({ pg: "treatment" });

const route = useRoute();
const ctx = await useTreatment(String(route.params.slug));
const { entity } = ctx;
const { bi } = useTx();
const absolute = useAbsoluteUrl();

usePageSeo(() => ({
  ...seoFrom(entity.value.seo, `${bi(entity.value.name)} | AURA Institute`),
  // 文案未完成的页面不收录
  noindex: entity.value.seo.noindex || !entity.value.copyComplete,
  jsonLd: [
    {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Home", item: absolute("/") },
        { "@type": "ListItem", position: 2, name: bi(entity.value.category.name) },
        { "@type": "ListItem", position: 3, name: bi(entity.value.name), item: absolute(route.path) }
      ]
    }
  ]
}));
</script>
