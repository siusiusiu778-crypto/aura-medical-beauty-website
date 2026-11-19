<template>
  <div>
    <div class="scrim" :class="{ on: state.open }" @click="close" />
    <div
      id="drawer"
      ref="drawerEl"
      class="drawer"
      :class="{ on: state.open }"
      role="dialog"
      aria-modal="true"
      aria-labelledby="dTitle"
      :aria-hidden="state.open ? 'false' : 'true'"
      :inert="!state.open"
    >
      <div class="dh">
        <div class="top">
          <h2 id="dTitle">{{ c("booking.title") }}</h2>
          <button ref="closeEl" class="close" type="button" aria-label="Close booking" @click="close">×</button>
        </div>
        <div class="steps" aria-hidden="true">
          <span v-for="n in 4" :key="n" :class="{ on: n - 1 <= st.step }" />
        </div>
        <div class="stepname">{{ st.sent ? tx("Request sent") : stepName }}</div>
      </div>

      <div ref="bodyEl" class="db">
        <!-- 完成 -->
        <div v-if="st.sent" class="done">
          <p class="eyebrow">{{ c("booking.done.eyebrow") }}</p>
          <h3>{{ fill(c("booking.done.title")) }}</h3>
          <p>{{ fill(c("booking.done.text")) }}</p>
          <button class="btn btn-line" type="button" @click="close">{{ tx("Back to site") }}</button>
        </div>

        <!-- 第 1 步：选项目 -->
        <template v-else-if="st.step === 0">
          <button type="button" class="opt" :aria-pressed="st.tx === consultLabel" @click="pick(consultLabel, null)">
            <b>{{ c("booking.consult.title") }}</b>
            <small>{{ c("booking.consult.text") }}</small>
          </button>
          <input v-model="st.q" class="search" type="search" :placeholder="c('booking.searchPlaceholder')" :aria-label="c('booking.searchPlaceholder')" />
          <div v-for="(group, gi) in groups" :key="gi" class="group">
            <h5>{{ group.title }}</h5>
            <div class="items">
              <button v-for="(item, ii) in group.items" :key="ii" type="button" class="item" :aria-pressed="st.tx === item.title" @click="pick(item.title, item.slug)">
                <b>{{ item.title }}</b>
                <small>{{ item.blurb }}</small>
                <span class="pr">{{ item.price }}</span>
              </button>
            </div>
          </div>
          <p v-if="!groups.length" class="note">{{ tx("No treatments match that search.") }}</p>
        </template>

        <!-- 第 2 步：希望的时间 -->
        <template v-else-if="st.step === 1">
          <div class="group">
            <h5>{{ tx("Day") }}</h5>
            <div class="dates">
              <button v-for="(d, i) in days" :key="i" type="button" class="date" :aria-pressed="st.dayIndex === i" @click="chooseDay(i)">
                <span>{{ fmtDay(d) }}</span>
                <b>{{ d.getDate() }}</b>
              </button>
            </div>
          </div>
          <div class="group">
            <h5>{{ tx("Time") }}<template v-if="st.dayIndex !== null"> · {{ fmtFull(days[st.dayIndex]!) }}</template></h5>
            <div v-if="st.dayIndex !== null" class="times">
              <button v-for="t in times" :key="t" type="button" class="chip" :aria-pressed="st.time === t" @click="st.time = t">{{ t }}</button>
            </div>
            <p v-else class="note">{{ tx("Choose a day to see time options.") }}</p>
          </div>
          <p class="note">{{ c("booking.locationNote") }}</p>
        </template>

        <!-- 第 3 步：联系方式 -->
        <template v-else-if="st.step === 2">
          <div class="field">
            <label for="fName">{{ tx("Full name") }}</label>
            <input id="fName" v-model="st.name" autocomplete="name" />
            <span class="err">{{ errors.name }}</span>
          </div>
          <div class="field">
            <label for="fEmail">{{ tx("Email") }}</label>
            <input id="fEmail" v-model="st.email" type="email" autocomplete="email" />
            <span class="err">{{ errors.email }}</span>
          </div>
          <div class="field">
            <label for="fPhone">{{ tx("Mobile number") }}</label>
            <input id="fPhone" v-model="st.phone" type="tel" autocomplete="tel" />
            <span class="err">{{ errors.phone }}</span>
          </div>
          <div class="field">
            <label for="fNotes">{{ tx("Anything we should know? (optional)") }}</label>
            <textarea id="fNotes" v-model="st.notes" rows="3" />
          </div>
          <label class="check"><input v-model="st.ok" type="checkbox" /> <span v-html="consentHtml" /></label>
          <span class="err">{{ errors.ok }}</span>
          <!-- 蜜罐：访客看不到，机器人会填 -->
          <input v-model="st.website" class="hp" type="text" tabindex="-1" autocomplete="off" aria-hidden="true" name="website" />
        </template>

        <!-- 第 4 步：确认 -->
        <template v-else>
          <div class="summary">
            <div><span>{{ tx("Treatment") }}</span><b>{{ st.tx }}</b></div>
            <div v-if="whenText"><span>{{ tx("When") }}</span><b>{{ whenText }}</b></div>
            <div><span>{{ tx("Name") }}</span><b>{{ st.name }}</b></div>
            <div><span>{{ tx("Mobile") }}</span><b>{{ st.phone }}</b></div>
          </div>
          <p class="note">{{ c("booking.intakeNote") }}</p>
          <p v-if="st.serverError" class="srverr" role="alert">{{ st.serverError }}</p>
        </template>
      </div>

      <div class="df">
        <button class="btn btn-line" type="button" :style="{ visibility: st.step === 0 || st.sent ? 'hidden' : 'visible' }" @click="back">{{ tx("Back") }}</button>
        <span class="sel">{{ st.sent ? "" : selText }}</span>
        <button v-if="!st.sent" class="btn btn-solid" type="button" :disabled="st.sending" @click="next">{{ st.step === 3 ? c("booking.submitLabel") : tx("Continue") }}</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 预约抽屉：四步收集线索（选项目 → 希望的时间 → 联系方式 → 确认），最后 POST /leads。
 * 它只提交"预约请求"，由诊所确认，不会产生"已预订"。文案来自 CMS「site.booking」，
 * 只有校验提示、按钮状态这类功能性文字在代码里。
 */
