"""Publish dist atomically using a token supplied only through the environment."""
import io,json,os,time,urllib.request,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
token=os.environ['NETLIFY_AUTH_TOKEN']
site=os.environ['NETLIFY_SITE_ID']
def request(path,data=None,kind='application/json'):
    req=urllib.request.Request('https://api.netlify.com/api/v1/'+path,data=data,headers={'Authorization':'Bearer '+token,'Content-Type':kind})
    with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted((root/'dist').rglob('*')):
        if p.is_file():z.write(p,p.relative_to(root/'dist').as_posix())
deploy=request('sites/'+site+'/deploys',buf.getvalue(),'application/zip')
for _ in range(60):
    status=request('deploys/'+deploy['id'])
    if status['state']=='ready':
        print('Netlify published:',status.get('ssl_url') or status.get('url'));break
    if status['state']=='error':raise RuntimeError('Netlify deployment failed')
    time.sleep(5)
else:raise RuntimeError('Netlify deployment did not become ready within five minutes')
