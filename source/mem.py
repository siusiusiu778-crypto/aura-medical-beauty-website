import sys, io, contextlib
sys.path.insert(0, '/home/claude/pages')
with contextlib.redirect_stdout(io.StringIO()):
    import svc
gen = svc.gen; OUT = gen.OUT
CSS = r'''
.mh{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);background:var(--tan);color:#241A14;margin-top:18px;min-height:560px}
@media(max-width:860px){.mh{grid-template-columns:1fr}.mh .ph{order:-1;aspect-ratio:4/3}}
.mh .tx{padding:64px clamp(24px,5vw,72px);display:grid;gap:18px;align-content:center}
.mh h1{font-family:var(--serif);font-size:clamp(48px,5.4vw,80px);line-height:.95}
.mh .pr{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}.mh .pr b{font-size:44px;font-weight:500}.mh .pr span{font-size:15px;letter-spacing:.06em}
.mh .pr i{font-style:normal;font-size:12px;letter-spacing:.14em;text-transform:uppercase;border:1px solid currentColor;padding:4px 10px;border-radius:99px}
.mh p{margin:0;font-size:17px;max-width:520px}.mh .btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:6px}
.mh .ph{overflow:hidden}.mh .ph img{width:100%;height:100%;object-fit:cover;display:block}
.perks{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}@media(max-width:900px){.perks{grid-template-columns:1fr}}
.perk{background:var(--card);border:1px solid var(--line);padding:30px 28px;display:grid;gap:12px;align-content:start}
.perk .fq{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--rust);font-weight:600}
.perk h3{font-family:var(--serif);font-size:30px;line-height:1.1}.perk p{margin:0;color:var(--muted);font-size:15px}
.perk ul{margin:0;padding:0;list-style:none;display:grid;gap:8px}.perk li{border-top:1px solid var(--line);padding-top:8px;font-size:15px}
.perk .eq{background:var(--surface);padding:12px 14px;font-size:15px;font-weight:600}
.perk .tags{display:flex;flex-wrap:wrap;gap:6px}.perk .tags span{font-size:12px;border:1px solid var(--line);border-radius:99px;padding:4px 10px;color:var(--muted)}
.yr{display:grid;grid-template-columns:repeat(12,1fr);gap:8px}@media(max-width:900px){.yr{grid-template-columns:repeat(6,1fr)}}
.mo{background:var(--card);border:1px solid var(--line);padding:12px 10px;display:grid;gap:6px;min-height:150px;align-content:start}
.mo b{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}.mo span{font-size:12.5px;padding:4px 6px;border-radius:4px}
.mo .f{background:#efe4d8}.mo .q{background:var(--accent);color:var(--on-accent)}.mo .c{background:#e4e8dc;color:#3e4a33}.mo .n{background:var(--rust);color:#fff}
.lg{display:flex;gap:18px;flex-wrap:wrap;margin-top:16px;font-size:13.5px;color:var(--muted)}.lg span::before{content:"";display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px;background:var(--c)}
.tot{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}@media(max-width:760px){.tot{grid-template-columns:1fr}}
.tot div{border-top:2px solid var(--fg);padding-top:12px}.tot b{display:block;font-family:var(--serif);font-size:44px;font-weight:400;line-height:1}.tot span{font-size:14px;color:var(--muted)}
.rules{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:0 40px}@media(max-width:760px){.rules{grid-template-columns:1fr}}
.rules li{display:grid;grid-template-columns:40px 1fr;padding:18px 0;border-bottom:1px solid var(--line);font-size:16px}.rules li i{font-style:normal;font-family:var(--serif);font-size:24px;color:var(--rust);line-height:1}
.cmpm{width:100%;border-collapse:collapse;font-size:15px}.cmpm th,.cmpm td{padding:16px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.cmpm thead th{font-family:var(--serif);font-size:26px;font-weight:400;border-bottom:2px solid var(--fg)}.cmpm thead th small{display:block;font-family:var(--sans);font-size:14px;color:var(--muted);margin-top:4px}
.cmpm td:first-child{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);width:20%}.cmpm .hl{background:var(--surface)}
.cmpm .bt td{border-bottom:0;padding-top:20px}
.join{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}@media(max-width:760px){.join{grid-template-columns:1fr}}
.join div{border-top:2px solid var(--fg);padding-top:14px}.join i{font-style:normal;font-family:var(--serif);font-size:34px;color:var(--rust)}.join h4{margin:4px 0;font-size:18px}.join p{margin:0;color:var(--muted);font-size:14.5px}
'''
open(OUT + '/mem.css', 'w').write(CSS)
HEAD = gen.HEAD.replace('<link rel="stylesheet" href="site.css">', '<link rel="stylesheet" href="site.css"><link rel="stylesheet" href="svc.css"><link rel="stylesheet" href="mem.css">')

