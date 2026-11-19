// 把原型的 CSS 按页面类型限定到 .pg-<页面> 之下（与 uswoo-website 的页面样式同一思路）。
// 原型每个页面各自加载自己的 CSS，合并进一个 SPA 后必须隔离，否则 site.css / l3.css 里同名选择器会互相覆盖。
// 用法：pnpm scope-css（读取 legacy/site，生成 app/assets/css/pages/*.css 与 chrome.css；生成物不要手改）。
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import postcss from "postcss";

const SRC = new URL("../legacy/site/", import.meta.url).pathname;
const OUT = new URL("../app/assets/css/", import.meta.url).pathname;
mkdirSync(OUT + "pages", { recursive: true });

const read = name => readFileSync(SRC + name, "utf8");
const inline = html => [...read(html).matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map(m => m[1]).join("\n");

function scopeSelector(selector, scope) {
  const s = selector.trim();
  if (!s) return s;
  if (s.startsWith("#site-header") || s.startsWith(".mnav")) return s; // nav.css 已自行限定，保持全局
  if (/^(:root|html|body)(?![\w-])/.test(s)) return s.replace(/^(:root|html|body)/, scope);
  return `${scope} ${s}`;
}

function scopeCss(css, scope, { only } = {}) {
  // 原型里个别内联样式的末尾被截断（缺右花括号、最后一条规则不完整）：先原样解析，失败就截到最后一个完整的右花括号再补齐
  let root;
  const attempts = [css];
  const cut = css.slice(0, css.lastIndexOf("}") + 1);
  for (let extra = 0; extra < 4; extra += 1) attempts.push(cut + "}".repeat(extra));
  for (const attempt of attempts) {
    try { root = postcss.parse(attempt); break; } catch { /* 试下一种 */ }
  }
  if (!root) throw new Error("CSS 无法解析：" + css.slice(0, 80));
  const walk = container => {
    container.each(node => {
      if (node.type === "rule") {
        if (node.parent.type === "atrule" && /keyframes$/i.test(node.parent.name)) return;
        node.selectors = node.selectors.map(sel => scopeSelector(sel, scope));
      } else if (node.type === "atrule") {
        if (/keyframes$/i.test(node.name) || node.name === "font-face" || node.name === "import" || node.name === "charset") return;
        if (node.nodes) walk(node);
      }
    });
  };
  walk(root);
  if (only) root.walkRules(rule => { if (!only(rule)) rule.remove(); });
  root.walkAtRules(at => { if (at.nodes && at.nodes.length === 0) at.remove(); });
  return root.toString();
}

const pages = {
  home: () => [inline("home.html")],
  about: () => [read("site.css"), inline("about.html")],
  treatment: () => [read("site.css"), read("l3.css")],
  membership: () => [read("site.css"), read("l3.css"), inline("aura-prime.html")],
  blueprint: () => [read("site.css"), read("l3.css"), inline("facial-blueprint.html")],
  goal: () => [read("site.css"), read("col.css"), inline("goal-skin-tightening.html")],
  faq: () => [read("site.css"), read("col.css")],
  journal: () => [read("site.css"), read("svc.css")]
};

for (const [name, parts] of Object.entries(pages)) {
  const scope = `.pg-${name}`;
  const css = parts().map(part => scopeCss(part, scope)).join("\n");
  writeFileSync(`${OUT}pages/${name}.css`, `/* 由 scripts/scope-css.mjs 从 legacy/site 生成，请勿手改；补充样式写在同名 .extra.css */\n${css}\n`);
}

// 站点外壳：导航（原本已限定在 #site-header 下）+ 页脚（取自 l3.css 里的 .foot 规则，限定在 .aura 下）
const chrome = read("nav.css") + "\n" + scopeCss(read("l3.css"), ".aura", { only: rule => rule.selector.includes(".foot") });
writeFileSync(`${OUT}chrome.css`, `/* 由 scripts/scope-css.mjs 生成，请勿手改 */\n${chrome}\n`);

// 预约抽屉：原型里它的样式写在首页的内联 CSS 里（其他页面点 Book 是跳转到首页再打开）。
// 现在抽屉全站可用，所以单独取出，限定在 .aura .drawer 下（不受各页面的 .btn、.steps、.group 等同名样式影响）。
{
  const home = inline("home.html");
  const start = home.search(/\/\*\s*drawer\s*\*\//);
  const end = home.search(/\/\*\s*-+\s*scroll reveal/);
  const slice = home.slice(start, end);
  // 抽屉里用到的按钮样式在首页顶部（.btn / .btn-solid / .btn-lg），一并带上
  const btn = home.slice(home.indexOf(".btn{"), home.search(/\/\*\s*hero \(type unchanged/));
  const scoped = css => {
    const root = postcss.parse(css);
    const walk = c => c.each(n => {
      if (n.type === "rule") n.selectors = n.selectors.map(sel => (/^\.(scrim|drawer)(?![\w-])/.test(sel.trim()) ? `.aura ${sel.trim()}` : `.aura .drawer ${sel.trim()}`));
      else if (n.type === "atrule" && n.nodes && !/keyframes$/.test(n.name)) walk(n);
    });
    walk(root);
    return root.toString();
  };
  writeFileSync(`${OUT}drawer.css`, `/* 由 scripts/scope-css.mjs 生成（预约抽屉），请勿手改 */\n${scoped(btn)}\n${scoped(slice)}\n`);
}
console.log("done");
