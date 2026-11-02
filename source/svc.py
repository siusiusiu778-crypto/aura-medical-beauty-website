import sys, io, contextlib
sys.path.insert(0, '/home/claude/pages')
with contextlib.redirect_stdout(io.StringIO()):
    import gen
from svc_css import CSS
OUT = gen.OUT
open(OUT + '/svc.css', 'w').write(CSS)
HEAD = gen.HEAD.replace('<link rel="stylesheet" href="site.css">', '<link rel="stylesheet" href="site.css"><link rel="stylesheet" href="svc.css">')

def page(fn, title, active, crumbs, body):
    html = HEAD.format(title=title) + gen.nav(active) + f'<main><div class="wrap crumbs"><a href="index.html">Home</a> / {crumbs}</div>' + body + '</main><footer>AURA Institute · 630 Fifth Avenue, Suite 1812, New York, NY 10111 · Results vary by individual.</footer></body></html>'
    open(f'{OUT}/{fn}', 'w').write(html)

def sec(sid, eyebrow, h2, p, inner, alt=False):
    pp = f'<p>{p}</p>' if p else ''
    return f'<section id="{sid}"{" class=\"alt\"" if alt else ""}><div class="wrap"><div class="head"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2>{pp}</div>{inner}</div></section>'

def cart_html(d):
    c = EX.get(d['h1plain'], {}).get('cart')
    if not c: return ''
    return f'<div class="cart"><span class="qty"><button aria-label="Fewer">−</button><b>1</b><button aria-label="More">+</button></span><span class="sub">{c[0]}</span><a class="btn line" href="#">Add to Treatment Cart</a></div>'

def pd(d):
    th = ''.join(f'<div><img src="{i}" alt="" style="object-position:{p}"></div>' for i, p in d['thumbs'])
    chips = ''.join(f'<span>{c}</span>' for c in d['chips'])
    opts = ''
    for h, items in d['opts']:
        opts += f'<div class="opt"><h4>{h}</h4><div class="pills">' + ''.join(f'<span class="{"on" if k == 0 else ""}">{x}</span>' for k, x in enumerate(items)) + '</div></div>'
    facts = ''.join(f'<div><span>{a}</span>{b}</div>' for a, b in d['facts'])
    return f'''<div class="wrap"><div class="pd"><div class="gal"><div class="main"><img src="{d['img']}" alt="" style="object-position:{d['pos']}"></div><div class="th">{th}</div></div>
<div class="info"><p class="eyebrow">{d['group']}</p><h1>{d['h1']}</h1><p class="lede">{d['lede']}</p><div class="chips">{chips}</div>{opts}
<div class="pr">{d['price']}</div>{cart_html(d)}<div class="acts2"><a class="btn" href="#book">{d.get('cta','Book Now')}</a><a class="btn line" href="#book">Ask an Expert</a><a class="btn line wl" href="#" aria-label="Add to wish list">♡</a></div>
<p class="rate"><b>★★★★★</b> [4.9] · [XXX] Google reviews</p>
<div class="facts">{facts}</div><p class="loc">AURA Institute · Rockefeller Center, New York · (212) [XXX-XXXX] · Text us anytime</p></div></div></div>'''

WHY = '''<div class="why"><div class="wrap"><div><h3>Designed by a provider</h3><p>Every plan starts with an assessment of your whole face, not a menu of units.</p></div>
<div><h3>Authentic, FDA-approved products</h3><p>Sourced directly and verified. We name every product we use.</p></div><div><h3>Lunch-break friendly</h3><p>Steps from Rockefeller Center, with private treatment rooms.</p></div></div></div>'''

def tabs(items):
    return '<div class="tabs"><div class="wrap">' + ''.join(f'<a href="#{i}"{" class=\"on\"" if k == 0 else ""}>{t}</a>' for k, (i, t) in enumerate(items)) + '</div></div>'

def areas(a): return '<div class="areas">' + ''.join(f'<div class="area"><h4>{h}</h4><p>{p}</p><b>{b}</b></div>' for h, p, b in a) + '</div>'
def reco(r): return '<ol class="reco">' + ''.join(f'<li><span>{x}</span></li>' for x in r) + '</ol>'
def steps(s): return '<div class="steps">' + ''.join(f'<div class="step"><h4>{h}</h4><p>{p}</p></div>' for k, (h, p) in enumerate(s)) + '</div>'
def tl(t): return '<div class="tl">' + ''.join(f'<div><b>{h}</b><p>{p}</p></div>' for h, p in t) + '</div>'
def table(head, rows, hi=None):
    return '<div style="overflow-x:auto"><table class="tbl2"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td{" class=\"hi\"" if hi is not None and j == hi else ""}>{c}</td>' for j, c in enumerate(r)) + '</tr>' for r in rows) + '</tbody></table></div>'
def ba(caps): return '<div class="ba">' + ''.join(f'<div><span>Before</span><span>After</span><small>{c}</small></div>' for c in caps) + '</div><p class="note2">Real AURA clients, shared with written consent. Individual results vary.</p>'
def pairs(ps): return '<div class="prods">' + ''.join(gen.prod(*p) for p in ps) + '</div>'
def qa(items): return '<div class="qa">' + gen.faq(items) + '</div>'

def std(items): return '<div class="stds">' + ''.join(f'<div><b>✓</b><h4>{h}</h4><p>{p}</p></div>' for h, p in items) + '</div>'
def care(do, wait): return f'<div class="two care"><div><h3>Aftercare</h3><ul>' + ''.join(f'<li>{x}</li>' for x in do) + '</ul></div><div><h3>Please wait if you…</h3><ul class="no">' + ''.join(f'<li>{x}</li>' for x in wait) + '</ul></div></div>'
def tech(items): return '<div class="tech">' + ''.join(f'<div><i>0{k+1}</i><h4>{h}</h4><p>{p}</p></div>' for k, (h, p) in enumerate(items)) + '</div>'

def blk(eyebrow, h, p, inner):
    pp = f'<p class="bp">{p}</p>' if p else ''
    return f'<div class="blk"><p class="eyebrow">{eyebrow}</p><h3 class="bh">{h}</h3>{pp}{inner}</div>'

def bookform(name):
    return f'''<div class="bookp"><div><h3 class="bh">Contact <em>us</em></h3><p class="bp">Questions before you book? Our team is here to help, by phone, text or in person.</p>
<ul class="ct"><li><b>Visit</b>AURA Institute · [Address], Rockefeller Center, New York, NY</li><li><b>Call</b>(212) [XXX-XXXX]</li><li><b>Text</b>Text us anytime at (212) [XXX-XXXX]</li><li><b>Hours</b>Mon–Fri [10–8] · Sat [10–6] · Sun [closed]</li></ul></div>
<form class="bf" onsubmit="event.preventDefault()"><h3 class="bh">Book an <em>appointment</em></h3><p class="bp">Choose a time and we’ll confirm within one business hour.</p>
<label>Treatment<select><option>{name}</option><option>Free consultation</option></select></label>
<div class="r2"><label>First name<input placeholder="Jane"></label><label>Last name<input placeholder="Doe"></label></div>
<div class="r2"><label>Phone<input placeholder="(212) 555-0100"></label><label>Email<input placeholder="jane@email.com"></label></div>
<div class="r2"><label>Preferred date<input placeholder="MM / DD"></label><label>Preferred time<select><option>Morning</option><option>Lunch break</option><option>Afternoon</option><option>Evening</option></select></label></div>
<label class="ck"><input type="checkbox" checked> I’m a new client</label><button class="btn" type="submit">Request Appointment</button></form></div>'''