const { c, ch, list, raw } = await useSite();
const { tx } = useTx();
const { state, close } = useBooking();
const api = useApi();
const route = useRoute();
const config = useRuntimeConfig();

// 摘要里用的项目名（卡片上的大标题是 CMS 里的 booking.consult.title）
const consultLabel = computed(() => tx("Complimentary Consultation"));
const consentHtml = computed(() => ch("booking.consentLabel"));
const times = computed(() => raw<string[]>("booking.times") ?? []);

const st = reactive({
  step: 0,
  tx: "",
  slug: null as string | null,
  q: "",
  dayIndex: null as number | null,
  time: "",
  name: "",
  email: "",
  phone: "",
  notes: "",
  ok: false,
  website: "",
  sent: false,
  sending: false,
  serverError: "",
  startedAt: 0
});
const errors = reactive({ name: "", email: "", phone: "", ok: "" });
const hint = ref("");

// 浏览器端才生成日期（接下来 5 个非周日）
const days = ref<Date[]>([]);
function makeDays() {
  const out: Date[] = [];
  for (let i = 1; out.length < 5 && i < 14; i += 1) {
    const d = new Date();
    d.setDate(d.getDate() + i);
    if (d.getDay() !== 0) out.push(d);
  }
  days.value = out;
}
const fmtDay = (d: Date) => d.toLocaleDateString("en-US", { weekday: "short" });
const fmtFull = (d: Date) => d.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });

const stepName = computed(() => c(`booking.stepLabels.${st.step}`));
const whenText = computed(() => (st.dayIndex !== null && st.time ? `${fmtFull(days.value[st.dayIndex]!)} · ${st.time}` : ""));
const selText = computed(() => {
  if (hint.value) return hint.value;
  return [st.tx, st.dayIndex !== null && days.value[st.dayIndex] ? fmtDay(days.value[st.dayIndex]!) : "", st.time].filter(Boolean).join(" · ");
});

interface MenuItem {
  title: string;
  blurb: string;
  price: string;
  slug: string | null;
}
const menu = computed(() =>
  list("booking.menu").map(gi => ({
    title: c(`booking.menu.${gi}.title`),
    items: list(`booking.menu.${gi}.items`).map(
      ii =>
        ({
          title: c(`booking.menu.${gi}.items.${ii}.title`),
          blurb: c(`booking.menu.${gi}.items.${ii}.blurb`),
          price: c(`booking.menu.${gi}.items.${ii}.price`),
          slug: raw<string>(`booking.menu.${gi}.items.${ii}.treatmentSlug`) ?? null
        }) as MenuItem
    )
  }))
);
const groups = computed(() => {
  const q = st.q.trim().toLowerCase();
  return menu.value
    .map(group => ({ ...group, items: group.items.filter(item => !q || item.title.toLowerCase().includes(q) || item.blurb.toLowerCase().includes(q)) }))
    .filter(group => group.items.length);
});

function pick(title: string, slug: string | null) {
  st.tx = title;
  st.slug = slug;
  hint.value = "";
}

