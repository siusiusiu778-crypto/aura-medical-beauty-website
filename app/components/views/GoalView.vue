<template>
  <main>
    <div class="wrap crumbs">
      <NuxtLink to="/">{{ tx("Home") }}</NuxtLink> / <span v-html="plainText(ch('hero.title'))" />
    </div>
    <div class="wrap">
      <div class="goalhd">
        <p class="eyebrow">{{ c("hero.eyebrow") }}</p>
        <h1 v-html="ch('hero.title')" />
        <p>{{ c("hero.lede") }}</p>
      </div>
    </div>
    <div class="wrap">
      <div class="grp2" style="padding-top: 0">
        <div v-if="list('groups').length" class="chips2">
          <div class="wrap">
            <a href="#" :class="{ on: group === 'all' }" @click.prevent="group = 'all'">{{ tx("All") }}</a>
            <a v-for="i in list('groups')" :key="i" href="#" :class="{ on: group === raw<string>(`groups.${i}.key`) }" @click.prevent="group = raw<string>(`groups.${i}.key`) ?? 'all'">{{ c(`groups.${i}.label`) }}</a>
          </div>
        </div>
        <NuxtLink
          v-for="i in list('items')"
          v-show="group === 'all' || raw<string>(`items.${i}.group`) === group"
          :key="i"
          class="row"
          :to="treatmentPath(raw<string>(`items.${i}.treatment`) ?? '')"
          :data-group="raw<string>(`items.${i}.group`) ?? 'all'"
        >
          <span class="ph"><img :src="img(`items.${i}.image`)" :alt="alt(`items.${i}.image`)" :style="{ objectPosition: focus(`items.${i}.image`) }" /></span>
          <div>
            <h3>{{ c(`items.${i}.title`) }}</h3>
            <p class="ex">{{ c(`items.${i}.text`) }}</p>
            <div v-if="list(`items.${i}.tags`).length" class="tg">
              <span v-for="t in list(`items.${i}.tags`)" :key="t">{{ c(`items.${i}.tags.${t}`) }}</span>
            </div>
            <span class="lm">{{ tx("Learn More") }} <span aria-hidden="true">→</span></span>
          </div>
        </NuxtLink>
      </div>
    </div>
    <section v-if="on('closing')" id="book" class="cta">
      <div class="wrap">
        <p class="eyebrow" style="color: inherit; opacity: 0.7">{{ c("closing.eyebrow") }}</p>
        <h2 v-html="ch('closing.title')" />
        <p>{{ c("closing.text") }}</p>
        <a class="btn" href="#book" role="button" @click.prevent="book.open()">{{ c("closing.cta") }}</a>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import "~/assets/css/pages/goal.css";

const props = defineProps<{ ctx: Awaited<ReturnType<typeof useGoal>> }>();
const { c, ch, img, alt, focus, raw, list, on } = props.ctx;
const { tx } = useTx();
const book = useBooking();
const group = ref("all");
</script>