TABJS = '''<script>(function(){const b=[...document.querySelectorAll('.ptabs button')],p=[...document.querySelectorAll('.panel')];
function show(id){b.forEach(x=>x.classList.toggle('on',x.dataset.t===id));p.forEach(x=>x.hidden=x.id!=='p-'+id);}
b.forEach(x=>x.addEventListener('click',()=>show(x.dataset.t)));document.querySelectorAll('a[href="#book"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();show('book');document.querySelector('.ptabs').scrollIntoView({behavior:'smooth'});}));
function fromHash(){const h=location.hash.replace('#tab-','');if(b.some(x=>x.dataset.t===h))show(h);}fromHash();addEventListener('hashchange',fromHash);})();</script>'''

def noprice_tbl(head, rows, hi=None):
    rows = [r for r in rows if not any('$' in c for c in r)]
    return table(head, rows)

def pcard(p):
    # related card without price: name, desc, meta, price, img, pos, sale, link
    name, desc, meta, _pr, img = p[:5]; pos = p[5] if len(p) > 5 else '50% 40%'; link = p[7] if len(p) > 7 else '#'
    return f'<a class="rel" href="{link}"><div class="ph"><img src="{img}" alt="" style="object-position:{pos}"></div><h4>{name}</h4><p>{desc}</p><span>Learn More →</span></a>'

def baslider(img, pos, caps):
    return f'''<div class="bas"><div class="sl"><img src="{img}" alt="" style="object-position:{pos}"><img class="af" src="{img}" alt="" style="object-position:{pos}"><span class="lb l">Before</span><span class="lb r">After</span><i class="hd"></i></div>
<div class="tx"><p class="eyebrow">Before and After</p><h2 class="bh2">Our clients’ <em>experiences</em></h2><p>At AURA, we design for natural results that still look like you. Every photo is shared with the client’s written consent, taken in the same light and angle.</p><ul>{''.join(f'<li>{c}</li>' for c in caps)}</ul><p class="note2">Individual results vary. Your provider will show you cases similar to your goals at consultation.</p><a class="btn" href="#book">Book a Consultation</a></div></div>'''

def service(fn, active, crumbs, d, overview, design, extra, expect, pricing, baps, pair, faqs, cta):
    X = EX.get(d['h1plain'], {})
    extra = extra or X.get('cmp')
    name = d['h1plain'].replace('&', '&amp;')
    th = d['thumbs']
    member = 'Membership' in d['h1plain']
    # ---- 1 hero (Genesys: square image left; title, intro, Ask an Expert, location, why) ----
    chips = ''.join(f'<span>{c}</span>' for c in d['chips'] if ('$' not in c or member))
    facts = ''.join(f'<div><span>{x}</span>{y}</div>' for x, y in d['facts'] if '$' not in y)
    body = f'''<div class="wrap"><div class="ph3"><div class="im"><img src="{d['img']}" alt="" style="object-position:{d['pos']}"></div>
<div class="tx"><p class="eyebrow">{d['group']}</p><h1>{d['h1']}</h1><p class="lede">{d['lede']}</p><div class="chips">{chips}</div><div class="facts">{facts}</div>
<ul class="ic"><li><b>?</b><div><strong>Ask an Expert</strong>Text us anytime at (212) [XXX-XXXX]. A provider replies within one business hour.</div></li>
<li><b>⌖</b><div><strong>AURA Institute · Rockefeller Center</strong>[Address], New York, NY · Tel (212) [XXX-XXXX]</div></li>
<li><b>♢</b><div><strong>Why choose AURA?</strong>Licensed providers, authentic FDA-approved products, and a plan designed around your whole face, not a menu of units.</div></li></ul>
<div class="acts2"><a class="btn" href="#book">{'Join Now' if member else 'Book a Consultation'}</a><a class="btn line wl" href="#" aria-label="Add to wish list">♡</a></div></div></div></div>'''
    # ---- 2 tabs: Description / Book an Appointment / Why AURA ----
    desc = f'<div class="blk"><p class="eyebrow">{d["group"]}</p><h3 class="bh">{overview[0]}</h3><p class="bp">{overview[1]}</p>{areas([(h, p, bb) for h, p, bb in overview[2] if "$" not in bb])}</div>'
    if X.get('tech'): desc += f'<div class="blk"><h3 class="bh">{X["tech"][1]}</h3>{tech(X["tech"][2])}</div>'
    if extra:
        inner = extra[4]
        if not member:
            import re
            inner = re.sub(r'<tr>(?:(?!</tr>).)*\$(?:(?!</tr>).)*</tr>', '', inner)
        desc += f'<div class="blk cmpb"><div class="ci"><img src="{th[1][0]}" alt="" style="object-position:{th[1][1]}"></div><div><h3 class="bh">{extra[2]}</h3><p class="bp">{extra[3]}</p>{inner}</div></div>'
    why = '<div class="blk"><h3 class="bh">Your trusted <em>partner</em></h3><ul class="why5">' + ''.join(f'<li><b>{h}</b>{p}</li>' for h, p in [('Expert care', 'Every treatment is planned and performed by a licensed RN, NP or MD.'), ('Personalized plans', 'Units, products and combinations are designed for your face at consultation, with a clear quote before you start.'), ('Comfort and privacy', 'Private treatment rooms steps from Rockefeller Center.'), ('Real reviews', '[4.9] ★ from [XXX] Google reviews.')] + X.get('std', [])) + '</ul></div>'
    T = [('desc', 'Description', desc), ('book', 'Book an Appointment', bookform(name)), ('why', 'Why AURA', why)]
    body += '<section class="tabsec" id="details"><div class="wrap"><div class="ptabs" role="tablist">' + ''.join(f'<button data-t="{i}" class="{"on" if k == 0 else ""}">{t}</button>' for k, (i, t, _) in enumerate(T)) + '</div>'
    body += ''.join(f'<div class="panel" id="p-{i}"{" hidden" if k else ""}>{c}</div>' for k, (i, _, c) in enumerate(T)) + '</div></section>'
    # ---- 3 full-width banner: text left, image right (How we design it) ----
    body += f'''<section class="ban alt" id="design"><div class="tx"><p class="eyebrow">How we design it</p><h2 class="bh2">{design[0]}</h2><p>{design[1]}</p><ol class="num">{''.join(f'<li><b>{h}</b> {p}</li>' for h, p in design[2])}</ol></div><div class="im"><img src="{th[2][0]}" alt="" style="object-position:{th[2][1]}"></div></section>'''
    # ---- 4 image left, Recommended for right ----
    body += f'''<section class="ban rev" id="reco"><div class="im"><img src="{th[3][0]}" alt="" style="object-position:{th[3][1]}"></div><div class="tx"><p class="eyebrow">Recommended for</p><h2 class="bh2">Is this <em>right</em> for you?</h2><ul class="chk">{''.join(f'<li>{x}</li>' for x in overview[3])}</ul></div></section>'''
    # ---- 5 what to expect + aftercare (compact) ----
    do, wait = X['care']
    body += f'''<section class="alt" id="expect"><div class="wrap"><div class="head"><p class="eyebrow">What to expect</p><h2>{expect[0]}</h2></div>{tl(expect[2])}{care(do, wait)}</div></section>'''
    # ---- 6 FAQ ----
    fq = [f for f in faqs if '$' not in f[1]]
    if not member: fq.append(('How much does it cost?', 'Every plan is different. The number of units, sessions and the right combination are decided with your provider at a complimentary consultation, and you’ll receive a clear quote before any treatment.'))
    body += f'<section id="faq"><div class="wrap faqc"><p class="eyebrow" style="text-align:center">FAQs</p><h2 class="bh2" style="text-align:center">Good <em>questions</em></h2>{qa(fq)}</div></section>'
    # ---- 7 Before & After ----
    body += f'<section class="alt" id="results"><div class="wrap">{baslider(d["img"], d["pos"], baps)}</div></section>'
    # ---- 8 related ----
    body += '<section id="pairs"><div class="wrap"><div class="head"><p class="eyebrow">Related services</p><h2>Pairs well <em>with</em></h2></div><div class="rels">' + ''.join(pcard(p) for p in pair) + '</div></div></section>'
    body += gen.cta(*cta) + TABJS
    page(fn, d['h1plain'] + ' · AURA Institute', active, crumbs, body)

