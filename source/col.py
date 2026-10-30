import sys, io, contextlib
sys.path.insert(0, '/home/claude/pages')
with contextlib.redirect_stdout(io.StringIO()):
    import gen
OUT = gen.OUT
CSS = r'''
.chd{padding-block:28px 8px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:end;border-bottom:1px solid var(--line);padding-bottom:28px}
@media(max-width:860px){.chd{grid-template-columns:1fr;gap:12px}}
.chd h1{font-family:var(--serif);font-size:clamp(48px,6vw,84px);line-height:.95}.chd p{margin:0;color:var(--muted);font-size:17px}
.chips2{position:sticky;top:68px;z-index:20;background:var(--bg);border-bottom:1px solid var(--line)}.chips2 .wrap{display:flex;gap:10px;padding-block:14px;overflow-x:auto}
.chips2 a{white-space:nowrap;text-decoration:none;font-size:13px;letter-spacing:.06em;border:1px solid var(--line);padding:8px 16px;border-radius:999px;background:var(--card)}.chips2 a.on{background:var(--accent);color:var(--on-accent);border-color:var(--accent)}
.grp2{padding-top:44px}.grp2>h2{font-family:var(--serif);font-size:34px;margin:0 0 4px}.grp2>p{margin:0 0 8px;color:var(--muted)}
/*x*/.row{display:grid;grid-template-columns:240px minmax(0,1fr);gap:32px;padding:28px 0;border-bottom:1px solid var(--line);align-items:start}
@media(max-width:860px){.row{grid-template-columns:120px minmax(0,1fr);gap:16px}.row .side{grid-column:2}}
.row .ph{aspect-ratio:1;overflow:hidden;background:var(--surface);position:relative}.row .ph img{width:100%;height:100%;object-fit:cover;display:block}
.row .ph .sale{position:absolute;top:10px;left:10px;font-size:11px;background:var(--rust);color:#fff;padding:3px 8px;letter-spacing:.08em;text-transform:uppercase}
.row h3{font-size:26px;font-weight:500;margin:0 0 8px;letter-spacing:-.01em}.row h3 a{text-decoration:none}.row h3 a:hover{text-decoration:underline;text-underline-offset:4px}
.row .ex{margin:0 0 12px;color:#4d4038;font-size:15px;line-height:1.65;max-width:720px}
.row .tg{display:flex;flex-wrap:wrap;gap:8px}.row .tg span{font-size:12px;border:1px solid var(--line);padding:4px 10px;border-radius:999px;color:var(--muted)}
.row .side{display:grid;gap:10px;justify-items:start}.row .pr2{font-size:14px;color:var(--muted)}.row .pr2 b{display:block;font-size:24px;font-weight:500;color:var(--fg)}.row .pr2 s{margin-right:6px}
.row .side .btn{padding:11px 20px;font-size:11.5px;width:100%}
.row .lm{display:inline-block;margin-top:16px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:3px}
.band{margin-top:44px;background:var(--accent);color:var(--on-accent);padding:36px 40px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:32px;align-items:center}
@media(max-width:760px){.band{grid-template-columns:1fr;padding:28px 22px}}
.band .eyebrow{color:inherit;opacity:.7}.band h3{font-family:var(--serif);font-size:clamp(26px,2.6vw,34px);margin:8px 0}.band p{margin:0;opacity:.8;max-width:640px}.band .btn{background:var(--on-accent);color:var(--accent)}
'''
open(OUT + '/col.css', 'w').write(CSS)
HEAD = gen.HEAD.replace('<link rel="stylesheet" href="site.css">', '<link rel="stylesheet" href="site.css"><link rel="stylesheet" href="col.css">')

SHOW_SALE = [False]
def row(name, ex, tags, price, img, pos='50% 40%', sale='', link='#', btn='Book'):
    s = f'<span class="sale">{sale}</span>' if (sale and SHOW_SALE[0]) else ''
    tags = [t for t in tags if '$' not in t]
    lab = btn if btn in ('Read', 'Visit', 'Open') else 'Learn More'
    return f'''<article class="row"><a class="ph" href="{link}"><img src="{img}" alt="" style="object-position:{pos}">{s}</a><div><h3><a href="{link}">{name}</a></h3><p class="ex">{ex}</p><div class="tg">{''.join(f'<span>{t}</span>' for t in tags)}</div><a class="lm" href="{link}">{lab} <span aria-hidden="true">→</span></a></div></article>'''

