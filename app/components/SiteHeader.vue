<template>
  <div id="site-header" ref="root" :data-current="current">
    <div class="brandrow">
      <div class="in">
        <NuxtLink class="hdlogo" to="/" :aria-label="`${c('brand.name')} ${c('brand.by')}, home`">
          {{ c("brand.name") }}<span v-if="c('brand.by')" class="by">{{ c("brand.by") }}</span>
        </NuxtLink>
        <div class="hr">
          <form class="hsearch" role="search" @submit.prevent="goFirst">
            <input
              v-model="q"
              type="search"
              :placeholder="c('header.searchPlaceholder')"
              :aria-label="c('header.searchLabel') || c('header.searchPlaceholder')"
              autocomplete="off"
              @focus="onSearchFocus"
              @input="index.load()"
              @keydown.esc="q = ''"
            />
            <button type="submit" aria-label="Search">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="6" /><path d="M20 20l-4.5-4.5" /></svg>
            </button>
            <ul v-if="q.trim()" class="sresults" role="listbox">
              <li v-for="item in results" :key="item.slug">
                <NuxtLink :to="treatmentPath(item.slug)" @click="q = ''">{{ bi(item.name) }}<small v-if="categoryName(item.category)">{{ categoryName(item.category) }}</small></NuxtLink>
              </li>
              <li v-if="!results.length" class="none">{{ tx("No treatments match that search.") }}</li>
            </ul>
          </form>
          <a v-if="on('header.account')" class="acct" href="#" @click.prevent>
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="8" r="4" /><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6" /></svg>
            <span>{{ c("header.account.label") }}</span>
          </a>
          <button id="hambBtn" class="hamb" type="button" :aria-expanded="mobileOpen ? 'true' : 'false'" aria-controls="mobilenav" :aria-label="c('header.menuLabel') || 'Open menu'" @click="mobileOpen = !mobileOpen">
            <span /><span /><span />
          </button>
        </div>
      </div>
    </div>

    <div class="navbar" aria-label="Main">
      <div class="in">
        <ul class="top">
          <li v-for="cat in categories" :key="cat.key" :data-cat="cat.key" :class="{ open: openCat === cat.key }" :aria-current="current === cat.key ? 'true' : undefined">
            <span v-if="cat.tag" class="tag">{{ bi(cat.tag) }}</span>
            <!-- 直链：Facial Blueprint / Membership / About -->
            <NuxtLink v-if="linkOf(cat)" :to="linkOf(cat)!" @click="closeAll">{{ bi(cat.name) }}</NuxtLink>
            <a
              v-else
              href="#"
              class="catbtn"
              role="button"
              aria-haspopup="true"
              :aria-expanded="openCat === cat.key ? 'true' : 'false'"
              :aria-controls="`mega-${cat.key}`"
              @click.prevent.stop="toggle(cat.key)"
              >{{ bi(cat.name) }}</a
            >
            <!-- 治疗下拉：有分组名用多列，没有分组名用单列小菜单 -->
            <div v-if="!linkOf(cat) && cat.groups.length" :id="`mega-${cat.key}`" class="mega" :class="{ small: !hasGroupNames(cat) }">
              <div v-if="hasGroupNames(cat)" class="cols">
                <div v-for="(group, gi) in cat.groups" :key="gi" class="grp">
                  <h5 v-if="group.name">{{ bi(group.name) }}</h5>
                  <NuxtLink v-for="t in group.treatments" :key="t.slug" :to="treatmentPath(t.slug)" @click="closeAll">{{ bi(t.name) }}</NuxtLink>
                </div>
              </div>
              <template v-else>
                <NuxtLink v-for="t in flat(cat)" :key="t.slug" :to="treatmentPath(t.slug)" @click="closeAll">{{ bi(t.name) }}</NuxtLink>
              </template>
            </div>
            <!-- 直链类别的下拉小菜单（About 的锚点、Membership），来自 site.nav.dropdowns -->
            <div v-else-if="subLinks(cat.key).length" :id="`mega-${cat.key}`" class="mega small">
              <NuxtLink v-for="(sub, si) in subLinks(cat.key)" :key="si" :to="sub.path" @click="closeAll">{{ sub.label }}</NuxtLink>
            </div>
          </li>
        </ul>
        <a class="btn nav-book" href="#book" role="button" @click.prevent="book.open()">{{ c("header.bookLabel") }}</a>
      </div>
    </div>

    <div class="mnscrim" :class="{ on: mobileOpen }" @click="mobileOpen = false" />
    <div id="mobilenav" class="mobilenav" :class="{ on: mobileOpen }" :aria-hidden="mobileOpen ? 'false' : 'true'" :inert="!mobileOpen">
      <div class="mnhead">
        <NuxtLink class="hdlogo" to="/" style="font-size: 18px" @click="mobileOpen = false">
          {{ c("brand.name") }}<span v-if="c('brand.by')" class="by">{{ c("brand.by") }}</span>
        </NuxtLink>
        <button id="mnClose" class="close" type="button" aria-label="Close menu" @click="mobileOpen = false">×</button>
      </div>
      <div class="mnbody">
        <template v-for="cat in categories" :key="cat.key">
          <NuxtLink v-if="linkOf(cat)" class="mnlink" :to="linkOf(cat)!" @click="mobileOpen = false">{{ bi(cat.name) }}</NuxtLink>
          <div v-else-if="cat.groups.length" class="macc" :class="{ open: accOpen === cat.key }" :data-acc="cat.key">
            <button type="button" class="machead" :aria-expanded="accOpen === cat.key ? 'true' : 'false'" @click="accOpen = accOpen === cat.key ? '' : cat.key">
              {{ bi(cat.name) }}<span class="chev">⌄</span>
            </button>
            <div class="mapanel">
              <template v-if="hasGroupNames(cat)">
                <div v-for="(group, gi) in cat.groups" :key="gi" class="mgrp">
                  <h5 v-if="group.name">{{ bi(group.name) }}</h5>
                  <NuxtLink v-for="t in group.treatments" :key="t.slug" :to="treatmentPath(t.slug)" @click="mobileOpen = false">{{ bi(t.name) }}</NuxtLink>
                </div>
              </template>
              <template v-else>
                <NuxtLink v-for="t in flat(cat)" :key="t.slug" :to="treatmentPath(t.slug)" @click="mobileOpen = false">{{ bi(t.name) }}</NuxtLink>
              </template>
            </div>
          </div>
        </template>
        <a class="btn mnbook" href="#book" role="button" @click.prevent="openBookFromMobile">{{ c("header.mobileBookLabel") || c("header.bookLabel") }}</a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NavCategory, NavTreatment } from "~~/shared/types/api";

