#!/usr/bin/env node
/**
 * 把 AURA 原型（legacy/site，或迁移前的 site）抽取成 CMS 种子。无需联网，不依赖任何第三方库。
 *
 *   node tools/aura-extract.mjs              # 写 seed/aura-seed.json 与 seed/fragments/*，并打印统计与校验
 *   node tools/aura-extract.mjs --check      # 只校验与统计，不写文件
 *
 * 产物：
 *   seed/aura-seed.json                       格式见 docs/api-contract.md §9，字段结构见 docs/content-schema.md
 *   seed/fragments/facial-blueprint-*.html    脸部比例图的 SVG（代码资产，不进 CMS）
 *
 * 抽取规则：文本叶子 {en, zh:""}；图片 {mediaKey, focus}；含方括号占位的内容置空并隐藏；
 * 原型横幅、"Prototype" 说明、示例评价不会进入可见内容。校验不通过时以非零状态退出。
 */
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const CHECK_ONLY = process.argv.includes("--check");
const SITE = [path.join(root, "legacy", "site"), path.join(root, "site")].find((d) => fs.existsSync(path.join(d, "home.html")));
if (!SITE) {
  console.error("找不到原型目录（legacy/site 或 site）");
  process.exit(2);
}

/* ------------------------------------------------------------------ 迷你 HTML 解析 */
const VOID = new Set(["img", "br", "input", "meta", "link", "hr", "source", "path", "circle", "line", "rect", "image"]);
const RAW = new Set(["script", "style"]);
const ENT = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", rsquo: "’", lsquo: "‘", rdquo: "”", ldquo: "“", mdash: "—", ndash: "–", hellip: "…", middot: "·", reg: "®", trade: "™", copy: "©", shy: "\u00ad" };
const decode = (s, keepShy = false) =>
  s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] === "#") return String.fromCodePoint(e[1] === "x" || e[1] === "X" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10));
    if (e === "shy" && keepShy) return "&shy;";
    return e in ENT ? ENT[e] : m;
  });

function parse(html) {
  const rootNode = { tag: "#root", attrs: {}, children: [], parent: null };
  let cur = rootNode;
  const re = /<!--[\s\S]*?-->|<!doctype[^>]*>|<\/([a-zA-Z][\w:-]*)\s*>|<([a-zA-Z][\w:-]*)((?:"[^"]*"|'[^']*'|[^'">])*?)(\/?)>|([^<]+|<)/gi;
  let m;
  while ((m = re.exec(html))) {
    if (m[1]) {
      const name = m[1].toLowerCase();
      let n = cur;
      while (n && n.tag !== name) n = n.parent;
      if (n && n.parent) cur = n.parent;
    } else if (m[2]) {
      const tag = m[2].toLowerCase();
      const attrs = {};
      m[3].replace(/([^\s=\/]+)(?:\s*=\s*("([^"]*)"|'([^']*)'|[^\s>]+))?/g, (_, k, v, d, s2) => {
        attrs[k.toLowerCase()] = d ?? s2 ?? (v ? v : "");
        return "";
      });
      const node = { tag, attrs, children: [], parent: cur };
      cur.children.push(node);
      if (RAW.has(tag)) {
        const end = html.toLowerCase().indexOf(`</${tag}`, re.lastIndex);
        node.children.push({ text: html.slice(re.lastIndex, end < 0 ? html.length : end) });
        re.lastIndex = end < 0 ? html.length : html.indexOf(">", end) + 1;
      } else if (!VOID.has(tag) && !m[4]) cur = node;
    } else if (m[5] !== undefined) {
      cur.children.push({ text: m[5] });
    }
  }
  return rootNode;
}

const isEl = (n) => n && n.tag;
const classes = (n) => (n.attrs.class || "").split(/\s+/).filter(Boolean);

