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
    html = HEAD.format(title=title) + gen.nav(fn) + f'<main><div class="wrap crumbs"><a href="index.html">Home</a> / {crumbs}</div>' + body + '</main><footer>AURA Institute · 630 Fifth Avenue, Suite 1812, New York, NY 10111 · Results vary by individual.</footer></body></html>'
    open(f'{OUT}/{fn}', 'w').write(html)

F = 'From '
# ======================= v4 · structure from the Nov 2 meeting =======================
# placeholder tags start with "!"  -> rendered dashed, rust (content still to come)
_row = row
def row(name, ex, tags, price, img, pos='50% 40%', sale='', link='#', btn='Book'):
    h = _row(name, ex, [t.lstrip('!') for t in tags], price, img, pos, sale, link, btn)
    for t in tags:
        if t.startswith('!'):
            h = h.replace(f'<span>{t[1:]}</span>', f'<span class="tbd">{t[1:]}</span>')
    return h
open(OUT + '/col.css', 'a').write('.row .tg span.tbd{border-style:dashed;border-color:var(--rust);color:var(--rust)}.grp2{scroll-margin-top:140px}.tbdnote{border:1px dashed var(--rust);color:var(--rust);padding:14px 18px;font-size:14px;margin-top:18px}')
PEND = '!Details to come'

# ---------- FACE DESIGN ----------
colpage('face-design.html', 'Face Design · AURA Institute', 'Face Design', 'Not a new face. <em>Your best one.</em>',
 'We don’t change your face. We keep your natural beauty and bring out a better version of you: lifting, restoring and refining, planned around your own features.',
 [('lift', 'Lift &amp; Tighten', 'Firmer skin and a lifted look, without surgery or downtime.', [
   ('Thermage® FLX', 'Radiofrequency tightening for hooded lids and crepey skin around the eyes, or for the full face. One session, with results that build over months.', ['Eyes · 450 pulses', 'Full face · 900 pulses', 'No downtime'], '', 'r-lift.jpg', '50% 45%'),
   ('EMFACE®', 'Needle-free lift for brows, cheeks and jawline. Tones the muscles and tightens the skin at the same time.', ['20 min', '1–4 areas', 'No downtime'], '', 'svc-lift.jpg', '40% 30%', '', 'emface.html'),
   ('Exion™ Collagen Lift', 'Radiofrequency and targeted ultrasound boost your skin’s own collagen and hyaluronic acid, for firmer, smoother skin. Choose one area, or any three planned together.', ['Cheeks', 'Eyes', 'Neck', 'Forehead', 'Any 3 areas', '4-session plan'], '', 'svc-skin.jpg', '50% 40%')]),
  ('balancing', 'Restore &amp; Fill', 'Restore softness and structure where it has faded, in balance with your own features.', [
   ('Chin &amp; Lower Face Balance', 'Chin projection and length, planned to balance your profile and lower face.', ['30–45 min', 'Filler', 'Natural finish'], '', 'r-smooth.jpg', '50% 35%'),
   ('Defined Jawline', 'A cleaner line from chin to ear, for definition that still looks like you.', ['30–45 min', 'HA filler or RADIESSE®'], '', 'r-lift.jpg', '50% 45%'),
   ('Under-Eye Hollows', 'Softens hollows and shadows under the eyes for a more rested look. For dark circles, see Under-Eye Brightening in Skin &amp; Glow.', ['30 min', 'Conservative approach'], '', 'r-texture.jpg', '50% 40%'),
   ('Temples', 'Restores soft fullness at the temples, so the upper face looks smooth and youthful.', ['30 min'], '', 'about.jpg', '50% 25%'),
   ('Lip Volume &amp; Shape', 'Volume, shape or both. We design to your natural lip proportions.', ['30 min', '1–3 days of swelling'], '', 'r-tone.jpg', '50% 55%'),
   ('Nose Profile', 'Subtle refinement of the nose bridge and columella for a smoother profile.', ['30 min', 'Non-surgical'], '', 's-skin2.jpg', '50% 40%'),
   ('Sculptra®', 'Gradual collagen restoration for cheek volume and fine cheek lines, developing naturally over a few months.', ['30–45 min', 'Series of 2–3'], '', 'r-tone.jpg', '50% 35%'),
   ('RADIESSE®', 'A collagen-stimulating filler that adds structure along the jaw and cheekbones. Also used to restore volume in the hands.', ['30–45 min', 'Jaw · Cheekbones · Hands', 'Lasts 12+ months'], '', 'r-lift.jpg', '50% 45%')]),
  ('lines', 'Smooth &amp; Relax', 'Soften lines and tension while keeping your expressions.', [
   ('Botox® &amp; Xeomin®', 'Forehead lines, frown lines and crow’s feet. Your provider maps your muscles and chooses the product and dose for you.', ['10–20 min', 'No downtime', 'Lasts 3–4 months'], '', 'r-texture.jpg', '50% 40%', '', 'botox-xeomin.html'),
   ('Brow Lift', 'A soft lift at the tail of the brow for a more open, rested eye.', ['10 min', 'No downtime'], '', 'svc-lift.jpg', '40% 30%')]),
  ('vline', 'V-Line &amp; Contour', 'A slimmer, more defined lower face.', [
   ('Masseter · Jaw Slimming', 'Relaxes jaw tension and clenching, and softens a square lower face.', ['15 min', 'No downtime'], '', 'about.jpg', '50% 25%'),
   ('Double Chin · KYBELLA®', 'An FDA-approved injectable that permanently destroys fat cells under the chin, for a more defined profile.', ['15–20 min', 'Series of 2–4', 'Swelling for a few days'], '', 'r-lift.jpg', '50% 45%'),
   ('Facial Harmonization', 'Contouring injections on one side of the face to bring both sides into balance.', ['One side', '!Product name to confirm'], '', 'r-smooth.jpg', '50% 35%'),
   ('Lower Face Tightening + Lift', 'Contouring injections on both sides to slim and define the lower face, with a lift.', ['Both sides', '!Product name to confirm'], '', 's-skin2.jpg', '50% 40%')])],
 ('Not a new face. A better version of <em>yourself</em>.', 'Book a complimentary Face Design Consultation. We’ll map your whole face, then build a written plan that stays true to you.', 'Book a Consultation'))