const { c, raw, list, on } = await useSite();
const { bi, tx } = useTx();
const categories = await useNav();
const book = useBooking();
const route = useRoute();
const index = useTreatmentIndex();

const root = ref<HTMLElement>();
const openCat = ref("");
const mobileOpen = ref(false);
const accOpen = ref("");
const q = ref("");

const closeAll = () => {
  openCat.value = "";
};
const toggle = (key: string) => {
  openCat.value = openCat.value === key ? "" : key;
};
function openBookFromMobile() {
  mobileOpen.value = false;
  book.open();
}

/** 直链类别：page → 对应页面；treatment → 治疗页；none → 下拉 */
function linkOf(cat: NavCategory): string | null {
  const link = cat.link;
  if (!link || link.type === "none") return null;
  return link.type === "page" ? pagePath(link.target) : treatmentPath(link.target);
}
const hasGroupNames = (cat: NavCategory) => cat.groups.some(group => group.name);
const flat = (cat: NavCategory): NavTreatment[] => cat.groups.flatMap(group => group.treatments);

/** site.nav.dropdowns[类别 key]：About 的锚点等 */
function subLinks(key: string) {
  const dropdowns = raw<Record<string, unknown[]>>("nav.dropdowns") ?? {};
  return list(`nav.dropdowns.${key}`).map(i => ({ label: c(`nav.dropdowns.${key}.${i}.label`), path: raw<string>(`nav.dropdowns.${key}.${i}.path`) ?? "/" })).filter(() => key in dropdowns);
}

// 当前页所属类别（高亮用）
const current = computed(() => {
  const path = route.path;
  const treatment = /^\/treatments\/([^/]+)/.exec(path)?.[1];
  if (treatment) return categories.value.find(cat => cat.groups.some(group => group.treatments.some(t => t.slug === treatment)))?.key ?? "";
  const pageKey = path.startsWith("/journal") ? "about" : Object.entries(PAGE_PATHS).find(([, value]) => value !== "/" && path === value)?.[0];
  return categories.value.find(cat => cat.link?.type === "page" && cat.link.target === pageKey)?.key ?? "";
});

// 搜索：按治疗名称在浏览器端过滤
const results = computed(() => {
  const needle = q.value.trim().toLowerCase();
  return needle ? index.items.value.filter(item => bi(item.name).toLowerCase().includes(needle)).slice(0, 8) : [];
});
const categoryName = (key: string) => bi(categories.value.find(cat => cat.key === key)?.name);
function onSearchFocus() {
  closeAll();
  index.load();
}
function goFirst() {
  const first = results.value[0];
  if (first) {
    q.value = "";
    navigateTo(treatmentPath(first.slug));
  }
}

// 点页面其他位置、按 Esc 收起；换页时收起
onMounted(() => {
  const onClick = (event: MouseEvent) => {
    if (root.value && !root.value.contains(event.target as Node)) {
      closeAll();
      q.value = "";
    }
  };
  const onKey = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
      closeAll();
      mobileOpen.value = false;
    }
  };
  document.addEventListener("click", onClick);
  document.addEventListener("keydown", onKey);
  onBeforeUnmount(() => {
    document.removeEventListener("click", onClick);
    document.removeEventListener("keydown", onKey);
  });
});
watch(
  () => route.fullPath,
  () => {
    closeAll();
    mobileOpen.value = false;
    q.value = "";
  }
);
watch(mobileOpen, open => {
  if (import.meta.client) document.body.style.overflow = open ? "hidden" : "";
});
</script>
