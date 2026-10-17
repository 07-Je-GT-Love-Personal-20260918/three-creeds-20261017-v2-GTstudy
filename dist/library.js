const button=document.getElementById('lib-toc-toggle');
function closeLib(){document.body.classList.remove('toc-mobile-open');if(matchMedia('(max-width:960px)').matches)button.setAttribute('aria-expanded','false')}
button.onclick=()=>{if(matchMedia('(max-width:960px)').matches){const open=document.body.classList.toggle('toc-mobile-open');button.setAttribute('aria-expanded',open)}else{const hidden=document.body.classList.toggle('toc-hidden');button.setAttribute('aria-expanded',!hidden)}};
document.getElementById('lib-print').onclick=()=>window.print();
document.querySelectorAll('#lib-toc a').forEach(a=>a.onclick=closeLib);
document.getElementById('lib-search').oninput=e=>{const q=e.target.value.trim();document.querySelectorAll('#lib-toc a').forEach(a=>a.hidden=q&&!a.textContent.includes(q))};
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeLib()});
if(matchMedia('(max-width:960px)').matches)button.setAttribute('aria-expanded','false');