EX = {
 'Gold Skin Analysis': dict(
  tech=('The technology', 'How the <em>imaging</em> works', [('Multi-light imaging', 'Daylight, polarized and UV light show the surface and the layers below.'), ('Side-by-side tracking', 'Every visit is saved, so you can see change over a series.'), ('Provider review', 'A licensed provider reads the results with you, not a machine score.')]),
  cmp=('compare', 'Analysis vs mirror check', 'Why not just <em>look</em>?', 'Much of what changes your skin sits below what the eye can see.', table(['', 'Mirror check', 'Gold Skin Analysis'], [['Sees', 'Surface only', 'Surface and deeper layers'], ['Pigment', 'Visible spots', 'Visible and hidden pigment'], ['Tracks progress', 'From memory', 'Saved images, visit to visit'], ['Result', 'A guess', 'A written plan']])),
  care=(['No special care needed. Back to your day right away.', 'Your report arrives by email the same day.', 'Bring it to your next visit so we can track progress.'], ['Have an active rash or open wound on the face (we’ll reschedule).', 'Just had a peel or laser in the last 7 days (results may read differently).']),
  std=[('Medical-grade imaging', 'A clinical skin analysis system, not a phone app. [Device name to confirm.]'), ('Read by a provider', 'Results are explained by an RN, NP or MD.'), ('Your data stays private', 'Images are stored securely and never shared without consent.')]),
 'Botox & Xeomin': dict(
  care=(['Stay upright for 4 hours.', 'Skip workouts, saunas and facial massage for 24 hours.', 'Don’t rub or press the treated areas today.', 'Come back at day 14 for your check.'], ['Are pregnant or breastfeeding.', 'Have a neuromuscular condition such as myasthenia gravis.', 'Have an infection or inflammation at the treatment site.', 'Have had a reaction to a botulinum toxin before.']),
  std=[('Sourced directly from the manufacturer', 'Botox® from Allergan Aesthetics and Xeomin® from Merz, never from third parties.'), ('Lot number on request', 'Ask to see the vial and lot number before treatment.'), ('Licensed injectors only', 'Every treatment is performed by an RN, NP or MD.')]),
 'Glow Booster': dict(cart=('First visit · $299',),
  care=(['Small bumps settle within 1–2 days.', 'No makeup until the next morning.', 'Skip saunas, hot yoga and alcohol for 24 hours.', 'Use gentle skincare and SPF for 3 days.'], ['Are pregnant or breastfeeding.', 'Have active acne, cold sores or infection on the face.', 'Have had filler or laser in the same area in the last 2 weeks.']),
  std=[('Sealed, single-use products', 'Every booster is opened in front of you.'), ('FDA-cleared delivery', 'Hyaluronic acid products used within their approved indications. [Products to confirm.]'), ('Provider-led', 'Placed by a licensed injector, not a technician.')]),
 'Body Sculpt': dict(cart=('4 sessions · $999',),
  tech=('The technology', 'Why this <em>device</em>', [('[Feature 1]', '[Device technology, e.g. how it targets fat cells.]'), ('[Feature 2]', '[Comfort, treatment time or coverage.]'), ('[Feature 3]', '[FDA clearance and indications.]')]),
  cmp=('compare', 'Body Sculpt vs surgery', 'Non-invasive vs <em>liposuction</em>', 'Body Sculpt is not a substitute for surgery. Here is how they differ.', table(['', 'Body Sculpt', 'Liposuction'], [['Anesthesia', 'None', 'Local or general'], ['Downtime', 'None', '1–2 weeks'], ['Results', 'Gradual, over 8–12 weeks', 'Faster, more dramatic'], ['Best for', 'Small, stubborn areas', 'Larger volume']])),
  care=(['Return to normal activity right away.', 'Drink plenty of water for the next few days.', 'Keep a steady routine of movement and diet.', 'Progress photos at weeks 4, 8 and 12.'], ['Are pregnant or breastfeeding.', 'Have a pacemaker or metal implant in the area.', 'Have a hernia or recent surgery in the area.']),
  std=[('FDA-cleared device', '[Device name and clearance to confirm.]'), ('Genuine parts', 'Original applicators and software, serviced on schedule.'), ('Measured results', 'Photos and measurements at every stage.')]),
 'NAD+ IV Drip': dict(cart=('6 drips · 250 mg · $1,999',),
  cmp=('compare', 'IV vs supplements', 'IV drip vs <em>oral supplements</em>', 'Both are options. The difference is how they are delivered.', table(['', 'NAD+ IV Drip', 'Oral supplement'], [['Delivery', 'Directly into the bloodstream', 'Through digestion'], ['Supervision', 'Licensed nurse', 'None'], ['Time', '60–90 minutes in clinic', 'Daily at home'], ['Screening', 'Health history reviewed first', 'None']])),
  care=(['Drink water for the rest of the day.', 'Keep the bandage on for 1 hour.', 'Back to work or the gym right away.'], ['Are pregnant or breastfeeding.', 'Have kidney or heart conditions (we’ll check with your provider).', 'Are currently undergoing cancer treatment.']),
  std=[('Licensed pharmacy source', 'NAD+ from a licensed U.S. pharmacy. [Pharmacy to confirm.]'), ('Medical screening', 'A provider reviews your health history before your first drip.'), ('Sterile, single-use supplies', 'Every IV line is opened in front of you.')]),
 'Glow Girl Membership': dict(cart=('$299 / month · 3-month minimum',),
  care=(['Book your facial early each month.', 'Your quarterly treatment unlocks after 3 consecutive months.', 'Check your Wellness Credits in your account.'], ['Want a one-time treatment only (try a first-visit offer instead).', 'Can’t commit to 3 months yet.']),
  std=[('Same standards, every visit', 'Members receive the same authentic products and licensed providers.'), ('Transparent billing', 'Billed monthly. No hidden fees.'), ('Easy to cancel', '30 days’ notice after the 3-month minimum.')]),
}

