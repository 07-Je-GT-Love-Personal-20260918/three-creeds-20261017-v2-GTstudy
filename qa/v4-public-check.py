"""Verify public releases without authentication, including every source unit."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib,json,re,requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent.parent
meta=json.loads((ROOT/'deployment.json').read_text(encoding='utf-8'))
docs=json.loads((ROOT/'content/fulltexts.json').read_text(encoding='utf-8'))['documents']
hosts=[meta[k] for k in ['githubPagesUrl','surgeUrl','vercelUrl'] if meta.get(k)]
files=['atlas.html','v4.js','v4.css','vendor/leaflet/leaflet.js','vendor/leaflet/leaflet.css','vendor/leaflet/LICENSE','index.html','library.html','background.html','reader-apostles.html','reader-nicene.html','reader-athanasian.html','styles.css','v2.css','study.css','app.js','v2.js','study.js','theme-init.js','favicon.svg','text-verification.json','assets/creed-story-apostles.svg','assets/creed-story-nicene.svg','assets/creed-story-athanasian.svg']
def get(item):
 host,file=item
 for attempt in range(3):
  try:
   r=requests.get(host+file,timeout=45);r.raise_for_status();break
  except requests.RequestException:
   if attempt==2:raise
 r.encoding='utf-8'
 return host,file,r
results=[];failures=[];sourcechecks=[]
with ThreadPoolExecutor(max_workers=6) as pool:
 for host,file,r in pool.map(get,[(h,f) for h in hosts for f in files]):
  item={'url':host+file,'http':r.status_code,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest()}
  if file.endswith(('.html','.js','.css','.svg')):
   canonical=lambda text:text.replace('\r\n','\n').rstrip()
   item['sameAsLocal']=canonical(r.text)==canonical((ROOT/'dist'/file).read_text(encoding='utf-8'))
   if not item['sameAsLocal']:failures.append(item['url']+' stale asset')
  if file=='index.html':
   soup=BeautifulSoup(r.text,'html.parser');item['coreNotes']=len(soup.select('.core-note'));item['themes']=len(soup.select('[data-palette-choice]'));item['v4']='v4.0' in r.text
   if item['coreNotes']!=38 or item['themes']!=4 or not item['v4']:failures.append(host+' wrong version')
  if file=='library.html':
   soup=BeautifulSoup(r.text,'html.parser');count=0;diff=[]
   for doc in docs:
    for i,section in enumerate(doc['sections'],1):
     count+=1;el=soup.select_one(f'#{doc["key"]}-{i} .original-body')
     if el is None or re.sub(r'\s','',el.get_text())!=re.sub(r'\s','',section['text']):diff.append(f'{doc["key"]}-{i}')
   sourcechecks.append({'host':host,'sections':count,'mismatches':diff})
   if diff:failures.append(host+' original text mismatch')
  results.append(item)
report={'checked':datetime.now(timezone.utc).isoformat(),'unauthenticated':True,'hosts':len(hosts),'resourcesPerHost':len(files),'resources':results,'originals':sourcechecks,'failures':failures}
(ROOT/'qa/v4-public-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='resources'},ensure_ascii=False,indent=2))
assert not failures
