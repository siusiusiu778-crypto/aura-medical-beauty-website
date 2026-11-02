import os, re, shutil
OUT = '/home/claude/pages/out'; os.makedirs(OUT, exist_ok=True)
for f in ['svc-lift.jpg','about.jpg','r-lift.jpg','svc-laser.jpg','r-tone.jpg','r-texture.jpg','r-smooth.jpg','r-care2.jpg','r-body2.jpg','s-skin2.jpg','s-laser.jpg','s-inject.jpg','s-body.jpg','about-reception.jpg','r-care.jpg','r-body.jpg','svc-skin.jpg']:
    shutil.copy('/home/claude/site/'+f, OUT+'/'+f)

NAV = [('face-design.html','Face Design'),('skin-glow.html','Skin &amp; Glow'),('wellness.html','Wellness &amp; Longevity'),('body-shape.html','Body'),('aura-prime.html','Membership'),('about.html','About')]

CSS = r'''
:root{--bg:#F7F3EE;--surface:#EFE7DE;--line:#DFD2C5;--fg:#221B17;--muted:#76665B;--accent:#3F3029;--on-accent:#F7F3EE;--card:#FCFAF7;--tan:#D9B48F;--rust:#A0533A;--sans:"Instrument Sans","Helvetica Neue",Arial,sans-serif;--serif:"Instrument Serif","Times New Roman",serif}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#141110;--surface:#1E1916;--line:#382E28;--fg:#EFE6DD;--muted:#A99789;--accent:#E3CDB9;--on-accent:#1C1512;--card:#1C1714;--rust:#E09A7E;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141110;--surface:#1E1916;--line:#382E28;--fg:#EFE6DD;--muted:#A99789;--accent:#E3CDB9;--on-accent:#1C1512;--card:#1C1714;--rust:#E09A7E;color-scheme:dark}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
img{max-width:100%}a{color:inherit}button{font:inherit;cursor:pointer}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.wrap{max-width:1240px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
@media(min-width:760px){.wrap{padding-left:max(48px,env(safe-area-inset-left,0px));padding-right:max(48px,env(safe-area-inset-right,0px))}}
h1,h2,h3{margin:0;font-weight:400;text-wrap:balance}em{font-family:var(--serif)}
.eyebrow{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin:0}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:14px 30px;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;border:1px solid transparent;text-decoration:none;background:var(--accent);color:var(--on-accent)}
.btn.line{background:transparent;border-color:currentColor;color:inherit}
.proto{background:var(--fg);color:var(--bg);font-size:12px;text-align:center;padding:6px 16px}
.proto a{color:inherit}
.nav{position:sticky;top:0;z-index:50;background:var(--bg);border-bottom:1px solid var(--line)}
.nav .wrap{height:68px;display:flex;align-items:center;justify-content:space-between;gap:16px;max-width:none}
.logo{font-size:24px;font-weight:500;letter-spacing:-.03em;text-decoration:none;white-space:nowrap}.logo span{font-size:.46em;letter-spacing:.3em;text-transform:uppercase;vertical-align:.4em;margin-left:4px}
.nav ul{list-style:none;margin:0;padding:0;display:flex;gap:20px;font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.nav ul a{text-decoration:none;white-space:nowrap}.nav ul .on{border-bottom:1px solid currentColor;padding-bottom:3px}
.nav .btn{padding:10px 20px;font-size:11.5px;border-radius:999px}
@media(max-width:1180px){.nav ul{display:none}}
.crumbs{font-size:12.5px;color:var(--muted);padding-block:18px 0}.crumbs a{text-decoration:none}
.hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);min-height:clamp(380px,38vw,520px);background:var(--tan);color:#241A14;margin-top:18px}
.hero .tx{display:flex;flex-direction:column;justify-content:center;gap:18px;padding:clamp(28px,5vw,72px)}
.hero h1{font-family:var(--serif);font-size:clamp(44px,5vw,72px);line-height:1}
.hero p{margin:0;font-size:clamp(16px,1.4vw,19px);max-width:36ch}
.hero .eyebrow{color:#5a4636}
.hero .btns{display:flex;gap:12px;flex-wrap:wrap}.hero .btn{background:#241A14;color:#F7F3EE}.hero .btn.line{background:transparent;color:#241A14;border-color:#241A14}
.hero .ph{position:relative;overflow:hidden;min-height:280px}
.hero .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero .ph::before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,var(--tan) 0%,rgba(217,180,143,0) 25%)}
@media(max-width:860px){.hero{grid-template-columns:1fr}.hero .ph{order:-1;aspect-ratio:4/3;min-height:0}.hero .ph::before{background:linear-gradient(0deg,var(--tan),rgba(217,180,143,0) 25%)}}
section{padding-block:clamp(56px,7vw,96px)}
.alt{background:var(--surface)}
.head{display:grid;gap:12px;margin-bottom:clamp(28px,4vw,44px);max-width:660px}
.head h2{font-family:var(--serif);font-size:clamp(32px,3.4vw,48px);line-height:1.05}
.head p{margin:0;color:var(--muted)}
.needs{display:grid;gap:clamp(36px,5vw,64px)}
.need{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(24px,4vw,64px);align-items:center}
.need:nth-child(even) .ph{order:2}
.need .ph{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--surface)}
.need .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.need .tx{display:grid;gap:14px;min-width:0}
.need h3{font-size:clamp(26px,2.4vw,34px);font-family:var(--serif)}
.need p{margin:0;color:var(--muted);max-width:50ch}
.tags{display:flex;flex-wrap:wrap;gap:8px}.tags span{border:1px solid var(--line);padding:6px 12px;font-size:13px;background:var(--card)}
.need .row{display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.price{font-variant-numeric:tabular-nums}.price b{font-size:20px;font-weight:600}.price s{color:var(--muted);margin-right:6px}
.more{font-size:12px;letter-spacing:.16em;text-transform:uppercase;text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:2px}
@media(max-width:860px){.need{grid-template-columns:1fr}.need:nth-child(even) .ph{order:0}}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
@media(max-width:960px){.grid3,.grid4{grid-template-columns:1fr 1fr}}@media(max-width:600px){.grid3,.grid4{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);display:flex;flex-direction:column;min-width:0}
.card .ph{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--surface)}.card .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.card .bd{padding:22px;display:grid;gap:10px;align-content:start;flex:1}.card h3{font-size:21px;font-weight:600}.card p{margin:0;font-size:14.5px;color:var(--muted)}
.card .ft{padding:0 22px 22px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.badge{display:inline-block;background:var(--rust);color:#fff;font-size:11px;letter-spacing:.12em;text-transform:uppercase;padding:4px 10px;justify-self:start}
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;counter-reset:s}
.steps div{border-top:1px solid var(--fg);padding-top:16px;counter-increment:s;display:grid;gap:6px}
.steps div::before{content:counter(s,decimal-leading-zero);font-family:var(--serif);font-size:28px;color:var(--rust)}
.steps b{font-size:17px;font-weight:600}.steps span{color:var(--muted);font-size:14.5px}
@media(max-width:860px){.steps{grid-template-columns:1fr 1fr}}
.tbl{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:15px;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:13px 10px;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:500}
td.hi{color:var(--rust);font-weight:600}
.note{font-size:12.5px;color:var(--muted);margin-top:14px}
details{border-bottom:1px solid var(--line);padding-block:18px}details:first-of-type{border-top:1px solid var(--line)}
summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px;font-size:17px;font-weight:500}summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-size:22px;line-height:1;color:var(--muted)}details[open] summary::after{content:"–"}details p{margin:12px 0 0;color:var(--muted);max-width:62ch}
.split{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(28px,5vw,80px);align-items:start}@media(max-width:860px){.split{grid-template-columns:1fr}}
.ph-empty{aspect-ratio:3/4;background:repeating-linear-gradient(135deg,var(--surface) 0 12px,var(--card) 12px 24px);border:1px dashed var(--line);display:grid;place-items:center;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.cta{background:var(--accent);color:var(--on-accent);text-align:center}.cta .wrap{display:grid;gap:16px;justify-items:center}
.cta h2{font-family:var(--serif);font-size:clamp(34px,4vw,52px)}.cta p{margin:0;opacity:.8;max-width:48ch}.cta .btn{background:var(--on-accent);color:var(--accent)}
footer{padding-block:28px;font-size:12.5px;color:var(--muted);text-align:center}
.mini{display:grid;gap:4px;font-size:14px}.mini div{display:flex;justify-content:space-between;gap:12px;border-bottom:1px dotted var(--line);padding-block:6px}

.cat{padding-block:clamp(40px,5vw,72px);border-top:1px solid var(--line)}
.cat:first-of-type{border-top:0}
.cat .ch{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin-bottom:24px}
.cat h2{font-family:var(--serif);font-size:clamp(30px,3vw,42px);line-height:1.05}
.cat .ch p{margin:6px 0 0;color:var(--muted);max-width:60ch}
.subnav{position:sticky;top:68px;z-index:40;background:var(--bg);border-bottom:1px solid var(--line)}
.subnav .wrap{display:flex;gap:26px;overflow-x:auto;scrollbar-width:none;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;padding-block:14px}
.subnav a{text-decoration:none;white-space:nowrap}.subnav a:hover{text-decoration:underline;text-underline-offset:5px}
.prods{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
@media(max-width:1100px){.prods{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:820px){.prods{grid-template-columns:1fr 1fr}}@media(max-width:520px){.prods{grid-template-columns:1fr}}
.prod{background:var(--card);border:1px solid var(--line);display:flex;flex-direction:column;min-width:0}
.prod .ph{position:relative;aspect-ratio:1/1;overflow:hidden;background:var(--surface)}.prod .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .8s ease}
.prod:hover .ph img{transform:scale(1.04)}
.prod .sale{position:absolute;top:10px;left:10px;background:var(--rust);color:#fff;font-size:11px;letter-spacing:.1em;text-transform:uppercase;padding:3px 9px}
.prod .bd{padding:16px 16px 6px;display:grid;gap:6px;flex:1;align-content:start}
.prod h3{font-size:17px;font-weight:600;letter-spacing:.01em}
.prod p{margin:0;font-size:13.5px;color:var(--muted);line-height:1.5}
.prod .meta{font-size:12px;color:var(--muted);letter-spacing:.04em}
.prod .ft{padding:12px 16px 16px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.prod .price{font-size:14px}.prod .price b{font-size:17px}
.prod .acts{display:flex;gap:12px;align-items:center}
.prod .bk{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;background:var(--accent);color:var(--on-accent);padding:7px 12px}
'''
open(OUT+'/site.css','w').write(CSS)