BAND = '''<div class="band"><div><p class="eyebrow">Designed for you</p><h3>Units, price and the right combination are planned with your provider.</h3><p>Every face is different. At a complimentary consultation, your provider assesses your goals and builds a plan with clear pricing before any treatment.</p></div><a class="btn" href="#book">Book a Consultation</a></div>'''

def colpage(fn, title, crumbs, h1, intro, groups, cta, consult=True, sale=False):
    SHOW_SALE[0] = sale
    chips = '<div class="chips2"><div class="wrap"><a class="on" href="#top">All</a>' + ''.join(f'<a href="#{g[0]}">{g[1]}</a>' for g in groups) + '</div></div>'
    if len(groups) == 1: chips = ''
    body = f'<div class="wrap" id="top"><div class="chd"><h1>{h1}</h1><div><p>{intro}</p>'+('<a class="btn" style="margin-top:18px" href="#book">Book a Consultation</a>' if consult else '')+'</div></div></div>' + chips + '<section style="padding-top:0"><div class="wrap">'
    for k, (gid, gt, gp, rows) in enumerate(groups):
        body += f'<div class="grp2" id="{gid}"><h2>{gt}</h2><p>{gp}</p>' + ''.join(row(*r) for r in rows) + '</div>'
        if consult and k == min(1, len(groups) - 1) and len(groups) > 1: body += BAND
    if consult and len(groups) == 1: body += BAND
    body += '</div></section>' + gen.cta(*cta)
    html = HEAD.format(title=title) + gen.nav(fn) + f'<main><div class="wrap crumbs"><a href="index.html">Home</a> / {crumbs}</div>' + body + '</main><footer>AURA Institute · Rockefeller Center, New York · Results vary by individual.</footer></body></html>'
    open(f'{OUT}/{fn}', 'w').write(html)

F = 'From '
# ---------- SPECIAL OFFERS ----------
colpage('special-offers.html', 'Special Offers · AURA Institute', 'Special Offers', 'Special <em>Offers</em>',
 'First-visit prices on our signature treatments, packages that make a full course easier, and gift cards for someone you love.',
 [('new', 'New Client Offers', 'One first-visit price per treatment, per client.', [
   ('Gold Skin Analysis', 'Start here. A provider maps your skin layer by layer, then builds a plan around your goals and budget. No obligation to book.', ['20 min', 'No downtime', 'New clients'], '<b>Free</b>', 'about-reception.jpg', '50% 50%', 'Free', 'gold-skin-analysis.html'),
   ('EMFACE® · 1 Area', 'A needle-free lift for brows, cheeks and jawline in 20 minutes. Our most popular first visit.', ['20 min', 'No downtime'], '<s>$1,000</s><b>$399</b>', 'svc-lift.jpg', '40% 30%', '60% off', 'emface.html'),
   ('Glow Booster', 'Hydration and brightening delivered into the skin for a dewy, lit-from-within look.', ['30 min', '1–2 days of tiny bumps'], '<s>$450</s><b>$299</b>', 'about.jpg', '50% 25%', '34% off', 'glow-booster.html'),
   ('Collagen Lift · Cheeks', 'A targeted collagen boost for the cheeks, the first step in a 4-session plan.', ['30 min', '4-session plan'], '<s>$300</s><b>$199</b>', 'svc-laser.jpg', '50% 30%', '34% off'),
   ('Gold RF Microneedling', 'Pores, texture, acne scars and tone in one treatment.', ['60–90 min', '2–3 days of redness'], '<s>$999</s><b>$799</b>', 'r-lift.jpg', '50% 45%', '20% off'),
   ('EXOMIND™', 'A calm, non-invasive seated session designed to support mood and wellbeing.', ['30 min', 'No downtime'], '<s>$550</s><b>$399</b>', 'svc-skin.jpg', '50% 40%', '27% off')]),
  ('packages', 'Treatment Packages', 'Results build over a series. Packages lower the price per session.', [
   ('HydraFacial® Deluxe · 4 Sessions', 'A monthly deep cleanse, extraction and hydration routine.', ['60 min each', 'Monthly'], '<b>$980</b>', 'r-care2.jpg', '50% 55%'),
   ('Glow Booster · 3 Sessions', 'The full series for lasting hydration and glow.', ['30 min each', '3–4 weeks apart'], '<b>$1,200</b>', 'about.jpg', '50% 25%', '', 'glow-booster.html'),
   ('NAD+ 250 mg · 6 Drips', 'A wellness routine for energy and recovery.', ['60 min each'], '<b>$1,999</b>', 'svc-skin.jpg', '50% 40%', '', 'nad-iv.html')]),
  ('gift', 'Gift Cards', 'Good for any treatment, package or membership.', [
   ('AURA Gift Card', 'Choose any amount. Delivered by email or as a printed card at the front desk.', ['Any amount', 'Never expires'], '<b>Any amount</b>', 'r-tone.jpg', '50% 35%', '', '#', 'Buy')])],
 ('Start with a <em>free</em> skin analysis', 'We’ll map your skin and goals, then recommend the offer that fits.', 'Book an Appointment'), sale=True)

