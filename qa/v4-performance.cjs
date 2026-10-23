const fs=require('fs'),path=require('path');const{chromium}=require('../../.task-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({channel:'msedge',headless:true}),results=[];
for(const[version,port]of[['V3',4174],['V4',4173]]){
const p=await b.newPage({viewport:{width:390,height:844}});let remote=0;
p.on('request',r=>{if(r.url().startsWith('https://'))remote++});
await p.route('https://fonts.googleapis.com/**',async route=>{await new Promise(r=>setTimeout(r,2000));await route.fulfill({status:200,contentType:'text/css',body:'/* simulated slow font stylesheet */'})});
await p.goto('http://127.0.0.1:'+port+'/',{waitUntil:'networkidle'});
const metrics=await p.evaluate(async()=>{const samples=[];let previous=performance.now();for(let i=0;i<80;i++){await new Promise(requestAnimationFrame);const now=performance.now();samples.push(now-previous);previous=now;scrollBy(0,55)}return{paints:performance.getEntriesByType('paint').map(e=>({name:e.name,ms:Math.round(e.startTime)})),scrollFrameP95ms:Math.round(samples.sort((a,b)=>a-b)[Math.floor(samples.length*.95)]),blurLayers:[...document.querySelectorAll('*')].filter(el=>el.getClientRects().length&&getComputedStyle(el).backdropFilter!=='none').length}});
results.push({version,remoteRequestsAtStartup:remote,...metrics});await p.close();}
await b.close();const report={checked:new Date().toISOString(),scenario:'Same local browser, phone viewport, remote font stylesheet artificially delayed by 2000ms. One run per version; indicative test, not a guarantee for every device.',results};fs.writeFileSync(path.join(__dirname,'v4-performance-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));})().catch(e=>{console.error(e);process.exitCode=1});