FD_CSS = """
.fm{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:56px;align-items:center;padding-block:48px 8px}
@media(max-width:860px){.fm{grid-template-columns:1fr;gap:28px}}
.fm .fig{position:relative;aspect-ratio:3/4;overflow:hidden;background:var(--surface)}.fm .fig img{width:100%;height:100%;object-fit:cover;display:block}
.fm .fig svg{position:absolute;inset:0;width:100%;height:100%}
.fm .fig .lb{position:absolute;font-size:12px;letter-spacing:.06em;background:rgba(252,250,247,.92);color:#3F3029;padding:4px 9px;white-space:nowrap;transform:translate(-50%,-50%)}
.fm .fig .lb i{font-style:normal;font-weight:600;margin-right:6px}
.fm h2{font-family:var(--serif);font-size:clamp(34px,4vw,52px);line-height:1.05;margin:10px 0 16px}.fm .lede2{font-size:18px;color:var(--muted);margin:0 0 22px}
.fm ol{list-style:none;margin:0;padding:0}.fm ol li{display:grid;grid-template-columns:36px 1fr;gap:12px;padding:14px 0;border-top:1px solid var(--line)}
.fm ol li b{font-weight:600;font-size:13px;color:var(--rust)}.fm ol li strong{display:block;font-weight:500}.fm ol li span{color:var(--muted);font-size:15px}
.prin{margin-top:56px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
@media(max-width:860px){.prin{grid-template-columns:1fr}}
.prin div{background:var(--card);padding:30px 28px}.prin h3{font-family:var(--serif);font-size:28px;margin:8px 0}.prin p{margin:0;color:var(--muted);font-size:15px}
.no2{margin-top:56px;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:48px;background:var(--accent);color:var(--on-accent);padding:44px}
@media(max-width:860px){.no2{grid-template-columns:1fr;padding:30px 22px;gap:20px}}
.no2 .eyebrow{color:inherit;opacity:.7}.no2 h2{font-family:var(--serif);font-size:clamp(32px,3.6vw,46px);line-height:1.05;margin:10px 0 12px}.no2 p{margin:0;opacity:.8}
.no2 ul{list-style:none;margin:0;padding:0}.no2 li{padding:14px 0;border-top:1px solid rgba(247,243,238,.22);display:grid;grid-template-columns:28px 1fr;gap:10px}.no2 li:first-child{border-top:0}
.no2 li b{opacity:.6;font-weight:500}
.fv{margin-top:56px}.fv>h2{font-family:var(--serif);font-size:34px;margin:0 0 4px}.fv>p{color:var(--muted);margin:0 0 20px}
.fv .st{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}@media(max-width:860px){.fv .st{grid-template-columns:1fr 1fr}}@media(max-width:520px){.fv .st{grid-template-columns:1fr}}
.fv .st div{border-top:2px solid var(--accent);padding-top:14px}.fv .st i{font-style:normal;font-size:12px;letter-spacing:.16em;color:var(--muted)}.fv .st h4{font-size:18px;font-weight:500;margin:6px 0}.fv .st p{margin:0;color:var(--muted);font-size:15px}
.fv .meet{margin-top:28px;display:grid;grid-template-columns:120px 1fr auto;gap:24px;align-items:center;border:1px solid var(--line);background:var(--card);padding:20px}
@media(max-width:700px){.fv .meet{grid-template-columns:80px 1fr}.fv .meet .btn{grid-column:1/-1}}
.fv .meet img{width:100%;aspect-ratio:1;object-fit:cover}.fv .meet h4{margin:0 0 4px;font-size:20px;font-weight:500}.fv .meet p{margin:0;color:var(--muted);font-size:15px}
"""
open(OUT + '/col.css', 'a').write(FD_CSS)

