<template>
  <main>
    <div class="wrap crumbs">
      <NuxtLink to="/">{{ tx("Home") }}</NuxtLink> / <NuxtLink to="/journal/faq">{{ tx("Journal & FAQ") }}</NuxtLink> / {{ c("header.eyebrow").split(" · ")[0] }}
    </div>
    <div v-if="on('header')" class="wrap">
      <div style="max-width: 880px; margin: 24px auto 0">
        <p class="eyebrow">{{ c("header.eyebrow") }}</p>
        <h1 style="font-family: var(--serif); font-size: clamp(40px, 5vw, 64px); line-height: 1.02; margin: 12px 0 18px" v-html="ch('header.title')" />
        <div class="byline">
          <template v-for="i in list('header.byline')" :key="i">
            <span v-if="on(`header.byline.${i}`) && c(`header.byline.${i}.label`)">{{ c(`header.byline.${i}.label`) }}</span>
          </template>
        </div>
      </div>
      <div class="arthero"><img :src="img('header.image')" :alt="alt('header.image')" :style="{ objectPosition: focus('header.image') }" /></div>
    </div>

    <section>
      <div class="wrap art">
        <nav class="toc">
          <b>{{ c("toc.title") }}</b>
          <a v-for="h in headings" :key="h.id" :href="`#${h.id}`">{{ h.text }}</a>
          <NuxtLink v-if="raw('toc.cta.path')" class="btn" style="margin-top: 12px" :to="raw<string>('toc.cta.path')!">{{ c("toc.cta.label") }}</NuxtLink>
        </nav>
        <article class="body">
          <template v-for="i in list('body')" :key="i">
            <h2 v-if="raw<string>(`body.${i}.type`) === 'h2'" :id="raw<string>(`body.${i}.id`)" v-html="ch(`body.${i}.text`)" />
            <div v-else-if="raw<string>(`body.${i}.type`) === 'callout'" class="callout">
              <b>{{ c(`body.${i}.label`) }}</b><span v-html="ch(`body.${i}.text`)" />
            </div>
            <p v-else v-html="ch(`body.${i}.text`)" />
          </template>
        </article>
      </div>
    </section>

    <section v-if="on('related')" class="alt">
      <div class="wrap">
        <div class="head">
          <p class="eyebrow">{{ c("related.eyebrow") }}</p>
          <h2 v-html="ch('related.title')" />
        </div>
        <div class="prods">
          <article v-for="i in list('related.items')" :key="i" class="prod">
            <div class="ph"><img :src="img(`related.items.${i}.image`)" :alt="alt(`related.items.${i}.image`)" :style="{ objectPosition: focus(`related.items.${i}.image`) }" /></div>
            <div class="bd">
              <h3>{{ c(`related.items.${i}.title`) }}</h3>
              <p>{{ c(`related.items.${i}.text`) }}</p>
              <span class="meta">{{ c(`related.items.${i}.meta`) }}</span>
            </div>
            <div class="ft">
              <span class="price" />
              <span class="acts">
                <NuxtLink class="more" :to="treatmentPath(raw<string>(`related.items.${i}.treatment`) ?? '')">{{ tx("Details") }}</NuxtLink>
                <a class="bk" href="#book" role="button" @click.prevent="book.open({ preset: raw<string>(`related.items.${i}.treatment`) })">{{ tx("Book") }}</a>
              </span>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section v-if="on('more')">
      <div class="wrap">
        <div class="head">
          <p class="eyebrow">{{ c("more.eyebrow") }}</p>
          <h2 v-html="ch('more.title')" />
        </div>
        <div class="prods">
          <article v-for="i in list('more.items')" :key="i" class="prod">
            <div class="ph"><img :src="img(`more.items.${i}.image`)" :alt="alt(`more.items.${i}.image`)" :style="{ objectPosition: focus(`more.items.${i}.image`) }" /></div>
            <div class="bd">
              <h3>{{ c(`more.items.${i}.title`) }}</h3>
              <p>{{ c(`more.items.${i}.text`) }}</p>
              <span class="meta">{{ c(`more.items.${i}.meta`) }}</span>
            </div>
            <div v-if="moreHref(i)" class="ft">
              <span class="price" />
              <span class="acts"><NuxtLink class="more" :to="moreHref(i)">{{ tx("Details") }}</NuxtLink></span>
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
import "~/assets/css/pages/journal.css";

const props = defineProps<{ ctx: Awaited<ReturnType<typeof usePageContent>> }>();
useFooterStyle(true);
const { c, ch, img, alt, focus, raw, list, on } = props.ctx;
const { tx } = useTx();
const book = useBooking();

// 目录由正文里带 id 的 h2 生成
const headings = computed(() =>
  list("body")
    .filter(i => raw<string>(`body.${i}.type`) === "h2" && raw<string>(`body.${i}.id`))
    .map(i => ({ id: raw<string>(`body.${i}.id`)!, text: plainText(ch(`body.${i}.text`)) }))
);
const moreHref = (i: number) => (raw<string>(`more.items.${i}.link.type`) === "journal" && raw<string>(`more.items.${i}.link.target`) ? pagePath(raw<string>(`more.items.${i}.link.target`)!) : "");
</script>