# ---------- FACE & CONTOUR ----------
colpage('face-contour.html', 'Face & Contour · AURA Institute', 'Face &amp; Contour', 'Face &amp; <em>Contour</em>',
 'Every face treatment, grouped by what you want to change. Each one is planned by a provider around your whole face.',
 [('lines', 'Smooth Lines', 'Soften expression lines while keeping your face natural.', [
   ('Botox® &amp; Xeomin®', 'Soften forehead lines, frown lines and crow’s feet. Your provider maps your muscles and chooses the right product and dose for you.', ['10–20 min', 'No downtime', 'Lasts 3–4 months'], F + '<b>$10 / unit</b>', 'r-texture.jpg', '50% 40%', '', 'botox-xeomin.html'),
   ('Trap Tox · Shoulder Line', 'Relaxes the trapezius muscle for a longer, softer neck and shoulder line.', ['15 min', 'No downtime'], '<b>By units</b>', 'r-lift.jpg', '50% 45%')]),
  ('volume', 'Restore Volume', 'Bring back lost volume in lips, cheeks, temples and under-eyes.', [
   ('Lip &amp; Face Filler', 'Hyaluronic acid filler for lips, cheeks, chin and under-eyes. Results are instant and fully adjustable.', ['30–45 min', '1–3 days swelling'], '<b>$850</b> half syringe $500', 'r-smooth.jpg', '50% 35%'),
   ('RADIESSE®', 'A collagen-stimulating filler that adds structure along the jaw, chin and cheekbones.', ['30–45 min', 'Lasts 12+ months'], '<b>$1,200</b>', 'r-lift.jpg', '50% 45%'),
   ('Sculptra®', 'Gradual collagen restoration for a fuller, firmer look that develops over a few months.', ['30–45 min', 'Series of 2–3'], '<b>$900</b>', 'r-tone.jpg', '50% 35%'),
   ('HArmonyCa™', 'A hybrid filler for instant lift plus long-term collagen support. [Availability to confirm.]', ['30–45 min'], '<b>$1,200</b>', 'svc-lift.jpg', '40% 30%')]),
  ('lift', 'Lift &amp; Tighten', 'Firmer skin and a lifted look, without surgery or downtime.', [
   ('EMFACE®', 'Needle-free lift for brows, cheeks and jawline. Tones the muscles and tightens the skin at the same time.', ['20 min', 'No downtime', '1–4 areas'], '<s>$1,000</s><b>$399</b>', 'svc-lift.jpg', '40% 30%', '60% off', 'emface.html'),
   ('Thermage® FLX', 'Radiofrequency tightening for the face and eyes. One treatment, results that build over months.', ['Eyes 450 / Face 900 pulses', 'No downtime'], F + '<b>$1,999</b>', 'r-lift.jpg', '50% 45%'),
   ('Collagen Lift', 'A targeted collagen boost for cheeks, eyes, neck or forehead, planned as a 4-session course.', ['30 min', '4-session plan'], '<s>$300</s><b>$199</b>', 'svc-laser.jpg', '50% 30%', '34% off')]),
  ('vline', 'V-Line Contour', 'A slimmer, more defined lower face and jawline.', [
   ('Jaw Slimming', 'Relaxes the masseter muscle to soften a square jaw and slim the lower face.', ['15 min', 'No downtime'], '<b>By units</b>', 'about.jpg', '50% 25%'),
   ('V-Line Injection', 'Contouring injections to slim and define the lower face. [Product to confirm.]', ['One side / both sides / + lift'], F + '<b>$350</b>', 'r-smooth.jpg', '50% 35%')]),
  ('design', 'Face Design', 'Not sure what you need? Start with a plan for your whole face.', [
   ('Face Design Consultation', 'A Gold Skin Analysis plus a full-face assessment with a provider.', ['30 min'], '<b>Free</b>', 'about-reception.jpg', '50% 50%'),
   ('Signature Face Plan', 'A step-by-step plan built around your face, schedule and budget.', ['Planned at consultation'], '<b>By plan</b>', 'r-texture.jpg')])],
 ('Not sure where to <em>start</em>?', 'Book a complimentary consultation. We’ll look at your whole face and suggest a plan.', 'Book an Appointment'))