# guide lines and labels, in percent of the portrait (r-tone.jpg)
GY = [5, 21, 46, 74]; GX = None
LB = [(12, 13, '1', 'Upper'), (12, 33, '2', 'Middle'), (12, 60, '3', 'Lower'), (34, 24, '', 'Temples'), (60, 37, '', 'Under-eye'), (88, 55, '', 'Lips'), (82, 80, '', 'Chin projection'), (38, 70, '', 'Jawline')]
lines = ''.join(f'<line x1="4" y1="{y*1.333:.1f}" x2="96" y2="{y*1.333:.1f}"/>' for y in GY)
svg = '<svg viewBox="0 0 100 133.3" preserveAspectRatio="none" aria-hidden="true"><g fill="none" stroke="#FCFAF7" stroke-width=".35" stroke-dasharray="1.6 1.2">' + lines + '</g></svg>'
labs = ''.join(f'<span class="lb" style="left:{x}%;top:{y}%">' + (f'<i>{n}</i>' if n else '') + f'{t}</span>' for x, y, n, t in LB)
FM = ('<div class="wrap"><div class="fm"><div class="fig"><img src="r-tone.jpg" alt="Front-facing portrait with dotted guide lines marking the upper, middle and lower face">' + svg + labs + '</div>'
 '<div><p class="eyebrow">Face Mapping</p><h2>We see your <em>whole face</em> first.</h2><p class="lede2">The concern may not be one feature. Often it is overall proportion. So before we treat anything, we map how your features work together.</p>'
 '<ol><li><b>01</b><div><strong>Balance across the thirds</strong><span>Upper, middle and lower face, and how they relate.</span></div></li>'
 '<li><b>02</b><div><strong>Profile and projection</strong><span>Brow, nose, lips and chin, seen from the side.</span></div></li>'
 '<li><b>03</b><div><strong>Light and shadow</strong><span>Temples, under-eyes and cheeks, where volume changes first.</span></div></li>'
 '<li><b>04</b><div><strong>Movement</strong><span>How your face moves when you talk, smile and frown.</span></div></li></ol></div></div></div>')