# ---------------- 1 GOLD SKIN ANALYSIS (Special Offers) ----------------
service('gold-skin-analysis.html', 'special-offers.html', '<a href="special-offers.html">Special Offers</a> / Gold Skin Analysis',
 dict(group='Special Offers · New Client', h1='Gold Skin <em>Analysis</em>', h1plain='Gold Skin Analysis',
  lede='See what your skin needs before you spend on any treatment. A provider maps your skin layer by layer, then builds a plan around your goals and budget.',
  chips=['Complimentary for new clients', '20 minutes', 'No commitment'], img='about-reception.jpg', pos='50% 50%',
  thumbs=[('about-reception.jpg', '50% 50%'), ('r-care2.jpg', '50% 55%'), ('r-tone.jpg', '50% 35%'), ('about.jpg', '50% 25%')],
  opts=[('Choose your visit', ['Skin Analysis only', 'Analysis + Face Design Consultation'])],
  price='<b>Free</b><span class="tag">New clients</span><small>Unlimited for Aura VIP Gold &amp; Black members.</small>', cta='Book My Analysis',
  facts=[('Time', '20 minutes'), ('Downtime', 'None'), ('You leave with', 'A written skin report'), ('Next step', 'A personal treatment plan')]),
 ('Know your skin <em>first</em>', 'Most people choose treatments by what a friend tried. We start with data from your own skin.',
  [('Hydration', 'Water level in the top layer of skin.', 'Measured'), ('Oil &amp; pores', 'Oil balance and visible pore size.', 'Measured'), ('Spots &amp; tone', 'Surface and deeper pigment, uneven tone.', 'UV imaging'), ('Redness', 'Sensitivity and visible vessels.', 'Imaged'), ('Lines &amp; texture', 'Fine lines, roughness and scarring.', 'Imaged'), ('Firmness', 'Early signs of laxity along the jaw and neck.', 'Provider check')],
  ['First time trying medical aesthetics', 'Not sure which treatment fits your skin', 'Sensitive, reactive or acne-prone skin', 'Planning a series and want a baseline to track progress', 'Members checking results each season']),
 ('Four steps, <em>one plan</em>', 'Your provider reviews every image with you. No pressure to book on the day.',
  [('Cleanse', 'A gentle cleanse so the readings reflect your bare skin.'), ('Image', 'Multi-light imaging captures the surface and the layers below.'), ('Review', 'Your provider walks you through each result on screen.'), ('Plan', 'A step-by-step plan, ordered by priority and budget.')]),
 None,
 ('Your <em>visit</em>', '', [('Before', 'Come without makeup if you can. We provide cleanser.'), ('During', '20 minutes, seated, completely painless.'), ('After', 'Your skin report is emailed to you the same day.'), ('Follow-up', 'Repeat every season to track progress.')]),
 ('Clear <em>pricing</em>', '', ['Visit', 'Who', 'Price'], [['Gold Skin Analysis', 'New clients', 'Free'], ['Gold Skin Analysis', 'Returning clients', '$50, credited toward any treatment that day'], ['Gold Skin Analysis', 'Aura VIP members', 'Unlimited']], 2),
 ['Hydration and tone, before and after a Glow Booster series', 'Redness map, before and after a barrier repair plan', 'Pores and texture, before and after Gold RF Microneedling'],
 [('Glow Booster', 'Hydration plus brightening, delivered into the skin.', '30 min', '<s>$450</s><b>$299</b>', 'about.jpg', '50% 25%', '34% off'),
  ('HydraFacial® Deluxe', 'Cleanse, extract and hydrate.', '60 min', '<b>$285</b>', 'r-care2.jpg', '50% 55%'),
  ('Face Design Consultation', 'A full-face assessment with a provider.', '30 min', '<b>Free</b>', 'r-texture.jpg')],
 [('Is it really free?', 'Yes, for new clients. There is no obligation to book a treatment.'), ('Who performs it?', 'A licensed provider (RN, NP or MD) reviews your results with you.'), ('Do I need to remove makeup?', 'Bare skin gives the most accurate reading. We provide a gentle cleanser on arrival.'), ('How often should I repeat it?', 'Every 3 months is ideal to track a treatment series or seasonal changes.')],
 ('Start with your <em>skin</em>', 'Book a complimentary Gold Skin Analysis. It takes 20 minutes.', 'Book My Analysis'))

