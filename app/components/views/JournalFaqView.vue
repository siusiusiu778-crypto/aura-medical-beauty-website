<template>
  <main>
    <div class="wrap crumbs">
      <NuxtLink to="/">{{ tx("Home") }}</NuxtLink> / {{ plainText(ch("hero.title")) }}
    </div>
    <div v-if="on('hero')" id="top" class="wrap">
      <div class="chd">
        <h1 v-html="ch('hero.title')" />
        <div><p>{{ c("hero.lede") }}</p></div>
      </div>
    </div>
    <div v-if="list('tabs').length" class="chips2">
      <div class="wrap">
        <a v-for="i in list('tabs')" :key="i" :class="{ on: tab === raw<string>(`tabs.${i}.key`) }" :href="anchorOf(raw<string>(`tabs.${i}.key`) ?? 'all')" @click="tab = raw<string>(`tabs.${i}.key`) ?? 'all'">{{ c(`tabs.${i}.label`) }}</a>
      </div>
    </div>

    <section style="padding-top: 0">
      <div class="wrap">
        <div v-for="s in list('sections')" :key="s" :id="raw<string>(`sections.${s}.key`)" class="grp2">
          <h2>{{ c(`sections.${s}.title`) }}</h2>
          <p v-if="c(`sections.${s}.lede`)">{{ c(`sections.${s}.lede`) }}</p>
          <article v-for="i in list(`sections.${s}.items`)" :key="i" class="row">
            <component :is="hrefOf(s, i) ? NuxtLink : 'span'" class="ph" :to="hrefOf(s, i) || undefined">
              <img :src="img(`sections.${s}.items.${i}.image`)" :alt="alt(`sections.${s}.items.${i}.image`)" :style="{ objectPosition: focus(`sections.${s}.items.${i}.image`) }" />
            </component>
            <div>
              <h3>
                <NuxtLink v-if="hrefOf(s, i)" :to="hrefOf(s, i)">{{ c(`sections.${s}.items.${i}.title`) }}</NuxtLink>
                <template v-else>{{ c(`sections.${s}.items.${i}.title`) }}</template>
              </h3>
              <p class="ex">{{ c(`sections.${s}.items.${i}.excerpt`) }}</p>
              <div v-if="list(`sections.${s}.items.${i}.tags`).length" class="tg">
                <span v-for="t in list(`sections.${s}.items.${i}.tags`)" :key="t">{{ c(`sections.${s}.items.${i}.tags.${t}`) }}</span>
              </div>
              <NuxtLink v-if="hrefOf(s, i)" class="lm" :to="hrefOf(s, i)">{{ tx("Read") }} <span aria-hidden="true">→</span></NuxtLink>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section v-if="on('closing')" id="book" class="cta">
      <div class="wrap">
        <p class="eyebrow" style="color: inherit; opacity: 0.7">{{ c("closing.eyebrow") }}</p>
        <h2 v-html="ch('closing.title')" />
        <p>{{ c("closing.text") }}</p>
        <a class="btn" href="#book" role="button" @click.prevent="book.open()">{{ c("closing.cta.label") }}</a>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { NuxtLink } from "#components";
import "~/assets/css/pages/faq.css";

const props = defineProps<{ ctx: Awaited<ReturnType<typeof usePageContent>> }>();
useFooterStyle(true);
const { c, ch, img, alt, focus, raw, list, on } = props.ctx;
const { tx } = useTx();
const book = useBooking();
const tab = ref("all");

/** 文章链接：type=journal → /journal/…；type=none（文章还没写）→ 不可点 */
function hrefOf(s: number, i: number): string {
  const type = raw<string>(`sections.${s}.items.${i}.link.type`);
  const target = raw<string>(`sections.${s}.items.${i}.link.target`);
  return type === "journal" && target ? pagePath(target) : "";
}
const anchorOf = (key: string) => (key === "all" ? "#top" : `#${key}`);
</script>