HEAD = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap">
<link rel="stylesheet" href="site.css"></head><body>'''

def nav(active):
    lis = ''.join(f'<li><a href="{h}"{" class=\"on\"" if h==active else ""}>{n}</a></li>' for h,n in NAV)
    return f'''<div class="proto">Page prototype · copy is a final draft, photos are placeholders · <a href="index.html">All pages</a></div>
<header class="nav"><div class="wrap"><a class="logo" href="index.html">aura<span>Institute</span></a><ul>{lis}</ul><a class="btn" href="#book">Book a Consultation</a></div></header>'''

def hero(eyebrow, h1, p, img, pos='50% 40%', btns=None):
    btns = btns or '<a class="btn" href="#book">Book a Consultation</a>'
    return f'''<div class="wrap"><div class="hero"><div class="tx"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p>{p}</p><div class="btns">{btns}</div></div>
<div class="ph"><img src="{img}" alt="" style="object-position:{pos}"></div></div></div>'''

def need(title, desc, tags, price, img, link='#', pos='50% 40%', more='Explore'):
    t = ''.join(f'<span>{x}</span>' for x in tags)
    return f'''<article class="need"><div class="ph"><img src="{img}" alt="" style="object-position:{pos}"></div><div class="tx"><h3>{title}</h3><p>{desc}</p><div class="tags">{t}</div>
