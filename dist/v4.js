/* Native scrolling, bounded animation, and opt-in map services. */
(()=>{'use strict';
const q=s=>document.querySelector(s),qa=s=>Array.from(document.querySelectorAll(s)),reduced=matchMedia('(prefers-reduced-motion:reduce)');
const behavior=()=>reduced.matches?'instant':'smooth';
const toggle=q('.corner-nav-toggle'),panel=q('#corner-nav-panel');
function closeNav(){panel.hidden=true;toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','展开快捷导航')}
toggle.onclick=()=>{panel.hidden=!panel.hidden;toggle.setAttribute('aria-expanded',!panel.hidden);toggle.setAttribute('aria-label',panel.hidden?'展开快捷导航':'收起快捷导航')};
qa('[data-nav]').forEach(b=>b.onclick=()=>{const action=b.dataset.nav;if(action==='back')history.back();if(action==='forward')history.forward();if(action==='top')window.scrollTo({top:0,behavior:behavior()});if(action==='bottom')window.scrollTo({top:document.documentElement.scrollHeight,behavior:behavior()});closeNav()});
document.addEventListener('click',e=>{if(!e.target.closest('.corner-nav'))closeNav()});document.addEventListener('keydown',e=>{if(e.key==='Escape')closeNav()});
if(navigator.connection?.saveData||(navigator.hardwareConcurrency&&navigator.hardwareConcurrency<=4))document.body.classList.add('lite-mode');
const ambient=q('.hero-collage');if(ambient){new IntersectionObserver(entries=>entries.forEach(e=>ambient.classList.toggle('ambient-paused',!e.isIntersecting)),{rootMargin:'70px'}).observe(ambient)}

// Preview edits never touch the selected source text.
const form=q('#mark-form'),preview=q('#mark-style-preview');
function previewStyle(){if(!form||!preview)return;const color=form.elements.color.value;preview.className='mark-style-preview';for(const key of ['bold','ink','fill','block'])if(form.elements[key]?.checked)preview.classList.add('note-'+key);if(form.elements.underline.value!=='none')preview.classList.add('note-'+form.elements.underline.value);for(const kind of ['ink','fill','line'])preview.style.setProperty('--mark-'+kind,'var(--note-'+kind+'-'+color+')')}
form?.addEventListener('change',previewStyle);if(form)new MutationObserver(previewStyle).observe(q('#mark-editor'),{attributes:true,attributeFilter:['open']});previewStyle();
q('#notes-search')?.addEventListener('input',e=>{const search=e.target.value.trim().toLowerCase();qa('.personal-note-card').forEach(card=>card.hidden=search&&!card.textContent.toLowerCase().includes(search))});
const routeWatch=new IntersectionObserver(entries=>entries.forEach(e=>e.target.classList.toggle('route-in-view',e.isIntersecting)),{rootMargin:'30px'});qa('.route-card').forEach(el=>routeWatch.observe(el));
const scenes=qa('[data-atlas-scene]'),play=q('#atlas-story-play');let storyTimer=null,sceneIndex=0;
function scenePick(i){sceneIndex=i;scenes.forEach((el,j)=>{el.classList.toggle('is-current',j===i);el.querySelector('button').setAttribute('aria-pressed',j===i)})}
function stopAtlasStory(){clearInterval(storyTimer);storyTimer=null;if(play){play.textContent='▶ 顺着历史读一遍';play.setAttribute('aria-pressed','false')}}
qa('[data-scene-pick]').forEach(b=>b.onclick=()=>{stopAtlasStory();scenePick(Number(b.dataset.scenePick))});
if(play){play.onclick=()=>{if(storyTimer)return stopAtlasStory();if(reduced.matches||document.body.classList.contains('motion-off'))return scenePick((sceneIndex+1)%scenes.length);play.textContent='Ⅱ 暂停演示';play.setAttribute('aria-pressed','true');storyTimer=setInterval(()=>scenePick((sceneIndex+1)%scenes.length),5500)};new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)stopAtlasStory()}).observe(q('#atlas-story'))}
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopAtlasStory()});reduced.addEventListener('change',()=>{if(reduced.matches)stopAtlasStory()});
if(!q('#geography-data'))return;
const info=JSON.parse(q('#geography-data').textContent),places=info.places,culture=info.culture;
let active=0,map=null,layer=null,markers=[],loaded=false,loadingPromise=null,loadTimer=null,generation=0;
const status=q('#map-status'),providers={
 esri:{url:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',attribution:'Tiles © Esri — Sources: Esri, HERE, Garmin, USGS, Intermap, INCREMENT P, NRCan, Esri Japan, METI, Esri China (Hong Kong), Esri Korea, Esri (Thailand), NGCC, <a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>, GIS User Community',maxZoom:18},
 osm:{url:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',attribution:'<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>',maxZoom:19}
};
function external(){const p=places[active];q('#map-external').href=`https://www.openstreetmap.org/?mlat=${p.lat}&mlon=${p.lon}#map=10/${p.lat}/${p.lon}`}
function select(i,scroll=false){active=i;external();qa('[data-atlas-stop]').forEach(b=>b.setAttribute('aria-pressed',places[i].id===b.dataset.atlasStop));if(document.body.classList.contains('atlas-page')){
 qa('[data-place]').forEach(el=>{el.classList.toggle('active',Number(el.dataset.place)===i);el.setAttribute('aria-pressed',Number(el.dataset.place)===i)});
 const p=places[i],box=q('#place-info');box.replaceChildren();for(const [tag,text]of [['h3',p.name],['p',p.body],['p','文化与处境：'+p.culture],['small','约略坐标 '+p.lat+'°N, '+p.lon+'°E · 现代定位，不代表古代疆界']]){const el=document.createElement(tag);el.textContent=text;box.append(el)}
 }
 if(map){map.setView([places[i].lat,places[i].lon],8,{animate:false});markers[i]?.openPopup()}
 if(scroll)q('.map-panel').scrollIntoView({block:'start',behavior:behavior()});
}
if(document.body.classList.contains('atlas-page')){
 places.forEach((p,i)=>{const b=document.createElement('button');b.type='button';b.dataset.place=i;b.textContent=(i+1)+' '+p.name.split(/[／/]/)[0];b.onclick=()=>select(i);q('#map-buttons').append(b)});
 qa('.map [data-place]').forEach(el=>{el.addEventListener('click',()=>select(Number(el.dataset.place)));el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(Number(el.dataset.place))}})});
}
window.addEventListener('creed-place-change',e=>select(e.detail.index));
qa('[data-atlas-stop]').forEach(b=>b.onclick=()=>{const i=places.findIndex(p=>p.id===b.dataset.atlasStop);if(i<0)return;if(document.body.classList.contains('atlas-page'))select(i,true);else{q('#map-buttons button[data-place="'+i+'"]').click();q('.map-panel').scrollIntoView({block:'start',behavior:behavior()})}});
select(0);
function leaflet(){if(window.L)return Promise.resolve();if(loadingPromise)return loadingPromise;loadingPromise=new Promise((resolve,reject)=>{const css=document.createElement('link');css.rel='stylesheet';css.href='vendor/leaflet/leaflet.css';document.head.append(css);const script=document.createElement('script');script.src='vendor/leaflet/leaflet.js';script.onload=resolve;script.onerror=()=>{script.remove();loadingPromise=null;reject(Error('local map library unavailable'))};document.head.append(script)});return loadingPromise}
function setProvider(autoFallback=false){if(!map)return;clearTimeout(loadTimer);const myGeneration=++generation,chosen=q('#map-provider').value,provider=providers[chosen];if(layer)layer.remove();let successes=0,errors=0;status.textContent='正在连接 '+(chosen==='esri'?'Esri':'OpenStreetMap')+'；本地图仍可使用。';
 layer=L.tileLayer(provider.url,{attribution:provider.attribution,maxZoom:provider.maxZoom,keepBuffer:1,updateWhenIdle:true,updateWhenZooming:false}).addTo(map);
 layer.on('tileload',()=>{if(myGeneration!==generation)return;successes++;clearTimeout(loadTimer);status.textContent='在线底图已连接。可拖动、缩放，点击标记查看城市。'});
 function fail(){if(myGeneration!==generation||successes)return;if(chosen==='esri'&&!autoFallback){q('#map-provider').value='osm';status.textContent='主服务连接不佳，尝试备用服务。';setProvider(true)}else status.textContent='当前网络未能显示在线底图。请切换服务、打开外部地图，或继续使用上方本地图。'}
 layer.on('tileerror',()=>{errors++;if(errors>=3)fail()});loadTimer=setTimeout(fail,10000);
}
q('#map-load').onclick=async()=>{q('#modern-map').hidden=false;q('#map-unload').hidden=false;q('#map-load').disabled=true;status.textContent='正在准备地图…';try{await leaflet();if(!map){map=L.map('modern-map',{scrollWheelZoom:false,zoomAnimation:!reduced.matches,fadeAnimation:false,preferCanvas:true}).setView([39,20],4);markers=places.map((p,i)=>{const icon=L.divIcon({className:'atlas-pin',html:'<span>'+(i+1)+'</span>',iconSize:[30,36],iconAnchor:[15,36]});const marker=L.marker([p.lat,p.lon],{icon,title:p.name});const label=document.createElement('div');const h=document.createElement('b');h.textContent=p.name;const t=document.createElement('p');t.textContent=p.body;label.append(h,t);marker.bindPopup(label);marker.addTo(map);return marker});map.fitBounds(places.map(p=>[p.lat,p.lon]),{padding:[28,28],maxZoom:5,animate:false});setProvider();loaded=true}else{map.invalidateSize();if(!layer)setProvider()}q('#map-load').textContent='◎ 地图已展开'}catch{q('#map-load').disabled=false;status.textContent='地图工具暂不能加载，请使用本地图或外部地图链接。'}};
q('#map-provider').onchange=()=>{if(map&&loaded&&!q('#modern-map').hidden)setProvider();else status.textContent='已选择底图，点击“打开可拖动地图”连接。'};
q('#map-fit').onclick=()=>{if(map)map.fitBounds(places.map(p=>[p.lat,p.lon]),{padding:[28,28],animate:false});else status.textContent='先打开在线地图；所有地点也已显示在上方本地图中。'};
q('#map-unload').onclick=()=>{generation++;clearTimeout(loadTimer);if(layer){layer.remove();layer=null}q('#modern-map').hidden=true;q('#map-unload').hidden=true;q('#map-load').disabled=false;q('#map-load').textContent='◎ 打开可拖动地图';status.textContent='已收起在线地图，停止新的底图请求。'};
})();
