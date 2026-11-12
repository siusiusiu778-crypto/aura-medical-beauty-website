/* AURA Institute · shared Level 3 page behavior: reveal on scroll, jump menu, one-open FAQ. */
/* reveal on scroll, as on the homepage */
(function(){const els=document.querySelectorAll('.rv,.rv-img,.big');
 if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window)){els.forEach(e=>e.classList.add('in'));return;}
 const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{threshold:0,rootMargin:'0px 0px 12% 0px'});
 els.forEach(e=>io.observe(e));})();
/* jump menu: close after picking a section, and when clicking elsewhere */
(function(){const j=document.querySelector('.jump');if(!j)return;
 j.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>j.removeAttribute('open')));
 document.addEventListener('click',e=>{if(!j.contains(e.target))j.removeAttribute('open');});})();
/* faq: one answer open at a time */
(function(){const ds=[...document.querySelectorAll('.faqlist details')];
 ds.forEach(d=>d.addEventListener('toggle',()=>{if(d.open)ds.forEach(o=>{if(o!==d)o.open=false;});}));})();
/* appointment picker: show the chosen option in the pill and close the list */
document.querySelectorAll('.bbrow').forEach(d=>{const sum=d.querySelector('summary');if(!sum)return;
 const t=[...sum.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());if(!t)return;
 const lab=document.createElement('span');lab.className='bbl';lab.textContent=t.textContent.trim();sum.replaceChild(lab,t);
 const opts=[...d.querySelectorAll('.bbopt')];
 opts.forEach(o=>o.addEventListener('click',e=>{const i=o.querySelector('input');if(i)i.checked=true;
  opts.forEach(x=>x.classList.toggle('sel',x===o));const tx=o.textContent.trim();lab.textContent=tx.includes(' · ')?tx.split(' · ').slice(1).join(' · '):tx;lab.title=tx;
  e.preventDefault();d.removeAttribute('open');}));
 document.addEventListener('click',e=>{if(d.open&&!d.contains(e.target))d.removeAttribute('open');});});
/* Continue to Booking: open booking with the chosen appointment already filled in */
document.querySelectorAll('.bookbox').forEach(b=>{const btn=b.querySelector('.btn');if(!btn)return;
 btn.addEventListener('click',e=>{const sel=b.querySelector('.bbopt.sel')||b.querySelector('.bbopt input:checked')?.closest('.bbopt');
  let tx=sel?sel.textContent.trim():'';if(!tx||/^complimentary consultation$/i.test(tx))tx='Complimentary Consultation';
  btn.href='home.html?tx='+encodeURIComponent(tx)+'#book';});});
/* picker: open upward when the list would run past the bottom of the screen */
document.querySelectorAll('.bbrow').forEach(d=>d.addEventListener('toggle',()=>{if(!d.open)return;
 const o=d.querySelector('.bbopts');if(!o)return;d.classList.remove('up');
 const r=d.getBoundingClientRect(),h=o.offsetHeight+16;
 if(r.bottom+h>innerHeight&&r.top-h>0)d.classList.add('up');}));
