<template>
  <div class="error-page">
    <div class="error-box">
      <NuxtLink class="error-mark" to="/">AURA INSTITUTE</NuxtLink>
      <p class="error-code">{{ notFound ? "404" : (error?.statusCode ?? 500) }}</p>
      <h1>{{ notFound ? "Page not found." : "Something went wrong." }}</h1>
      <p class="error-text">{{ notFound ? "The page you're looking for has moved or no longer exists." : "Please try again in a moment." }}</p>
      <button type="button" class="error-cta" @click="home">Back to Home</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NuxtError } from "#app";

/** 全站错误页（404 与渲染出错）。不依赖接口，保证任何情况下都能显示。 */
const props = defineProps<{ error: NuxtError | null }>();
const notFound = computed(() => props.error?.statusCode === 404);
const home = () => clearError({ redirect: "/" });

useHead({
  title: () => (notFound.value ? "Page not found | AURA Institute" : "AURA Institute"),
  meta: [{ name: "robots", content: "noindex" }]
});
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  background: #f8f0eb;
  color: #2f221d;
  font-family: "Hanken Grotesk", system-ui, sans-serif;
  text-align: center;
}
.error-mark {
  font-family: "Tenor Sans", sans-serif;
  font-size: 18px;
  letter-spacing: 0.14em;
  color: inherit;
  text-decoration: none;
}
.error-code {
  margin: 40px 0 0;
  font-family: "Cormorant Garamond", serif;
  font-weight: 400;
  font-size: clamp(88px, 18vw, 160px);
  line-height: 1;
}
h1 {
  margin: 12px 0 0;
  font-family: "Cormorant Garamond", serif;
  font-weight: 500;
  font-size: clamp(26px, 4vw, 36px);
}
.error-text {
  margin: 14px auto 0;
  max-width: 420px;
  color: #5b4840;
  line-height: 1.6;
}
.error-cta {
  margin-top: 32px;
  padding: 15px 34px;
  border: 0;
  background: #2f221d;
  color: #fbf4ef;
  font: 600 11px "Hanken Grotesk", system-ui, sans-serif;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  cursor: pointer;
}
</style>
