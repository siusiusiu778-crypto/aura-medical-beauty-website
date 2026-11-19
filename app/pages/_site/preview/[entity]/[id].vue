<template>
  <div>
    <div class="preview-bar">{{ tx("Draft preview — not published yet. This link expires in 30 minutes.") }}</div>
    <TreatmentView v-if="view === 'treatment'" :ctx="tctx!" />
    <GoalView v-else-if="view === 'goal'" :ctx="gctx!" />
    <HomeView v-else-if="view === 'home'" :ctx="pctx!" />
    <AboutView v-else-if="view === 'about'" :ctx="pctx!" />
    <MembershipView v-else-if="view === 'membership'" :ctx="pctx!" />
    <BlueprintView v-else-if="view === 'facial-blueprint'" :ctx="pctx!" />
    <JournalFaqView v-else-if="view === 'journal-faq'" :ctx="pctx!" />
    <JournalArticleView v-else-if="view === 'journal-botox-vs-xeomin'" :ctx="pctx!" />
  </div>
</template>

<script setup lang="ts">
import type { GoalDetail, PageContent, TreatmentDetail } from "~~/shared/types/api";

/**
 * 草稿预览：CMS 里点「预览」得到带签名、限时的链接（/_site/preview/{entity}/{id}?exp=…&sig=…），打开后看到还没发布的内容。
 * 签名由后端校验；无效、过期或内容不存在一律 404。预览页不缓存、不收录。
 * entity：page（id 是页面键）、treatment、goal（id 是数字编号）。
 */
definePageMeta({ pg: "home" });

const route = useRoute();
const api = useApi();
const { tx } = useTx();
const deps = useContentDeps();
const pgOverride = useState("pg-override", () => "");

const entity = String(route.params.entity);
const id = String(route.params.id);
const query = Object.fromEntries(["exp", "sig", "token"].map(key => [key, String(route.query[key] ?? "")]).filter(([, value]) => value));
const notFound = () => createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true });
if (!["page", "treatment", "goal"].includes(entity) || !/^[\w-]+$/.test(id) || !(query.sig || query.token)) throw notFound();

const { data } = await useAsyncData(`preview:${entity}:${id}`, () => orNull(api<TreatmentDetail | GoalDetail | PageContent>(`/preview/${entity}/${id}`, { query })).catch(() => null));
if (!data.value) throw notFound();

const view = ref(entity === "page" ? (data.value as PageContent).key : entity);
const tctx = entity === "treatment" ? buildCtx(data as Ref<TreatmentDetail>, `treatment:${(data.value as TreatmentDetail).slug}`, deps) : undefined;
const gctx = entity === "goal" ? buildCtx(data as Ref<GoalDetail>, `goal:${(data.value as GoalDetail).slug}`, deps) : undefined;
const pctx = entity === "page" ? buildPageCtx(data as Ref<PageContent>, (data.value as PageContent).key, deps) : undefined;

// 样式作用域随预览的页面类型变化（见 app.vue）
const PG: Record<string, string> = { treatment: "treatment", goal: "goal", home: "home", about: "about", membership: "membership", "facial-blueprint": "blueprint", "journal-faq": "faq", "journal-botox-vs-xeomin": "journal" };
pgOverride.value = PG[view.value] ?? "home";
onBeforeUnmount(() => (pgOverride.value = ""));

useHead({ title: "Draft preview", meta: [{ name: "robots", content: "noindex, nofollow" }] });
</script>