PRIN = ('<div class="prin"><div><p class="eyebrow">01</p><h3>You, <em>refined</em></h3><p>We don’t design you to look like someone else. We design to your own features, so you look like yourself on your best day.</p></div>'
 '<div><p class="eyebrow">02</p><h3>Precision <em>over</em> perfection</h3><p>Small, precise changes in the right places, rather than more product. Balance matters more than any single feature.</p></div>'
 '<div><p class="eyebrow">03</p><h3>An eye for <em>balance</em></h3><p>An Eastern-trained eye for proportion, applied to your own face. [The AURA aesthetic method and lead injector Star’s approach. Materials to come.]</p></div></div>')
NO = ('<div class="no2"><div><p class="eyebrow">Honest advice</p><h2>When we’ll tell you <em>no</em></h2><p>A good plan is as much about what we leave out. Your provider will tell you when a treatment isn’t right for you.</p></div>'
 '<ul><li><b>01</b><span>If it would change how you look, rather than refine it.</span></li><li><b>02</b><span>If you don’t need it yet. Starting early is not always better.</span></li><li><b>03</b><span>If another treatment would do the job better, or with less.</span></li><li><b>04</b><span>If a health condition, pregnancy or a recent treatment means it’s safer to wait.</span></li><li><b>05</b><span>If adding more would make the result look overdone.</span></li></ul></div>')
FV = ('<div class="fv"><h2>Your first <em>visit</em></h2><p>About 30 minutes. No pressure to book a treatment.</p>'
 '<div class="st"><div><i>STEP 1</i><h4>Talk</h4><p>What you’d like to change, and what you want to keep.</p></div><div><i>STEP 2</i><h4>Map</h4><p>A full-face assessment and Gold Skin Analysis.</p></div><div><i>STEP 3</i><h4>Plan</h4><p>A written plan with options, timing and a clear quote.</p></div><div><i>STEP 4</i><h4>Decide</h4><p>Start the same day, or take the plan home and think it over.</p></div></div>'
 '<div class="meet"><img src="s-inject.jpg" alt="" style="object-position:45% 40%"><div><h4>Meet your injector</h4><p>[Star · Lead Injector. Credentials, approach and Instagram link to come.]</p></div><a class="btn" href="#book">Book a Consultation</a></div></div>')
_p = OUT + '/face-design.html'; _h = open(_p).read()
_h = _h.replace('</div></div></div><div class="chips2">', '</div></div></div>' + FM + '<div class="chips2">', 1)
_h = _h.replace('</div></section><section class="cta"', PRIN + NO + FV + '</div></section><section class="cta"', 1)
open(_p, 'w').write(_h)