<div class="row"><span class="price">{price}</span><a class="more" href="{link}">{more}</a></div></div></article>'''

def cta(h, p, b='Book Now'):
    return f'<section class="cta" id="book"><div class="wrap"><p class="eyebrow" style="color:inherit;opacity:.7">Rockefeller Center, New York</p><h2>{h}</h2><p>{p}</p><a class="btn" href="#book">{b}</a></div></section>'

def page(fn, title, active, crumbs, body):
    html = HEAD.format(title=title) + nav(active) + f'<main><div class="wrap crumbs"><a href="index.html">Home</a> / {crumbs}</div>' + body + '</main><footer>AURA Institute · 630 Fifth Avenue, Suite 1812, New York, NY 10111 · Results vary by individual.</footer></body></html>'
    open(f'{OUT}/{fn}','w').write(html)

def faq(items):
    return ''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(items))


def prod(name, desc, meta, price, img, pos='50% 40%', sale='', link='#'):
    s = f'<span class="sale">{sale}</span>' if sale else ''
    return f'''<article class="prod"><div class="ph"><img src="{img}" alt="" style="object-position:{pos}">{s}</div><div class="bd"><h3>{name}</h3><p>{desc}</p><span class="meta">{meta}</span></div>
<div class="ft"><span class="price">{price}</span><span class="acts"><a class="more" href="{link}">Details</a><a class="bk" href="#book">Book</a></span></div></article>'''

def cat(cid, title, desc, prods, guide=''):
    g = f'<a class="more" href="{guide}">Read the guide</a>' if guide else ''
    return f'<div class="cat" id="{cid}"><div class="ch"><div><h2>{title}</h2><p>{desc}</p></div>{g}</div><div class="prods">{"".join(prods)}</div></div>'

def subnav(items):
    return '<div class="subnav"><div class="wrap">'+''.join(f'<a href="#{i}">{t}</a>' for i,t in items)+'</div></div>'

# 1 SPECIAL OFFERS
page('special-offers.html','Special Offers · AURA Institute','special-offers.html','Special Offers',
 hero('Special Offers','Try us <em>first</em>.','Signature treatments at first-visit prices, plus packages that make a full course easier on your budget.','svc-lift.jpg','40% 30%','<a class="btn" href="#new">See New Client Offers</a><a class="btn line" href="#packages">Packages</a>') +
 '''<section id="new"><div class="wrap"><div class="head"><p class="eyebrow">New Client Offers</p><h2>Your <em>first visit</em>, for less</h2><p>Every new client starts with a complimentary Gold Skin Analysis. Then choose one signature treatment at a first-visit price.</p></div>
