const fs=require('fs'),path=require('path'),assert=require('assert');
const {chromium}=require('../../.task-tools/node_modules/playwright');
(async()=>{const meta=JSON.parse(fs.readFileSync(path.join(__dirname,'../deployment.json'),'utf8')),b=await chromium.launch({channel:'msedge',headless:true}),results=[];
for(const host of [meta.githubPagesUrl,meta.surgeUrl,meta.vercelUrl].filter(Boolean)){
 const p=await b.newPage({viewport:{width:390,height:844}}),errors=[];p.on('pageerror',e=>errors.push(e.message));
 const res=await p.goto(host,{waitUntil:'networkidle'});assert.equal(res.status(),200);
 assert.equal(await p.locator('.core-note').count(),38);await p.locator('[data-palette-choice="ocean"]').click();
 assert.equal(await p.locator('html').getAttribute('data-palette'),'ocean');await p.reload();assert.equal(await p.locator('html').getAttribute('data-palette'),'ocean');
 await p.locator('#a01 .core-thesis').evaluate(el=>{const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);document.dispatchEvent(new Event('pointerup'))});
 await p.locator('#selection-tools').waitFor({state:'visible'});await p.locator('[data-quick-mark="fill"]').click();
 await p.reload();assert.equal(await p.locator('.personal-mark').count(),1);
 await p.locator('[data-notes-open]').click();assert.equal(await p.locator('.personal-note-card').count(),1);await p.locator('#notes-library [data-close-dialog]').click();
 assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth),390);assert.equal(errors.length,0);
 await p.goto(host+'atlas.html',{waitUntil:'networkidle'});assert.equal(await p.locator('.culture-card').count(),10);assert.equal(await p.locator('[data-atlas-scene]').count(),5);assert.equal(await p.locator('.route-card').count(),3);await p.locator('[data-atlas-stop="nicaea"]').first().click();assert((await p.locator('#place-info').textContent()).includes('尼西亚'));assert.equal(await p.locator('.corner-nav-toggle').count(),1);
 results.push({historyCulture:'10 cards / 5 scenes / 3 diagrams; map point navigation pass',host,http:res.status(),coreNotes:38,themes:'switch and persist',marks:'save and persist',mobileOverflow:false,errors});await p.close();
}await b.close();fs.writeFileSync(path.join(__dirname,'v4-live-report.json'),JSON.stringify({checked:new Date().toISOString(),results},null,2));console.log(JSON.stringify(results,null,2));})().catch(e=>{console.error(e);process.exitCode=1});