# ---------------- 2 BOTOX & XEOMIN (Face & Contour) ----------------
service('botox-xeomin.html', 'face-contour.html', '<a href="face-contour.html">Face &amp; Contour</a> / Smooth Lines / Botox® &amp; Xeomin®',
 dict(group='Face &amp; Contour · Smooth Lines', h1='Botox® &amp; <em>Xeomin®</em>', h1plain='Botox & Xeomin',
  lede='Soften forehead lines, frown lines and crow’s feet while keeping your expressions. Your provider maps your muscles and chooses the right product and dose for you.',
  chips=['FDA-approved', '10–20 minutes', 'No downtime'], img='r-texture.jpg', pos='50% 40%',
  thumbs=[('r-texture.jpg', '50% 40%'), ('s-inject.jpg', '45% 40%'), ('about.jpg', '50% 25%'), ('r-lift.jpg', '50% 45%')],
  opts=[('Product', ['Botox® Cosmetic · $12 / unit', 'Xeomin® · $10 / unit']), ('Area', ['Forehead', 'Frown lines (11s)', 'Crow’s feet', 'Jaw slimming'])],
  price='From <b>$10</b><span style="color:var(--muted)">/ unit</span><small>Typical upper-face treatment: 30–60 units. Exact units confirmed at your consultation.</small>',
  facts=[('Treatment time', '10–20 minutes'), ('Downtime', 'None'), ('Results begin', '3–5 days'), ('Lasts', 'About 3–4 months')]),
 ('Smooth, not <em>frozen</em>', 'Wrinkle relaxers soften the muscles that crease your skin when you frown, squint or raise your brows. Placed well, you still look like you, just more rested.',
  [('Forehead lines', 'Horizontal lines when you raise your brows.', 'Typically 10–20 units'), ('Frown lines (11s)', 'Vertical lines between the brows.', 'Typically 20 units'), ('Crow’s feet', 'Fan lines at the outer eyes when you smile.', 'Typically 12 units per side'), ('Jaw slimming', 'Softens a square jaw from a strong masseter.', 'Planned at consultation')],
  ['First lines that stay after your face relaxes', 'Looking tired or stern when you’re not', 'Preventing deeper lines from setting in', 'A square jaw from clenching', 'Anyone who wants subtle, natural movement']),
 ('Mapped to <em>your</em> face', 'The product matters less than where and how much. This is where design comes in.',
  [('Assess', 'We watch your face at rest and in motion to see which muscles create each line.'), ('Map', 'Injection points are marked to your anatomy, balancing brows and eyes.'), ('Dose', 'Your provider chooses Botox® or Xeomin® and the units for each point.'), ('Refine', 'A 2-week check to fine-tune, included with your first treatment.')]),
 ('compare', 'Botox® vs Xeomin®', 'Which one is <em>right</em> for me?', 'Both are FDA-approved and work the same way. The differences are small, and your provider will recommend one.',
  table(['', 'Botox® Cosmetic', 'Xeomin®'], [['Results begin', '3–5 days', '3–5 days'], ['Lasts', 'About 3–4 months', 'About 3–4 months'], ['Formula', 'Active ingredient with accessory proteins', 'Purified, no accessory proteins'], ['Good fit for', 'The most studied option; first-timers', 'Clients who prefer a “naked” formula'], ['Price', '$12 / unit', '$10 / unit']])),
 ('Your <em>timeline</em>', '', [('Day 0', 'Tiny bumps at each point fade within 20–30 minutes. Back to work right away.'), ('Days 3–5', 'Lines start to soften.'), ('Day 14', 'Full result. Come in for your check and touch-up.'), ('Months 3–4', 'Movement slowly returns. Time to rebook.')]),
 ('Clear <em>pricing</em>', 'Priced per unit, so you only pay for what your face needs.', ['Area', 'Typical units', 'Botox® ($12)', 'Xeomin® ($10)'], [['Frown lines (11s)', '20', '$240', '$200'], ['Forehead', '10–20', '$120–$240', '$100–$200'], ['Crow’s feet', '24 (both sides)', '$288', '$240'], ['Upper face (3 areas)', '50–60', '$600–$720', '$500–$600']], None),
 ['Frown lines, 2 weeks after treatment', 'Forehead lines, 2 weeks after treatment', 'Crow’s feet, 2 weeks after treatment'],
 [('Lip &amp; Face Filler', 'Hyaluronic acid filler for lips, cheeks and under-eyes.', '30–45 min', '<b>$850</b>', 'r-smooth.jpg', '50% 35%'),
  ('Glow Booster', 'Hydration plus brightening, delivered into the skin.', '30 min', '<s>$450</s><b>$299</b>', 'about.jpg', '50% 25%', '34% off'),
  ('EMFACE®', 'Needle-free lift for brows, cheeks and jawline.', '20 min', '<s>$1,000</s><b>$399</b>', 'svc-lift.jpg', '40% 30%', '60% off', 'emface.html')],
 [('Does it hurt?', 'Most clients describe a quick pinch. We use a very fine needle and can apply ice first.'), ('Will I look frozen?', 'Not when it is dosed well. We aim for softer lines with natural movement.'), ('Should I choose Botox® or Xeomin®?', 'Both work very well. Your provider recommends one based on your history and goals.'), ('What should I avoid afterwards?', 'Stay upright for 4 hours and skip workouts, saunas and facial massage for 24 hours.'), ('Who should not have it?', 'Anyone pregnant or breastfeeding, or with certain neuromuscular conditions. We review your health history first.')],
 ('Ready for a <em>softer</em> look?', 'Book a consultation. Your provider will map your face and confirm your units.', 'Book Now'))

# ---------------- 3 GLOW BOOSTER (Skin & Glow) ----------------
service('glow-booster.html', 'skin-glow.html', '<a href="skin-glow.html">Skin &amp; Glow</a> / Hydrate &amp; Glow / Glow Booster',
 dict(group='Skin &amp; Glow · Hydrate &amp; Glow', h1='Glow <em>Booster</em>', h1plain='Glow Booster',
  lede='Hydration and brightening delivered directly into the skin. Skin looks plumper, smoother and lit from within, without changing your features.',
  chips=['Hyaluronic acid based', '30 minutes', '1–2 days of tiny bumps'], img='about.jpg', pos='50% 25%',
  thumbs=[('about.jpg', '50% 25%'), ('r-tone.jpg', '50% 35%'), ('svc-skin.jpg', '50% 40%'), ('r-care2.jpg', '50% 55%')],
  opts=[('Choose', ['First visit', 'Single session', 'Series of 3'])],
  price='<s>$450</s><b>$299</b><span class="tag">34% off</span><small>First-visit price, once per client. Series of 3: $1,200.</small>',
  facts=[('Treatment time', '30 minutes'), ('Downtime', '1–2 days of tiny bumps'), ('Glow visible', '1–2 weeks'), ('Best as', 'A series of 3, 3–4 weeks apart')]),
 ('Hydration <em>inside</em> the skin', 'Creams sit on top. A booster places hyaluronic acid and brightening ingredients into the skin in tiny, even droplets.',
  [('Dullness', 'Brings back light reflection and radiance.', 'Brightening'), ('Dryness', 'Deep, lasting hydration from within.', 'Hyaluronic acid'), ('Fine lines', 'Plumps fine, dry lines around the eyes and cheeks.', 'Smoothing'), ('Uneven tone', 'Helps even out tone over a series.', 'Over 3 sessions')],
  ['Dull, tired-looking skin', 'Dry or dehydrated skin, especially in winter', 'Before a wedding or big event', 'Fine lines that come from dryness', 'Anyone who wants glow without volume']),
 ('Layered for <em>your</em> skin', 'Your Gold Skin Analysis tells us where your skin is dry, dull or sensitive.',
  [('Analyze', 'We check hydration, tone and sensitivity first.'), ('Plan', 'We choose the areas and depth based on your analysis.'), ('Map', 'Even droplets across the face, neck or hands.'), ('Repeat', 'A series of 3 builds results that last.')]),
 ('compare', 'Booster vs filler', 'Glow or <em>volume</em>?', 'Two different jobs. Your provider will recommend the right one, or both.',
  table(['', 'Glow Booster', 'Filler'], [['Main goal', 'Hydration, glow and smoother texture', 'Volume, shape and contour'], ['Changes face shape', 'No', 'Yes'], ['How it works', 'Tiny droplets spread across the skin', 'Gel placed in specific areas'], ['Results', 'Build over a series of 3', 'Instant'], ['Best for', 'Dull, dry, tired-looking skin', 'Hollows, lips, cheeks, jawline']])),
 ('Your <em>timeline</em>', '', [('Day 0', 'Numbing cream, then 30 minutes of treatment. Small bumps are normal.'), ('Days 1–2', 'Bumps settle. Makeup the next day.'), ('Weeks 1–2', 'Skin looks plumper and more radiant.'), ('Session 2–3', 'Results build and last longer with each session.')]),
 ('Clear <em>pricing</em>', '', ['Option', 'Sessions', 'Price', 'Per session'], [['First visit', '1', '$299', '$299'], ['Single session', '1', '$450', '$450'], ['Series', '3', '$1,200', '$400']], 2),
 ['Radiance and hydration, after a series of 3', 'Fine lines under the eyes, after a series of 3', 'Dull tone, 2 weeks after one session'],
 [('HydraFacial® Platinum', 'Adds lymphatic drainage and boosters.', '75 min', '<b>$329</b>', 'about.jpg', '50% 25%'),
  ('M22™ Photofacial', 'Intense pulsed light for spots and redness.', '30 min', '<b>Consult</b>', 'r-care2.jpg', '50% 55%'),
  ('Botox® &amp; Xeomin®', 'Softens expression lines.', '10–20 min', 'From <b>$10</b>/unit', 'r-texture.jpg', '50% 40%', '', 'botox-xeomin.html')],
 [('Does it hurt?', 'We apply numbing cream first. Most clients feel light pressure.'), ('Will it change my face shape?', 'No. Boosters add hydration and glow, not volume.'), ('How long does it last?', 'After a series of 3, most clients maintain with one session every 2–3 months.'), ('Can I wear makeup?', 'Wait until the next day.'), ('Is it included in membership?', 'AURA Prime members receive a BBL™ or Rejuran® session every 3 months.')],
 ('Your glow, <em>booked</em>', 'Start with a free skin analysis. Your provider will recommend the right booster for you.', 'Book Now'))

