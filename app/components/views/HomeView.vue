<template>
  <main id="top">
    <!-- 1 · 首屏 -->
    <section v-if="on('hero')" class="hero" :aria-label="c('hero.eyebrow')">
      <img class="hbg" :src="img('hero.images.0')" alt="" fetchpriority="high" aria-hidden="true" :style="{ objectPosition: focus('hero.images.0') }" />
      <img v-if="img('hero.images.1')" class="hbg alt" :src="img('hero.images.1')" alt="" aria-hidden="true" :style="{ objectPosition: focus('hero.images.1') }" />
      <div class="veil" aria-hidden="true" />
      <div class="center">
        <p class="eyebrow">{{ c("hero.eyebrow") }}</p>
        <h1 :aria-label="plainText(ch('hero.title'))" v-html="heroTitle" />
        <p>{{ c("hero.lede") }}</p>
        <button class="btn" type="button" @click="book.open()">{{ c("hero.cta.label") }}</button>
      </div>
    </section>

    <!-- 2 · 按目标找治疗 -->
    <section v-if="on('results')" id="results" class="results">
      <div class="wrap stage">
        <div class="head">
          <div class="t">
            <p class="eyebrow">{{ c("results.eyebrow") }}</p>
            <h2 v-html="ch('results.title')" />
          </div>
        </div>
        <div id="fxGrid" class="fxgrid">
          <NuxtLink
            v-for="i in list('results.items')"
            :key="i"
            class="fx rv"
            :style="{ '--d': `${((i % 3) * 0.1 + Math.floor(i / 3) * 0.08).toFixed(2)}s` }"
            :to="goalPath(raw<string>(`results.items.${i}.goal`) ?? '')"
            :aria-label="`${c(`results.items.${i}.name`)}: see treatments`"
          >
            <img :src="img(`results.items.${i}.image`)" :alt="alt(`results.items.${i}.image`)" :style="{ objectPosition: focus(`results.items.${i}.image`) }" />
            <span class="ttl">{{ c(`results.items.${i}.name`) }}</span>
            <ul class="list" aria-hidden="true">
              <li v-for="b in list(`results.items.${i}.bullets`)" :key="b">{{ c(`results.items.${i}.bullets.${b}`) }}</li>
            </ul>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- 3 · 本季专题 -->
    <section v-if="on('season')" id="season" class="promo-sec gut" :aria-label="c('season.label')">
      <div class="promo-in">
        <div class="ph promo-img rv-img">
          <span class="badge">{{ c("season.badge") }}</span>
          <img :src="img('season.image')" :alt="alt('season.image')" :style="{ objectPosition: focus('season.image') }" />
        </div>
        <div class="promo-copy">
          <p class="label rv">{{ c("season.label") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('season.title')" />
          <div class="promo-main rv" style="--d: 0.16s">
            <b>{{ c("season.main.title") }}</b><span>{{ c("season.main.text") }}</span>
          </div>
          <ul class="olist rv" style="--d: 0.24s">
            <li v-for="i in list('season.facts')" :key="i">{{ c(`season.facts.${i}.value`) }}<small>{{ c(`season.facts.${i}.label`) }}</small></li>
          </ul>
          <p v-if="c('season.note')" class="note rv" style="--d: 0.28s; margin: 0; color: var(--muted); font-size: 13px">{{ c("season.note") }}</p>
          <div class="promo-cta rv" style="--d: 0.32s">
            <button class="btn btn-solid btn-lg" type="button" @click="book.open()">{{ c("season.cta.label") }}</button>
          </div>
        </div>
      </div>
    </section>

    <!-- 4 · 最受欢迎（桌面端固定住，随滚动横向移动） -->
    <section v-if="on('stars')" id="stars" ref="starsEl" class="stars" :aria-label="c('stars.title')">
      <div class="pin">
        <div class="shead gut">
          <p class="label rv">{{ c("stars.label") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('stars.title')" />
        </div>
        <div class="sview gut">
          <div class="wrap2">
            <div id="starTrack" ref="trackEl" class="track">
              <NuxtLink v-for="i in list('stars.items')" :key="i" class="star rv" :style="{ '--d': `${(i * 0.1).toFixed(1)}s` }" :to="treatmentPath(raw<string>(`stars.items.${i}.treatment`) ?? '')">
                <span class="ph"><img :src="img(`stars.items.${i}.image`)" :alt="alt(`stars.items.${i}.image`)" loading="lazy" :style="{ objectPosition: focus(`stars.items.${i}.image`) }" /></span>
                <span class="no">{{ String(i + 1).padStart(2, "0") }}</span>
                <h3>{{ c(`stars.items.${i}.name`) }}</h3>
                <p class="effect">{{ c(`stars.items.${i}.effect`) }}</p>
              </NuxtLink>
            </div>
            <div class="sprog" aria-hidden="true">
              <span>01</span><i><b ref="fillEl" /></i><span>{{ String(list("stars.items").length).padStart(2, "0") }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 5 · 关于 -->
    <section v-if="on('about')" id="about" class="about3" :aria-label="c('about.label')">
      <div class="asplit">
        <div class="ph aimg rv-img"><img :src="img('about.image')" :alt="alt('about.image')" :style="{ objectPosition: focus('about.image') }" /></div>
        <div class="acopy">
          <p class="label rv">{{ c("about.label") }}</p>
          <h2 class="big" :aria-label="plainText(ch('about.title'))">
            <span v-for="(line, i) in splitLines(ch('about.title'))" :key="i" class="ln"><i :style="i ? { '--d': `${(i * 0.12).toFixed(2)}s` } : undefined" v-html="line" /></span>
          </h2>
          <p class="rv" style="--d: 0.2s">{{ c("about.text") }}</p>
          <NuxtLink v-if="raw('about.link.path')" class="tlink rv" style="--d: 0.28s" :to="raw<string>('about.link.path')!">
            {{ c("about.link.label") }}<svg viewBox="0 0 30 10" aria-hidden="true"><path d="M0 5h28M24 1l4 4-4 4" fill="none" stroke="currentColor" /></svg>
          </NuxtLink>
        </div>
      </div>
      <div class="values" :aria-label="values.join(', ')">
        <div class="vtrack" aria-hidden="true">
          <template v-for="rep in 2" :key="rep">
            <template v-for="(v, k) in values" :key="k">
              <span><em v-if="k % 2">{{ v }}</em><template v-else>{{ v }}</template></span><i />
            </template>
          </template>
        </div>
      </div>
    </section>

    <!-- 6 · 到店流程 -->
    <section v-if="on('experience')" id="experience" class="journey gut" :aria-label="c('experience.title')">
      <div class="jin">
        <div class="head">
          <p class="label rv">{{ c("experience.label") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('experience.title')" />
        </div>
        <ol id="j4" ref="stepsEl" class="j4 rv" style="--d: 0.16s">
          <li v-for="i in list('experience.steps')" :key="i" tabindex="0" :class="{ on: activeStep === i }" @mouseenter="holdStep(i)" @focus="holdStep(i)">
            <span class="k">{{ String(i + 1).padStart(2, "0") }}</span>
            <h3>{{ c(`experience.steps.${i}.title`) }}</h3>
            <p>{{ c(`experience.steps.${i}.text`) }}</p>
          </li>
        </ol>
        <div class="cta rv">
          <button class="btn btn-solid btn-lg" type="button" @click="book.open({ preset: raw<string>('experience.cta.bookPreset') })">{{ c("experience.cta.label") }}</button>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import "~/assets/css/pages/home.css";

const props = defineProps<{ ctx: Awaited<ReturnType<typeof usePageContent>> }>();
const { c, ch, img, alt, focus, raw, list, on } = props.ctx;
const book = useBooking();

/** 首屏标题：每个词包一层 .w，入场时逐词升起；<em> 里的词包进 em.s（斜体衬线） */
const heroTitle = computed(() => {
  let n = 0;
  return ch("hero.title")
    .split(/(<em>[\s\S]*?<\/em>)/)
    .filter(Boolean)
    .map(part => {
      const em = /^<em>([\s\S]*)<\/em>$/.exec(part);
      const words = (em ? em[1]! : part)
        .trim()
        .split(/\s+/)
        .filter(Boolean)
        .map(word => `<span class="w" style="--i:${n++}"><i>${word}</i></span>`)
        .join(" ");
      return em ? `<em class="s">${words}</em>` : words;
    })
    .join(" ");
});

const values = computed(() => list("about.values").map(i => c(`about.values.${i}`)));

// ---- 最受欢迎：桌面端固定住，随滚动横向移动（移植自原型） ----
const starsEl = ref<HTMLElement>();
const trackEl = ref<HTMLElement>();
const fillEl = ref<HTMLElement>();

function setupStars() {
  const sec = starsEl.value;
  const tr = trackEl.value;
  const fill = fillEl.value;
  if (!sec || !tr || !fill) return () => {};
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const mq = matchMedia("(min-width:901px)");
  const SLOW = 2;
  let travel = 0;
  let cur = 0;
  let target = 0;
  let raf = 0;
  const paint = () => {
    tr.style.transform = `translate3d(${-cur}px,0,0)`;
    fill.style.transform = `scaleX(${travel ? Math.max(0.18, cur / travel) : 1})`;
  };
  const step = () => {
    cur += (target - cur) * 0.09;
    if (Math.abs(target - cur) < 0.5) cur = target;
    paint();
    raf = cur !== target ? requestAnimationFrame(step) : 0;
  };
  const update = () => {
    if (!sec.classList.contains("hs")) return;
    target = Math.min(Math.max(-sec.getBoundingClientRect().top, 0) / SLOW, travel);
    if (reduced) {
      cur = target;
      paint();
      return;
    }
    if (!raf) raf = requestAnimationFrame(step);
  };
  const size = () => {
    if (!mq.matches) {
      sec.classList.remove("hs");
      sec.style.height = "";
      tr.style.transform = "";
      return;
    }
    sec.classList.add("hs");
    tr.style.transform = "";
    travel = Math.max(0, tr.scrollWidth - (tr.parentElement?.clientWidth ?? 0));
    fill.style.transform = "scaleX(.18)";
    sec.style.height = `${innerHeight + travel * SLOW + Math.round(innerHeight * 0.3)}px`;
    update();
  };
  addEventListener("scroll", update, { passive: true });
  addEventListener("resize", size);
  size();
  return () => {
    removeEventListener("scroll", update);
    removeEventListener("resize", size);
    cancelAnimationFrame(raf);
  };
}

// ---- 到店流程：当前步骤的横线走满后交给下一步（移植自原型） ----
const stepsEl = ref<HTMLElement>();
const activeStep = ref(0);
let stepTimer: ReturnType<typeof setInterval> | undefined;
const stopSteps = () => {
  clearInterval(stepTimer);
  stepTimer = undefined;
};
const runSteps = () => {
  stopSteps();
  const count = list("experience.steps").length;
  stepTimer = setInterval(() => (activeStep.value = (activeStep.value + 1) % count), 4200);
};
function holdStep(i: number) {
  stopSteps();
  stepsEl.value?.classList.add("hold");
  activeStep.value = i;
}
function setupSteps() {
  const ol = stepsEl.value;
  if (!ol) return () => {};
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
    ol.querySelectorAll("li").forEach(li => li.classList.add("on"));
    return () => {};
  }
  const leave = () => {
    ol.classList.remove("hold");
    runSteps();
  };
  ol.addEventListener("mouseleave", leave);
  const io = new IntersectionObserver(
    ([entry]) => {
      if (entry?.isIntersecting) {
        if (!stepTimer) runSteps();
      } else stopSteps();
    },
    { threshold: 0.4 }
  );
  io.observe(ol);
  return () => {
    ol.removeEventListener("mouseleave", leave);
    io.disconnect();
    stopSteps();
  };
}

onMounted(() => {
  const cleanups = [setupStars(), setupSteps()];
  onBeforeUnmount(() => cleanups.forEach(fn => fn()));
});
useReveal({ threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
</script>