# ---------- SKIN & GLOW ----------
colpage('skin-glow.html', 'Skin & Glow · AURA Institute', 'Skin &amp; Glow', 'Skin &amp; <em>Glow</em>',
 'Clear, bright, hydrated skin, from face to neck to scalp. Every treatment is grouped by what it does and where it works. Not sure where to start? Begin with a Gold Skin Analysis.',
 [('start', 'Start Here', 'Know your skin before you treat it.', [
   ('Gold Skin Analysis', 'A provider maps hydration, tone, texture and sensitivity layer by layer, then recommends a plan. No obligation to book.', ['20 min', 'Complimentary', 'New clients'], '', 'about-reception.jpg', '50% 50%', '', 'gold-skin-analysis.html')]),
  ('cleanse', 'Deep Cleanse', 'Regular cleansing, extraction and hydration for clear, calm skin.', [
   ('HydraFacial®', 'Cleanse, extract and hydrate in one relaxing hour, the monthly reset for congested skin and clogged pores. Choose Deluxe, or Platinum with added lymphatic drainage and targeted boosters.', ['Deluxe · 60 min', 'Platinum · 75 min', 'Monthly'], '', 'r-care2.jpg', '50% 55%'),
   ('Signature Facial', 'Our relaxing, restorative spa facial for everyday skin care.', ['60 min'], '', 'r-tone.jpg', '50% 35%'),
   ('Barrier Recovery Facial', 'Calms and repairs sensitive, reactive or post-treatment skin.', ['60 min', 'Sensitive skin'], '', 'svc-laser.jpg', '50% 30%')]),
  ('tone', 'Brighten &amp; Even Tone', 'Fade sun spots and redness for brighter, more even skin.', [
   ('BBL™ Photofacial', 'Broadband light that targets sun spots, redness and dull, uneven tone. Best as a series of 3, then maintained.', ['30 min', 'Series of 3'], '', 'r-care.jpg', '50% 45%')]),
  ('pores', 'Pores, Acne &amp; Texture', 'Refine pores and smooth texture and acne scars.', [
   ('Gold RF Microneedling', 'Microneedling with radiofrequency, using the mFace system, for enlarged pores, rough texture, acne scars and tone in one treatment.', ['60–90 min', 'Series of 3', '2–3 days of redness'], '', 'r-lift.jpg', '50% 45%')]),
  ('hydrate', 'Hydrate &amp; Glow · Face', 'Deep hydration delivered into the skin, planned by area.', [
   ('Face Hydration · Rejuran®', 'Deep hydration and renewal for the full face, for smoother texture and a dewy glow. The amount is planned to your face, including larger face areas.', ['30 min', 'Series of 3', 'Skin test first', '!Copy pending compliance review'], '', 'about.jpg', '50% 25%', '', 'glow-booster.html'),
   ('Long-Lasting Glow · SKINVIVE™', 'A hyaluronic acid microdroplet treatment that improves cheek skin smoothness, with results that last about 6 months. For adults 21+.', ['30 min', 'One session', 'About 6 months'], '', 's-skin2.jpg', '50% 40%'),
   ('Under-Eye Brightening · PRP / PRF', 'Uses your own platelet-rich plasma, prepared from a small blood draw, to refresh dark, tired-looking under-eyes. For hollows rather than dark circles, see <a href="face-design.html#balancing">Under-Eye Hollows</a> in Face Design.', ['45–60 min', 'Includes blood draw'], '', 'r-texture.jpg', '50% 40%')]),
  ('neck', 'Neck', 'Smoother skin and softer lines on the neck.', [
   ('Neck Hydration', 'Hydration for crepey, dry neck skin and fine early lines.', ['30 min'], '', 'svc-lift.jpg', '40% 30%'),
   ('Tech Neck Treatment · Levels 1–4', 'Four levels, matched to your neck lines: from fine early lines at Level 1 to deeper, set-in lines at Level 4. Your provider confirms your level at consultation.', ['Level 1–4', '!Level descriptions to come'], '', 'r-body2.jpg', '50% 35%')]),
  ('scalp', 'Scalp &amp; Hair', 'Support a healthier scalp and fuller-looking hair.', [
   ('Scalp &amp; Hair Restoration', 'Two options, planned to your scalp: a hydrating scalp treatment for a healthy scalp, or PRP made from your own platelet-rich plasma to support thinning hair.', ['Hydration · 30 min', 'PRP · includes blood draw', 'Series'], '', 'r-care2.jpg', '50% 55%')])],
 ('Start with a <em>Gold Skin Analysis</em>', 'We’ll check hydration, tone and texture, then build your plan.', 'Book a Consultation'))

