<template>
  <main>
    <div class="wrap crumbs">
      <NuxtLink to="/">{{ tx("Home") }}</NuxtLink> / {{ tx("Membership") }} / {{ plainText(ch("hero.titleLines.0")) }} {{ plainText(ch("hero.titleLines.1")) }}
    </div>

    <section v-if="on('hero')" id="top" class="phero">
      <div class="wrap">
        <div ref="frameEl" class="pframe">
          <img :src="img('hero.image')" :alt="alt('hero.image')" :style="{ objectPosition: focus('hero.image') }" />
          <p class="ptag rv" style="--d: 0.5s">
            <span>{{ c("hero.tag.kicker") }}</span><i>{{ c("hero.tag.line") }}</i>
          </p>
          <h1 ref="titleEl" class="ptitle" :aria-label="`${plainText(ch('hero.titleLines.0'))} ${plainText(ch('hero.titleLines.1'))}`">
            <span v-for="i in list('hero.titleLines')" :key="i" class="ln"><i :style="{ '--d': `${0.2 + i * 0.16}s` }" v-html="ch(`hero.titleLines.${i}`)" /></span>
          </h1>
        </div>
        <div class="pbody">
          <div class="pl">
            <p class="eyebrow kicker rv" style="--d: 0.1s">{{ c("hero.kicker") }}</p>
            <p class="pline rv" style="--d: 0.18s" v-html="ch('hero.tagline')" />
            <div class="pjoin rv" style="--d: 0.3s">
              <a class="btn" href="#book" role="button" @click.prevent="book.open({ preset: raw<string>('hero.join.bookPreset') })">{{ c("hero.join.label") }}</a>
              <p v-if="on('talkDialog')" class="ptalk">
                {{ c("hero.talk.lead") }} <a href="#faq" aria-haspopup="dialog" aria-controls="talk" @click.prevent="talk?.showModal()">{{ c("hero.talk.linkLabel") }} <span aria-hidden="true">→</span></a>
              </p>
            </div>
          </div>
          <div class="pr">
            <p class="lede rv" style="--d: 0.26s">{{ c("hero.lede") }}</p>
            <div class="pprice rv" style="--d: 0.32s">
              <p class="pricetag"><b>{{ c("hero.price.amount") }}</b><span>{{ c("hero.price.unit") }}</span></p>
              <p class="pricenote">{{ c("hero.price.note") }}</p>
            </div>
            <div class="chips rv" style="--d: 0.38s">
              <span v-for="i in list('hero.chips')" :key="i">{{ c(`hero.chips.${i}`) }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section v-if="on('included')" id="how" class="tsec alt">
      <div class="wrap">
        <div class="hhead">
          <div class="head">
            <p class="eyebrow rv">{{ c("included.eyebrow") }}</p>
            <h2 class="rv" style="--d: 0.08s" v-html="ch('included.title')" />
          </div>
          <div class="hintro rv" style="--d: 0.16s">
            <p>{{ c("included.intro") }}</p>
            <p v-if="c('included.tagline')" class="tagline">{{ c("included.tagline") }}</p>
          </div>
        </div>
        <div id="inc3" class="inc3">
          <article v-for="i in list('included.cards')" :key="i">
            <p class="num rv" :style="{ '--d': `${(i * 0.3).toFixed(1)}s` }">{{ c(`included.cards.${i}.number`) }}</p>
            <p class="cap">{{ c(`included.cards.${i}.caption`) }}</p>
            <span class="lbl">{{ c(`included.cards.${i}.label`) }}</span>
            <h3>{{ c(`included.cards.${i}.title`) }}</h3>
            <p>{{ c(`included.cards.${i}.text`) }}</p>
            <NuxtLink v-if="raw(`included.cards.${i}.link.path`)" class="more" :to="raw<string>(`included.cards.${i}.link.path`)!">{{ c(`included.cards.${i}.link.label`) }} →</NuxtLink>
          </article>
        </div>
        <div class="incfoot rv">
          <span>{{ c("included.foot.note") }}</span>
          <a href="#book" role="button" @click.prevent="book.open({ preset: raw<string>('included.foot.link.bookPreset') })">{{ c("included.foot.link.label") }} →</a>
        </div>
      </div>
    </section>

    <section v-if="on('faq')" id="faq" class="tsec">
      <div class="wrap faqrev">
        <div class="faqside">
          <div class="head">
            <p class="eyebrow rv">{{ c("faq.eyebrow") }}</p>
            <h2 class="rv" style="--d: 0.08s" v-html="ch('faq.title')" />
          </div>
          <div class="ph rv-img"><img :src="img('faq.image')" :alt="alt('faq.image')" :style="{ objectPosition: focus('faq.image') }" /></div>
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
        <a class="btn rv" style="--d: 0.2s" href="#book" role="button" @click.prevent="book.open({ preset: raw<string>('closing.cta.bookPreset') })">{{ c("closing.cta.label") }}</a>
      </div>
    </section>

    <!-- Talk to us first -->
    <dialog v-if="on('talkDialog')" id="talk" ref="talk" class="talkdlg" aria-labelledby="talkT" @click="onBackdrop">
      <div class="tin">
        <button type="button" class="x" aria-label="Close" @click="talk?.close()">×</button>
        <div class="tx">
          <p class="eyebrow cl">{{ c("talkDialog.eyebrow") }}</p>
          <h2 id="talkT" v-html="ch('talkDialog.title')" />
          <p class="lead">{{ c("talkDialog.lead") }}</p>
          <dl>
            <template v-for="i in list('talkDialog.rows')" :key="i">
              <div v-if="on(`talkDialog.rows.${i}`) && c(`talkDialog.rows.${i}.html`)">
                <dt>{{ c(`talkDialog.rows.${i}.label`) }}</dt>
                <dd v-html="ch(`talkDialog.rows.${i}.html`)" />
              </div>
            </template>
          </dl>
        </div>
        <div class="bk">
          <p class="eyebrow">{{ c("talkDialog.consult.eyebrow") }}</p>
          <h3 v-html="ch('talkDialog.consult.title')" />
          <ul>
            <li v-for="i in list('talkDialog.consult.bullets')" :key="i">{{ c(`talkDialog.consult.bullets.${i}`) }}</li>
          </ul>
          <a class="btn" href="#book" role="button" @click.prevent="openConsult">{{ c("talkDialog.consult.cta") }} →</a>
          <p class="fine">{{ c("talkDialog.consult.fine") }}</p>
        </div>
      </div>
    </dialog>
  </main>
</template>

<script setup lang="ts">
import "~/assets/css/pages/membership.css";

const props = defineProps<{ ctx: Awaited<ReturnType<typeof usePageContent>> }>();
const { c, ch, img, alt, focus, raw, list, on } = props.ctx;
const { tx } = useTx();
const book = useBooking();

const talk = ref<HTMLDialogElement>();
const frameEl = ref<HTMLElement>();
const titleEl = ref<HTMLElement>();
const faqEl = ref<HTMLElement>();

const onBackdrop = (event: MouseEvent) => {
  if (event.target === talk.value) talk.value?.close();
};
function openConsult() {
  talk.value?.close();
  book.open({ preset: "consultation" });
}

useOneOpen(faqEl);
useReveal();
useFitChips();
// 首屏：图片与标题在首帧之后淡入
onMounted(() => requestAnimationFrame(() => requestAnimationFrame(() => [frameEl.value, titleEl.value].forEach(el => el?.classList.add("in")))));
</script>