<div class="grid4">'''+''.join(f'<article class="card"><div class="bd"><span class="badge">{b}</span><h3>{n}</h3><p>{d}</p></div><div class="ft"><span class="price">{p}</span><a class="more" href="#book">Book</a></div></article>' for b,n,d,p in [
 ('Free','Gold Skin Analysis','A provider maps your skin and goals before any treatment.','<b>$0</b>'),
 ('34% off','Collagen Lift · Cheeks','Targeted collagen boost for the cheeks.','<s>$300</s><b>$199</b>'),
 ('34% off','Glow Booster','Deep hydration and glow, delivered into the skin.','<s>$450</s><b>$299</b>'),
 ('60% off','EMFACE® · 1 Area','Needle-free lift in 20 minutes.','<s>$1,000</s><b>$399</b>'),
 ('27% off','EXOMIND™','A calm, non-invasive treatment for mood and focus.','<s>$550</s><b>$399</b>'),
 ('20% off','Gold RF Microneedling','Pores, texture and tone in one treatment.','<s>$999</s><b>$799</b>')])+'''</div><p class="note">First-visit prices apply once per client per treatment.</p></div></section>
<section class="alt"><div class="wrap split"><div class="head"><p class="eyebrow">Monthly Specials</p><h2>This month at <em>AURA</em></h2><p>A rotating offer on one treatment each month. Sign up to hear first.</p></div>
<div class="card"><div class="bd"><span class="badge">Coming soon</span><h3>Monthly special to be announced</h3><p>The team will set one featured offer each month. This block shows the treatment, the offer, the dates and a Book button.</p></div></div></div></section>
<section id="packages"><div class="wrap"><div class="head"><p class="eyebrow">Treatment Packages</p><h2>Save with a <em>series</em></h2><p>Results build over several sessions. Packages lock in your plan at a lower price per visit.</p></div>
<div class="tbl"><table><thead><tr><th>Treatment</th><th>Sessions</th><th>Package price</th><th>Single session</th></tr></thead><tbody>'''+''.join(f'<tr><td>{a}</td><td>{b}</td><td class="hi">{c}</td><td>{d}</td></tr>' for a,b,c,d in [
 ('HydraFacial® Deluxe','4','$980','$285'),('HydraFacial® Platinum','4','$1,199','$329'),('Signature Facial / Barrier Recovery Facial','4','$819','$229'),('Glow Booster','3','$1,200','$450'),('Gold RF Microneedling','3','$2,699','$999'),('EMFACE® · 1 area','4','$3,200','$1,000'),('Collagen Lift · any 3 areas','4','$2,699','$800'),('Body Sculpt · Abdomen','4','$999','$300'),('NAD+ 250mg','6','$1,999','$400'),('EXOMIND™','6','$3,000','$550')])+'''</tbody></table></div></div></section>