# ---------- SKIN & GLOW ----------
colpage('skin-glow.html', 'Skin & Glow · AURA Institute', 'Skin &amp; Glow', 'Skin &amp; <em>Glow</em>',
 'Boosters, light treatments and facials, grouped by your skin concern. Not sure? Start with a free skin analysis.',
 [('glow', 'Hydrate &amp; Glow', 'Skin boosters that hydrate deeply and bring back a dewy glow.', [
   ('Glow Booster', 'Hydration and brightening delivered directly into the skin. Plumper, smoother, lit from within.', ['30 min', 'Series of 3'], '<s>$450</s><b>$299</b>', 'about.jpg', '50% 25%', '34% off', 'glow-booster.html'),
   ('Collagen Booster', 'Firmness and bounce, layer by layer, for early laxity and fine lines.', ['30 min'], '<s>$1,200</s><b>$999</b>', 'svc-laser.jpg', '50% 30%', '17% off'),
   ('Regen Booster', 'Renewal and radiance for tired, thinning or stressed skin.', ['30 min'], '<s>$900</s><b>$699</b>', 'r-tone.jpg', '50% 35%', '22% off')]),
  ('tone', 'Spots &amp; Redness', 'Even out sun spots, redness and dull tone.', [
   ('M22™ Photofacial', 'Intense pulsed light that targets sun spots, redness and uneven tone. Best as a monthly series.', ['30 min', 'Monthly series'], '<b>Consult</b>', 'r-care2.jpg', '50% 55%')]),
  ('pores', 'Pores, Acne &amp; Scars', 'Refine pores and smooth texture and acne scars.', [
   ('Gold RF Microneedling', 'Microneedling with radiofrequency for pores, texture, acne scars and tone in one treatment.', ['60–90 min', '2–3 days of redness'], '<s>$999</s><b>$799</b>', 'r-lift.jpg', '50% 45%', '20% off')]),
  ('facials', 'Facials', 'Regular deep cleansing, hydration and repair.', [
   ('HydraFacial® Deluxe', 'Cleanse, extract and hydrate in one relaxing hour.', ['60 min', '4 for $980'], '<b>$285</b>', 'r-care2.jpg', '50% 55%'),
   ('HydraFacial® Platinum', 'Everything in Deluxe, plus lymphatic drainage and targeted boosters.', ['75 min', '4 for $1,199'], '<b>$329</b>', 'about.jpg', '50% 25%'),
   ('Signature Facial', 'Our relaxing, restorative house facial.', ['60 min', '4 for $819'], '<b>$229</b>', 'r-tone.jpg', '50% 35%'),
   ('Barrier Recovery Facial', 'Calms and repairs sensitive or post-laser skin.', ['60 min', '4 for $819'], '<b>$229</b>', 'svc-laser.jpg', '50% 30%')]),
  ('sensitive', 'Sensitive Skin', 'Redness or stinging? We repair the barrier first, then treat.', [
   ('Gold Skin Analysis', 'A provider maps hydration, tone, texture and sensitivity before any treatment.', ['20 min'], '<b>Free</b>', 'about-reception.jpg', '50% 50%', 'Free', 'gold-skin-analysis.html'),
   ('Repair-First Plan', 'Barrier Recovery Facials to calm and rebuild, then gentle brightening.', ['Planned at consultation'], F + '<b>$229</b>', 'r-care2.jpg', '50% 55%')])],
 ('Get a <em>free</em> skin analysis', 'We’ll check hydration, tone and texture, then build your plan.', 'Book an Appointment'))

