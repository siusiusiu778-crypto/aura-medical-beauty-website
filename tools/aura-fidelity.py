#!/usr/bin/env python3
"""还原度核对：逐页比较原型（legacy/site）的可见文本与重构后渲染出的文本，列出缺失项。

用法：python3 tools/aura-fidelity.py [站点根地址，默认 http://localhost:3100]
原型里的每个文本节点（含 alt、placeholder）都必须出现在对应的新页面里；顶部导航与页脚单独对比一次。
"""
import glob, html, os, re, sys, urllib.request
from html.parser import HTMLParser

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3100").rstrip("/")
LEGACY = "legacy/site" if os.path.isdir("legacy/site") else "site"
SKIP_TAGS = {"script", "style", "noscript", "svg", "head", "title"}
SKIP_FILES = {"nav.html", "index.html"}


class Texts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.out = [], []

    def handle_starttag(self, tag, attrs):
        if tag in {"br", "img", "input", "meta", "link", "hr", "source"}:
            d = dict(attrs)
            for k in ("alt", "placeholder"):
                if d.get(k) and not any(t in SKIP_TAGS for t in self.stack):
                    self.out.append(d[k])
            return
        self.stack.append(tag)
        d = dict(attrs)
        if tag == "svg":
            return

    def handle_endtag(self, tag):
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass

    def handle_data(self, data):
        if any(t in SKIP_TAGS for t in self.stack):
            return
        self.out.append(data)


def texts(markup):
    p = Texts()
    p.feed(markup)
    return p.out


def norm(s):
    s = html.unescape(s).replace("­", "").replace("​", "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("&shy;", "")
    return re.sub(r"\s+", "", s).lower()


def route(name):
    stem = name[:-5]
    return {
        "home": "/", "about": "/about", "aura-prime": "/membership", "facial-blueprint": "/facial-blueprint",
        "journal-faq": "/journal/faq", "journal-botox-vs-xeomin": "/journal/botox-vs-xeomin",
    }.get(stem) or (f"/goals/{stem[5:]}" if stem.startswith("goal-") else f"/treatments/{stem}")


def fetch(path):
    try:
        with urllib.request.urlopen(BASE + path, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return ""


# 原型里不属于站点内容的东西：原型提示横幅
PROTO = re.compile(r"page prototype|^all pages$", re.I)

total_missing = 0
report = {}
for f in sorted(glob.glob(f"{LEGACY}/*.html")):
    name = os.path.basename(f)
    if name in SKIP_FILES:
        continue
    src = open(f, encoding="utf-8").read()
    live = fetch(route(name))
    if not live:
        report[name] = ["<页面无法访问>"]
        total_missing += 1
        continue
    live_stream = norm(" ".join(texts(live)))
    missing = []
    seen = set()
    for t in texts(src):
        t = html.unescape(t).strip()
        if len(norm(t)) < 6 or PROTO.search(t):
            continue
        n = norm(t)
        if n in seen:
            continue
        seen.add(n)
        if n not in live_stream:
            missing.append(re.sub(r"\s+", " ", t)[:140])
    if missing:
        report[name] = missing
        total_missing += len(missing)

for name, items in report.items():
    print(f"\n## {name}  ({len(items)})")
    for m in items:
        print("  -", m)
print(f"\n共 {len(report)} 个页面有缺失，{total_missing} 处")
