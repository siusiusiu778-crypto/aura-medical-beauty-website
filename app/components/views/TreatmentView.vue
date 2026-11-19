<template>
  <main>
    <div class="wrap crumbs">
      <NuxtLink to="/">{{ tx("Home") }}</NuxtLink> / {{ bi(entity.category.name) }} / {{ c("hero.crumb") || bi(entity.name) }}
    </div>

    <section v-if="on('hero')" id="top" class="thtop">
      <div class="wrap thero2">
        <div class="tframe">
          <div class="ph rv-img"><img :src="img('hero.image')" :alt="alt('hero.image')" :style="{ objectPosition: focus('hero.image') }" /></div>
        </div>
        <div class="tx">
          <p class="eyebrow kicker rv" style="--d: 0.15s">{{ c("hero.kicker") || bi(entity.category.name) }}</p>
          <h1 class="big" :aria-label="plainText(ch('hero.title'))">
            <span v-for="(line, i) in splitLines(ch('hero.title'))" :key="i" class="ln"><i :style="{ '--d': `${0.25 + i * 0.12}s` }" v-html="line" /></span>
          </h1>
          <p class="lede rv" style="--d: 0.45s">{{ c("hero.lede") }}</p>
          <div v-if="list('hero.chips').length" class="chips rv" style="--d: 0.52s">
            <span v-for="i in list('hero.chips')" :key="i">{{ c(`hero.chips.${i}`) }}</span>
          </div>
          <div v-if="on('hero.bookbox') && list('hero.bookbox.options').length" class="bookbox rv" style="--d: 0.6s">
            <details :ref="el => (box.el.value = el as HTMLDetailsElement)" class="bbrow" :class="{ up: box.up.value }" @toggle="box.onToggle">
              <summary>
                <span class="bbl" :title="box.picked.value >= 0 ? optionText(box.picked.value) : undefined">{{ box.shown(c("hero.bookbox.label")) }}</span>
                <span class="chev" aria-hidden="true">⌄</span>
              </summary>
              <div class="bbopts">
                <label v-for="i in list('hero.bookbox.options')" :key="i" class="bbopt" :class="{ sel: box.picked.value === i }" @click="box.pick(i, $event)">
                  <input type="radio" name="appt" :checked="box.picked.value < 0 ? i === 0 : box.picked.value === i" /> {{ c(`hero.bookbox.options.${i}`) }}
                </label>
              </div>
            </details>
            <a class="btn" href="#book" role="button" @click.prevent="box.proceed">{{ c("hero.bookbox.cta") }}</a>
          </div>
          <div v-if="c('hero.learnMore') && on('how')" class="ctas rv" style="--d: 0.7s">
            <a class="tlink" href="#how">{{ c("hero.learnMore") }}</a>
          </div>
        </div>
      </div>
    </section>

    <section v-if="on('how')" id="how" class="tsec alt">
      <div class="wrap">
        <div class="hhead">
          <div class="head">
            <p class="eyebrow rv">{{ c("how.eyebrow") }}</p>
            <h2 class="rv" style="--d: 0.08s" v-html="ch('how.title')" />
          </div>
          <div class="hintro rv" style="--d: 0.16s">
            <div v-html="ch('how.intro')" />
            <p v-if="c('how.tagline')" class="tagline">{{ c("how.tagline") }}</p>
          </div>
        </div>
        <div class="bcards photo">
          <div v-for="i in list('how.cards')" :key="i" class="rv" :style="{ '--d': `${i * 0.1}s` }">
            <span class="bimg"><img :src="img(`how.cards.${i}.image`)" :alt="alt(`how.cards.${i}.image`)" loading="lazy" :style="{ objectPosition: focus(`how.cards.${i}.image`) }" /></span>
            <h3 :data-zone="c(`how.cards.${i}.zone`) || undefined">{{ c(`how.cards.${i}.title`) }}</h3>
            <p>{{ c(`how.cards.${i}.text`) }}</p>
          </div>
        </div>
        <p v-if="c('how.note')" class="fda rv">{{ c("how.note") }}</p>
      </div>
    </section>

    <!-- 适合人群 -->
    <section v-if="on('fit')" id="fit" class="tsec">
      <div class="wrap">
        <div class="head">
          <p class="eyebrow rv">{{ c("fit.eyebrow") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('fit.title')" />
        </div>
        <div class="fit5">
          <div class="rv" style="--d: 0.14s">
            <h4>{{ c("fit.yes.title") }}</h4>
            <ul class="rows yes">
              <li v-for="i in list('fit.yes.items')" :key="i">{{ c(`fit.yes.items.${i}`) }}</li>
            </ul>
          </div>
          <div class="rv" style="--d: 0.24s">
            <h4>{{ c("fit.no.title") }}</h4>
            <ul class="rows no">
              <li v-for="i in list('fit.no.items')" :key="i">{{ c(`fit.no.items.${i}`) }}</li>
            </ul>
          </div>
          <div class="ph rv-img fitimg"><img :src="img('fit.image')" :alt="alt('fit.image')" :style="{ objectPosition: focus('fit.image') }" /></div>
        </div>
        <p v-if="c('fit.pairNote.html')" class="pairnote rv">
          <span class="pl">{{ c("fit.pairNote.label") }}</span><span class="pt" v-html="ch('fit.pairNote.html')" />
        </p>
      </div>
    </section>

    <!-- 六件事（Gold Skin Analysis 用它代替适合人群） -->
    <section v-if="on('grid') && raw('grid')" id="fit" class="tsec">
      <div class="wrap">
        <div class="head ctr">
          <p class="eyebrow rv">{{ c("grid.eyebrow") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('grid.title')" />
        </div>
        <ol class="g6">
          <li v-for="i in list('grid.items')" :key="i" class="rv" :style="{ '--d': `${(i * 0.08).toFixed(2)}s` }">
            <span class="k">{{ String(i + 1).padStart(2, "0") }}</span>
            <h3>{{ c(`grid.items.${i}.title`) }}</h3>
            <p>{{ c(`grid.items.${i}.text`) }}</p>
          </li>
        </ol>
        <p v-if="c('grid.foot')" class="g6foot rv" v-html="ch('grid.foot')" />
      </div>
    </section>

    <section v-if="on('tech')" :id="raw<string>('tech.anchor') || 'tech'" class="techband">
      <div class="tgrid">
        <div class="ph rv-img"><img :src="img('tech.image')" :alt="alt('tech.image')" loading="lazy" :style="{ objectPosition: focus('tech.image') }" /></div>
        <div class="tcopy">
          <p class="eyebrow rv">{{ c("tech.eyebrow") }}</p>
          <h2 class="rv" style="--d: 0.08s" v-html="ch('tech.title')" />
          <ol class="tsteps">
            <li v-for="i in list('tech.steps')" :key="i" class="rv" :style="{ '--d': `${(0.14 + i * 0.08).toFixed(2)}s` }">
              <span class="n">{{ String(i + 1).padStart(2, "0") }}</span>
              <div>
                <b>{{ c(`tech.steps.${i}.title`) }}</b>
                <div class="tdd" v-html="ch(`tech.steps.${i}.text`)" />
              </div>
            </li>
          </ol>
        </div>
      </div>
    </section>

    <section v-if="on('faq')" id="faq" class="tsec alt">
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

    <!-- 没有正式文案的页面：原型里只有标题和占位说明的文本区块，按原样显示 -->
    <section v-for="i in list('extras')" :key="`extra-${i}`" :id="raw<boolean>(`extras.${i}.center`) ? 'faq' : undefined" class="tsec" :class="{ alt: raw<string>(`extras.${i}.tone`) === 'alt' }">
      <div class="wrap" :class="{ faqnarrow: raw<boolean>(`extras.${i}.center`) }">
        <div class="head" :style="raw<boolean>(`extras.${i}.center`) ? 'text-align:center;justify-items:center' : undefined">
          <p class="eyebrow">{{ c(`extras.${i}.eyebrow`) }}</p>
          <h2 v-html="ch(`extras.${i}.title`)" />
        </div>
        <p class="placeholder" :style="raw<boolean>(`extras.${i}.center`) ? 'text-align:center' : undefined">{{ c(`extras.${i}.text`) }}</p>
      </div>
    </section>

    <section v-if="on('closing')" id="book" class="closing tsec">
      <img :src="img('closing.image')" alt="" aria-hidden="true" :style="{ objectPosition: focus('closing.image') }" />
      <div class="wrap">
        <h2 class="rv" v-html="ch('closing.title')" />
        <p class="rv" style="--d: 0.1s">{{ c("closing.text") }}</p>
        <a class="btn rv" style="--d: 0.2s" href="#book" role="button" @click.prevent="book.open()">{{ c("closing.cta") }}</a>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import "~/assets/css/pages/treatment.css";

const props = defineProps<{ ctx: Awaited<ReturnType<typeof useTreatment>> }>();
const { c, ch, img, alt, focus, raw, list, on, entity } = props.ctx;
const { tx, bi } = useTx();
const book = useBooking();
useFooterStyle(raw<string>("layout.footer") === "simple");

const optionText = (i: number) => c(`hero.bookbox.options.${i}`);
// 下拉选项的原始文字（不带编辑预览的隐形标记）
const box = useBookBox(
  () => list("hero.bookbox.options").map(i => bi(raw<{ en?: string; zh?: string }>(`hero.bookbox.options.${i}`))),
  () => "Complimentary Consultation",
  () => entity.value.slug
);

const faqEl = ref<HTMLElement>();
useOneOpen(faqEl);
useReveal();
useFitChips();
</script>