def sec(sid, eb, h2, p, inner, alt=False):
    return svc.sec(sid, eb, h2, p, inner, alt)

# 12-month view: facial every month; quarterly perk at month 3,6,9,12 (unlocks after 3 consecutive months); credits 50/mo; NAD+ at 500 (month 10)
months = ''
for m in range(1, 13):
    cells = '<span class="f">Facial</span>'
    if m % 3 == 0: cells += '<span class="q">IPL or Glow Booster</span>'
    cells += f'<span class="c">{m*50} credits</span>' if m < 10 else ('<span class="n">500 = 1 NAD+</span>' if m == 10 else f'<span class="c">{(m-10)*50} credits</span>')
    months += f'<div class="mo"><b>Month {m}</b>{cells}</div>'

body = f'''<div class="wrap"><div class="mh"><div class="tx"><p class="eyebrow" style="color:inherit;opacity:.75">AURA Membership</p><h1>Glow Girl <em>Membership</em></h1>
<div class="pr"><b>$299</b><span>/ month</span><i>3-month minimum</i></div>
<p>A steady, consistent, never-overdone rhythm for your skin. From everyday facials to seasonal light treatments, make glowing a monthly habit.</p>
<div class="btns"><a class="btn" href="#join">Join Now</a><a class="btn line" href="#compare">Compare Memberships</a></div></div>
<div class="ph"><img src="about.jpg" alt="" style="object-position:50% 30%"></div></div></div>'''

body += sec('included', 'What’s included', 'Three perks, <em>every</em> month', 'Everything you need to keep skin consistent, from monthly care to seasonal resets.', f'''<div class="perks">
<div class="perk"><span class="fq">✦ Every month</span><h3>1 facial of your choice</h3><p>Pick the facial your skin needs that month.</p><ul><li>HydraFacial®</li><li>Barrier Recovery Facial</li><li>Signature Facial</li></ul></div>
<div class="perk"><span class="fq">✦ Every 3 months</span><h3>IPL Photofacial or Glow Booster</h3><p>Unlocks after 3 consecutive months. A seasonal reset for:</p><div class="tags"><span>Dull tone</span><span>Uneven tone</span><span>Redness</span><span>Skin maintenance</span></div></div>
<div class="perk"><span class="fq">✦ Every month</span><h3>50 Wellness Credits</h3><p>Credits are added automatically and keep adding up.</p><div class="eq">500 Wellness Credits = 1 NAD+ Wellness Treatment</div></div></div>''')

body += sec('year', 'Your first year', 'A year of <em>Glow</em>, month by month', 'Here is how the perks add up over 12 consecutive months.', f'''<div class="yr">{months}</div>
<div class="lg"><span style="--c:#efe4d8">Monthly facial</span><span style="--c:var(--accent)">Quarterly IPL or Glow Booster</span><span style="--c:#e4e8dc">Wellness Credits</span><span style="--c:var(--rust)">NAD+ unlocked</span></div>
<div class="tot"><div><b>12</b><span>facials</span></div><div><b>4</b><span>IPL Photofacials or Glow Boosters</span></div><div><b>600</b><span>Wellness Credits, enough for 1 NAD+ treatment</span></div></div>''', alt=True)

rules = ['Glow Girl Membership has a 3-month minimum.', 'The quarterly IPL / Glow Booster perk unlocks after 3 consecutive months.', 'Your monthly facial must be used within that month.', 'Perks not yet unlocked cannot be exchanged for cash or refunded.', 'Wellness Credits keep adding up.', 'To cancel, please give 30 days’ notice.']
body += sec('rules', 'Membership rules', 'Simple, <em>clear</em> rules', '', '<ol class="rules">' + ''.join(f'<li><i>0{k+1}</i><span>{r}</span></li>' for k, r in enumerate(rules)) + '</ol>')