<section class="alt"><div class="wrap split"><div class="head"><p class="eyebrow">Gift Cards</p><h2>Give the <em>glow</em></h2><p>Gift cards can be used for any treatment, package or membership.</p></div>
<div class="card"><div class="bd"><h3>AURA Gift Card</h3><p>Choose any amount. Delivered by email or as a printed card at the front desk.</p></div><div class="ft"><span class="price">Any amount</span><a class="more" href="#book">Buy a Gift Card</a></div></div></div></section>'''
 + cta('Start with a <em>free</em> skin analysis','We’ll map your skin and goals, then recommend the offer that fits.'))

# 2 FACE & CONTOUR
P=prod
page('face-contour.html','Face & Contour · AURA Institute','face-contour.html','Face &amp; Contour',
 hero('Face &amp; Contour','Face &amp; <em>Contour</em>','Every face treatment in one place. Choose by goal, see the price and book.','r-texture.jpg','50% 40%','<a class="btn" href="#wrinkles">Browse Treatments</a><a class="btn line" href="#book">Free Consultation</a>') +
 subnav([('lines','Smooth Lines'),('volume','Restore Volume'),('lift','Lift &amp; Tighten'),('vline','V-Line Contour'),('design','Face Design')]) +
 '<section style="padding-top:0"><div class="wrap">' +
 cat('lines','Smooth Lines','Soften expression lines while keeping your face natural and expressive.',[
   P('Botox® &amp; Xeomin®','Forehead lines, frown lines and crow’s feet. Your provider chooses the product and dose for you.','10–20 min · no downtime','From <b>$10</b> / unit','r-texture.jpg','50% 40%','','botox-xeomin.html'),
   P('Trap Tox · Shoulder Line','Relaxes the trapezius for a longer, softer neckline.','15 min · no downtime','<b>By units</b>','r-lift.jpg','50% 45%')]) +
 cat('volume','Restore Volume','Bring back lost volume in the lips, cheeks, temples and under-eyes.',[
   P('Lip &amp; Face Filler','Hyaluronic acid filler for lips, cheeks, chin and under-eyes. Half syringe available.','30–45 min · 1–3 days swelling','<b>$850</b> · half $500','r-smooth.jpg','50% 35%'),
   P('RADIESSE®','Collagen-stimulating filler for structure and contour.','30–45 min','<b>$1,200</b>','r-lift.jpg','50% 45%'),
   P('Sculptra®','Gradual collagen restoration for a fuller, firmer look.','30–45 min · series of 2–3','<b>$900</b>','r-tone.jpg','50% 35%')]) +
 cat('lift','Lift &amp; Tighten','Firmer skin and a lifted look, without surgery or downtime.',[
   P('EMFACE®','Needle-free lift for brows, cheeks and jawline.','20 min · no downtime · 1–4 areas','<s>$1,000</s><b>$399</b>','svc-lift.jpg','40% 30%','60% off','emface.html'),
   P('Thermage® FLX','Radiofrequency tightening for face and eyes.','Eyes 450 / Face 900 pulses','From <b>$1,999</b>','r-lift.jpg','50% 45%'),
   P('Collagen Lift','Targeted collagen boost for cheeks, eyes, neck or forehead.','4-session packages','<s>$300</s><b>$199</b>','svc-laser.jpg','50% 30%','34% off')],'lift-tighten.html') +
 cat('vline','V-Line Contour','A slimmer, more defined lower face and jawline.',[
   P('Jaw Slimming','Relaxes the masseter to soften a square jaw.','15 min · no downtime','<b>By units</b>','about.jpg','50% 25%'),
   P('V-Line Injection','Contouring injections to slim and define the lower face.','One side / both sides / + lift','From <b>$350</b>','r-smooth.jpg','50% 35%')]) +
 cat('design','Face Design','Not sure what you need? We plan your whole face in the right order: support, lift, volume, refine.',[
   P('Face Design Consultation','Gold Skin Analysis plus a full-face assessment with a provider.','30 min','<b>Free</b>','about-reception.jpg','50% 50%'),
   P('Signature Face Plan','A step-by-step plan built around your face, schedule and budget.','Planned at consultation','<b>By plan</b>','r-texture.jpg')]) +
 '</div></section>' + cta('Not sure where to <em>start</em>?','Book a complimentary consultation. We’ll look at your whole face and suggest a plan.'))

# 3 SKIN & GLOW
page('skin-glow.html','Skin & Glow · AURA Institute','skin-glow.html','Skin &amp; Glow',
 hero('Skin &amp; Glow','Skin &amp; <em>Glow</em>','Every skin treatment in one place: boosters, lasers and facials.','r-tone.jpg','50% 35%','<a class="btn" href="#glow">Browse Treatments</a><a class="btn line" href="#book">Free Skin Analysis</a>') +
 subnav([('glow','Hydrate &amp; Glow'),('tone','Spots &amp; Redness'),('pores','Pores, Acne &amp; Scars'),('facials','Facials'),('sensitive','Sensitive Skin')]) +
 '<section style="padding-top:0"><div class="wrap">' +
 cat('glow','Hydrate &amp; Glow','Skin boosters that hydrate deeply and bring back a dewy glow.',[
   P('Glow Booster','Hydration plus brightening, delivered into the skin.','30 min · series of 3 · 3 for $1,200','<s>$450</s><b>$299</b>','about.jpg','50% 25%','34% off','glow-booster.html')]) +
 cat('tone','Spots &amp; Redness','Even out sun spots, redness and dull tone.',[
   P('M22™ Photofacial','Intense pulsed light for spots, redness and uneven tone.','30 min · monthly series','<b>Consult</b>','r-care2.jpg','50% 55%')]) +
 cat('pores','Pores, Acne &amp; Scars','Refine pores and smooth acne scars and texture.',[
   P('Gold RF Microneedling','Pores, texture, acne scars and tone in one treatment.','60–90 min · 3 for $2,699','<s>$999</s><b>$799</b>','r-lift.jpg','50% 45%','20% off')]) +
 cat('facials','Facials','Regular deep cleansing, hydration and repair.',[
   P('HydraFacial® Deluxe','Cleanse, extract and hydrate.','60 min · 4 for $980','<b>$285</b>','r-care2.jpg','50% 55%'),
   P('HydraFacial® Platinum','Adds lymphatic drainage and boosters.','75 min · 4 for $1,199','<b>$329</b>','about.jpg','50% 25%'),
   P('Signature Facial','Our relaxing, restorative house facial.','60 min · 4 for $819','<b>$229</b>','r-tone.jpg','50% 35%'),
   P('Barrier Recovery Facial','Calms and repairs sensitive or post-laser skin.','60 min · 4 for $819','<b>$229</b>','svc-laser.jpg','50% 30%')]) +
 cat('sensitive','Sensitive Skin','Redness or stinging? We repair the barrier first, then treat.',[
   P('Gold Skin Analysis','A provider maps hydration, tone, texture and sensitivity.','20 min','<b>Free</b>','about-reception.jpg','50% 50%'),
   P('Repair-First Plan','Barrier Recovery Facials to calm and rebuild, then gentle brightening.','Planned at consultation','From <b>$229</b>','r-care2.jpg','50% 55%')]) +
 '</div></section>' + cta('Get a <em>free</em> skin analysis','We’ll check hydration, tone and texture, then build your plan.'))

# 4 BODY SHAPE
page('body-shape.html','Body Shape · AURA Institute','body-shape.html','Body Shape',
 hero('Body Shape','Body <em>Shape</em>','Contour, smooth and refine, from waistline to shoulder line.','r-body2.jpg','50% 35%','<a class="btn" href="#contour">Browse Treatments</a><a class="btn line" href="#book">Free Consultation</a>') +
 subnav([('contour','Body Sculpt'),('stretch','Stretch Mark Repair'),('shoulder','Shoulder &amp; Neckline')]) +
 '<section style="padding-top:0"><div class="wrap">' +
 cat('contour','Body Sculpt','Non-invasive fat reduction with no needles or downtime.',[
   P('Body Sculpt · Abdomen','Targets stubborn fat around the waist.','30 min · 4 for $999','<b>$300</b>','s-body.jpg','45% 50%','','body-sculpt.html')]) +
 cat('stretch','Stretch Mark Repair','Two steps: break up old scar tissue, then rebuild collagen.',[
   P('Gold RF Microneedling','Step 1: loosens scar tissue and opens the skin.','60–90 min','<b>$999</b>','r-body.jpg'),
   P('Sculptra®','Step 2: helps rebuild collagen in the skin.','Planned with step 1','<b>Consult</b>','r-body2.jpg','50% 35%')]) +
 cat('shoulder','Shoulder &amp; Neckline','A softer line from jaw to shoulder, planned as one.',[
   P('Trap Tox · Shoulder Line','Relaxes the trapezius for a longer neck.','15 min · no downtime','<b>By units</b>','r-lift.jpg','50% 45%'),
   P('Neck &amp; Jawline Sculpt','Firms the neck and defines the jawline.','Planned at consultation','<b>Consult</b>','svc-lift.jpg','40% 30%')]) +
 '</div></section>' + cta('Plan your body <em>goals</em>','Body treatments are planned at a free consultation.'))

# 5 WELLNESS
page('wellness.html','Wellness · AURA Institute','wellness.html','Wellness',
 hero('Wellness','Feel well, <em>look</em> well','Energy, recovery and a calmer mind, right in Midtown.','about.jpg','50% 25%','<a class="btn" href="#energy">Browse Treatments</a><a class="btn line" href="membership.html">Wellness Credits</a>') +
 subnav([('energy','Energy &amp; Recovery'),('mind','Mood &amp; Mind')]) +
 '<section style="padding-top:0"><div class="wrap">' +
 cat('energy','Energy &amp; Recovery','NAD+ IV supports cellular energy and recovery. Relax in our lounge during your drip.',[
   P('NAD+ IV Drip · 250mg','A shorter drip for regular support.','About 60 min · 6 for $1,999','<b>$400</b>','svc-skin.jpg'),
   P('NAD+ IV Drip · 500mg','A fuller dose for a deeper reset.','About 90 min · 6 for $3,750','<b>$750</b>','about.jpg','50% 25%')]) +
 cat('mind','Mood &amp; Mind','A calm, non-invasive seated session.',[
   P('EXOMIND™','Designed to support mood and mental wellbeing.','30 min · 6 for $3,000','<s>$550</s><b>$399</b>','svc-laser.jpg','50% 30%','27% off')]) +
 '</div></section>' + cta('Book your <em>reset</em>','Glow Girl members earn Wellness Credits toward NAD+ every month.'))

# 6 MEMBERSHIP
page('membership.html','Membership · AURA Institute','membership.html','Membership',
 hero('Membership','Glow, <em>every</em> month','Make great skin a habit with a monthly membership, or prepay for credit and year-round perks.','svc-laser.jpg','50% 30%','<a class="btn" href="#glowgirl">Glow Girl Membership</a><a class="btn line" href="#vip">Aura VIP</a>') +
 '''<section id="glowgirl"><div class="wrap split"><div class="head"><p class="eyebrow">Glow Girl Membership</p><h2><em>$299</em> / month</h2><p>A steady, never-overdone rhythm for your skin. From everyday care to seasonal brightening.</p><a class="btn" href="#book" style="justify-self:start">Join Glow Girl</a></div>
