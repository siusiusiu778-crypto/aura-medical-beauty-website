<template>
  <main>
    <section v-if="on('hero')" id="top" class="ahero">
      <img :src="img('hero.image')" alt="" aria-hidden="true" fetchpriority="high" :style="{ objectPosition: focus('hero.image') }" />
      <div class="wrap">
        <div>
          <p class="eyebrow rv">{{ c("hero.eyebrow") }}</p>
          <h1 :aria-label="plainText(ch('hero.title'))">
            <span v-for="(line, i) in splitLines(ch('hero.title'))" :key="i" class="ln"><i :style="{ '--d': `${0.15 + i * 0.15}s` }" v-html="line" /></span>
          </h1>
        </div>
        <div class="hbar rv" style="--d: 0.5s">
          <p>{{ c("hero.lede") }}</p>
          <a class="btn" href="#book" role="button" @click.prevent="book.open()">{{ c("hero.cta.label") }} →</a>
        </div>
      </div>
    </section>

    <section v-if="on('intro')" class="intro">
      <div class="wrap">
        <p class="eyebrow cl rv">{{ c("intro.eyebrow") }}</p>
        <p class="lead rv" style="--d: 0.1s" v-html="ch('intro.text')" />
      </div>
    </section>

    <section v-if="on('who')" id="who">
      <div class="wrap two">
        <div>
          <p class="eyebrow rv">{{ c("who.eyebrow") }}</p>
          <h2 class="h2 rv" style="--d: 0.1s" v-html="ch('who.title')" />
          <p class="copy rv" style="--d: 0.2s">{{ c("who.text") }}</p>
        </div>
        <figure class="rv-img" style="--d: 0.15s"><img :src="img('who.image')" :alt="alt('who.image')" :style="{ objectPosition: focus('who.image') }" /></figure>
      </div>
    </section>

    <section v-if="on('standards')" id="standards" class="alt">
      <div class="wrap">
        <div class="ctr">
          <p class="eyebrow cl rv">{{ c("standards.eyebrow") }}</p>
          <h2 class="h2 rv" style="--d: 0.08s" v-html="ch('standards.title')" />
        </div>
        <ol class="std">
          <li v-for="i in list('standards.items')" :key="i" class="rv" :style="{ '--d': `${(i % 3) * 0.08}s` }">
            <span class="n">{{ String(i + 1).padStart(2, "0") }}</span>
            <h3>{{ c(`standards.items.${i}.title`) }}</h3>
            <p>{{ c(`standards.items.${i}.text`) }}</p>
          </li>
        </ol>
      </div>
    </section>

    <section v-if="on('technology')" id="technology">
      <div class="wrap tech">
        <div>
          <p class="eyebrow cl rv">{{ c("technology.eyebrow") }}</p>
          <h2 class="h2 rv" style="--d: 0.08s" v-html="ch('technology.title')" />
          <p class="copy rv" style="--d: 0.16s">{{ c("technology.text") }}</p>
          <div class="ph rv-img"><img :src="img('technology.image')" :alt="alt('technology.image')" :style="{ objectPosition: focus('technology.image') }" /></div>
        </div>
        <div class="rv" style="--d: 0.2s">
          <table class="brands">
            <thead>
              <tr>
                <th v-for="h in list('technology.table.head')" :key="h" scope="col">{{ c(`technology.table.head.${h}`) }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in list('technology.table.rows')" :key="r">
                <td v-for="k in list(`technology.table.rows.${r}`)" :key="k">{{ c(`technology.table.rows.${r}.${k}`) }}</td>
              </tr>
            </tbody>
          </table>
          <p class="fda">{{ c("technology.note") }}</p>
        </div>
      </div>
    </section>

    <section v-if="on('aesthetic')" id="aesthetic" class="alt">
      <div class="wrap aes">
        <div class="t1">
          <p class="eyebrow cl rv">{{ c("aesthetic.eyebrow") }}</p>
          <h2 class="h2 rv" style="--d: 0.08s" v-html="ch('aesthetic.title')" />
          <p class="copy rv" style="--d: 0.16s">{{ c("aesthetic.text") }}</p>
          <NuxtLink v-if="raw('aesthetic.link.path')" class="tlink rv" style="--d: 0.24s" :to="raw<string>('aesthetic.link.path')!">{{ c("aesthetic.link.label") }} →</NuxtLink>
        </div>
        <figure class="p1 rv-img"><img :src="img('aesthetic.images.0')" :alt="alt('aesthetic.images.0')" :style="{ objectPosition: focus('aesthetic.images.0') }" /></figure>
        <figure class="p2 rv-img" style="--d: 0.1s"><img :src="img('aesthetic.images.1')" :alt="alt('aesthetic.images.1')" :style="{ objectPosition: focus('aesthetic.images.1') }" /></figure>
        <div class="side">
          <figure class="p3 rv-img" style="--d: 0.2s"><img :src="img('aesthetic.images.2')" :alt="alt('aesthetic.images.2')" :style="{ objectPosition: focus('aesthetic.images.2') }" /></figure>
          <p class="q rv" style="--d: 0.3s">{{ c("aesthetic.quote") }}</p>
        </div>
      </div>
    </section>

    <section v-if="on('closing')" id="book" class="closing">
      <img :src="img('closing.image')" alt="" aria-hidden="true" :style="{ objectPosition: focus('closing.image') }" />
      <div class="wrap cgrid">
        <div>
          <h2 class="rv" v-html="ch('closing.title')" />
          <a class="btn rv" style="--d: 0.2s" href="#book" role="button" @click.prevent="book.open()">{{ c("closing.cta.label") }}</a>
        </div>
        <p class="rv" style="--d: 0.12s">{{ c("closing.text") }}</p>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import "~/assets/css/pages/about.css";

const props = defineProps<{ ctx: Awaited<ReturnType<typeof usePageContent>> }>();
const { c, ch, img, alt, focus, raw, list, on } = props.ctx;
const book = useBooking();
useReveal({ selector: ".rv,.rv-img,.ahero h1", threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
</script>
