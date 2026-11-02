# Builds out/home.html (prototype homepage with real links) from the standalone homepage.
import re, shutil
SRC = '/home/claude/hp/aurelle-homepage.html'
OUT = '/home/claude/pages/out'
for f in ['hero-aura3.mp4', 'poster-aura3.jpg']:
    shutil.copy('/mnt/user-data/outputs/' + f, OUT + '/' + f)
s = open(SRC).read()

TOP = {'Face Design': 'face-design.html', 'Skin &amp; Glow': 'skin-glow.html', 'Wellness &amp; Longevity': 'wellness.html',
       'Body': 'body-shape.html', 'Membership': 'aura-prime.html', 'About': 'about.html'}
GRP = {'Lift &amp; Tighten': 'face-design.html#lift', 'Restore &amp; Fill': 'face-design.html#balancing', 'Smooth &amp; Relax': 'face-design.html#lines',
       'V-Line &amp; Contour': 'face-design.html#vline', 'Start Here': 'skin-glow.html#start', 'Deep Cleanse': 'skin-glow.html#cleanse',
       'Brighten &amp; Texture': 'skin-glow.html#tone', 'Hydrate &amp; Glow · Face': 'skin-glow.html#hydrate', 'Neck &amp; Scalp': 'skin-glow.html#neck'}
ITEM = {'Gold RF Microneedling': 'skin-glow.html#pores', 'Scalp &amp; Hair Restoration': 'skin-glow.html#scalp', 'Gold Skin Analysis': 'gold-skin-analysis.html',
        'Botox® &amp; Xeomin®': 'botox-xeomin.html', 'EMFACE®': 'emface.html', 'Face Hydration · Rejuran®': 'glow-booster.html',
        'NAD+ IV Drip': 'nad-iv.html', 'EXOMIND™ · Sleep, mood &amp; focus': 'wellness.html#mind', 'More coming soon': 'wellness.html#more',
        'Body Sculpt · Abdomen': 'body-sculpt.html', 'AURA Prime': 'aura-prime.html', 'The AURA Aesthetic': 'face-design.html',
        'Our Team': 'about.html', 'The Clinic': 'about.html', 'Journal &amp; FAQ': 'journal-faq.html'}

# rewrite the navbar links
i = s.index('<nav class="navbar"'); j = s.index('</nav>', i)
nav = s[i:j]
out, pos = '', 0
for li in re.finditer(r'<li>(.*?)</li>', nav, re.S):
    body = li.group(1)
    top = re.search(r'<a href="#">([^<]+)</a>', body).group(1)
    page = TOP.get(top, '#')
    body = body.replace(f'<a href="#">{top}</a>', f'<a href="{page}">{top}</a>', 1)
    def grp_sub(m):
        h5, links = m.group(1), m.group(2)
        tgt = GRP.get(h5, page)
        links = re.sub(r'<a href="#">([^<]+)</a>', lambda a: f'<a href="{ITEM.get(a.group(1), tgt)}">{a.group(1)}</a>', links)
        return f'<div class="grp"><h5>{h5}</h5>{links}</div>'
    body = re.sub(r'<div class="grp"><h5>([^<]+)</h5>(.*?)</div>', grp_sub, body)
    body = re.sub(r'<a href="#">([^<]+)</a>', lambda a: f'<a href="{ITEM.get(a.group(1), page)}">{a.group(1)}</a>', body)
    out += nav[pos:li.start()] + f'<li>{body}</li>'; pos = li.end()
nav = out + nav[pos:]
s = s[:i] + nav + s[j:]
# top-level links: follow on click (desktop hover opens the menu)
s = s.replace("a.addEventListener('click',e=>{e.preventDefault();place();", "a.addEventListener('click',e=>{if(matchMedia('(hover:hover)').matches)return;e.preventDefault();place();")

# goal tiles -> Level 2 sections
LINK = {'lift': 'face-design.html#lift', 'balance': 'face-design.html#balancing', 'smooth': 'face-design.html#lines',
        'skin': 'skin-glow.html#cleanse', 'glow': 'skin-glow.html#hydrate', 'bodywell': 'body-shape.html'}
s = s.replace("document.getElementById('fxGrid').addEventListener('click',e=>{const b=e.target.closest('.fx'); if(b) openBook(null,null,b.dataset.result);});",
              "const FXLINK=" + str(LINK).replace("'", '"') + ";\ndocument.getElementById('fxGrid').addEventListener('click',e=>{const b=e.target.closest('.fx'); if(b) location.href=FXLINK[b.dataset.result];});")
s = s.replace('aria-label="${r.name}: see treatments and book"', 'aria-label="${r.name}: see treatments"')
# featured Learn More -> pages
s = s.replace('<a class="more" href="#" data-learn="bodywell">', '<a class="more" href="wellness.html">').replace('<a class="more" href="#" data-learn="lift">', '<a class="more" href="emface.html">')
s = s.replace('<a class="logo" href="#top"', '<a class="logo" href="home.html"')
# prototype bar + full document
k = s.index('</style>') + len('</style>')
head, rest = s[:k], s[k:]
bar = '<div style="background:#221B17;color:#F7F3EE;font:12px/1.4 Arial,sans-serif;text-align:center;padding:6px 16px">Page prototype · copy is a final draft, photos are placeholders · <a href="index.html" style="color:inherit">All pages</a></div>'
html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' + head + '</head><body>' + bar + rest + '</body></html>'
open(OUT + '/home.html', 'w').write(html)

# every prototype page: Home and logo go to home.html
import glob
for p in glob.glob(OUT + '/*.html'):
    if p.endswith('/home.html') or p.endswith('/index.html'): continue
    t = open(p).read(); o = t
    t = t.replace('<a href="index.html">Home</a>', '<a href="home.html">Home</a>').replace('<a class="logo" href="index.html">', '<a class="logo" href="home.html">')
    if t != o: open(p, 'w').write(t)
idx = open(OUT + '/index.html').read()
idx = idx.replace('<a class="card" href="https://claude.ai/artifact/P8EsT9wiLWWw4JFeaPUpnq" target="_blank" rel="noopener"><div class="bd"><span class="lv">Homepage · opens separately</span>',
                  '<a class="card" href="home.html"><div class="bd"><span class="lv">Homepage</span>')
open(OUT + '/index.html', 'w').write(idx)
print('home built')