<div class="grid3" style="grid-template-columns:1fr">'''+''.join(f'<article class="card"><div class="bd"><h3>{a}</h3><p>{b}</p></div></article>' for a,b in [
 ('1 facial every month','Choose HydraFacial®, Barrier Recovery Facial or Signature Facial.'),('Every 3 months: IPL or Brightening Booster','Unlocks after 3 consecutive months, for dullness, uneven tone and redness.'),('50 Wellness Credits monthly','Credits roll over. 500 credits = 1 NAD+ treatment.')])+'''</div></div>
<div class="wrap"><p class="note">3-month minimum. Monthly facial must be used that month. Quarterly perk unlocks after 3 consecutive months and has no cash value. Cancel with 30 days’ notice.</p></div></section>
<section class="alt" id="vip"><div class="wrap"><div class="head"><p class="eyebrow">Aura VIP</p><h2>Prepay, get <em>more</em></h2><p>Load your account once and enjoy bonus credit and perks all year.</p></div>
<div class="tbl"><table><thead><tr><th>Perk</th><th>Aura Gold · $5,000</th><th>Aura Black · $10,000</th></tr></thead><tbody>'''+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in [
 ('Bonus credit','<b>+$800</b>','<b>+$1,500</b>'),('Complimentary facials','1 per quarter','2 per quarter'),('Gold Skin Analysis','Unlimited','Unlimited'),('Anti-aging plan consultation','—','Every quarter'),('Birthday credit','$100','$300'),('Share credit with friends','1 friend','2 friends'),('Events','Priority access','First invitations, launches &amp; private events')])+'''</tbody></table></div></div></section>