# ---------- BODY SHAPE ----------
colpage('body-shape.html', 'Body Shape · AURA Institute', 'Body Shape', 'Body <em>Shape</em>',
 'Contour, smooth and refine, from waistline to shoulder line. Every body plan starts with a free consultation.',
 [('all', 'Body Treatments', 'Planned around proportion, not just inches.', [
   ('Body Sculpt', 'Non-invasive fat reduction for stubborn areas. No needles, no downtime, back to your day in 30 minutes.', ['30 min', 'No downtime', 'Series of 4'], '<b>$300</b> 4 for $999', 's-body.jpg', '45% 50%', '', 'body-sculpt.html'),
   ('Stretch Mark Repair', 'Two steps: Gold RF Microneedling breaks up scar tissue, then Sculptra® helps rebuild collagen.', ['Planned at consultation'], '<b>Consult</b>', 'r-body.jpg'),
   ('Trap Tox · Shoulder Line', 'Relaxes the trapezius for a longer neck and a softer shoulder line.', ['15 min', 'No downtime'], '<b>By units</b>', 'r-lift.jpg', '50% 45%'),
   ('Neck &amp; Jawline Sculpt', 'Firms the neck and defines the jawline, planned as one line from jaw to shoulder.', ['Planned at consultation'], '<b>Consult</b>', 'svc-lift.jpg', '40% 30%')])],
 ('Plan your body <em>goals</em>', 'Body treatments are planned at a free consultation.', 'Book an Appointment'))

# ---------- WELLNESS ----------
colpage('wellness.html', 'Wellness · AURA Institute', 'Wellness', 'Well<em>ness</em>',
 'Energy, recovery and a calmer mind, right in Midtown. Glow Girl members earn credits toward NAD+ every month.',
 [('all', 'Wellness Treatments', 'Supervised by licensed providers.', [
   ('NAD+ IV Drip', 'A slow, supervised IV infusion of NAD+. Relax in our private lounge during your drip.', ['60–90 min', 'Health screening included'], F + '<b>$400</b>', 'svc-skin.jpg', '50% 40%', '', 'nad-iv.html'),
   ('EXOMIND™', 'A calm, non-invasive seated session designed to support mood and mental wellbeing.', ['30 min', 'No downtime', '6 for $3,000'], '<s>$550</s><b>$399</b>', 'svc-laser.jpg', '50% 30%', '27% off')])],
 ('Book your <em>reset</em>', 'Your first visit includes a health screening.', 'Book an Appointment'))