# ---------------- 4 BODY SCULPT (Body Shape) ----------------
service('body-sculpt.html', 'body-shape.html', '<a href="body-shape.html">Body Shape</a> / Body Sculpt',
 dict(group='Body Shape', h1='Body <em>Sculpt</em>', h1plain='Body Sculpt',
  lede='Non-invasive fat reduction for the stubborn areas diet and exercise don’t reach. No needles, no downtime, back to your day in 30 minutes.',
  chips=['Non-invasive', '30 minutes', 'No downtime'], img='s-body.jpg', pos='45% 50%',
  thumbs=[('s-body.jpg', '45% 50%'), ('r-body2.jpg', '50% 35%'), ('r-body.jpg', '50% 40%'), ('svc-lift.jpg', '40% 30%')],
  opts=[('Area', ['Abdomen', 'Other areas · consult']), ('Plan', ['Single session', '4 sessions'])],
  price='<b>$300</b><span style="color:var(--muted)">/ session</span><small>4 sessions for $999 ($250 each).</small>',
  facts=[('Treatment time', '30 minutes'), ('Downtime', 'None'), ('Results', 'Build over 8–12 weeks'), ('Best as', 'A series of 4')]),
 ('Shape what <em>stays</em>', 'Body Sculpt targets fat cells in one area at a time, so your shape changes gradually and naturally.',
  [('Abdomen', 'Lower and upper belly.', '$300 / session'), ('Flanks', 'The “love handle” area.', 'Consult'), ('Thighs &amp; arms', 'Planned by area.', 'Consult')],
  ['Close to your goal weight with one stubborn area', 'Not ready for surgery', 'Want no downtime', 'Postpartum body goals (after you finish breastfeeding)']),
 ('Planned like <em>design</em>', 'We look at proportion, not just inches.',
  [('Measure', 'Photos, measurements and a pinch test of each area.'), ('Plan', 'Which areas, in what order, for a balanced shape.'), ('Treat', 'Four sessions, spaced for your schedule.'), ('Track', 'Progress photos at weeks 4, 8 and 12.')]),
 None,
 ('Your <em>timeline</em>', '', [('Session 1', '30 minutes, lie back and relax. Mild warmth or tingling.'), ('Weeks 2–4', 'Your body begins to clear treated fat cells.'), ('Weeks 8–12', 'Visible change in shape and how clothes fit.'), ('Maintain', 'A steady weight keeps results.')]),
 ('Clear <em>pricing</em>', '', ['Area', 'Single', '4 sessions'], [['Abdomen', '$300', '$999'], ['Other areas', 'Consult', 'Consult']], 2),
 ['Abdomen, 12 weeks after 4 sessions', 'Flanks, 12 weeks after 4 sessions', 'Lower belly, 8 weeks after 4 sessions'],
 [('Stretch Mark Repair', 'Gold RF Microneedling, then collagen rebuild.', 'Planned at consult', '<b>Consult</b>', 'r-body.jpg'),
  ('Trap Tox · Shoulder Line', 'A longer, softer neckline.', '15 min', '<b>By units</b>', 'r-lift.jpg', '50% 45%'),
  ('NAD+ IV Drip', 'Energy and recovery.', '60–90 min', 'From <b>$400</b>', 'svc-skin.jpg', '50% 40%', '', 'nad-iv.html')],
 [('Is it a weight-loss treatment?', 'No. It reduces fat in targeted areas. It works best close to your goal weight.'), ('Does it hurt?', 'Most clients feel warmth or tingling. You can read or nap.'), ('When will I see results?', 'Change builds over 8–12 weeks as your body clears treated fat.'), ('Which device do you use?', '[Device name to be confirmed by the medical team.]')],
 ('Plan your body <em>goals</em>', 'Book a free consultation. We measure and plan before your first session.', 'Book Now'))

# ---------------- 5 NAD+ IV (Wellness) ----------------
service('nad-iv.html', 'wellness.html', '<a href="wellness.html">Wellness</a> / NAD+ IV Drip',
 dict(group='Wellness · Energy &amp; Recovery', h1='NAD+ <em>IV Drip</em>', h1plain='NAD+ IV Drip',
  lede='A slow, supervised IV infusion of NAD+, a coenzyme your cells use to make energy. Relax in our private lounge during your drip.',
  chips=['Medical screening included', '60–90 minutes', 'Private lounge'], img='svc-skin.jpg', pos='50% 40%',
  thumbs=[('svc-skin.jpg', '50% 40%'), ('about.jpg', '50% 25%'), ('about-reception.jpg', '50% 50%'), ('r-tone.jpg', '50% 35%')],
  opts=[('Dose', ['250 mg · about 60 min', '500 mg · about 90 min']), ('Plan', ['Single drip', '6 drips'])],
  price='<b>$400</b><small>500 mg: $750. Packages: 6 × 250 mg $1,999 · 6 × 500 mg $3,750.</small>',
  facts=[('Time', '60–90 minutes'), ('Downtime', 'None'), ('Before your first drip', 'Health screening with a provider'), ('Members', 'Earn credits toward NAD+')]),
 ('Energy, at the <em>cellular</em> level', 'NAD+ levels naturally fall with age. Many clients use regular drips as part of their wellness routine.',
  [('Energy', 'Support for everyday energy.', 'Wellness'), ('Recovery', 'After travel, training or long weeks.', 'Wellness'), ('Focus', 'Part of a balanced routine.', 'Wellness')],
  ['Busy professionals in Midtown', 'Frequent travelers', 'Active clients focused on recovery', 'Anyone building a long-term wellness routine']),
 ('Supervised, <em>start to finish</em>', '',
  [('Screen', 'A provider reviews your health history and medications.'), ('Dose', '250 mg or 500 mg, chosen with you.'), ('Drip', 'A slow infusion, adjusted for your comfort.'), ('Rest', 'Water, snacks and a quiet lounge.')]),
 None,
 ('Your <em>visit</em>', '', [('Before', 'Eat a light meal and drink water.'), ('During', 'Some warmth or chest tightness is common; we slow the drip.'), ('After', 'Back to your day right away.'), ('Routine', 'Many clients book a series of 6.')]),
 ('Clear <em>pricing</em>', '', ['Dose', 'Single', '6 drips', 'Per drip'], [['250 mg', '$400', '$1,999', '$333'], ['500 mg', '$750', '$3,750', '$625']], 2),
 ['Client stories (text only, no medical claims)', 'Lounge experience', 'Member routine'],
 [('EXOMIND™', 'A calm, non-invasive session for mood.', '30 min', '<s>$550</s><b>$399</b>', 'svc-laser.jpg', '50% 30%', '27% off'),
  ('AURA Prime', '50 Wellness Credits every month.', 'Monthly', '', 's-inject.jpg', '45% 40%', '', 'aura-prime.html'),
  ('Glow Booster', 'Hydration plus brightening.', '30 min', '<s>$450</s><b>$299</b>', 'about.jpg', '50% 25%', '34% off', 'glow-booster.html')],
 [('Who administers the drip?', 'A licensed nurse, under provider supervision.'), ('Does it feel uncomfortable?', 'Some clients feel warmth or pressure. We slow the drip so you stay comfortable.'), ('Is it covered by insurance?', 'No. NAD+ IV is a wellness service.'), ('Can I use Wellness Credits?', 'Yes. 500 AURA Prime Wellness Credits = 1 NAD+ drip.')],
 ('Book your <em>reset</em>', 'Your first visit includes a health screening.', 'Book Now'))