# ---------- WELLNESS & LONGEVITY ----------
colpage('wellness.html', 'Wellness & Longevity · AURA Institute', 'Wellness &amp; Longevity', 'Wellness &amp; <em>Longevity</em>',
 'Beauty that starts from within. Energy, recovery, sleep and focus, with treatments that support how you feel as much as how you look.',
 [('energy', 'Energy &amp; Recovery', 'Restore and recharge.', [
   ('NAD+ IV Drip', 'A slow, supervised IV infusion of NAD+. Relax in our private lounge during your drip. Your provider recommends the dose after a health screening.', ['250 mg or 500 mg', '60–90+ min', 'Series of 6'], '', 'svc-skin.jpg', '50% 40%', '', 'nad-iv.html')]),
  ('mind', 'Sleep, Mood &amp; Focus', 'A calmer mind and better rest.', [
   ('EXOMIND™', 'A calm, non-invasive seated session designed to support mood, sleep and focus.', ['30 min', 'No downtime', 'Series of 6'], '', 'svc-laser.jpg', '50% 30%')]),
  ('more', 'Coming Soon', 'Our longevity menu is growing.', [
   ('[New longevity treatments]', '[Placeholder for future wellness and longevity services. Add only after compliance review.]', [PEND], '', 'about-reception.jpg', '50% 50%')])],
 ('Book your <em>reset</em>', 'Your first visit includes a health screening.', 'Book a Consultation'))

# ---------- BODY ----------
colpage('body-shape.html', 'Body · AURA Institute', 'Body', '<em>Body</em>',
 'Contour, smooth and refine, from shoulder line to waistline. Every body plan starts with a complimentary consultation.',
 [('shape', 'Contour &amp; Shape', 'Planned around proportion, not just inches.', [
   ('Body Sculpt · Abdomen', 'Non-invasive fat reduction for the stubborn belly area. No needles, no downtime, back to your day in 30 minutes.', ['30 min', 'No downtime', 'Series of 4'], '', 's-body.jpg', '45% 50%', '', 'body-sculpt.html'),
   ('Fat Dissolving · Body', 'Injections that break down stubborn fat in one small area at a time, planned at consultation.', ['One area per session', '!Product &amp; compliance to confirm'], '', 'r-body.jpg', '50% 40%'),
   ('[New body device]', '[Placeholder: body contouring device to be added. Name and details to confirm.]', [PEND], '', 'r-body2.jpg', '50% 35%')]),
  ('line', 'Shoulder Line', 'A longer, softer line from neck to shoulder.', [
   ('Trap Tox · Shoulder Line', 'Relaxes the trapezius for a longer neck and a softer shoulder line.', ['15 min', 'No downtime'], '', 'r-lift.jpg', '50% 45%')]),
  ('skin', 'Body Skin', 'Smoother, more even skin on the body.', [
   ('Stretch Mark Repair', 'Two steps: Gold RF Microneedling breaks up scar tissue, then Sculptra® helps rebuild collagen.', ['Planned at consultation'], '', 'r-body.jpg')])],
 ('Plan your body <em>goals</em>', 'Body treatments are planned at a complimentary consultation.', 'Book a Consultation'))

# ---------- ABOUT ----------
colpage('about.html', 'About · AURA Institute', 'About', 'About <em>AURA</em>',
 'Look better, feel more confident. Medical aesthetics and wellness at 630 Fifth Avenue, built around a refined aesthetic and care from within.',
 [('all', 'Get to know us', '', [
   ('The AURA Aesthetic', 'Our Eastern-inspired eye for proportion and balance, and how we design a plan for your whole face.', ['!Materials to come'], '', 'r-texture.jpg', '50% 40%', '', 'face-design.html', 'Visit'),
   ('Our Team', 'Licensed aesthetic providers, led by our injector [Star]. Every treatment is performed by a licensed professional.', ['!Bios to come'], '', 'about.jpg', '50% 25%', '', '#', 'Visit'),
   ('The Clinic', 'A calm, private suite at 630 Fifth Avenue, inside Rockefeller Center.', ['Suite 1812', 'Private treatment rooms'], '', 'svc-skin.jpg', '50% 40%', '', '#', 'Visit'),
   ('Reviews', 'What our clients say, from real Google reviews.', ['!Available after opening'], '', 'r-care2.jpg', '50% 55%', '', '#', 'Visit')])],
 ('Come say <em>hello</em>', 'Book a complimentary Gold Skin Analysis and see the clinic.', 'Book a Consultation'), consult=False)

