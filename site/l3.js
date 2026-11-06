/* AURA Institute · shared Level 3 page behavior: reveal on scroll, jump menu, one-open FAQ. */
/* reveal on scroll, as on the homepage */
(function(){const els=document.querySelectorAll('.rv,.rv-img,.big');
 if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window)){els.forEach(e=>e.classList.add('in'));return;}
 const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{threshold:.15,rootMargin:'0px 0px -6% 0px'});
 els.forEach(e=>io.observe(e));})();
/* jump menu: close after picking a section, and when clicking elsewhere */
(function(){const j=document.querySelector('.jump');if(!j)return;
 j.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>j.removeAttribute('open')));
 document.addEventListener('click',e=>{if(!j.contains(e.target))j.removeAttribute('open');});})();
/* faq: one answer open at a time */
(function(){const ds=[...document.querySelectorAll('.faqlist details')];
 ds.forEach(d=>d.addEventListener('toggle',()=>{if(d.open)ds.forEach(o=>{if(o!==d)o.open=false;});}));})();