# ---------------- 6 GLOW GIRL MEMBERSHIP (Membership) ----------------
service('glow-girl.html', 'membership.html', '<a href="membership.html">Membership</a> / Glow Girl Membership',
 dict(group='Membership', h1='Glow Girl <em>Membership</em>', h1plain='Glow Girl Membership',
  lede='A steady, never-overdone rhythm for your skin. One facial every month, a glow treatment every quarter, and credits toward wellness.',
  chips=['$299 / month', '3-month minimum', 'Cancel with 30 days’ notice'], img='s-inject.jpg', pos='45% 40%',
  thumbs=[('s-inject.jpg', '45% 40%'), ('r-care2.jpg', '50% 55%'), ('about.jpg', '50% 25%'), ('svc-skin.jpg', '50% 40%')],
  opts=[('Your monthly facial', ['HydraFacial®', 'Barrier Recovery Facial', 'Signature Facial'])],
  price='<b>$299</b><span style="color:var(--muted)">/ month</span><small>Billed monthly. 3-month minimum.</small>', cta='Join Now',
  facts=[('Every month', '1 facial'), ('Every 3 months', 'IPL Photofacial or Glow Booster'), ('Credits', '50 Wellness Credits / month'), ('Rollover', 'Credits roll over')]),
 ('What’s <em>included</em>', '',
  [('Monthly facial', 'HydraFacial®, Barrier Recovery Facial or Signature Facial.', 'Up to $329 value'), ('Quarterly glow', 'IPL Photofacial or Glow Booster every 3 months.', 'Up to $450 value'), ('Wellness Credits', '50 each month. 500 credits = 1 NAD+ drip.', 'Rolls over')],
  ['Clients who want consistent, gradual results', 'Busy schedules that need a routine', 'Anyone already booking a monthly facial', 'Members who want a path to NAD+']),
 ('How it <em>works</em>', '',
  [('Join', 'Sign up online or at the front desk.'), ('Book', 'Choose your facial each month.'), ('Unlock', 'After 3 consecutive months, your quarterly treatment unlocks.'), ('Earn', 'Credits add up toward NAD+.')]),
 ('save', 'Member value', 'Member vs <em>pay as you go</em>', '',
  table(['Over 3 months', 'Pay as you go', 'Glow Girl'], [['3 HydraFacial® Platinum', '$987', 'Included'], ['1 Glow Booster', '$450', 'Included'], ['150 Wellness Credits', '—', 'Included'], ['Total', '$1,437', '$897']])),
 ('Membership <em>rules</em>', '', [('Minimum', '3 months, billed monthly.'), ('Monthly facial', 'Use it within the month; it does not roll over.'), ('Quarterly perk', 'Unlocks after 3 consecutive months.'), ('Cancel', '30 days’ notice after the minimum.')]),
 ('Compare <em>memberships</em>', '', ['', 'Glow Girl', 'Aura VIP Gold', 'Aura VIP Black'], [['Price', '$299 / month', '$5,000 prepaid', '$10,000 prepaid'], ['Bonus credit', '—', '+$800', '+$1,500'], ['Facials', '1 / month', '1 / quarter', '2 / quarter'], ['Skin Analysis', 'Free', 'Unlimited', 'Unlimited']], None),
 ['Member skin, month 1', 'Member skin, month 6', 'Member skin, month 12'],
 [('Aura VIP Gold', 'Prepaid credit with bonus value.', 'Prepaid', '<b>$5,000</b>', 's-body.jpg', '45% 50%'),
  ('HydraFacial® Platinum', 'Your monthly facial option.', '75 min', '<b>$329</b>', 'about.jpg', '50% 25%'),
  ('NAD+ IV Drip', 'Redeem 500 credits for a drip.', '60 min', 'From <b>$400</b>', 'svc-skin.jpg', '50% 40%', '', 'nad-iv.html')],
 [('Can I pause?', 'Yes, once per year for up to 1 month. [Policy to be confirmed.]'), ('Do credits expire?', 'Credits roll over while your membership is active.'), ('Can I combine it with first-visit offers?', 'First-visit prices apply to non-member treatments once per client.'), ('Can I share it?', 'Glow Girl is personal. Aura VIP credit can be shared with friends.')],
 ('Glow, <em>every</em> month', 'Join at the front desk or online.', 'Join Now'))