# ---------- JOURNAL & FAQ ----------
colpage('journal-faq.html', 'Journal & FAQ · AURA Institute', 'Journal &amp; FAQ', 'Journal &amp; <em>FAQ</em>',
 'Honest, simple answers about treatments, skin care and what to expect. Written by the AURA team.',
 [('edu', 'Skin Education', 'Simple guides to treatments and skin care.', [
   ('Botox® vs Xeomin®: what’s the difference?', 'Both are FDA-approved wrinkle relaxers. Here is what our providers tell clients in consultation.', ['5 min read', 'Injectables'], '', 'r-texture.jpg', '50% 40%', '', 'journal-botox-vs-xeomin.html', 'Read'),
   ('Hydration vs filler', 'Glow or volume? How to tell which one you need.', ['4 min read', 'Skin care'], '', 'about.jpg', '50% 25%', '', '#', 'Read'),
   ('Why skin loosens', 'The aging cascade, from bone to surface, and what each treatment addresses.', ['6 min read', 'Lifting'], '', 'r-lift.jpg', '50% 45%', '', '#', 'Read'),
   ('Winter skin reset', 'Repair first, then treat. A simple plan for dry, reactive winter skin.', ['3 min read', 'Skin care'], '', 'r-care2.jpg', '50% 55%', '', '#', 'Read')]),
  ('faq', 'FAQ &amp; Contact', '', [
   ('Frequently Asked Questions', 'Complimentary consultation, lunch-break visits, booking and cancellation policy.', ['12 questions'], '', 'about-reception.jpg', '50% 50%', '', '#', 'Open')])],
 ('Still have a <em>question</em>?', 'Text us anytime or book a complimentary consultation.', 'Book a Consultation'), consult=False)


# ---------- cleanup + site-wide relink ----------
import os, glob, re as _re
for f in ['face-contour.html','special-offers.html','lift-tighten.html','membership.html','glow-girl.html','lift-renew.html','seasonal-programs.html','our-story.html']:
    p = OUT + '/' + f
    if os.path.exists(p): os.remove(p)
LINKS = [('lift-renew.html','face-design.html'),('seasonal-programs.html','skin-glow.html'),('our-story.html','about.html'),('glow-girl.html','aura-prime.html'),('membership.html','aura-prime.html'),('face-contour.html','face-design.html'),('special-offers.html','skin-glow.html'),('lift-tighten.html','face-design.html')]
for p in glob.glob(OUT + '/*.html'):
    s2 = open(p).read(); o = s2
    for a, b in LINKS: s2 = s2.replace(a, b)
    s2 = s2.replace('<a href="face-design.html">Face &amp; Contour</a> / <a href="lift-renew.html">Lift &amp; Tighten</a>', '<a href="lift-renew.html">Lift &amp; Renew</a>')
    s2 = s2.replace('>Lift &amp; Renew</a>', '>Face Design</a>').replace('>Seasonal Programs</a>', '>Skin &amp; Glow</a>')
    s2 = s2.replace('>Face &amp; Contour</a>', '>Face Design</a>').replace('>Body Shape</a>', '>Body</a>').replace('>Special Offers</a>', '>Skin &amp; Glow</a>')
    # static sample pages (emface) carry their own nav list: swap for the current one
    m = _re.search(r'<header class="nav">.*?<ul>(.*?)</ul>', s2, _re.S)
    if m and 'face-design.html">Face Design</a></li><li><a' not in m.group(1)[:200]:
        act = _re.search(r'class="on" href="([^"]+)"', m.group(1))
        act = act.group(1) if act else ''
        if os.path.basename(p) == 'emface.html': act = 'face-design.html'
        lis = ''.join(f'<li><a href="{h}"{" class=\"on\"" if h==act else ""}>{n}</a></li>' for h,n in gen.NAV)
        s2 = s2[:m.start(1)] + lis + s2[m.end(1):]
    if s2 != o: open(p, 'w').write(s2)
print('done v4')
