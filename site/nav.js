/* AURA Institute · shared header behavior. The nav markup itself is embedded directly in every
   page inside #site-header (no fetch — this must work from a plain double-clicked file, no server).
   This script only wires up the interactive bits: mega-menu toggles, mobile accordion, Esc, current-page highlight. */
(function(){
  var mount = document.getElementById('site-header');
  if(!mount) return;
  var current = mount.getAttribute('data-current') || '';

  function init(){
    // keep the nav bar pinned: the sticky header is offset by exactly the brand row's height
    var brand = mount.querySelector('.brandrow');
    function setBrandH(){ if(brand) mount.style.setProperty('--brand-h', brand.offsetHeight + 'px'); }
    setBrandH(); window.addEventListener('resize', setBrandH);

    if(current){
      var li = mount.querySelector('.navbar ul.top>li[data-cat="'+current+'"]');
      if(li) li.setAttribute('aria-current','true');
    }

    // desktop: category links toggle their mega menu instead of navigating (hover already handled in CSS)
    var catbtns = [].slice.call(mount.querySelectorAll('.catbtn'));
    function closeAll(){
      catbtns.forEach(function(b){ b.setAttribute('aria-expanded','false'); b.closest('li').classList.remove('open'); });
    }
    catbtns.forEach(function(b){
      b.addEventListener('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        var li = b.closest('li');
        var willOpen = !li.classList.contains('open');
        closeAll();
        if(willOpen){ li.classList.add('open'); b.setAttribute('aria-expanded','true'); }
      });
    });
    document.addEventListener('click', function(e){
      if(!mount.contains(e.target)) closeAll();
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape'){ closeAll(); closeMobile(); }
    });

    // mobile: hamburger opens slide-in menu
    var hamb = mount.querySelector('#hambBtn');
    var mnav = mount.querySelector('#mobilenav');
    var scrim = mount.querySelector('#navScrim');
    var mnClose = mount.querySelector('#mnClose');
    function openMobile(){
      mnav.classList.add('on'); scrim.classList.add('on');
      mnav.setAttribute('aria-hidden','false'); hamb.setAttribute('aria-expanded','true');
      document.body.style.overflow = 'hidden';
    }
    function closeMobile(){
      mnav.classList.remove('on'); scrim.classList.remove('on');
      mnav.setAttribute('aria-hidden','true'); hamb.setAttribute('aria-expanded','false');
      document.body.style.overflow = '';
    }
    if(hamb){
      hamb.addEventListener('click', function(){
        hamb.getAttribute('aria-expanded') === 'true' ? closeMobile() : openMobile();
      });
      scrim.addEventListener('click', closeMobile);
      mnClose.addEventListener('click', closeMobile);
    }

    // mobile accordion: clone each desktop mega's links into its mobile panel
    [].slice.call(mount.querySelectorAll('.macc')).forEach(function(acc){
      var cat = acc.getAttribute('data-acc');
      var mega = mount.querySelector('#mega-'+cat);
      var panel = acc.querySelector('.mapanel');
      if(mega && panel){
        var cols = mega.querySelector('.cols');
        if(cols){
          [].slice.call(cols.querySelectorAll('.grp')).forEach(function(grp){
            var h5 = grp.querySelector('h5');
            var wrap = document.createElement('div');
            wrap.className = 'mgrp';
            if(h5){ var h = document.createElement('h5'); h.textContent = h5.textContent; wrap.appendChild(h); }
            [].slice.call(grp.querySelectorAll('a')).forEach(function(a){ wrap.appendChild(a.cloneNode(true)); });
            panel.appendChild(wrap);
          });
        } else {
          [].slice.call(mega.querySelectorAll('a')).forEach(function(a){ panel.appendChild(a.cloneNode(true)); });
        }
      }
      var head = acc.querySelector('.machead');
      head.addEventListener('click', function(){
        var open = acc.classList.toggle('open');
        head.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });

    // Book button: if this page has the full booking drawer (home.html), wire it to open that instead of anchor-scrolling
    if(document.getElementById('drawer')){
      [].slice.call(mount.querySelectorAll('.nav-book, .mnbody .btn[href="#book"]')).forEach(function(a){
        a.removeAttribute('href'); a.setAttribute('data-book',''); a.setAttribute('role','button'); a.style.cursor = 'pointer';
      });
    }
  }

  /* chip rows between two rules (treatment hero, AURA Prime): always one line. The type and the spacing
     shrink together to fit the row's width, and grow back up to the design size when there is room. */
  function fitChips(){
    [].slice.call(document.querySelectorAll('.thero2 .chips, .pr .chips')).forEach(function(row){
      var spans = [].slice.call(row.children);
      spans.forEach(function(s){ s.style.fontSize = ''; s.style.paddingLeft = ''; s.style.paddingRight = ''; s.style.letterSpacing = ''; });
      var avail = row.clientWidth;
      if(!avail) return;
      // short on room: close up the wide tracking first, so the type itself has to shrink less
      if(row.scrollWidth > avail + 0.5) spans.forEach(function(s){ s.style.letterSpacing = '.07em'; });
      for(var k = 0; k < 3; k++){
        var need = row.scrollWidth;
        if(need <= avail + 0.5) break;
        var r = avail / need;
        spans.forEach(function(s, i){
          var cs = getComputedStyle(s);
          s.style.fontSize = Math.max(7, parseFloat(cs.fontSize) * r) + 'px';
          if(i > 0) s.style.paddingLeft = (parseFloat(cs.paddingLeft) * r) + 'px';
          s.style.paddingRight = (parseFloat(cs.paddingRight) * r) + 'px';
        });
      }
    });
  }
  function startFit(){
    fitChips();
    var t; window.addEventListener('resize', function(){ clearTimeout(t); t = setTimeout(fitChips, 60); });
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(fitChips);
    window.addEventListener('load', fitChips);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', startFit); else startFit();

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