# ---------------- 7 OUR STORY (About) ----------------
page('our-story.html', 'Our Story · AURA Institute', 'about.html', '<a href="about.html">About</a> / Our Story',
 '<div class="wrap"><div class="hero" style="margin-top:18px"><div class="tx"><p class="eyebrow">Our Story</p><h1>Not someone else. <em>A better you.</em></h1><p>Why we built a medical aesthetics clinic around design, not discounts.</p></div><div class="ph"><img src="about-reception.jpg" alt="" style="object-position:50% 50%"></div></div></div>' +
 '<section><div class="wrap story"><div class="ph"><img src="about.jpg" alt="" style="object-position:50% 25%"></div><div><p class="eyebrow">Where we started</p><p class="quote">“We kept meeting people who had treatments, but no plan.”</p><p style="color:var(--muted);margin-top:22px">[Founder story to be written with the team: why AURA, the experience behind the brand, and why New York.] AURA Institute began with a simple idea: aesthetic treatment should start with understanding your face, then choosing the right steps in the right order.</p><p style="color:var(--muted)">Today our providers combine medicine, aesthetics and skin science to design results that look like you on your best day.</p><p style="margin-top:20px"><b>[Founder name]</b><br><span style="color:var(--muted)">Founder, AURA Institute</span></p></div></div></section>' +
 '<section class="alt"><div class="wrap"><div class="head"><p class="eyebrow">What we believe</p><h2>Three <em>principles</em></h2></div>' + steps([('Design before product', 'We plan the whole face first, then choose products.'), ('Repair before treat', 'Healthy skin responds better to every treatment.'), ('Less, more often', 'Gradual, natural change over dramatic one-time results.'), ('Honest advice', 'We will tell you when you don’t need a treatment.')]) + '</div></section>' +
 '<section><div class="wrap"><div class="nums"><div><b>[X]+</b><span>Years of combined experience</span></div><div><b>[X]</b><span>Licensed providers</span></div><div><b>FDA</b><span>Approved products only</span></div><div><b>[X.X]★</b><span>Google rating</span></div></div></div></section>' +
 '<section class="alt"><div class="wrap"><div class="head"><p class="eyebrow">Our journey</p><h2>From one clinic to <em>Rockefeller Center</em></h2></div>' + tl([('[Year]', 'Our first clinic opens.'), ('[Year]', 'Our design-led consultation method takes shape.'), ('[Year]', 'AURA Institute opens at Rockefeller Center.'), ('Today', 'Medical aesthetics, body and wellness under one roof.')]) + '</div></section>' +
 '<section><div class="wrap"><div class="head"><p class="eyebrow">Keep exploring</p><h2>Meet the <em>team</em></h2></div><div class="prods">' + ''.join(gen.prod(*p) for p in [('Our Approach', 'Understand, analyze, explain, plan.', '4 steps', '', 'r-texture.jpg'), ('Our Providers', 'Licensed MDs, NPs and RNs.', 'Meet the team', '', 'about.jpg', '50% 25%'), ('The Clinic', 'A calm space in Midtown.', 'Visit us', '', 'about-reception.jpg', '50% 50%')]) + '</div></div></section>' +
 gen.cta('Come say <em>hello</em>', 'Book a complimentary Gold Skin Analysis and see the clinic.', 'Book Now'))

# ---------------- 8 JOURNAL ARTICLE (Journal & FAQ · Skin Education) ----------------
toc = [('diff', 'What’s the difference?'), ('same', 'What’s the same'), ('choose', 'How we choose'), ('expect', 'What to expect'), ('bottom', 'The bottom line')]
page('journal-botox-vs-xeomin.html', 'Botox vs Xeomin · AURA Journal', 'journal-faq.html', '<a href="journal-faq.html">Journal &amp; FAQ</a> / Skin Education',
 '<div class="wrap"><div style="max-width:880px;margin:24px auto 0"><p class="eyebrow">Skin Education · Injectables</p><h1 style="font-family:var(--serif);font-size:clamp(40px,5vw,64px);line-height:1.02;margin:12px 0 18px">Botox® vs Xeomin®: what’s the <em>difference</em>?</h1>'
 '<div class="byline"><span>By [Author], AURA Journal</span><span>Medically reviewed by [Provider name, NP]</span><span>5 min read</span><span>Updated [date]</span></div></div>'
 '<div class="arthero"><img src="r-texture.jpg" alt="" style="object-position:50% 40%"></div></div>'
 '<section><div class="wrap art"><nav class="toc"><b>In this article</b>' + ''.join(f'<a href="#{i}">{t}</a>' for i, t in toc) + '<a class="btn" style="margin-top:12px" href="botox-xeomin.html">See the treatment</a></nav><article class="body">'
 '<p>Both are FDA-approved wrinkle relaxers that soften expression lines. So why do clinics offer two? Here is what our providers tell clients in consultation.</p>'
 '<h2 id="diff">What’s the difference?</h2><p>Botox® contains the active ingredient plus accessory proteins. Xeomin® is purified to the active ingredient alone, which is why it is sometimes called a “naked” formula.</p>'
 '<div class="callout"><b>Provider note</b>For most people, results look the same. Placement and dose matter far more than the brand.</div>'
 '<h2 id="same">What’s the same</h2><p>Both start working in about 3–5 days, reach full effect around day 14, and last about 3–4 months.</p>'
 '<h2 id="choose">How we choose</h2><p>We consider your history with each product, your goals and your budget. Your provider explains the options and gives you a clear quote at consultation.</p>'
 '<h2 id="expect">What to expect</h2><p>Treatment takes 10–20 minutes with no downtime. Stay upright for 4 hours and skip workouts for 24 hours.</p>'
 '<h2 id="bottom">The bottom line</h2><p>Choose a provider, not a brand. A good plan uses the right product in the right places.</p>'
 '<div class="callout"><b>Medical disclaimer</b>This article is for education only and is not medical advice. Results vary.</div></article></div></section>' +
 '<section class="alt"><div class="wrap"><div class="head"><p class="eyebrow">Related treatments</p><h2>Ready to <em>try</em>?</h2></div><div class="prods">' + ''.join(gen.prod(*p) for p in [('Botox® &amp; Xeomin®', 'Softens expression lines.', '10–20 min', '', 'r-texture.jpg', '50% 40%', '', 'botox-xeomin.html'), ('Gold Skin Analysis', 'Know your skin first.', '20 min', '', 'about-reception.jpg', '50% 50%', '', 'gold-skin-analysis.html')]) + '</div></div></section>' +
 '<section><div class="wrap"><div class="head"><p class="eyebrow">Keep reading</p><h2>More from the <em>Journal</em></h2></div><div class="prods">' + ''.join(gen.prod(*p) for p in [('Skin booster vs filler', 'Glow or volume? How to tell what you need.', '4 min read', '', 'about.jpg', '50% 25%'), ('Why skin loosens', 'The aging cascade, from bone to surface.', '6 min read', '', 'r-lift.jpg', '50% 45%'), ('Winter skin reset', 'Repair first, then treat.', '3 min read', '', 'r-care2.jpg', '50% 55%')]) + '</div></div></section>' +
 gen.cta('Still have a <em>question</em>?', 'Text us anytime or book a free consultation.', 'Book Now'))

# link index
s = open(OUT + '/index.html').read()
add = ''.join(f'<a class="card" href="{h}"><div class="bd"><span class="lv">Level 2 · service page</span><h3>{t}</h3><ul><li>{n}</li></ul></div></a>' for h, t, n in [
 ('gold-skin-analysis.html', 'Gold Skin Analysis', 'Special Offers'), ('botox-xeomin.html', 'Botox® &amp; Xeomin®', 'Face &amp; Contour'), ('glow-booster.html', 'Glow Booster', 'Skin &amp; Glow'), ('body-sculpt.html', 'Body Sculpt', 'Body Shape'),
 ('nad-iv.html', 'NAD+ IV Drip', 'Wellness'), ('aura-prime.html', 'AURA Prime', 'Membership'), ('our-story.html', 'Our Story', 'About'), ('journal-botox-vs-xeomin.html', 'Journal article', 'Journal &amp; FAQ')])
if 'gold-skin-analysis.html' not in s:
    s = s.replace('</div>\n</div></section>\n</main>', add + '</div>\n</div></section>\n</main>')
    open(OUT + '/index.html', 'w').write(s)
print('done')