/** 支持：tag、.class、#id、[attr]、[attr=val] 的复合，空格=后代，> = 子代，逗号=并集 */
function compile(sel) {
  return sel.split(",").map((part) => {
    const toks = part.trim().replace(/\s*>\s*/g, " > ").split(/\s+/);
    const out = [];
    let child = false;
    for (const t of toks) {
      if (t === ">") {
        child = true;
        continue;
      }
      const c = { child, tag: null, id: null, cls: [], attr: [], not: [] };
      child = false;
      let rest = t;
      const nots = [...rest.matchAll(/:not\(([^)]*)\)/g)].map((x) => x[1]);
      rest = rest.replace(/:not\([^)]*\)/g, "");
      for (const n of nots) c.not.push(compile(n)[0][0]);
      const tag = rest.match(/^[a-zA-Z][\w-]*/);
      if (tag) c.tag = tag[0].toLowerCase();
      for (const x of rest.matchAll(/([.#])([\w-]+)|\[([\w-]+)(?:=["']?([^\]"']*)["']?)?\]/g)) {
        if (x[1] === ".") c.cls.push(x[2]);
        else if (x[1] === "#") c.id = x[2];
        else c.attr.push([x[3], x[4]]);
      }
      out.push(c);
    }
    return out;
  });
}
function matchOne(n, c) {
  if (!isEl(n)) return false;
  if (c.tag && n.tag !== c.tag) return false;
  if (c.id && n.attrs.id !== c.id) return false;
  const cl = classes(n);
  if (!c.cls.every((x) => cl.includes(x))) return false;
  if (!c.attr.every(([k, v]) => (v === undefined ? k in n.attrs : n.attrs[k] === v))) return false;
  if (c.not.some((x) => matchOne(n, x))) return false;
  return true;
}
function matches(n, chain) {
  const last = chain[chain.length - 1];
  if (!matchOne(n, last)) return false;
  let node = n;
  let i = chain.length - 2;
  let child = last.child;
  while (i >= 0) {
    let p = node.parent;
    if (child) {
      if (!p || !matchOne(p, chain[i])) return false;
      node = p;
    } else {
      while (p && !matchOne(p, chain[i])) p = p.parent;
      if (!p) return false;
      node = p;
    }
    child = chain[i].child;
    i--;
  }
  return true;
}
function walk(n, fn) {
  if (!isEl(n) && n.tag !== "#root") return;
  for (const c of n.children) {
    if (isEl(c)) {
      fn(c);
      walk(c, fn);
    }
  }
}
function all(node, sel) {
  const chains = compile(sel);
  const out = [];
  walk(node, (n) => {
    if (chains.some((ch) => matches(n, ch))) out.push(n);
  });
  return out;
}
const one = (node, sel) => all(node, sel)[0] || null;

/* ------------------------------------------------------------------ 文本与 HTML 序列化 */
const HIDDEN = (n) => n.attrs && (n.attrs["aria-hidden"] === "true" || RAW.has(n.tag) || n.tag === "svg");
const collapse = (s) => s.replace(/\s+/g, " ").trim();
const PLACEHOLDER = /\[[^\]]*(copy to come|xxx|author|provider|date|aurainstitute|client name)[^\]]*\]/i;
const hasPlaceholder = (s) => PLACEHOLDER.test(s) || /\[XXX/i.test(s);

/** 纯文本：忽略 aria-hidden、script/style/svg；br 变空格 */
function plain(node) {
  if (!node) return "";
  let s = "";
  const rec = (n) => {
    if (n.text !== undefined) s += decode(n.text);
    else if (n.tag === "br") s += " ";
    else if (!HIDDEN(n)) n.children.forEach(rec);
  };
  rec(node);
  return collapse(s);
}
/** 按 br 切行 */
function lines(node) {
  if (!node) return [];
  const out = [""];
  const rec = (n) => {
    if (n.text !== undefined) out[out.length - 1] += decode(n.text);
    else if (n.tag === "br") out.push("");
    else if (!HIDDEN(n)) n.children.forEach(rec);
  };
  rec(node);
  return out.map(collapse).filter(Boolean);
}

const KEEP = new Set(["em", "b", "strong", "br", "a", "ul", "ol", "li", "p"]);
/** 站内链接映射：*.html → 根相对路径 */
const PAGE_ROUTE = { home: "/", about: "/about", "aura-prime": "/membership", "facial-blueprint": "/facial-blueprint", "journal-faq": "/journal/faq", "journal-botox-vs-xeomin": "/journal/botox-vs-xeomin" };
const TREATMENT_SLUGS = new Set();
function mapHref(href) {
  if (!href) return "";
  if (/^(https?:|mailto:|tel:)/i.test(href)) return href;
  if (href === "#") return "";
  const m = href.match(/^([\w-]+)\.html(\?[^#]*)?(#.*)?$/);
  if (!m) return href.startsWith("#") ? href : "";
  const [, name, , hash = ""] = m;
  if (name === "home" && hash === "#book") return "#book";
  if (name in PAGE_ROUTE) return PAGE_ROUTE[name] + (name === "home" && hash ? "" : hash);
  if (name.startsWith("goal-")) return `/goals/${name.slice(5)}`;
  return `/treatments/${name}` + hash;
}
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/** 白名单 HTML。opts.iToBr：<i> 变成换行；opts.stripArrow：去掉末尾箭头 */
function rich(node, opts = {}) {
  if (!node) return "";
  const rec = (n) => {
    if (n.text !== undefined) return esc(decode(n.text, true).replace(/\u00ad/g, "&shy;")).replace(/&amp;shy;/g, "&shy;");
    if (HIDDEN(n)) return "";
    if (n.tag === "br") return "<br>";
    const inner = n.children.map(rec).join("");
    if (n.tag === "i" && opts.iToBr) return `<br>${inner}`;
    if (!KEEP.has(n.tag)) return inner;
    if (n.tag === "a") {
      const href = mapHref(n.attrs.href || "");
      return href ? `<a href="${href}">${inner}</a>` : inner;
    }
    return `<${n.tag}>${inner}</${n.tag}>`;
  };
  let s = node.children.map(rec).join("");
  s = s.replace(/\s+/g, " ").replace(/\s*<br>\s*/g, "<br>").trim();
  if (opts.stripArrow) s = s.replace(/\s*→\s*$/, "");
  return s;
}
/** 标题：有 span.ln 的按行拼 <br>；否则整体 rich */
function title(node) {
  if (!node) return "";
  const ln = all(node, "span.ln");
  if (ln.length) return ln.map((l) => rich(l)).join("<br>");
  return rich(node);
}
const L = (en) => ({ en: en || "", zh: "" });
const Lp = (node) => L(plain(node));
const Lt = (node) => L(title(node));
const Lr = (node, o) => L(rich(node, o));
const LpArrow = (node) => L(plain(node).replace(/\s*→\s*$/, ""));
/** 多段落 → <p> 拼接 */
const paras = (nodes) => L(nodes.map((p) => `<p>${rich(p)}</p>`).join(""));

/* ------------------------------------------------------------------ 媒体 */
const mediaAlt = new Map(); // key → alt（取第一处非空）
const mediaUsed = new Set();
const mediaMissing = new Set();
function mediaKeyOf(src) {
  return (src || "").split("?")[0].split("#")[0].replace(/^\.?\//, "");
}
function focusOf(style) {
  const m = /object-position:\s*([^;]+)/i.exec(style || "");
  return m ? m[1].trim() : undefined;
}
function useMedia(key, alt) {
  if (!key) return;
  mediaUsed.add(key);
  if (!fs.existsSync(path.join(SITE, key))) mediaMissing.add(key);
  if (alt && !mediaAlt.get(key)) mediaAlt.set(key, alt);
  else if (!mediaAlt.has(key)) mediaAlt.set(key, "");
}
function media(imgNode) {
  if (!imgNode) return null;
  const src = imgNode.attrs.src || imgNode.attrs.href || "";
  const key = mediaKeyOf(src);
  if (!key) return null;
  useMedia(key, decode(imgNode.attrs.alt || ""));
  const f = focusOf(imgNode.attrs.style);
  return f ? { mediaKey: key, focus: f } : { mediaKey: key };
}
function mediaFrom(key, focus, alt) {
  const k = mediaKeyOf(key);
  useMedia(k, alt || "");
  return focus ? { mediaKey: k, focus } : { mediaKey: k };
}

/* ------------------------------------------------------------------ 读文件 */
const read = (f) => fs.readFileSync(path.join(SITE, f), "utf8");
const doms = new Map();
const raws = new Map();
function dom(name) {
  if (!doms.has(name)) {
    const raw = read(`${name}.html`);
    raws.set(name, raw);
    doms.set(name, parse(raw));
  }
  return doms.get(name);
}
const metaOf = (name) => {
  const raw = raws.get(name) || (dom(name), raws.get(name));
  const t = /<title>([\s\S]*?)<\/title>/i.exec(raw);
  const d = /<meta\s+name="description"\s+content="([^"]*)"/i.exec(raw);
  return { title: t ? collapse(decode(t[1])) : "", description: d ? collapse(decode(d[1])) : "" };
};
const seoOf = (name, noindex = false) => {
  const m = metaOf(name);
  return { title: L(m.title), description: L(m.description), keywords: L(""), ogMediaId: null, noindex };
};

/** 执行页面脚本里的一段字面量（const NAME = [...]; 或 var NAME = {...};） */
function literal(name, src) {
  const re = new RegExp(`(?:const|var|let)\\s+${name}\\s*=\\s*`);
  const m = re.exec(src);
  if (!m) throw new Error(`脚本里找不到 ${name}`);
  let i = m.index + m[0].length;
  const open = src[i];
  const close = open === "[" ? "]" : "}";
  let depth = 0;
  let inStr = null;
  let j = i;
  for (; j < src.length; j++) {
    const ch = src[j];
    if (inStr) {
      if (ch === "\\") j++;
      else if (ch === inStr) inStr = null;
    } else if (ch === '"' || ch === "'" || ch === "`") inStr = ch;
    else if (ch === open) depth++;
    else if (ch === close && --depth === 0) break;
  }
  return vm.runInNewContext(`(function(){const C="Consult",P="Planned at consult";return ${src.slice(i, j + 1)}})()`);
}
const dec = (s) => collapse(decode(String(s ?? "")));

/* ------------------------------------------------------------------ 页面清单 */
const NON_TREATMENT = new Set(["home", "about", "aura-prime", "facial-blueprint", "journal-faq", "journal-botox-vs-xeomin", "index", "nav"]);
const files = fs.readdirSync(SITE).filter((f) => f.endsWith(".html")).map((f) => f.slice(0, -5)).sort();
const goalFiles = files.filter((f) => f.startsWith("goal-"));
const treatmentFiles = files.filter((f) => !NON_TREATMENT.has(f) && !f.startsWith("goal-"));
treatmentFiles.forEach((f) => TREATMENT_SLUGS.add(f));
const warnings = [];
const warn = (m) => warnings.push(m);

/* ------------------------------------------------------------------ 导航（取自一个完整页面） */
const navDom = dom("thermage-flx");
const header = one(navDom, "#site-header");
const navTop = all(header, "ul.top > li");
const CATEGORY_LINK_PAGES = { blueprint: "facial-blueprint", membership: "membership", about: "about" };
const categories = [];
const navOf = new Map(); // slug → {category, group, groupSort, sort}
const nameOf = new Map(); // slug → 名称
const nameToSlug = new Map(); // 规范化名称 → slug
const norm = (s) => dec(s).toLowerCase().replace(/[®™]/g, "").replace(/\s*[·&]\s*/g, " ").replace(/\s+/g, " ").trim();
let treatmentSort = 0;
const dropdowns = {};
navTop.forEach((li, ci) => {
  const key = li.attrs["data-cat"];
  const tag = plain(one(li, "span.tag"));
  const a = one(li, "a");
  const catName = plain(one(li, "a.catbtn") || a);
  const cat = { key, name: L(catName), tag: tag ? L(tag) : null, linkType: "none", linkTarget: "", sort: ci, isOnline: true };
  if (CATEGORY_LINK_PAGES[key]) {
    cat.linkType = "page";
    cat.linkTarget = CATEGORY_LINK_PAGES[key];
    const mega = one(li, ".mega");
    if (mega && (key === "about" || key === "membership")) {
      dropdowns[key] = all(mega, "a").map((x) => ({ label: Lp(x), path: mapHref(x.attrs.href) }));
    }
  } else {
    const groups = all(li, ".grp");
    if (groups.length) {
      groups.forEach((g, gi) => {
        const gname = plain(one(g, "h5"));
        all(g, "a").forEach((x, xi) => reg(x, key, gname, gi, treatmentSort++));
      });
    } else {
      all(li, ".mega > a").forEach((x) => reg(x, key, null, 0, treatmentSort++));
    }
  }
  categories.push(cat);
});
function reg(a, cat, group, groupSort, sort) {
  const slug = (a.attrs.href || "").replace(/\.html.*$/, "");
  navOf.set(slug, { category: cat, group, groupSort, sort });
  nameOf.set(slug, plain(a));
  nameToSlug.set(norm(plain(a)), slug);
}

/* ------------------------------------------------------------------ 治疗页 */
function bookbox(d, scope) {
  const bb = one(scope, ".bookbox");
  if (!bb) return { show: false, label: L(""), options: [], cta: L("") };
  const sum = one(bb, "summary");
  const label = sum ? collapse(sum.children.filter((c) => c.text !== undefined).map((c) => decode(c.text)).join("")) : "";
  return { show: true, label: L(label), options: all(bb, ".bbopt").map((o) => Lp(o)), cta: Lp(one(bb, "a.btn")) };
}
function faqItems(scope) {
  return all(scope, "details").map((d) => ({ q: Lp(one(d, "summary")), a: paras(d.children.filter((c) => c.tag === "p")) }));
}
function headOf(scope) {
  const h = one(scope, ".head") || scope;
  return { eyebrow: Lp(one(h, ".eyebrow")), title: Lr(one(h, "h2")) };
}
function closingOf(scope) {
  const sec = one(scope, "section#book");
  if (!sec) return { show: false, image: null, title: L(""), text: L(""), cta: L("") };
  const img = one(sec, "img");
  return { show: true, image: media(img), title: Lr(one(sec, "h2")), text: Lp(one(sec, "p")), cta: Lp(one(sec, ".btn")) };
}
const goalRowInfo = new Map(); // slug → {text, tags, image}
function extractTreatment(slug) {
  const d = dom(slug);
  const raw = raws.get(slug);
  const placeholder = /Copy to come/.test(raw);
  const top = one(d, "section#top");
  const content = {};
  if (slug === "tech-neck") {
    // 占位页：只有 hero 与 closing；其余区块保留标题但隐藏
    const heroImg = one(top, ".ph img");
    content.hero = {
      show: true,
      image: media(heroImg),
      kicker: Lp(one(top, ".eyebrow")),
      title: Lr(one(top, "h1")),
      lede: Lp(one(top, ".lede")),
      chips: [],
      bookbox: bookbox(d, top),
      learnMore: L(""),
    };
    const secs = all(d, "main > section").filter((s) => s !== top);
    const names = ["how", "fit", "tech", "glance", "faq"];
    secs.forEach((s, i) => {
      const k = names[i];
      if (!k || s.attrs.id === "book") return;
      const h = headOf(s);
      if (k === "glance") return;
      content[k] = { show: false, eyebrow: h.eyebrow, title: h.title };
    });
    // 隐藏区块也给出完整的空结构，管理端可以直接填写
    Object.assign(content.how, { intro: L(""), tagline: L(""), cards: [], note: L("") });
    Object.assign(content.fit, { yes: { title: L(""), items: [] }, no: { title: L(""), items: [] }, image: null });
    Object.assign(content.tech, { anchor: "treatment", image: null, steps: [] });
    Object.assign(content.faq, { items: [] });
    content.closing = closingOf(d);
    return { content, placeholder };
  }
  // hero
  content.hero = {
    show: true,
    image: media(one(top, ".tframe img")),
    kicker: Lp(one(top, ".kicker")),
    title: Lt(one(top, "h1")),
    lede: Lp(one(top, ".lede")),
    chips: all(top, ".chips span").map(Lp),
    bookbox: bookbox(d, top),
    learnMore: Lp(one(top, ".tlink")),
  };
  // how
  const how = one(d, "section#how");
  const hintroP = all(one(how, ".hintro"), "p:not(.tagline)");
  content.how = {
    show: true,
    ...headOf(how),
    intro: paras(hintroP),
    tagline: Lp(one(how, ".hintro .tagline")),
    cards: all(how, ".bcards > div").map((c) => ({ image: media(one(c, "img")), title: Lp(one(c, "h3")), text: Lp(one(c, "p")), zone: one(c, "h3").attrs["data-zone"] ? L(dec(one(c, "h3").attrs["data-zone"])) : L("") })),
    note: Lp(one(how, ".fda")),
  };
  // fit 或 grid
  const fit = one(d, "section#fit");
  if (fit && one(fit, ".g6")) {
    content.fit = { show: false, ...headOf(fit), yes: { title: L(""), items: [] }, no: { title: L(""), items: [] }, image: null };
    content.grid = {
      show: true,
      ...headOf(fit),
      items: all(fit, ".g6 li").map((li) => ({ title: Lp(one(li, "h3")), text: Lp(one(li, "p")) })),
      foot: Lr(one(fit, ".g6foot")),
    };
  } else if (fit) {
    const pn = one(fit, ".pairnote");
    content.fit = {
      show: true,
      ...headOf(fit),
      yes: { title: Lp(one(fit, ".fit5 h4")), items: all(fit, "ul.rows.yes li").map(Lp) },
      no: { title: Lp(all(fit, ".fit5 h4")[1]), items: all(fit, "ul.rows.no li").map(Lp) },
      image: media(one(fit, ".fitimg img")),
      pairNote: pn ? { label: Lp(one(pn, ".pl")), html: Lr(one(pn, ".pt")) } : { label: L(""), html: L("") },
    };
  }
  // tech / treatment
  const tech = one(d, "section#tech") || one(d, "section#treatment");
  if (tech) {
    content.tech = {
      show: true,
      anchor: tech.attrs.id,
      eyebrow: Lp(one(tech, ".eyebrow")),
      title: Lr(one(tech, "h2")),
      image: media(one(tech, ".tgrid .ph img")),
      steps: all(tech, ".tsteps li").map((li) => ({ title: Lp(one(li, "b")), text: Lr(one(li, ".tdd")) })),
    };
  }
  // faq
  const faq = one(d, "section#faq");
  content.faq = { show: true, ...headOf(faq), items: faqItems(faq) };
  content.closing = closingOf(d);
  return { content, placeholder };
}

/* ------------------------------------------------------------------ 首页脚本里的数据 */
const homeRaw = (dom("home"), raws.get("home"));
const homeScript = [...homeRaw.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join("\n");
const RESULTS = literal("RESULTS", homeScript);
const MOSTLOVED = literal("MOSTLOVED", homeScript);
const JSTEPS = literal("JSTEPS", homeScript);
const FXLINK = literal("FXLINK", homeScript);
const BOOK_TIMES = literal("times", homeScript);
const BOOK_STEPS = literal("STEPS", homeScript);
const RESULT_TO_GOAL = Object.fromEntries(Object.entries(FXLINK).map(([k, v]) => [k, v.replace(/^goal-/, "").replace(/\.html$/, "")]));

function slugOfName(name) {
  const s = nameToSlug.get(norm(name));
  if (!s) warn(`名称无法对应治疗：${dec(name)}`);
  return s || null;
}

/* ------------------------------------------------------------------ 目标页 */
const goals = [];
goalFiles.forEach((f, gi) => {
  const d = dom(f);
  const slug = f.slice(5);
  const hd = one(d, ".goalhd");
  const rows = all(d, "a.row");
  const groupsEl = all(d, ".chips2 a").filter((a) => a.attrs["data-g"] && a.attrs["data-g"] !== "all");
  const items = [];
  rows.forEach((r) => {
    const t = (r.attrs.href || "").replace(/\.html.*$/, "");
    if (!TREATMENT_SLUGS.has(t)) {
      warn(`${f}: 条目链接不是治疗页：${r.attrs.href}`);
      return;
    }
    const it = {
      treatment: t,
      group: r.attrs["data-group"] && groupsEl.length ? r.attrs["data-group"] : null,
      image: media(one(r, "img")),
      title: Lp(one(r, "h3")),
      text: Lp(one(r, ".ex")),
      tags: all(r, ".tg span").map(Lp),
    };
    if (!goalRowInfo.has(t)) goalRowInfo.set(t, { text: plain(one(r, ".ex")), tags: all(r, ".tg span").map(plain), image: it.image });
    items.push(it);
  });
  const cta = one(d, "section.cta");
  const result = RESULTS.find((r) => RESULT_TO_GOAL[r.id] === slug);
  goals.push({
    slug,
    name: Lp(one(hd, "h1")),
    summary: Lp(one(hd, "p:not(.eyebrow)")),
    cardMedia: result ? mediaFrom(result.img, (/(?:object-position:)?\s*(.+)/.exec(result.pos || "") || [])[1], result.alt || "") : null,
    content: {
      hero: { eyebrow: Lp(one(hd, ".eyebrow")), title: Lr(one(hd, "h1")), lede: Lp(one(hd, "p:not(.eyebrow)")) },
      groups: groupsEl.map((a) => ({ key: a.attrs["data-g"], label: Lp(a) })),
      items,
      closing: { show: true, eyebrow: Lp(one(cta, ".eyebrow")), title: Lr(one(cta, "h2")), text: Lp(one(cta, "p:not(.eyebrow)")), cta: Lp(one(cta, ".btn")) },
    },
    treatmentSlugs: items.map((i) => i.treatment),
    seo: seoOf(f),
    status: "published",
    sort: gi,
  });
});
// 首页卡片顺序与原型一致
const goalOrder = RESULTS.map((r) => RESULT_TO_GOAL[r.id]);
goals.sort((a, b) => goalOrder.indexOf(a.slug) - goalOrder.indexOf(b.slug));
goals.forEach((g, i) => (g.sort = i));

/* ------------------------------------------------------------------ 预约抽屉的目录（来自首页脚本的 RESULTS） */
const bookingMenu = RESULTS.map((r) => ({
  title: L(dec(r.name)),
  items: r.items.map(([n, blurb, price]) => ({ treatmentSlug: slugOfName(n), title: L(dec(n)), blurb: L(dec(blurb)), price: L(dec(price)) })),
}));
const listingOf = new Map(); // slug → {blurb, price}
RESULTS.forEach((r) => r.items.forEach(([n, blurb, price]) => {
  const s = nameToSlug.get(norm(n));
  if (s && !listingOf.has(s)) listingOf.set(s, { blurb: dec(blurb), price: dec(price) });
}));

/* ------------------------------------------------------------------ 治疗实体 */
const treatments = [];
let placeholderTreatments = [];
treatmentFiles.forEach((slug) => {
  const nv = navOf.get(slug);
  if (!nv) warn(`导航里没有这个治疗：${slug}`);
  const { content, placeholder } = extractTreatment(slug);
  const lst = listingOf.get(slug) || { blurb: "", price: "" };
  const gr = goalRowInfo.get(slug);
  content.listing = { blurb: L(lst.blurb), price: L(lst.price), tags: (gr?.tags || []).map(L) };
  if (placeholder) placeholderTreatments.push(slug);
  const heroImg = content.hero.image;
  treatments.push({
    slug,
    name: L(nameOf.get(slug) || plain(one(dom(slug), "h1"))),
    categoryKey: nv?.category || "",
    group: nv?.group ? L(nv.group) : null,
    groupSort: nv?.groupSort ?? 0,
    summary: L(gr?.text || content.hero.lede.en),
    cardMedia: gr?.image || heroImg,
    content,
    seo: seoOf(slug, placeholder),
    copyComplete: !placeholder,
    status: "published",
    sort: nv?.sort ?? 999,
  });
});
treatments.sort((a, b) => a.sort - b.sort);

/* ------------------------------------------------------------------ 页面：site */
const footer = one(navDom, "footer.foot");
const fcols = all(footer, ".top > div");
const colOf = (title) => fcols.find((c) => plain(one(c, "h4")) === title);
const locCol = colOf("Location");
const hoursCol = colOf("Hours");
const contactCol = colOf("Contact");
const contactLines = lines(one(contactCol, "p"));
const phoneRaw = contactLines.find((l) => /^\(?\d{3}/.test(l)) || "";
const emailRaw = contactLines.find((l) => /@/.test(l)) || "";
const insta = one(contactCol, "a");
const legalLinks = all(footer, ".legal nav a");
const hdLogo = one(header, "a.hdlogo");
const pageSite = {
  content: {
    brand: { name: L(plain({ children: hdLogo.children.filter((c) => !(c.tag === "span")) })), by: Lp(one(hdLogo, ".by")), tagline: Lp(one(footer, ".tagl")) },
    header: {
      searchPlaceholder: L(one(header, ".hsearch input").attrs.placeholder),
      searchLabel: L(one(header, ".hsearch button").attrs["aria-label"]),
      account: { show: false, label: Lp(one(header, "a.acct")) },
      bookLabel: Lp(one(header, ".nav-book")),
      mobileBookLabel: Lp(one(header, ".mnbody > a.btn")),
      menuLabel: L(one(header, "#hambBtn").attrs["aria-label"]),
    },
    nav: { dropdowns },
    footer: {
      show: true,
      location: { title: Lp(one(locCol, "h4")), lines: lines(one(locCol, "p a")).map(L), mapUrl: one(locCol, "p a").attrs.href },
      hours: { title: Lp(one(hoursCol, "h4")), lines: lines(one(hoursCol, "p")).map(L) },
      contact: {
        title: Lp(one(contactCol, "h4")),
        phone: { show: !!phoneRaw && !hasPlaceholder(phoneRaw), label: L(hasPlaceholder(phoneRaw) ? "" : phoneRaw), href: "" },
        email: { show: !!emailRaw && !hasPlaceholder(emailRaw), label: L(hasPlaceholder(emailRaw) ? "" : emailRaw), href: "" },
        instagram: { show: !!insta, label: Lp(insta), href: insta ? insta.attrs.href : "" },
      },
      legal: { text: Lp(one(footer, ".legal > span")), links: legalLinks.map((a) => ({ label: Lp(a), href: mapHref(a.attrs.href) })) },
    },
    floatBook: { show: false, label: L("Book Now") },
    booking: bookingCopy(),
  },
  seo: seoOf("home"),
};
function bookingCopy() {
  const need = (s) => {
    if (!homeRaw.includes(s) && !homeScript.includes(s)) warn(`预约抽屉文案在原型里找不到：${s}`);
    return s;
  };
  const stepLabels = BOOK_STEPS.map((s) => s.split("·").slice(1).join("·").trim());
  return {
    title: L(need("Book your visit")),
    stepLabels: stepLabels.map(L),
    consult: { title: L(need("Not sure yet? Book a complimentary consultation")), text: L(need("30 minutes to build a plan around your whole face and your goals")) },
    searchPlaceholder: L("Search treatments"),
    viewAll: L(need("View all treatments")),
    menu: bookingMenu,
    times: BOOK_TIMES,
    locationNote: L(need("Location: AURA Institute, Rockefeller Center. Lunch-hour appointments available.")),
    consentLabel: L(need("I agree to the cancellation policy and to receive appointment texts.")),
    intakeNote: L(need("Your first visit includes a brief medical intake with your provider. A card on file holds your appointment; you won’t be charged today.")),
    submitLabel: L(need("Request Appointment")),
    // 原型的提示"Prototype: nothing was booked…"不进入官网；成功文案按真实流程改写
    done: { eyebrow: L(need("Thank you")), title: L("See you soon, {firstName}."), text: L("Your request for {treatment} on {date} at {time} is in. We’ll text you to confirm.") },
  };
}

/* ------------------------------------------------------------------ 页面：home */
const hd = dom("home");
const heroSec = one(hd, "section.hero");
const posOf = (p) => (p || "").replace(/^object-position:\s*/, "");
const pageHome = (() => {
  const season = one(hd, "section#season");
  const about = one(hd, "section#about");
  const exp = one(hd, "section#experience");
  const stars = one(hd, "section#stars");
  const res = one(hd, "section#results");
  const valueSpans = all(about, ".vtrack span");
  const values = [];
  valueSpans.forEach((s) => {
    const t = plain(s);
    if (!values.includes(t)) values.push(t);
  });
  return {
    content: {
      hero: {
        show: true,
        images: all(heroSec, "img.hbg").map(media),
        eyebrow: Lp(one(heroSec, ".eyebrow")),
        title: Lr(one(heroSec, "h1")),
        lede: Lp(one(heroSec, ".center > p:not(.eyebrow)")),
        cta: { label: Lp(one(heroSec, ".btn")) },
      },
      results: {
        show: true,
        eyebrow: Lp(one(res, ".head .eyebrow")),
        title: Lr(one(res, ".head h2")),
        items: RESULTS.map((r) => ({ goal: RESULT_TO_GOAL[r.id], name: L(dec(r.name)), image: mediaFrom(r.img, posOf(r.pos), dec(r.alt || "")), bullets: r.show.map((x) => L(dec(x))) })),
      },
      season: {
        show: true,
        badge: Lp(one(season, ".badge")),
        image: media(one(season, ".promo-img img")),
        label: Lp(one(season, ".label")),
        title: Lr(one(season, "h2")),
        main: { title: Lp(one(season, ".promo-main b")), text: Lp(one(season, ".promo-main span")) },
        facts: all(season, ".olist li").map((li) => ({ label: Lp(one(li, "small")), value: L(collapse(li.children.filter((c) => c.text !== undefined).map((c) => decode(c.text)).join(""))) })),
        note: Lp(one(season, "p.note")),
        cta: { label: Lp(one(season, ".promo-cta .btn")) },
      },
      stars: {
        show: true,
        label: Lp(one(stars, ".label")),
        title: Lr(one(stars, "h2")),
        items: MOSTLOVED.map((t) => ({ treatment: t.href.replace(/\.html$/, ""), image: mediaFrom(t.img, posOf(t.pos), dec(t.alt || "")), name: L(dec(t.name)), effect: L(dec(t.fx)) })),
      },
      about: {
        show: true,
        image: media(one(about, ".aimg img")),
        label: Lp(one(about, ".label")),
        title: Lt(one(about, "h2.big")),
        text: Lp(one(about, ".acopy > p:not(.label)")),
        link: { label: Lp(one(about, ".tlink")), path: mapHref(one(about, ".tlink").attrs.href) },
        values: values.map(L),
      },
      experience: {
        show: true,
        label: Lp(one(exp, ".head .label")),
        title: Lr(one(exp, ".head h2")),
        steps: JSTEPS.map(([t, x]) => ({ title: L(dec(t)), text: L(dec(x)) })),
        cta: { label: Lp(one(exp, ".cta .btn")), bookPreset: "consultation" },
      },
    },
    seo: seoOf("home"),
  };
})();
RESULTS.forEach((r) => {
  if (!RESULT_TO_GOAL[r.id]) warn(`首页目标卡片没有对应的目标页：${r.id}`);
});

/* ------------------------------------------------------------------ 页面：about */
const pageAbout = (() => {
  const d = dom("about");
  const hero = one(d, "section#top");
  const who = one(d, "section#who");
  const std = one(d, "section#standards");
  const tech = one(d, "section#technology");
  const aes = one(d, "section#aesthetic");
  const intro = one(d, "section.intro");
  const figs = all(aes, "figure img").map(media);
  const tbl = one(tech, "table.brands");
  return {
    content: {
      hero: { show: true, image: media(one(hero, "img")), eyebrow: Lp(one(hero, ".eyebrow")), title: Lt(one(hero, "h1")), lede: Lp(one(hero, ".hbar p")), cta: { label: LpArrow(one(hero, ".hbar .btn")) } },
      intro: { show: true, eyebrow: Lp(one(intro, ".eyebrow")), text: Lr(one(intro, ".lead")) },
      who: { show: true, eyebrow: Lp(one(who, ".eyebrow")), title: Lr(one(who, "h2")), text: Lp(one(who, ".copy")), image: media(one(who, "figure img")) },
      standards: { show: true, eyebrow: Lp(one(std, ".eyebrow")), title: Lr(one(std, "h2")), items: all(std, "ol.std li").map((li) => ({ title: Lp(one(li, "h3")), text: Lp(one(li, "p")) })) },
      technology: {
        show: true,
        eyebrow: Lp(one(tech, ".eyebrow")),
        title: Lr(one(tech, "h2")),
        text: Lp(one(tech, ".copy")),
        image: media(one(tech, ".ph img")),
        table: { head: all(tbl, "thead th").map(Lp), rows: all(tbl, "tbody tr").map((tr) => all(tr, "td").map(Lp)) },
        note: Lp(one(tech, ".fda")),
      },
      aesthetic: {
        show: true,
        eyebrow: Lp(one(aes, ".eyebrow")),
        title: Lr(one(aes, "h2")),
        text: Lp(one(aes, ".copy")),
        link: { label: LpArrow(one(aes, ".tlink")), path: mapHref(one(aes, ".tlink").attrs.href) },
        images: figs,
        quote: Lp(one(aes, "p.q")),
      },
      closing: closingOf(d),
    },
    seo: seoOf("about"),
  };
})();
// about 的 closing 是 .closing 且 id=book；标题在 cgrid 里，文案在 p
{
  const d = dom("about");
  const sec = one(d, "section#book");
  pageAbout.content.closing = { show: true, image: media(one(sec, "img")), title: Lr(one(sec, "h2")), text: Lp(one(sec, ".cgrid > p")), cta: { label: Lp(one(sec, ".btn")) } };
}

/* ------------------------------------------------------------------ 页面：membership */
const pageMembership = (() => {
  const d = dom("aura-prime");
  const hero = one(d, "section#top");
  const inc = one(d, "section#how");
  const faq = one(d, "section#faq");
  const closing = one(d, "section#book");
  const talk = one(d, "dialog#talk");
  const ptitle = all(hero, ".ptitle .ln").map((l) => rich(l));
  const pr = one(hero, ".pr");
  const join = one(hero, ".pjoin");
  const talkP = one(join, ".ptalk");
  const talkA = one(talkP, "a");
  const rows = all(talk, "dl > div").map((r) => {
    const dd = one(r, "dd");
    const t = plain(dd);
    return { label: Lp(one(r, "dt")), html: Lr(dd), show: !hasPlaceholder(t) && !!t };
  });
  const bk = one(talk, ".bk");
  return {
    content: {
      hero: {
        show: true,
        image: media(one(hero, ".pframe img")),
        tag: { kicker: Lp(one(hero, ".ptag span")), line: Lp(one(hero, ".ptag i")) },
        titleLines: ptitle.map(L),
        kicker: Lp(one(hero, ".pl .kicker")),
        tagline: Lr(one(hero, ".pline")),
        join: { label: Lp(one(join, ".btn")), bookPreset: "aura-prime" },
        talk: { lead: L(collapse(talkP.children.filter((c) => c.text !== undefined).map((c) => decode(c.text)).join(""))), linkLabel: LpArrow(talkA) },
        lede: Lp(one(pr, ".lede")),
        price: { amount: Lp(one(pr, ".pricetag b")), unit: Lp(one(pr, ".pricetag span")), note: Lp(one(pr, ".pricenote")) },
        chips: all(pr, ".chips span").map(Lp),
      },
      included: {
        show: true,
        ...headOf(inc),
        intro: Lp(one(inc, ".hintro p:not(.tagline)")),
        tagline: Lp(one(inc, ".hintro .tagline")),
        cards: all(inc, "#inc3 article").map((a) => ({
          number: Lp(one(a, ".num")),
          caption: Lp(one(a, ".cap")),
          label: Lp(one(a, ".lbl")),
          title: Lp(one(a, "h3")),
          text: Lp(all(a, "p").filter((p) => !p.attrs.class)[0]),
          link: { label: LpArrow(one(a, "a.more")), path: mapHref(one(a, "a.more").attrs.href) },
        })),
        foot: { note: Lp(one(inc, ".incfoot span")), link: { label: LpArrow(one(inc, ".incfoot a")), bookPreset: "aura-prime" } },
      },
      faq: { show: true, ...headOf(faq), image: media(one(faq, ".faqside img")), items: faqItems(faq) },
      closing: { show: true, image: media(one(closing, "img")), title: Lr(one(closing, "h2")), text: Lp(one(closing, "p")), cta: { label: Lp(one(closing, ".btn")), bookPreset: "aura-prime" } },
      talkDialog: {
        show: true,
        eyebrow: Lp(one(talk, ".tx .eyebrow")),
        title: Lr(one(talk, "h2")),
        lead: Lp(one(talk, ".lead")),
        rows,
        consult: { eyebrow: Lp(one(bk, ".eyebrow")), title: Lr(one(bk, "h3")), bullets: all(bk, "li").map(Lp), cta: LpArrow(one(bk, ".btn")), fine: Lp(one(bk, ".fine")) },
      },
    },
    seo: seoOf("aura-prime"),
  };
})();

/* ------------------------------------------------------------------ 页面：facial-blueprint */
const fragments = {};
const pageBlueprint = (() => {
  const d = dom("facial-blueprint");
  const raw = raws.get("facial-blueprint");
  const hero = one(d, "section#top");
  const modes = literal("M", raw.slice(raw.indexOf("var M")));
  const order = all(hero, ".fbchips button").map((b) => b.attrs["data-mode"]);
  const svgM = /<svg class="fbsvg"[\s\S]*?<\/svg>\s*(?=<\/div>)/.exec(raw);
  if (!svgM) warn("facial-blueprint：找不到脸部比例图 SVG");
  else
    fragments["facial-blueprint-map.svg.html"] = svgM[0].replace(/href="fb-front\.webp"/, 'href="{{front}}"').replace(/href="fb-side\.webp"/, 'href="{{side}}"').trim();
  const dots = [...raw.matchAll(/<svg class="dots"[\s\S]*?<\/svg>/g)].map((m) => m[0]);
  const dotNames = ["scale", "line"];
  dots.forEach((s, i) => (fragments[`facial-blueprint-dots-${dotNames[i] || i}.svg.html`] = s));
  useMedia("fb-front.webp", "");
  useMedia("fb-side.webp", "");
  const steps = one(d, "section#steps");
  const aes = one(d, "section#aesthetic");
  const rev = one(d, "section#reviews");
  const faq = one(d, "section#faq");
  const stepText = plain(one(hero, ".fbstep"));
  return {
    content: {
      hero: {
        show: true,
        eyebrow: Lp(one(hero, ".fbcopy .eyebrow")),
        title: Lt(one(hero, "h1")),
        lede: Lp(one(hero, ".lede")),
        cta: { label: Lp(one(hero, ".fbcta .btn")) },
        map: {
          stepIntro: Lp(one(hero, "#fbStep")),
          label: Lp(one(hero, "#fbLabel")),
          caption: Lp(one(hero, "#fbCap")),
          kicker: L(stepText.split("·").slice(1).join("·").trim()),
          modes: order.map((k) => ({ key: k, name: L(dec(modes[k][0])), sub: L(dec(modes[k][1])), caption: L(dec(modes[k][2])), view: modes[k][3] })),
          front: mediaFrom("fb-front.webp", undefined, ""),
          side: mediaFrom("fb-side.webp", undefined, ""),
        },
      },
      steps: { show: true, ...headOf(steps), items: all(steps, ".bcards > div").map((c) => ({ title: Lp(one(c, "h3")), text: Lp(one(c, "p")) })) },
      aesthetic: {
        show: true,
        ...headOf(aes),
        intro: Lr(one(aes, "p.intro"), { iToBr: true }),
        rows: all(aes, ".fbrow").map((r) => {
          const img = one(r, "img");
          const key = mediaKeyOf(img.attrs.src);
          return { image: media(img), dots: /scale/.test(key) ? "scale" : /line/.test(key) ? "line" : null, name: Lp(one(r, ".k")), title: Lp(one(r, "h3")), text: Lp(one(r, "p")) };
        }),
      },
      // 示例评价（版面示意，带 Sample 标签）：按 FTC 规则不得当真实评价发布，默认隐藏
      reviews: {
        show: false,
        ...headOf(rev),
        items: all(rev, "figure").map((f) => ({ rating: 5, quote: Lp(one(f, "blockquote")), name: Lp(one(f, "figcaption span")), sample: true })),
        cta: { label: Lp(one(rev, ".btn")) },
      },
      faq: { show: true, ...headOf(faq), items: faqItems(faq) },
      closing: closingOf(d),
    },
    seo: seoOf("facial-blueprint"),
  };
})();

/* ------------------------------------------------------------------ 页面：journal */
function journalLink(href) {
  const m = /^([\w-]+)\.html$/.exec(href || "");
  if (m && m[1].startsWith("journal-")) return { type: "journal", target: m[1] };
  return { type: "none", target: "" };
}
const journalCta = (sec) => ({ show: true, eyebrow: Lp(one(sec, ".eyebrow")), title: Lr(one(sec, "h2")), text: Lp(one(sec, "p:not(.eyebrow)")), cta: { label: Lp(one(sec, ".btn")) } });
const pageJournalFaq = (() => {
  const d = dom("journal-faq");
  const chd = one(d, ".chd");
  const grp = all(d, ".grp2");
  return {
    content: {
      hero: { show: true, title: Lr(one(chd, "h1")), lede: Lp(one(chd, "p")) },
      tabs: all(d, ".chips2 a").map((a) => ({ key: a.attrs.href.replace("#", "") === "top" ? "all" : a.attrs.href.replace("#", ""), label: Lp(a) })),
      sections: grp.map((g) => ({
        key: g.attrs.id,
        title: Lp(one(g, "h2")),
        lede: Lp(one(g, "h2 + p") || all(g, "p")[0]),
        items: all(g, "article.row").map((r) => ({
          title: Lp(one(r, "h3")),
          excerpt: Lp(one(r, ".ex")),
          image: media(one(r, "img")),
          tags: all(r, ".tg span").map(Lp),
          link: journalLink(one(r, "a.lm").attrs.href),
        })),
      })),
      closing: journalCta(one(d, "section.cta")),
    },
    seo: seoOf("journal-faq"),
  };
})();
const pageJournalArticle = (() => {
  const d = dom("journal-botox-vs-xeomin");
  const wraps = all(d, "main > .wrap");
  const head = wraps.find((w) => one(w, "h1"));
  const art = one(d, "article.body");
  const toc = one(d, "nav.toc");
  const body = [];
  art.children.filter(isEl).forEach((n) => {
    if (n.tag === "p") body.push({ type: "p", text: Lr(n) });
    else if (n.tag === "h2") body.push({ type: "h2", id: n.attrs.id || "", text: Lr(n) });
    else if (classes(n).includes("callout")) {
      const b = one(n, "b");
      const rest = { children: n.children.filter((c) => c !== b) };
      body.push({ type: "callout", label: Lp(b), text: Lr(rest) });
    }
  });
  const secs = all(d, "main > section");
  const cards = (sec) =>
    all(sec, "article.prod").map((a) => {
      const href = one(a, ".acts a.more")?.attrs.href;
      return { image: media(one(a, "img")), title: Lp(one(a, "h3")), text: Lp(one(a, ".bd p")), meta: Lp(one(a, ".meta")), href };
    });
  const relatedSec = secs.find((s) => plain(one(s, ".eyebrow")) === "Related treatments");
  const moreSec = secs.find((s) => plain(one(s, ".eyebrow")) === "Keep reading");
  return {
    content: {
      header: {
        show: true,
        eyebrow: Lp(one(head, ".eyebrow")),
        title: Lr(one(head, "h1")),
        byline: all(head, ".byline span").map((s) => ({ label: hasPlaceholder(plain(s)) ? L("") : Lp(s), show: !hasPlaceholder(plain(s)) })),
        image: media(one(head, ".arthero img")),
      },
      toc: { title: Lp(one(toc, "b")), cta: { label: Lp(one(toc, "a.btn")), path: mapHref(one(toc, "a.btn").attrs.href) } },
      body,
      related: { show: true, ...headOf(relatedSec), items: cards(relatedSec).map((c) => ({ treatment: (c.href || "").replace(/\.html$/, ""), image: c.image, title: c.title, text: c.text, meta: c.meta })) },
      more: { show: true, ...headOf(moreSec), items: cards(moreSec).map((c) => ({ image: c.image, title: c.title, text: c.text, meta: c.meta, link: journalLink(c.href) })) },
      closing: journalCta(one(d, "section.cta")),
    },
    seo: seoOf("journal-botox-vs-xeomin"),
  };
})();

/* ------------------------------------------------------------------ 组装 */
const pages = {
  site: pageSite,
  home: pageHome,
  about: pageAbout,
  membership: pageMembership,
  "facial-blueprint": pageBlueprint,
  "journal-faq": pageJournalFaq,
  "journal-botox-vs-xeomin": pageJournalArticle,
};
const mediaList = [...mediaUsed].sort().map((key) => ({ key, alt: L(mediaAlt.get(key) || ""), name: key }));
const seed = {
  _comment: "由 tools/aura-extract.mjs 生成，请勿手改；字段结构见 docs/content-schema.md，格式见 docs/api-contract.md §9",
  categories,
  treatments,
  goals,
  pages,
  media: mediaList,
  mediaDir: path.relative(root, SITE),
};

/* ------------------------------------------------------------------ 校验 */
const errors = [];
const err = (m) => errors.push(m);
// 1 slug 唯一
const seen = new Set();
for (const t of treatments) {
  if (seen.has(t.slug)) err(`治疗 slug 重复：${t.slug}`);
  seen.add(t.slug);
}
for (const g of goals) {
  if (seen.has(`goal:${g.slug}`)) err(`目标 slug 重复：${g.slug}`);
  seen.add(`goal:${g.slug}`);
}
// 2 媒体文件存在
for (const k of mediaMissing) err(`媒体文件不存在：${k}`);
// 3 导航链接都能对应到治疗或页面
const catKeys = new Set(categories.map((c) => c.key));
for (const [slug, nv] of navOf) {
  if (!TREATMENT_SLUGS.has(slug)) err(`导航里的链接找不到治疗页文件：${slug}`);
  if (!catKeys.has(nv.category)) err(`导航类别不存在：${nv.category}`);
}
for (const c of categories) {
  if (c.linkType === "page" && !(Object.values(CATEGORY_LINK_PAGES).includes(c.linkTarget))) err(`类别页面链接无效：${c.key}`);
}
for (const t of treatments) if (!t.categoryKey) err(`治疗没有出现在导航里：${t.slug}`);
for (const [k, list] of Object.entries(dropdowns))
  for (const it of list) {
    const p = it.path.replace(/#.*$/, "");
    if (!Object.values(PAGE_ROUTE).includes(p) && !/^\/(treatments|goals)\//.test(p)) err(`导航下拉链接无效：${k} → ${it.path}`);
  }
// 4 内容里的站内链接（html 字段）与 treatment/goal 引用
const json = JSON.stringify(seed);
for (const m of json.matchAll(/href=\\"(\/[^"\\#]*)/g)) {
  const p = m[1];
  const ok = Object.values(PAGE_ROUTE).includes(p) || (/^\/treatments\/([\w-]+)$/.test(p) && TREATMENT_SLUGS.has(p.split("/")[2])) || (/^\/goals\/([\w-]+)$/.test(p) && goals.some((g) => g.slug === p.split("/")[2]));
  if (!ok) err(`内容里的站内链接无效：${p}`);
}
const refSlug = (s, where) => {
  if (s && !TREATMENT_SLUGS.has(s)) err(`${where} 引用了不存在的治疗：${s}`);
};
pageHome.content.stars.items.forEach((i) => refSlug(i.treatment, "home.stars"));
pageJournalArticle.content.related.items.forEach((i) => refSlug(i.treatment, "journal.related"));
goals.forEach((g) => g.content.items.forEach((i) => refSlug(i.treatment, `goal ${g.slug}`)));
bookingMenu.forEach((g) => g.items.forEach((i) => i.treatmentSlug === null && warn(`预约菜单条目没有对应治疗页：${i.title.en}`)));
// 5 不允许占位或原型残留进入可见内容
const visibleText = JSON.stringify(
  JSON.parse(json, (k, v) => (v && typeof v === "object" && v.show === false ? undefined : v)),
  (k, v) => v,
);
for (const re of [/Copy to come/i, /\[XXX/i, /\[Author\]/i, /\[Provider/i, /\[date\]/i, /\[aurainstitute\]/i, /Page prototype/i, /Prototype:/i]) {
  if (re.test(visibleText)) err(`可见内容里仍有占位或原型文字：${re}`);
}
// 6 html 字段只含白名单标签
for (const m of json.matchAll(/<\/?([a-z][a-z0-9]*)/g)) {
  if (!KEEP.has(m[1])) err(`html 字段含不允许的标签：<${m[1]}>`);
}
// 7 每个治疗页文案完整性
for (const t of treatments) {
  if (t.copyComplete) {
    for (const k of ["hero", "how", "tech", "faq", "closing"]) if (!t.content[k] || t.content[k].show === false) err(`${t.slug} 缺少区块 ${k}`);
    if (!t.content.fit?.show && !t.content.grid?.show) err(`${t.slug} 缺少 fit/grid`);
  }
}
if (treatments.length !== 35) err(`治疗页数量不是 35：${treatments.length}`);
if (goals.length !== 6) err(`目标页数量不是 6：${goals.length}`);

/* ------------------------------------------------------------------ 输出 */
if (!CHECK_ONLY) {
  fs.mkdirSync(path.join(root, "seed", "fragments"), { recursive: true });
  fs.writeFileSync(path.join(root, "seed", "aura-seed.json"), JSON.stringify(seed, null, 2) + "\n");
  for (const [name, content] of Object.entries(fragments)) fs.writeFileSync(path.join(root, "seed", "fragments", name), content + "\n");
}
const stat = {
  原型目录: path.relative(root, SITE),
  HTML文件: files.length,
  页面: Object.keys(pages).length,
  类别: categories.length,
  治疗: treatments.length,
  目标页: goals.length,
  媒体引用: mediaList.length,
  媒体缺失: [...mediaMissing],
  占位治疗页: placeholderTreatments,
  SVG片段: Object.keys(fragments),
  预约菜单条目: bookingMenu.reduce((n, g) => n + g.items.length, 0),
};
console.log(JSON.stringify(stat, null, 2));
const unused = fs.readdirSync(SITE).filter((f) => /\.(jpg|png|webp|mp4)$/.test(f) && !mediaUsed.has(f));
console.log(`未被内容引用的媒体文件：${unused.length} 个（旧版迭代遗留，不导入媒体库；含 hero-aura3/4.mp4 与海报）。前 8 个：${unused.slice(0, 8).join(", ") || "无"}`);
if (warnings.length) console.log(`\n警告（${warnings.length}）：\n- ${warnings.join("\n- ")}`);
if (errors.length) {
  console.error(`\n校验失败（${errors.length}）：\n- ${errors.join("\n- ")}`);
  process.exit(1);
}
console.log("\n校验通过");
