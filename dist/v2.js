/* Animation enhances the static teaching; every paragraph remains accessible. */
(()=>{
  const q=s=>document.querySelector(s),qa=s=>Array.from(document.querySelectorAll(s));
  const reduced=matchMedia('(prefers-reduced-motion:reduce)');
  let motion=saved.get('motion',!reduced.matches);
  const animations=new Set();
  function animate(el,options={}){if(!motion||reduced.matches||!el)return;const a=el.animate([{opacity:.45,transform:'translateY(12px)'},{opacity:1,transform:'translateY(0)'}],{duration:480,easing:'cubic-bezier(.2,.8,.2,1)',...options});animations.add(a);a.onfinish=()=>animations.delete(a)}
  function setMotion(){document.body.classList.toggle('motion-off',!motion);q('#motion-toggle').setAttribute('aria-pressed',motion);q('#motion-toggle').textContent=motion?'◌ 动效开启':'◌ 动效关闭';if(!motion){animations.forEach(a=>a.finish());stopAllGuides();if(typeof stopStory==='function')stopStory();}}
  q('#motion-toggle').onclick=()=>{motion=!motion;saved.set('motion',motion);setMotion()};
  const initial=Number(saved.get('readingSize',innerWidth<=400?21:22));
  function setSize(n){n=Math.max(18,Math.min(30,Number(n)||22));document.documentElement.style.setProperty('--reading-size',n+'px');q('#reading-size').value=n;q('#font-value').textContent=n;q('#font-toggle').setAttribute('aria-label','切换正文字号，当前'+n+'像素');saved.set('readingSize',n);requestAnimationFrame(()=>{if(typeof updateProgress==='function')updateProgress()})}
  q('#reading-size').addEventListener('input',e=>setSize(e.target.value));q('#font-smaller').onclick=()=>setSize(Number(q('#reading-size').value)-1);q('#font-larger').onclick=()=>setSize(Number(q('#reading-size').value)+1);q('#font-toggle').onclick=()=>{const current=Number(q('#reading-size').value);setSize(current<24?24:current<27?27:22);toast('正文字号 '+q('#reading-size').value+' 像素')};setSize(initial);
  const reveal=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting){animate(entry.target);reveal.unobserve(entry.target)}},{threshold:.04,rootMargin:'0px 0px -20px 0px'});
  qa('.hub-card,.creed-illustration,.central-question,.guided-story,.doctrine-lab,.clause,.visual-matrix,.salvation-flow').forEach(el=>reveal.observe(el));
  qa('[data-journey]').forEach(button=>button.onclick=()=>{const i=button.dataset.journey;qa('[data-journey]').forEach(b=>b.setAttribute('aria-pressed',b===button));qa('[data-journey-note]').forEach(note=>{note.hidden=note.dataset.journeyNote!==i;if(!note.hidden)animate(note)})});
  qa('[data-version]').forEach(button=>button.onclick=()=>{const i=button.dataset.version;qa('[data-version]').forEach(b=>b.setAttribute('aria-pressed',b===button));qa('[data-version-note]').forEach(note=>{note.hidden=note.dataset.versionNote!==i;if(!note.hidden)animate(note)})});
  qa('[data-term]').forEach(button=>button.onclick=()=>{const key=button.dataset.term;qa('[data-term]').forEach(b=>b.setAttribute('aria-pressed',b===button));qa('[data-term-panel]').forEach(panel=>{panel.hidden=panel.dataset.termPanel!==key;if(!panel.hidden)animate(panel)})});
  const guideTimers=new Map();
  function stopGuide(key){const record=guideTimers.get(key);if(record){clearInterval(record.timer);record.button.textContent='▶ 顺序演示';record.button.setAttribute('aria-pressed','false');guideTimers.delete(key)}}
  function stopAllGuides(){Array.from(guideTimers.keys()).forEach(stopGuide)}
  qa('[data-guide-play]').forEach(button=>button.onclick=()=>{const key=button.dataset.guidePlay;if(guideTimers.has(key)){stopGuide(key);return}stopAllGuides();const parent=button.closest('[data-story]'),stops=Array.from(parent.querySelectorAll('.story-stop'));if(!stops.length)return;let current=0;function highlight(){stops.forEach((el,i)=>el.classList.toggle('is-current',i===current));animate(stops[current],{duration:350});current=(current+1)%stops.length}highlight();button.textContent='Ⅱ 暂停演示';button.setAttribute('aria-pressed','true');guideTimers.set(key,{timer:setInterval(highlight,6500),button});});
  const sceneWatcher=new MutationObserver(()=>{animate(q('#story-display'));qa('.salvation-flow>div').forEach((el,i)=>el.classList.toggle('flow-current',i===scene))});sceneWatcher.observe(q('#story-display'),{childList:true});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stopAllGuides()});
  const guideObserver=new IntersectionObserver(entries=>entries.forEach(e=>{if(!e.isIntersecting)stopGuide(e.target.dataset.story)}),{threshold:0});qa('[data-story]').forEach(el=>guideObserver.observe(el));
  reduced.addEventListener?.('change',()=>{if(reduced.matches){motion=false;setMotion()}});
  setMotion();
})();