<section><div class="wrap split"><div class="head"><p class="eyebrow">FAQ</p><h2>Membership <em>questions</em></h2></div><div>'''+faq([
 ('Can I pause my Glow Girl membership?','Ask the front desk about your options. Cancellation needs 30 days’ notice after the 3-month minimum.'),
 ('Do VIP credits expire?','Expiry terms will be confirmed by the team before launch.'),
 ('Can I combine membership with first-visit offers?','Ask at your consultation and we’ll apply the best option for you.')])+'</div></div></section>' +
 cta('Join the <em>AURA</em> family','Sign up at the front desk or at your next visit.','Book a Visit'))

# 7 ABOUT
page('about.html','About · AURA Institute','about.html','About',
 hero('About AURA','Not someone else. <em>A better you.</em>','Medical aesthetics and wellness at Rockefeller Center, built on science, design and care.','about-reception.jpg','50% 50%') +
 '''<section><div class="wrap split"><div class="head"><p class="eyebrow">Our Story</p><h2>The science of <em>glowing</em> skin</h2></div><div style="display:grid;gap:14px"><p style="margin:0">AURA Institute brings medical aesthetics and wellness together in the heart of Midtown. We pair FDA-cleared technology with provider-led care, so every plan is built around your skin, your tone and your goals.</p><p style="margin:0;color:var(--muted)">Our promise is simple: natural-looking results, honest advice and an experience that feels personal, precise and calm.</p><p class="note">Founder story and history to be added by the team.</p></div></div></section>
<section class="alt"><div class="wrap"><div class="head"><p class="eyebrow">Our Approach</p><h2>Four steps to <em>your</em> plan</h2><p>We do what your skin truly needs, in the right order, with the right material for each area.</p></div><div class="steps">'''+''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in [('Understand','We listen to your goals, lifestyle and history.'),('Analyze','A Gold Skin Analysis and face assessment find the cause.'),('Explain','We walk you through the why, in plain words.'),('Plan','A step-by-step plan that fits your schedule and budget.')])+'''</div></div></section>
<section><div class="wrap"><div class="head"><p class="eyebrow">Our Providers</p><h2>Medical hands, <em>natural</em> results</h2><p>Every treatment is performed or supervised by a licensed medical provider in New York State.</p></div><div class="grid3">'''+''.join(f'<article class="card"><div class="ph-empty">Portrait</div><div class="bd"><h3>{a}</h3><p>{b}</p></div></article>' for a,b in [('[Name], MD','Medical Director'),('[Name], NP','Lead Injector'),('[Name], RN','Laser &amp; Skin Specialist')])+'''</div></div></section>
<section class="alt"><div class="wrap split"><div class="head"><p class="eyebrow">The Clinic</p><h2>A calm space in <em>Midtown</em></h2><p>Steps from Fifth Avenue at Rockefeller Center. Private treatment suites, a relaxing lounge and lunch-hour appointments.</p></div><div style="position:relative;aspect-ratio:4/3;overflow:hidden"><img src="about-reception.jpg" alt="AURA Institute reception" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"></div></div></section>
<section><div class="wrap"><div class="head"><p class="eyebrow">Reviews</p><h2>What clients <em>say</em></h2></div><div class="grid3">'''+''.join('<article class="card"><div class="bd"><h3>★★★★★</h3><p>Real client review to be added from Google once the clinic opens.</p></div></article>' for _ in range(3))+'</div></div></section>' +
 cta('Come say <em>hello</em>','Book a complimentary consultation and see the space for yourself.'))

# 8 JOURNAL & FAQ
page('journal-faq.html','Journal & FAQ · AURA Institute','journal-faq.html','Journal &amp; FAQ',
 hero('Journal &amp; FAQ','Learn your <em>skin</em>','Honest, simple answers about treatments, skin care and what to expect.','r-care2.jpg','50% 55%','<a class="btn" href="#articles">Read the Journal</a><a class="btn line" href="#faq">FAQ</a>') +
 '''<section id="articles"><div class="wrap"><div class="head"><p class="eyebrow">Skin Education · Treatment Guides</p><h2>From the <em>Journal</em></h2></div><div class="grid3">'''+''.join(f'<article class="card"><div class="ph"><img src="{i}" alt="" style="object-position:50% 35%"></div><div class="bd"><p class="eyebrow">{c}</p><h3>{t}</h3><p>{d}</p></div><div class="ft"><a class="more" href="#">Read</a></div></article>' for i,c,t,d in [
 ('about.jpg','Treatment Guide','Skin booster or filler: what’s the difference?','Hydration versus volume, explained in two minutes.'),
 ('r-lift.jpg','Skin Education','Why skin loosens, and what actually helps','Aging starts below the surface. Here is what that means for treatment.'),
 ('r-care2.jpg','Seasonal Care','Your winter skin reset','Repair first, then brighten: a simple plan for the colder months.')])+'''</div></div></section>
