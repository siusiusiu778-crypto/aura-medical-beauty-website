<template>
  <footer v-if="on('footer')" id="contact" class="foot">
    <div class="in">
      <div class="top">
        <div>
          <NuxtLink class="logo" to="/" :aria-label="`${c('brand.name')} home`">{{ c("brand.name") }}</NuxtLink>
          <p class="tagl">{{ c("brand.tagline") }}</p>
        </div>
        <div>
          <h4>{{ c("footer.location.title") }}</h4>
          <p>
            <a v-if="raw('footer.location.mapUrl')" :href="raw<string>('footer.location.mapUrl')" target="_blank" rel="noopener"><template v-for="i in list('footer.location.lines')" :key="i"><br v-if="i" />{{ c(`footer.location.lines.${i}`) }}</template></a
            ><template v-else><template v-for="i in list('footer.location.lines')" :key="i"><br v-if="i" />{{ c(`footer.location.lines.${i}`) }}</template></template>
          </p>
        </div>
        <div>
          <h4>{{ c("footer.hours.title") }}</h4>
          <p><template v-for="i in list('footer.hours.lines')" :key="i"><br v-if="i" />{{ c(`footer.hours.lines.${i}`) }}</template></p>
        </div>
        <div>
          <h4>{{ c("footer.contact.title") }}</h4>
          <p>
            <template v-for="(item, n) in contacts" :key="item.key">
              <br v-if="n" />
              <a v-if="item.href" :href="item.href" :target="item.key === 'instagram' ? '_blank' : undefined" :rel="item.key === 'instagram' ? 'noopener' : undefined">{{ item.label }}</a>
              <template v-else>{{ item.label }}</template>
            </template>
          </p>
        </div>
      </div>
      <div class="legal">
        <span>{{ c("footer.legal.text") }}</span>
        <nav>
          <template v-for="i in list('footer.legal.links')" :key="i">
            <a v-if="raw(`footer.legal.links.${i}.href`)" :href="raw<string>(`footer.legal.links.${i}.href`)">{{ c(`footer.legal.links.${i}.label`) }}</a>
            <span v-else>{{ c(`footer.legal.links.${i}.label`) }}</span>
          </template>
        </nav>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const { c, raw, list, on } = await useSite();
// 电话、邮箱、Instagram：show 为 true 且文字不为空才显示（原型里电话邮箱是占位，种子里是关闭的）
const contacts = computed(() =>
  ["phone", "email", "instagram"]
    .filter(key => on(`footer.contact.${key}`) && c(`footer.contact.${key}.label`))
    .map(key => ({ key, label: c(`footer.contact.${key}.label`), href: raw<string>(`footer.contact.${key}.href`) }))
);
</script>
