CSS = r'''
.pd{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:56px;padding-block:22px 64px;align-items:start}
@media(max-width:900px){.pd{grid-template-columns:1fr;gap:28px}}
.gal .main{aspect-ratio:4/5;overflow:hidden;background:var(--surface)}.gal img{width:100%;height:100%;object-fit:cover;display:block}
.gal .th{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px}.gal .th div{aspect-ratio:1;overflow:hidden;background:var(--surface);opacity:.75}.gal .th div:first-child{opacity:1;outline:1px solid var(--fg)}
.info{display:grid;gap:18px;position:sticky;top:90px}
.info h1{font-family:var(--serif);font-size:clamp(40px,4.4vw,60px);line-height:1}
.info .lede{margin:0;color:var(--muted);font-size:17px}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips span{font-size:12px;letter-spacing:.06em;border:1px solid var(--line);padding:5px 11px;border-radius:999px;background:var(--card)}
.opt h4{margin:0 0 8px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:600}
.opt .pills{display:flex;flex-wrap:wrap;gap:8px}.opt .pills span{border:1px solid var(--line);padding:10px 14px;font-size:14px;background:var(--card)}.opt .pills .on{border-color:var(--fg);box-shadow:inset 0 0 0 1px var(--fg)}
.pr{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}.pr b{font-size:32px;font-weight:500}.pr s{color:var(--muted)}.pr .tag{font-size:11px;background:var(--rust);color:#fff;padding:3px 8px;letter-spacing:.08em;text-transform:uppercase}
.pr small{width:100%;color:var(--muted);font-size:13.5px}
.acts2{display:flex;gap:10px;flex-wrap:wrap}.acts2 .btn{flex:1;min-width:150px}.acts2 .wl{flex:0 0 auto;padding:14px 16px}
.facts{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line)}.facts div{padding:12px 0;border-bottom:1px solid var(--line);font-size:14px}.facts div:nth-child(odd){padding-right:16px}
.facts span{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.loc{font-size:13.5px;color:var(--muted)}
.why{background:var(--accent);color:var(--on-accent)}.why .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;padding-block:40px}
@media(max-width:760px){.why .wrap{grid-template-columns:1fr}}
.why h3{font-family:var(--serif);font-size:26px;margin-bottom:6px}.why p{margin:0;opacity:.8;font-size:14.5px}
.tabs{position:sticky;top:68px;z-index:20;background:var(--bg);border-bottom:1px solid var(--line)}.tabs .wrap{display:flex;gap:30px;overflow-x:auto}
.tabs a{padding:16px 0;font-size:12px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;white-space:nowrap;border-bottom:2px solid transparent}.tabs a.on{border-color:var(--fg)}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px}@media(max-width:860px){.two{grid-template-columns:1fr;gap:28px}}
.two p{color:var(--muted);margin:0 0 14px}
.areas{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
.area{background:var(--card);border:1px solid var(--line);padding:18px;display:grid;gap:6px}.area h4{margin:0;font-size:16px;font-weight:600}.area p{margin:0;font-size:13.5px;color:var(--muted)}.area b{font-size:13px;font-weight:500}
.reco{counter-reset:r;list-style:none;margin:0;padding:0;display:grid;gap:12px}.reco li{counter-increment:r;display:grid;grid-template-columns:36px 1fr;font-size:15px}.reco li::before{content:counter(r,decimal-leading-zero);font-family:var(--serif);font-size:22px;color:var(--rust);line-height:1}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}@media(max-width:900px){.steps{grid-template-columns:1fr 1fr}}
.step{border-top:2px solid var(--fg)!important}.step h4{margin:0;font-size:17px;font-weight:600}.step p{margin:0;font-size:14px;color:var(--muted)}
.tl{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:0;border-top:1px solid var(--line)}
.tl div{padding:22px 18px 6px 0;position:relative}.tl div::before{content:"";position:absolute;top:-6px;left:0;width:11px;height:11px;border-radius:50%;background:var(--rust)}
.tl b{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase}.tl p{margin:6px 0 0;font-size:14px;color:var(--muted)}
.ba{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}@media(max-width:760px){.ba{grid-template-columns:1fr}}
.ba div{display:grid;grid-template-columns:1fr 1fr;gap:4px}.ba span{aspect-ratio:3/4;background:repeating-linear-gradient(135deg,var(--surface) 0 10px,var(--line) 10px 11px);display:grid;place-items:end start;padding:8px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.ba small{grid-column:span 2;font-size:12.5px;color:var(--muted);padding-top:6px}
.tbl2{width:100%;border-collapse:collapse;font-size:15px}.tbl2 th,.tbl2 td{text-align:left;padding:14px 12px;border-bottom:1px solid var(--line);vertical-align:top}.tbl2 th{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600}.tbl2 td:first-child{font-weight:600}
.tbl2 .hi{color:var(--rust);font-weight:600}
.qa details{border-bottom:1px solid var(--line);padding:16px 0}.qa summary{cursor:pointer;font-size:17px;list-style:none;display:flex;justify-content:space-between;gap:16px}.qa summary::after{content:"+";font-size:22px;line-height:1}.qa details[open] summary::after{content:"–"}.qa p{margin:10px 0 0;color:var(--muted)}
.note2{font-size:13px;color:var(--muted);margin-top:14px}
.story{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:64px;align-items:center}@media(max-width:860px){.story{grid-template-columns:1fr;gap:28px}}
.story .ph{aspect-ratio:4/5;overflow:hidden}.story .ph img{width:100%;height:100%;object-fit:cover}
.quote{font-family:var(--serif);font-size:clamp(28px,3vw,40px);line-height:1.15;margin:0}
.nums{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;text-align:center}@media(max-width:760px){.nums{grid-template-columns:1fr 1fr}}
.nums b{display:block;font-family:var(--serif);font-size:48px;font-weight:400;line-height:1}.nums span{font-size:13px;color:var(--muted)}
.art{display:grid;grid-template-columns:220px minmax(0,680px);gap:64px;justify-content:center}@media(max-width:900px){.art{grid-template-columns:1fr}}
.toc{position:sticky;top:90px;align-self:start;font-size:14px;display:grid;gap:10px}.toc b{font-size:11px;letter-spacing:.14em;text-transform:uppercase}.toc a{text-decoration:none;color:var(--muted)}
.body h2{font-family:var(--serif);font-size:34px;margin:40px 0 12px}.body p{color:#463a33;font-size:17px;line-height:1.75}
.callout{background:var(--surface);padding:22px 26px;border-left:3px solid var(--rust);margin:24px 0}.callout b{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;margin-bottom:6px}
.byline{display:flex;gap:18px;flex-wrap:wrap;font-size:13.5px;color:var(--muted)}
.arthero{aspect-ratio:21/9;overflow:hidden;margin-top:28px}.arthero img{width:100%;height:100%;object-fit:cover}

.rate{margin:0;font-size:13.5px;color:var(--muted)}.rate b{color:var(--rust);letter-spacing:.1em;margin-right:4px}
.cart{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:var(--surface);padding:12px}
.cart .qty{display:inline-flex;align-items:center;border:1px solid var(--line);background:var(--card)}.cart .qty button{border:0;background:none;width:34px;height:38px;font-size:18px;color:var(--fg)}.cart .qty b{min-width:24px;text-align:center;font-weight:500}
.cart .sub{flex:1;font-size:14px}.cart .btn{padding:11px 16px}
.tech{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}@media(max-width:860px){.tech{grid-template-columns:1fr}}
.tech div{background:var(--card);border:1px solid var(--line);padding:22px;display:grid;gap:8px}.tech i{font-style:normal;font-family:var(--serif);font-size:40px;color:var(--rust);line-height:1}.tech h4{margin:0;font-size:18px;font-weight:600}.tech p{margin:0;color:var(--muted);font-size:14.5px}
.care h3{font-family:var(--serif);font-size:28px;margin-bottom:12px}.care ul{margin:0;padding:0;list-style:none;display:grid;gap:10px}.care li{padding-left:28px;position:relative;font-size:15px}.care li::before{content:"✓";position:absolute;left:0;color:var(--rust);font-weight:700}.care .no li::before{content:"✕"}
.stds{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}@media(max-width:860px){.stds{grid-template-columns:1fr}}
.stds div{border:1px solid var(--line);background:var(--card);padding:22px;display:grid;gap:6px}.stds b{width:34px;height:34px;border-radius:50%;background:var(--accent);color:var(--on-accent);display:grid;place-items:center}.stds h4{margin:0;font-size:17px;font-weight:600}.stds p{margin:0;font-size:14px;color:var(--muted)}


.tabsec{padding-block:48px 72px}
.ptabs{display:flex;gap:36px;justify-content:center;border-bottom:1px solid var(--line);overflow-x:auto;margin-bottom:8px}
.ptabs button{background:none;border:0;border-bottom:3px solid transparent;padding:16px 0 14px;font-size:17px;font-weight:600;color:var(--muted);white-space:nowrap}
.ptabs button.on{color:var(--fg);border-color:var(--fg)}
@media(max-width:760px){.ptabs{justify-content:flex-start;gap:22px}.ptabs button{font-size:14px}}
.panel[hidden]{display:none}
.blk{padding-top:44px}.blk+.blk{margin-top:12px;border-top:1px solid var(--line)}
.bh{font-family:var(--serif);font-size:clamp(28px,2.8vw,38px);line-height:1.1;margin:6px 0 10px}.bp{color:var(--muted);margin:0 0 22px;max-width:720px}
.h4{font-family:var(--serif);font-size:26px;font-weight:400;margin:0 0 14px}
.bookp{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:56px;padding-top:44px}@media(max-width:860px){.bookp{grid-template-columns:1fr}}
.ct{list-style:none;margin:0;padding:0;display:grid;gap:14px}.ct li{display:grid;grid-template-columns:70px 1fr;font-size:15px;border-bottom:1px solid var(--line);padding-bottom:12px}.ct b{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;padding-top:3px}
.bf{background:var(--card);border:1px solid var(--line);padding:28px;display:grid;gap:14px}
.bf label{display:grid;gap:6px;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.bf input,.bf select{font:inherit;font-size:15px;letter-spacing:0;text-transform:none;color:var(--fg);padding:11px 12px;border:1px solid var(--line);background:var(--bg)}
.bf .r2{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:560px){.bf .r2{grid-template-columns:1fr}}
.bf .ck{display:flex;gap:8px;align-items:center;text-transform:none;letter-spacing:0;font-size:14px;color:var(--fg)}.bf .ck input{width:auto}

.blk .tl{margin-top:26px}.blk .steps{margin-top:6px}


.ph3{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;padding-block:22px 56px;align-items:start}@media(max-width:900px){.ph3{grid-template-columns:1fr;gap:24px}}
.ph3 .im{aspect-ratio:1;overflow:hidden;background:var(--surface)}.ph3 .im img{width:100%;height:100%;object-fit:cover;display:block}
.ph3 .tx{display:grid;gap:16px}.ph3 h1{font-family:var(--serif);font-size:clamp(40px,4.4vw,60px);line-height:1}.ph3 .lede{margin:0;color:var(--muted);font-size:17px}
.ic{list-style:none;margin:0;padding:0;display:grid;gap:14px;border-top:1px solid var(--line);padding-top:16px}.ic li{display:grid;grid-template-columns:34px 1fr;gap:12px;font-size:14px;color:var(--muted)}
.ic b{width:30px;height:30px;border-radius:50%;background:var(--surface);display:grid;place-items:center;color:var(--fg);font-size:14px}.ic strong{display:block;color:var(--fg);font-weight:600;font-size:14.5px}
.cmpb{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:40px;align-items:start}@media(max-width:860px){.cmpb{grid-template-columns:1fr}}
.cmpb .ci{aspect-ratio:16/10;overflow:hidden}.cmpb .ci img{width:100%;height:100%;object-fit:cover}
.why5{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:14px 32px}@media(max-width:760px){.why5{grid-template-columns:1fr}}
.why5 li{border-bottom:1px solid var(--line);padding-bottom:14px;font-size:15px;color:var(--muted)}.why5 b{display:block;color:var(--fg);font-size:16px;margin-bottom:2px}
.ban{display:grid;grid-template-columns:1fr 1fr;align-items:stretch;padding:0}@media(max-width:860px){.ban{grid-template-columns:1fr}.ban.rev .im{order:-1}}
.ban .im{min-height:560px;overflow:hidden}.ban .im img{width:100%;height:100%;object-fit:cover;display:block}
.ban .tx{padding:72px max(48px,6vw);display:grid;gap:14px;align-content:center}
.bh2{font-family:var(--serif);font-size:clamp(32px,3.4vw,46px);line-height:1.05;margin:4px 0}
.ban p{margin:0;color:var(--muted)}.num{margin:8px 0 0;padding-left:22px;display:grid;gap:12px;font-size:15px}.num b{font-weight:600}
.chk{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:12px}.chk li{padding-left:30px;position:relative;font-size:16px}.chk li::before{content:"✓";position:absolute;left:0;color:var(--rust);font-weight:700}
#expect .care{margin-top:40px}
.faqc{max-width:860px}
.bas{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;align-items:center}@media(max-width:860px){.bas{grid-template-columns:1fr}}
.sl{position:relative;aspect-ratio:4/5;overflow:hidden}.sl img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.sl .af{clip-path:inset(0 0 0 50%);filter:brightness(1.06) saturate(1.05)}
.sl .hd{position:absolute;top:0;bottom:0;left:50%;width:2px;background:#fff}.sl .hd::after{content:"⟷";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:44px;height:44px;border-radius:50%;background:#fff;display:grid;place-items:center;color:#221B17}
.sl .lb{position:absolute;bottom:14px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;background:rgba(0,0,0,.45);color:#fff;padding:4px 10px}.sl .l{left:14px}.sl .r{right:14px}
.bas .tx{display:grid;gap:14px}.bas .tx p{margin:0;color:var(--muted)}.bas ul{margin:0;padding-left:18px;color:var(--muted);font-size:14.5px;display:grid;gap:6px}.bas .btn{justify-self:start}
.rels{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}@media(max-width:760px){.rels{grid-template-columns:1fr}}
.rel{text-decoration:none;display:grid;gap:8px}.rel .ph{aspect-ratio:4/3;overflow:hidden}.rel img{width:100%;height:100%;object-fit:cover}.rel h4{margin:6px 0 0;font-size:18px;font-weight:600}.rel p{margin:0;color:var(--muted);font-size:14px}.rel span{font-size:12px;letter-spacing:.14em;text-transform:uppercase}

'''