/** 把预选解析成项目名：consultation / aura-prime / 治疗 slug / 已选好的文字 */
function resolve(request: BookRequest) {
  if (request.text) {
    const found = menu.value.flatMap(group => group.items).find(item => item.title === request.text);
    if (/^complimentary consultation$/i.test(request.text)) pick(consultLabel.value, null);
    else pick(request.text, request.slug ?? found?.slug ?? null);
    return true;
  }
  const preset = request.preset;
  if (!preset) return false;
  if (preset === "consultation") pick(consultLabel.value, null);
  else if (preset === "aura-prime") pick(tx("AURA Prime"), null);
  else {
    const item = menu.value.flatMap(group => group.items).find(entry => entry.slug === preset);
    if (!item) return false;
    pick(item.title, item.slug);
  }
  return true;
}

// 每次打开：重置并应用预选
watch(
  () => state.value.nonce,
  () => {
    if (!state.value.open) return;
    Object.assign(st, { step: 0, tx: "", slug: null, q: "", dayIndex: null, time: "", sent: false, sending: false, serverError: "", website: "", startedAt: Date.now() });
    hint.value = "";
    makeDays();
    if (resolve(state.value.request)) st.step = 1;
  }
);

const drawerEl = ref<HTMLElement>();
const closeEl = ref<HTMLButtonElement>();
const bodyEl = ref<HTMLElement>();
let lastFocus: Element | null = null;
watch(
  () => state.value.open,
  open => {
    if (!import.meta.client) return;
    if (open) {
      lastFocus = document.activeElement;
      document.body.style.overflow = "hidden";
      setTimeout(() => closeEl.value?.focus(), 50);
    } else {
      document.body.style.overflow = "";
      (lastFocus as HTMLElement | null)?.focus?.();
    }
  }
);

function chooseDay(index: number) {
  st.dayIndex = index;
  st.time = "";
}

function validate(): boolean {
  if (st.step === 0) {
    if (!st.tx) hint.value = tx("Choose a treatment to continue");
    return !!st.tx;
  }
  if (st.step === 1) {
    const ok = st.dayIndex !== null && !!st.time;
    if (!ok) hint.value = tx("Choose a day and time");
    return ok;
  }
  if (st.step === 2) {
    errors.name = st.name.trim().length < 2 ? tx("Enter your full name.") : "";
    errors.email = /^\S+@\S+\.\S+$/.test(st.email) ? "" : tx("Enter an email like name@example.com.");
    errors.phone = st.phone.replace(/\D/g, "").length >= 10 ? "" : tx("Enter a 10-digit mobile number.");
    errors.ok = st.ok ? "" : tx("Please accept to continue.");
    return !errors.name && !errors.email && !errors.phone && !errors.ok;
  }
  return true;
}

async function submit() {
  st.sending = true;
  st.serverError = "";
  const preferred = whenText.value ? `Preferred: ${whenText.value}` : "";
  const message = [st.tx, preferred, st.notes.trim()].filter(Boolean).join("\n");
  const base = String(config.app.baseURL).replace(/\/$/, "");
  try {
    await api("/leads", {
      method: "POST",
      body: {
        name: st.name.trim(),
        email: st.email.trim(),
        phone: st.phone.trim(),
        treatment: st.slug ?? "",
        message,
        pageUrl: base + route.path,
        env: String(config.public.deployEnv),
        website: st.website,
        startedAt: st.startedAt
      }
    });
    st.sent = true;
  } catch (error) {
    const key = (error as { errorKey?: string }).errorKey;
    st.serverError = key === "lead_rate_limited" ? tx("Too many requests. Please try again in a few minutes.") : tx("We couldn't send your request. Please try again.");
  } finally {
    st.sending = false;
  }
}

function next() {
  hint.value = "";
  if (!validate()) return;
  if (st.step === 3) return void submit();
  st.step += 1;
  nextTick(() => bodyEl.value && (bodyEl.value.scrollTop = 0));
}
function back() {
  hint.value = "";
  if (st.step > 0) st.step -= 1;
}

/** 完成页文案里的占位：{firstName} {treatment} {date} {time} */
function fill(text: string): string {
  const date = st.dayIndex !== null && days.value[st.dayIndex] ? fmtFull(days.value[st.dayIndex]!) : "";
  return text
    .replace(/\{firstName\}/g, st.name.trim().split(" ")[0] ?? "")
    .replace(/\{treatment\}/g, st.tx)
    .replace(/\{date\}/g, date)
    .replace(/\{time\}/g, st.time);
}

// Esc 关闭；网址 #book（可带 ?tx=）直接打开
onMounted(() => {
  const onKey = (event: KeyboardEvent) => {
    if (event.key === "Escape" && state.value.open) close();
  };
  window.addEventListener("keydown", onKey);
  onBeforeUnmount(() => window.removeEventListener("keydown", onKey));
  if (location.hash === "#book") {
    const text = new URLSearchParams(location.search).get("tx");
    history.replaceState(null, "", location.pathname + location.search.replace(/[?&]tx=[^&]*/, ""));
    useBooking().open(text ? { text } : {});
  }
});
</script>