rows = [('Price', '$299 / month', '$5,000 prepaid', '$10,000 prepaid'), ('Commitment', '3-month minimum', 'One-time top-up', 'One-time top-up'), ('Bonus credit', '—', '+$800 Aura Credit', '+$1,500 Aura Credit'),
 ('Facials', '1 every month', '1 every quarter', '2 every quarter'), ('Seasonal treatment', 'IPL or Glow Booster every 3 months', '—', '—'), ('Wellness', '50 credits / month', '—', '—'),
 ('Gold Skin Analysis', '—', 'Unlimited', 'Unlimited'), ('Plan consultation', '—', '—', 'Quarterly skin &amp; anti-aging plan'), ('Birthday credit', '—', '$100', '$300'),
 ('Share credit', '—', 'With 1 friend', 'With 2 friends'), ('Events', '—', 'Priority sign-up for private events', 'First invitations to events, launches &amp; private events')]
tbl = '<div style="overflow-x:auto"><table class="cmpm"><thead><tr><th></th><th class="hl">Glow Girl<small>Monthly membership</small></th><th>Aura Gold<small>Prepaid VIP</small></th><th>Aura Black<small>Prepaid VIP</small></th></tr></thead><tbody>'
tbl += ''.join(f'<tr><td>{a}</td><td class="hl">{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in rows)
tbl += '<tr class="bt"><td></td><td class="hl"><a class="btn" href="#join">Join Glow Girl</a></td><td><a class="btn line" href="#join">Ask about Gold</a></td><td><a class="btn line" href="#join">Ask about Black</a></td></tr></tbody></table></div>'
body += sec('compare', 'Compare memberships', 'Monthly or <em>prepaid</em>?', 'Glow Girl is a monthly routine. Aura VIP is prepaid credit with bonus value and year-round perks. Facials in every plan are your choice of HydraFacial®, Barrier Recovery Facial or Signature Facial.', tbl, alt=True)

body += sec('join', 'How to join', 'Start your <em>Glow</em> routine', '', '''<div class="join"><div><i>01</i><h4>Join</h4><p>Sign up at the front desk or book a visit online. Billing starts on your join date.</p></div>
<div><i>02</i><h4>Choose your facial</h4><p>Book your monthly facial any time that month.</p></div><div><i>03</i><h4>Keep glowing</h4><p>Your quarterly perk unlocks at month 3. Credits add up toward NAD+.</p></div></div>''')

faqs = [('When does the quarterly IPL or Glow Booster unlock?', 'After 3 consecutive months of membership, and every 3 months after that.'),
 ('What if I don’t use my facial this month?', 'Monthly facials must be used within that month and don’t carry over.'),
 ('Do Wellness Credits expire?', 'Credits keep adding up while you are a member. 500 credits can be redeemed for 1 NAD+ Wellness Treatment.'),
 ('Can I get cash or a refund for unused perks?', 'Perks that haven’t been unlocked cannot be exchanged for cash or refunded.'),
 ('How do I cancel?', 'After the 3-month minimum, give us 30 days’ notice at the front desk or by email.'),
 ('What’s the difference between Glow Girl and Aura VIP?', 'Glow Girl is a monthly routine with set perks. Aura VIP is prepaid credit with bonus value you can use on any treatment, plus year-round perks.')]
body += f'<section class="alt" id="faq"><div class="wrap faqc"><p class="eyebrow" style="text-align:center">FAQs</p><h2 class="bh2" style="text-align:center">Membership <em>questions</em></h2>{svc.qa(faqs)}</div></section>'
body += gen.cta('$299/month, make great skin a <em>habit</em>.', 'Join at the front desk, or book a visit and we’ll set you up.', 'Join Now')

html = HEAD.format(title='Glow Girl Membership · AURA Institute') + gen.nav('membership.html') + '<main><div class="wrap crumbs"><a href="index.html">Home</a> / <a href="membership.html">Membership</a> / Glow Girl Membership</div>' + body + '</main><footer>AURA Institute · Rockefeller Center, New York · Results vary by individual.</footer></body></html>'
open(OUT + '/glow-girl.html', 'w').write(html)
print('done')
