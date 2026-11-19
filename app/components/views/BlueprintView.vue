<template>
  <main>
    <section v-if="on('hero')" id="top" class="fbhero">
      <div class="fbmap" v-html="mapHtml" />
      <div class="fbtop">
        <div class="fbread">
          <p class="fbstep"><span>{{ stepText }}</span> · {{ c("hero.map.kicker") }}</p>
          <p class="fbtitle">{{ labelText }}</p>
          <p class="fbdesc" aria-live="polite">{{ capText }}</p>
        </div>
        <div class="fbnav">
          <button type="button" class="fbarrow" aria-label="Previous proportion" @click="step(-1)"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5" /></svg></button>
          <div ref="chipsEl" class="fbchips" :class="{ auto }" role="group" aria-label="Show a proportion">
            <button v-for="(m, k) in modes" :key="m.key" type="button" :aria-pressed="current === k ? 'true' : 'false'" :class="{ done: current > k }" @click="pick(k)"><i>{{ String(k + 1).padStart(2, "0") }}</i>{{ m.short }}</button>
          </div>
          <button type="button" class="fbarrow" aria-label="Next proportion" @click="step(1)"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3l5 5-5 5" /></svg></button>
        </div>
      </div>
      <div class="fbin">
        <div class="fbcopy">
          <p class="eyebrow kicker rv" style="--d: 0.1s">{{ c("hero.eyebrow") }}</p>
          <h1 class="big" :aria-label="plainText(ch('hero.title'))">
            <span v-for="(line, i) in splitLines(ch('hero.title'))" :key="i" class="ln"><i :style="{ '--d': `${0.2 + i * 0.1}s` }" v-html="line" /></span>
          </h1>
          <p class="lede rv" style="--d: 0.45s">{{ c("hero.lede") }}</p>
          <div class="fbcta rv" style="--d: 0.55s"><a class="btn" href="#book" role="button" @click.prevent="book.open()">{{ c("hero.cta.label") }}</a></div>
        </div>
      </div>
    </section>

    <section v-if="on('steps')" id="steps" class="tsec alt">
      <div class="wrap">
        <div class="head">
          <p class="eyebrow rv">{{ c("steps.eyebrow") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('steps.title')" />
        </div>
        <div class="bcards txt" style="margin-top: clamp(40px, 5vw, 64px)">
          <div v-for="i in list('steps.items')" :key="i" class="rv" :style="i ? { '--d': `${(i * 0.08).toFixed(2)}s` } : undefined">
            <span class="k">{{ String(i + 1).padStart(2, "0") }}</span>
            <h3>{{ c(`steps.items.${i}.title`) }}</h3>
            <p>{{ c(`steps.items.${i}.text`) }}</p>
          </div>
        </div>
      </div>
    </section>

    <section v-if="on('aesthetic')" id="aesthetic" class="tsec fbaes">
      <div class="wrap">
        <div class="head">
          <p class="eyebrow rv">{{ c("aesthetic.eyebrow") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('aesthetic.title')" />
        </div>
        <p class="intro rv" style="--d: 0.14s">
          {{ introLines[0] }}<i v-if="introLines[1]" v-html="introLines.slice(1).join(' ')" />
        </p>
        <div class="fbrows">
          <div v-for="i in list('aesthetic.rows')" :key="i" class="fbrow">
            <div class="ph rv-img">
              <img :src="img(`aesthetic.rows.${i}.image`)" :alt="alt(`aesthetic.rows.${i}.image`)" loading="lazy" :style="{ objectPosition: focus(`aesthetic.rows.${i}.image`) }" />
              <span v-if="dotsOf(i)" class="dotsw" v-html="dotsOf(i)" />
            </div>
            <div class="rv">
              <span class="n">{{ String(i + 1).padStart(2, "0") }}</span>
              <span class="k">{{ c(`aesthetic.rows.${i}.name`) }}</span>
              <h3>{{ c(`aesthetic.rows.${i}.title`) }}</h3>
              <p>{{ c(`aesthetic.rows.${i}.text`) }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 客户评价：只有真实评价（没有 sample 标记）才展示；示意用的评价按美国 FTC 规定不得当真实评价发布 -->
    <section v-if="on('reviews') && reviews.length" id="reviews" class="tsec alt">
      <div class="wrap fbrv">
        <div class="head">
          <p class="eyebrow rv">{{ c("reviews.eyebrow") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('reviews.title')" />
        </div>
        <div class="rvrow">
          <figure v-for="(r, n) in reviews" :key="r" class="rv" :style="n ? { '--d': `${n * 0.1}s` } : undefined">
            <p class="stars" role="img" :aria-label="`Rated ${raw<number>(`reviews.items.${r}.rating`) ?? 5} out of 5`">
              <svg v-for="s in raw<number>(`reviews.items.${r}.rating`) ?? 5" :key="s" viewBox="0 0 20 20"><path d="M10 1.6l2.47 5.3 5.8.7-4.27 4 1.1 5.74L10 14.5l-5.1 2.84 1.1-5.74-4.27-4 5.8-.7z" /></svg>
            </p>
            <blockquote>{{ c(`reviews.items.${r}.quote`) }}</blockquote>
            <figcaption><span>{{ c(`reviews.items.${r}.name`) }}</span></figcaption>
          </figure>
        </div>
        <a class="btn rv" href="#book" role="button" @click.prevent="book.open()">{{ c("reviews.cta.label") }}</a>
      </div>
    </section>

    <section v-if="on('faq')" id="faq" class="tsec">
      <div class="wrap faqgrid">
        <div class="head">
          <p class="eyebrow rv">{{ c("faq.eyebrow") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('faq.title')" />
        </div>
        <div ref="faqEl" class="faqlist">
          <details v-for="i in list('faq.items')" :key="i" class="rv">
            <summary>{{ c(`faq.items.${i}.q`) }}</summary>
            <div v-html="ch(`faq.items.${i}.a`)" />
          </details>
        </div>
      </div>
    </section>

    <section v-if="on('closing')" id="book" class="closing tsec">
      <img :src="img('closing.image')" alt="" aria-hidden="true" :style="{ objectPosition: focus('closing.image') }" />
      <div class="wrap">
        <h2 class="rv" v-html="ch('closing.title')" />
        <p class="rv" style="--d: 0.1s">{{ c("closing.text") }}</p>
        <a class="btn rv" style="--d: 0.2s" href="#book" role="button" @click.prevent="book.open()">{{ c("closing.cta.label") }}</a>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import "~/assets/css/pages/blueprint.css";
// 脸部比例图与图上的圆点是代码资产（由原型抽出的 SVG），不进 CMS；图片地址与文字来自内容
import mapSvg from "~/assets/fragments/facial-blueprint-map.svg.html?raw";
import dotsScale from "~/assets/fragments/facial-blueprint-dots-scale.svg.html?raw";
import dotsLine from "~/assets/fragments/facial-blueprint-dots-line.svg.html?raw";

const props = defineProps<{ ctx: Awaited<ReturnType<typeof usePageContent>> }>();
const { c, ch, img, alt, focus, raw, list, on } = props.ctx;
const book = useBooking();

const mapHtml = computed(() => mapSvg.replace("{{front}}", img("hero.map.front")).replace("{{side}}", img("hero.map.side")));
const dotsOf = (i: number) => ({ scale: dotsScale, line: dotsLine })[raw<string>(`aesthetic.rows.${i}.dots`) ?? ""] ?? "";
const introLines = computed(() => splitLines(ch("aesthetic.intro")));
// 真实评价才展示（sample:true 的不输出）
const reviews = computed(() => list("reviews.items").filter(i => raw<boolean>(`reviews.items.${i}.sample`) !== true));

const modes = computed(() =>
  list("hero.map.modes").map(i => ({
    key: raw<string>(`hero.map.modes.${i}.key`) ?? "",
    // 按钮上的短名称：内容里有 short 就用它，没有时取 name 去掉开头的 "Facial "（如 Facial thirds → Thirds）
    short: c(`hero.map.modes.${i}.short`) || c(`hero.map.modes.${i}.name`).replace(/^Facial\s+/i, "").replace(/^./, ch => ch.toUpperCase()),
    label: c(`hero.map.modes.${i}.name`),
    caption: c(`hero.map.modes.${i}.caption`),
    view: raw<string>(`hero.map.modes.${i}.view`) ?? "front"
  }))
);

// 五种比例轮播（移植自原型脚本）：先画出完整的脸部图，再每 4.8 秒换下一种；点击跳到某一种后继续
const current = ref(-1);
const auto = ref(false);
const chipsEl = ref<HTMLElement>();
const faqEl = ref<HTMLElement>();
const stepText = computed(() => (current.value < 0 ? c("hero.map.stepIntro") : `0${current.value + 1} / 0${modes.value.length}`));
const labelText = computed(() => (current.value < 0 ? c("hero.map.label") : modes.value[current.value]?.label));
const capText = computed(() => (current.value < 0 ? c("hero.map.caption") : modes.value[current.value]?.caption));

let timer: ReturnType<typeof setInterval> | null = null;
let reduce = false;

function random(a: number, b: number) {
  return `${(a + Math.random() * (b - a)).toFixed(2)}s`;
}
function applyScene() {
  const svg = document.querySelector<SVGElement>(".fbsvg");
  if (!svg) return;
  const mode = modes.value[current.value];
  svg.querySelectorAll(".ov").forEach(g => g.classList.toggle("on", g.getAttribute("data-ov") === mode?.key));
  svg.classList.add("focus");
  svg.querySelector("#fbFront")?.classList.toggle("off", mode?.view !== "front");
  svg.querySelector("#fbSide")?.classList.toggle("off", mode?.view !== "side");
}
function show(index: number) {
  current.value = index;
  applyScene();
}
function restartBar() {
  auto.value = false;
  nextTick(() => {
    void chipsEl.value?.offsetWidth;
    auto.value = true;
  });
}
function restart() {
  if (timer) clearInterval(timer);
  timer = null;
  if (reduce || !modes.value.length) return;
  restartBar();
  timer = setInterval(() => {
    if (!document.hidden) {
      show((current.value + 1) % modes.value.length);
      restartBar();
    }
  }, 4800);
}
function pick(index: number) {
  show(index);
  restart();
  const button = chipsEl.value?.children[index] as HTMLElement | undefined;
  const chips = chipsEl.value;
  if (button && chips && chips.scrollWidth > chips.clientWidth) chips.scrollTo({ left: chips.scrollLeft + button.getBoundingClientRect().left - chips.getBoundingClientRect().left, behavior: "smooth" });
}
function step(delta: number) {
  const n = modes.value.length;
  pick(((current.value < 0 ? 0 : current.value) + delta + n) % n);
}

onMounted(() => {
  reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  // 每个点和线各自随机的节奏，"分析"的闪烁不会形成规律
  const svg = document.querySelector<SVGElement>(".fbsvg");
  svg?.querySelectorAll<SVGElement>(".md circle").forEach(el => {
    el.style.setProperty("--td", random(2.2, 6.5));
    el.style.setProperty("--tl", random(0.8, 6));
  });
  document.querySelectorAll<SVGElement>(".fbrow .dots circle").forEach(el => {
    el.style.setProperty("--td", random(2.2, 6.5));
    el.style.setProperty("--tl", random(0.3, 4));
  });
  svg?.querySelectorAll<SVGElement>(".ml line").forEach(el => {
    el.style.setProperty("--sd", random(2.5, 7));
    el.style.setProperty("--sl", random(0.8, 7));
  });
  svg?.querySelectorAll<SVGElement>(".kd").forEach(el => {
    el.style.setProperty("--pd", random(1.6, 3.6));
    el.style.setProperty("--pl", `-${random(0, 3)}`);
  });
  if (reduce) show(0);
  else pick(0);
});
onBeforeUnmount(() => {
  if (timer) clearInterval(timer);
});

useOneOpen(faqEl);
useReveal();
</script>
