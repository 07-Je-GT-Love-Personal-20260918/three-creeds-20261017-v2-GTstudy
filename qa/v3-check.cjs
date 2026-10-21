const fs=require('fs'),path=require('path'),assert=require('assert');
const {chromium}=require('../../.task-tools/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[],themes=[],layouts=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'});
 const original=await page.locator('#original-apostles .original-body').textContent();
 assert.equal(await page.locator('.core-note').count(),38);
 for(const theme of ['forest','ocean','violet','amber']){
  await page.locator(`[data-palette-choice="${theme}"]`).click();
  themes.push({theme,color:await page.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor)});
  assert.equal(await page.locator('html').getAttribute('data-palette'),theme);
  await page.locator('[data-study-night]').click();assert.equal(await page.locator('html').getAttribute('data-scheme'),'dark');
  await page.locator('[data-study-night]').click();
 }
 assert.equal(new Set(themes.map(t=>t.color)).size,4);
 await page.reload();assert.equal(await page.locator('html').getAttribute('data-palette'),'amber');
 await page.locator('[data-palette-choice="forest"]').click();
 async function select(start,end){await page.locator('#original-apostles .original-body [data-note-scope]').first().evaluate((el,{start,end})=>{
  const walk=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let pos=0,n,a,b;while(n=walk.nextNode()){if(!a&&start<pos+n.length)a=[n,start-pos];if(end<=pos+n.length){b=[n,end-pos];break}pos+=n.length}
  const r=document.createRange();r.setStart(...a);r.setEnd(...b);const s=getSelection();s.removeAllRanges();s.addRange(r);document.dispatchEvent(new Event('pointerup'));
 },{start,end});await page.locator('#selection-tools').waitFor({state:'visible'});}
 await select(0,5);await page.locator('[data-quick-mark="bold"]').click();
 await select(2,9);await page.locator('#mark-custom').click();
 await page.locator('input[name=ink]').check();await page.locator('input[name=color][value=purple]').check();
 await page.locator('select[name=underline]').selectOption('dashed');await page.locator('#mark-note').fill('重点：真实的神，真实的救恩。');
 await page.locator('.save-mark').click();
 assert.equal(await page.locator('#original-apostles .original-body').textContent(),original);
 assert.equal(await page.locator('.personal-mark.note-bold.note-fill.note-dashed').count(),1);
 await page.reload();assert(await page.locator('.personal-mark').count()>0);
 await page.locator('[data-notes-open]').click();assert.equal(await page.locator('.personal-note-card').count(),2);
 await page.locator('.personal-note-card').first().getByText('编辑标记',{exact:true}).click();
 await page.locator('#mark-note').fill('已修改的笔记');await page.locator('.save-mark').click();
 await page.locator('[data-notes-open]').click();assert.equal(await page.locator('.personal-note-card').count(),2);
 assert(await page.getByText('已修改的笔记',{exact:true}).isVisible());
 const downloadPromise=page.waitForEvent('download');await page.locator('#notes-export').click();const download=await downloadPromise;
 const saved=path.join(__dirname,'screenshots/v3-notes.json');await download.saveAs(saved);
 await page.locator('#notes-library [data-close-dialog]').click();
 await page.locator('[data-notes-visible]').click();assert.equal(await page.locator('.personal-mark').count(),0);
 await page.locator('[data-notes-visible]').click();assert(await page.locator('.personal-mark').count()>0);
 await page.goto('http://127.0.0.1:4173/reader-apostles.html',{waitUntil:'networkidle'});
 assert.equal(await page.locator('.personal-mark').count(),0);await page.locator('[data-notes-visible]').click();
 assert(await page.locator('.personal-mark').count()>0);assert.equal(await page.locator('.original-body').textContent(),original);
 const fresh=await browser.newPage();await fresh.goto('http://127.0.0.1:4173/');
 await fresh.locator('[data-notes-open]').click();await fresh.locator('#notes-import').setInputFiles(saved);
 await fresh.waitForFunction(()=>document.querySelectorAll('.personal-note-card').length===2);await fresh.close();
 for(const width of [1920,1440,820,390,320]){
  await page.setViewportSize({width,height:900});await page.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'});
  const m=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));layouts.push(m);assert.equal(m.width,m.scroll);
  await page.locator('[data-notes-open]').click();assert.equal(await page.locator('#notes-library').evaluate(el=>el.scrollWidth<=el.clientWidth),true);
  await page.locator('#notes-library [data-close-dialog]').click();
  await page.locator('#a01').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,`screenshots/v3-core-${width}.png`)});
 }
 assert.equal(errors.length,0);const report={checked:new Date().toISOString(),themes,layouts,coreNotes:38,checks:['theme and dark mode','theme persistence','overlapping styles','personal note edit','persistence','export/import','hide/show','original text unchanged','shared original anchors across clean reader','dialogs responsive'],errors};
 fs.writeFileSync(path.join(__dirname,'v3-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