# ---------- MEMBERSHIP ----------
colpage('membership.html', 'Membership · AURA Institute', 'Membership', 'Member<em>ship</em>',
 'Make great skin a habit with a monthly membership, or prepay for credit and year-round perks.',
 [('all', 'Memberships', 'Choose monthly or prepaid.', [
   ('Glow Girl Membership', 'One facial every month, a glow treatment every quarter, and 50 Wellness Credits toward NAD+.', ['Monthly', '3-month minimum'], '<b>$299 / month</b>', 's-inject.jpg', '45% 40%', '', 'glow-girl.html', 'Join'),
   ('Aura VIP Gold', 'Prepay $5,000 and receive $800 bonus credit, a quarterly facial and unlimited skin analysis.', ['Prepaid', '+$800 credit'], '<b>$5,000</b>', 's-body.jpg', '45% 50%', '', '#', 'Join'),
   ('Aura VIP Black', 'Prepay $10,000 and receive $1,500 bonus credit, two facials each quarter and a quarterly plan review.', ['Prepaid', '+$1,500 credit'], '<b>$10,000</b>', 'about-reception.jpg', '50% 50%', '', '#', 'Join')])],
 ('Join the AURA <em>family</em>', 'Questions about membership? Ask us at the front desk or by text.', 'Book a Visit'), consult=False)

# ---------- ABOUT ----------
colpage('about.html', 'About · AURA Institute', 'About', 'About <em>AURA</em>',
 'Medical aesthetics and wellness at Rockefeller Center, built on science, design and care.',
 [('all', 'Get to know us', '', [
   ('Our Story', 'Why we built a medical aesthetics clinic around design, not discounts.', ['Founder story'], '', 'about-reception.jpg', '50% 50%', '', 'our-story.html', 'Visit'),
   ('Our Approach', 'Understand, analyze, explain, plan. How every treatment plan is made.', ['4 steps'], '', 'r-texture.jpg', '50% 40%', '', '#', 'Visit'),
   ('Our Providers', 'Licensed MDs, NPs and RNs, each with their own focus.', ['Meet the team'], '', 'about.jpg', '50% 25%', '', '#', 'Visit'),
   ('The Clinic', 'A calm, private space steps from Rockefeller Center.', ['Private treatment rooms'], '', 'svc-skin.jpg', '50% 40%', '', '#', 'Visit'),
   ('Reviews', 'What our clients say, from real Google reviews.', ['[4.9] ★ · [XXX] reviews'], '', 'r-care2.jpg', '50% 55%', '', '#', 'Visit')])],
 ('Come say <em>hello</em>', 'Book a complimentary Gold Skin Analysis and see the clinic.', 'Book Now'), consult=False)

# ---------- JOURNAL & FAQ ----------
colpage('journal-faq.html', 'Journal & FAQ · AURA Institute', 'Journal &amp; FAQ', 'Journal &amp; <em>FAQ</em>',
 'Honest, simple answers about treatments, skin care and what to expect. Every article is reviewed by a provider.',
 [('edu', 'Skin Education', 'Articles reviewed by our providers.', [
   ('Botox® vs Xeomin®: what’s the difference?', 'Both are FDA-approved wrinkle relaxers. Here is what our providers tell clients in consultation.', ['5 min read', 'Injectables'], '', 'r-texture.jpg', '50% 40%', '', 'journal-botox-vs-xeomin.html', 'Read'),
   ('Skin booster vs filler', 'Glow or volume? How to tell which one you need.', ['4 min read', 'Boosters'], '', 'about.jpg', '50% 25%', '', '#', 'Read'),
   ('Why skin loosens', 'The aging cascade, from bone to surface, and what each treatment addresses.', ['6 min read', 'Lifting'], '', 'r-lift.jpg', '50% 45%', '', '#', 'Read'),
   ('Winter skin reset', 'Repair first, then treat. A simple plan for dry, reactive winter skin.', ['3 min read', 'Skin care'], '', 'r-care2.jpg', '50% 55%', '', '#', 'Read')]),
  ('faq', 'FAQ &amp; Contact', '', [
   ('Frequently Asked Questions', 'Free consultation, who performs treatments, lunch-break visits, products and cancellation policy.', ['12 questions'], '', 'about-reception.jpg', '50% 50%', '', '#', 'Open'),
   ('Contact &amp; Visit', 'Address, phone, text, hours and directions from Rockefeller Center.', ['Map &amp; hours'], '', 'svc-skin.jpg', '50% 40%', '', '#', 'Open')])],
 ('Still have a <em>question</em>?', 'Text us anytime or book a free consultation.', 'Book Now'), consult=False)
print('done')