<section class="alt"><div class="wrap"><div class="head"><p class="eyebrow">Myths &amp; Facts</p><h2>Let’s clear that <em>up</em></h2></div><div class="grid3">'''+''.join(f'<article class="card"><div class="bd"><span class="badge">Myth</span><h3>{m}</h3><p><b>Fact:</b> {f}</p></div></article>' for m,f in [
 ('Expensive creams fix wrinkles.','Most skincare works on the surface. Deeper changes need treatments that reach the layers below.'),
 ('Your skin needs to breathe.','Skin doesn’t breathe air. It needs a healthy barrier, hydration and daily SPF.'),
 ('Filler makes everyone look puffy.','The right product, in the right layer and amount, looks natural. Planning matters most.')])+'''</div></div></section>
<section id="faq"><div class="wrap split"><div class="head"><p class="eyebrow">FAQ</p><h2>Common <em>questions</em></h2></div><div>'''+faq([
 ('Is my first consultation really free?','Yes. Every new client gets a complimentary Gold Skin Analysis and consultation.'),
 ('Who performs the treatments?','Licensed medical providers in New York State perform or supervise every treatment.'),
 ('Can I come in on my lunch break?','Many treatments take 20–60 minutes with little or no downtime. Lunch-hour appointments are available.'),
 ('What products do you use?','Only FDA-approved or FDA-cleared products and devices. We tell you exactly what was used and how much.'),
 ('What is your cancellation policy?','Policy details to be confirmed by the team before launch.')])+'''</div></div></section>
<section class="alt" id="visit"><div class="wrap split"><div class="head"><p class="eyebrow">Contact &amp; Visit</p><h2>Find <em>us</em></h2></div><div class="mini"><div><span>Address</span><span>[Street], Rockefeller Center, New York, NY 10020</span></div><div><span>Phone</span><span>(212) [XXX-XXXX]</span></div><div><span>Email</span><span>hello@[aurainstitute].com</span></div><div><span>Hours</span><span>Mon–Fri 9am–8pm · Sat 10am–6pm (example)</span></div></div></div></section>''' +
 cta('Still have a <em>question</em>?','Text us or book a free consultation. We’re happy to help.'))

# wrap existing samples
for src, dst, title in [('/mnt/user-data/outputs/lift-tighten.html','lift-tighten.html','Lift & Tighten · AURA Institute'),('/mnt/user-data/outputs/emface.html','emface.html','EMFACE · AURA Institute')]:
    s = open(src).read()
    s = re.sub(r'^<title>.*?</title>\s*<meta name="claude:viewport-fit-sides" content="cover">', '', s, flags=re.S)
    s = s.replace('<a class="logo" href="#">', '<a class="logo" href="index.html">')
    for h,n in NAV:
        s = s.replace(f'<li><a href="#">{n}</a></li>', f'<li><a href="{h}">{n}</a></li>').replace(f'<li><a class="on" href="#">{n}</a></li>', f'<li><a class="on" href="{h}">{n}</a></li>')
    s = s.replace('<a href="#">Home</a>', '<a href="index.html">Home</a>').replace('<a href="#">Face &amp; Contour</a> /', '<a href="face-contour.html">Face &amp; Contour</a> /').replace('<a href="#">Lift &amp; Tighten</a>', '<a href="lift-tighten.html">Lift &amp; Tighten</a>')
    s = s.replace('<h3>EMFACE®</h3><p class="one">Lifts', '<h3>EMFACE®</h3><p class="one">Lifts')
    s = s.replace('<a class="more" href="#">Learn More</a></div></article>\n      <article class="card"><div class="ph"><img src="r-lift.jpg"', '<a class="more" href="emface.html">Learn More</a></div></article>\n      <article class="card"><div class="ph"><img src="r-lift.jpg"', 1)
    head = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{title}</title>'
    open(f'{OUT}/{dst}', 'w').write(head + s + '</html>')
print('ok')
