"""Build a complete, readable static site. Python standard library only."""
from pathlib import Path
from html import escape
import json, re, shutil, hashlib
from html.parser import HTMLParser
from edition_v2 import guide,hub,synthesis,supporting_page,icon
from edition_v3 import core_note,essentials,enhance_pages
from edition_v4 import build_atlas,enhance_v4

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
CONTENT = ROOT / 'content'
fw = json.loads((CONTENT/'framework.json').read_text(encoding='utf-8'))
fw['timeline']=fw['timeline'][:15]
fw['places']=fw['places'][:7]+[
 {'name':'阿奎莱亚／Aquileia','lat':45.77,'lon':13.368,'body':'鲁非努的受洗宣认与解释见证了西方信仰表达在地域之间的差异，帮助我们理解使徒信经逐步定型的过程。','culture':'意大利东北的拉丁教会处于东西交流的交通网络中。地方受洗宣认具有共同骨架，也存在具体词句差异。'},
 {'name':'以弗所／Ephesus','lat':37.941,'lon':27.341,'body':'431年会议的争论围绕道成肉身者的位格统一。它帮助说明：马利亚所生的是神的儿子成为人，不是她创造了神性。','culture':'小亚细亚的希腊语城市；基督论争论发生在释经、敬拜称谓、主教关系与帝国政治交织的教会生活中。'},
 {'name':'托莱多／Toledo','lat':39.858,'lon':-4.024,'body':'589年第三次托莱多会议处于西哥特王国由亚流传统转向尼西亚信仰的背景，是“和子”条款在西方传播的重要节点。','culture':'伊比利亚的拉丁教会与王国宗教转向密切相关；西方礼仪传播史不能直接等同381年东方希腊文本。'}]
culture_v4=json.loads((CONTENT/'history-culture-v4.json').read_text(encoding='utf-8'))
for entry in culture_v4['places']:
    match=next((p for p in fw['places'] if abs(p['lat']-entry['lat'])+abs(p['lon']-entry['lon'])<.7),None)
    if match:
        match.update({'id':entry['id'],'body':entry['why'],'culture':entry['culture']})
    else:
        fw['places'].append({'id':entry['id'],'name':entry['name'],'lat':entry['lat'],'lon':entry['lon'],'body':entry['why'],'culture':entry['culture']})
comm = json.loads((CONTENT/'commentary.json').read_text(encoding='utf-8'))
full_path=CONTENT/'fulltexts.json'
full=json.loads(full_path.read_text(encoding='utf-8')) if full_path.exists() else {'documents':[]}
docs={d['key']:d for d in full['documents']}
E = lambda s: escape(str(s), quote=True)
CCI = 'https://ccifellowship.org/books/book-of-praise/'
CONF = {'海':CCI+'confessions/heidelberg-catechism','比':CCI+'confessions/the-belgic-confession','多特':CCI+'confessions/canons-of-dort'}

def ref_links(s):
    chunks = str(s).split('；')
    output=[]
    for chunk in chunks:
        key=next((k for k in CONF if k in chunk),None)
        if key:
            output.append(f'<a href="{CONF[key]}" target="_blank" rel="noopener">{E(chunk)}</a>')
        else: output.append(E(chunk))
    return '；'.join(output)

def emphasize(text):
    count=0
    def wrap(match):
        nonlocal count
        count+=1
        return '<mark class="theology-key">'+match.group()+'</mark>' if count<=3 else match.group()
    return re.sub(r'同一位永恒的子|一体三位|一位二性|位格区别|位格联合|完整人性|完全神性|同具神性|身体复活|基督的义|信心的果子|三一神|受生|称义',wrap,E(text))

class SafeHTML(HTMLParser):
    allowed={'p','div','article','ol','ul','li','sup','sub','strong','em','b','i','br','h2','h3','h4','h5','h6','span','blockquote'}
    def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in {'script','style','iframe','object'}:self.skip+=1;return
        if self.skip or tag not in self.allowed:return
        safe=[]
        for k,v in attrs:
            if k=='class' and v=='reference-list':safe.append('class="reference-list"')
            if tag=='ol' and k=='start' and str(v).isdigit():safe.append(f'start="{v}"')
        self.parts.append('<'+tag+(' '+' '.join(safe) if safe else '')+'>')
    def handle_endtag(self,tag):
        if tag in {'script','style','iframe','object'}:self.skip=max(0,self.skip-1);return
        if not self.skip and tag in self.allowed and tag!='br':self.parts.append('</'+tag+'>')
    def handle_data(self,data):
        if not self.skip:self.parts.append(escape(data))

def safe_original(section):
    assert hashlib.sha256(section['text'].encode()).hexdigest()==section['sha256'],'Original hash mismatch'
    p=SafeHTML();p.feed(section['html']);return ''.join(p.parts)

def overview():
    return ''.join(f'<article class="card overview-card"><h3>{E(x["title"])}</h3><p class="body">{E(x["body"])}</p><div class="bib">经文定位：{E(x["bible"])}<br>认信互证：{ref_links(x["confessions"])}</div></article>' for x in fw['overview'])

def timeline():
    output=[]
    for x in fw['timeline']:
        source=x['source']
        link=f'<a href="{E(source)}" target="_blank" rel="noopener">核查史料 ↗</a>' if source.startswith('https://') else E(source)
        output.append(f'<article class="event"><time>{E(x["year"])}</time><div><h3>{E(x["title"])}</h3><span class="tag">⌖ {E(x["place"])}</span><p>{E(x["body"])}</p><div class="source">{link}</div></div></article>')
    return ''.join(output)

CREEDS = {
 'apostles':('02','APOSTLES’ CREED','使徒信经','十二条，沿着救恩故事认识神。','从西方受洗宣认逐渐形成，内容具有使徒性；不能据此认定十二使徒一人写一句。本文按常用十二条教学结构展开，与海德堡问答23–58的安排相互参照。','apostles-creed','故事骨架 · 12条'),
 'nicene':('03','NICENE CREED','尼西亚信经','不止问发生什么，更问救主是谁。','本文解读指定网站采用的西方通行形式，以381年尼西亚—君士坦丁堡信经为基础，并含后来西方的“和子”条款。325版、381版与西方增补有不同历史层次；以下14段为教学分段，不冒充古代统一条号。','nicene-creed','身份澄清 · 14段'),
 'athanasian':('04','ATHANASIAN CREED','亚他那修信经','一体三位，一位二性。','作者不详，形成于后来的拉丁西方，不是亚他那修亲笔。指定网页正文有42段，而引言段号存在不一致；以下12组逐一覆盖正文1–42段。传统称“普世信经”，不代表东正教同样把它作为普世会议文件接纳。','athanasian-creed','教义边界 · 42段 / 12组')
}

def creeds():
    output=[]
    for key,(num,en,name,title,intro,path,tag) in CREEDS.items():
        output.append(f'<section class="chapter creed-section theme-{key}" id="{key}"><div class="section-head"><div><div class="eyebrow"><span class="section-num">{num}</span> {en}</div><h2>{name} · 深度解读</h2></div><p>{title}</p></div><div class="creed-intro"><div class="biglabel">{E(tag)}</div><h3 style="margin-top:12px">{title}</h3><p>{intro}</p><a href="{CCI}creeds/{path}" target="_blank" rel="noopener">打开指定网站中文全文 ↗</a><span class="small">　原文区与原创解读区分别标识。</span></div><div class="clauses">')
        output.append(f'<nav class="creed-chapter-nav" aria-label="{name}章内导航"><a href="#original-{key}">{icon("book")}完整原文</a><a href="#{comm[key][0]["id"]}">{icon("scroll")}逐条解读</a><a href="#lab-{key}">{icon("layers")}互动图解</a><a href="reader-{key}.html">{icon("target")}纯净阅读</a></nav>')
        output.append(guide(ROOT,key))
        if key in docs:
            sec=docs[key]['sections'][0]
            output.append(f'<div class="original-panel" id="original-{key}"><div class="reader-title"><span class="tag gold">指定网站中文原文 · 完整阅读</span><h3>{name}</h3><a class="small" href="reader-{key}.html">打开独立清洁阅读版 ↗</a></div><div class="original-body">{safe_original(sec)}</div><div class="original-meta">来源：<a href="{E(sec["source"])}" target="_blank" rel="noopener">ccifellowship.org</a> · 正文字词及标点保留；段落样式重新排版。<br>以下开始原创解读。</div></div>')
        for i,x in enumerate(comm[key]):
            output.append(f'<article class="clause theme-{key}" id="{E(x["id"])}"><div class="clause-head"><span class="clause-number">{i+1:02}</span><div><span class="tag">{E(x["range"])}</span><h3>{E(x["title"])}</h3></div></div><div class="clause-body">{core_note(ROOT,x["id"])}<p>{emphasize(x["explanation"])}</p><div class="clause-bottom"><div><b>{icon("layers")} 圣约联结</b>{E(x["covenant"])}</div><div><b>{icon("shield")} 误区辨析</b>{E(x["error"])}</div><div><b>{icon("target")} 生活应用</b>{E(x["application"])}</div></div><div class="refs"><span>经文：{E(x["bible"])}</span><span>认信：{ref_links(x["confessions"])}</span></div></div></article>')
        output.append('</div></section>')
    return ''.join(output)

def comparison():
    return ''.join('<tr>'+''.join(f'<td data-label="{label}">{E(x[k])}</td>' for k,label in [('aspect','比较维度'),('apostles','使徒信经'),('nicene','尼西亚信经'),('athanasian','亚他那修信经')])+'</tr>' for x in fw['comparison'])

def difficulties():
    return ''.join(f'<article class="difficulty" id="faq-{i+1}"><h3><span class="tag gold">{i+1:02}</span> {E(x["question"])}</h3><p>{E(x["answer"])}</p><div class="bib">经文：{E(x["bible"])}<br>认信：{ref_links(x["confessions"])}</div></article>' for i,x in enumerate(fw['difficulties']))

def map_svg():
    base_path=CONTENT/'map-base.svg'
    def xy(lon,lat):return (lon+12)/60*960,(56-lat)/30*480
    if not base_path.exists():
        countries=json.loads((ROOT/'countries.json').read_text(encoding='utf-8'))
        parts=[]
        for country in countries['features']:
            geo=country['geometry'];polys=geo['coordinates'] if geo['type']=='MultiPolygon' else [geo['coordinates']]
            for poly in polys:
                coords=poly[0]
                if not any(-15 <= p[0] <= 50 and 23 <= p[1] <= 59 for p in coords):continue
                d=' '.join(('M' if i==0 else 'L')+f'{xy(*p)[0]:.1f},{xy(*p)[1]:.1f}' for i,p in enumerate(coords))+' Z'
                parts.append(f'<path class="land" d="{d}"/>')
        base_path.write_text(''.join(parts),encoding='utf-8')
    parts=['<svg class="map" viewBox="0 0 960 480" role="img" aria-labelledby="map-title map-desc"><title id="map-title">信经历史地图</title><desc id="map-desc">欧洲与东地中海的11个历史地点。点击标记或下方按钮查看详细说明。相邻城市用引线错开标记，圆点才是其真实近似位置。</desc><defs><clipPath id="map-clip"><rect width="960" height="480"/></clipPath></defs><g clip-path="url(#map-clip)">']
    for lon in range(-10,50,10):
        x,_=xy(lon,0);parts.append(f'<path class="gridline" d="M{x},0V480"/>')
    for lat in range(30,60,10):
        _,y=xy(0,lat);parts.append(f'<path class="gridline" d="M0,{y}H960"/>')
    parts.append(base_path.read_text(encoding='utf-8'))
    parts.append('<text x="410" y="362" letter-spacing="7">地 中 海</text><text x="107" y="220" letter-spacing="4">欧 洲</text><text x="752" y="212" letter-spacing="3">小 亚 细 亚</text><text x="275" y="444" letter-spacing="4">北 非</text>')
    # Offsets keep the close Byzantine cities and Low Countries distinct.
    offsets={3:(48,40),4:(-25,-22),5:(38,-10),8:(-25,10),9:(16,-15)}
    for i,p in enumerate(fw['places']):
        x,y=xy(p['lon'],p['lat']);dx,dy=offsets.get(i,(0,0));tx,ty=x+dx,y+dy
        if dx or dy:parts.append(f'<path d="M{x:.1f},{y:.1f}L{tx:.1f},{ty:.1f}" stroke="#58715e" stroke-width="1"/><circle cx="{x:.1f}" cy="{y:.1f}" r="2.8" fill="#174e42"/>')
        parts.append(f'<g class="marker" data-place="{i}" tabindex="0" role="button" aria-label="{E(p["name"])}"><circle cx="{tx:.1f}" cy="{ty:.1f}" r="11"/><text x="{tx:.1f}" y="{ty+7:.1f}" text-anchor="middle">{i+1}</text></g>')
    parts.append('</g></svg>')
    return ''.join(parts)

def toc():
    sections=[('panorama','01 先看圣经全景'),('apostles','02 使徒信经 · 12条'),('nicene','03 尼西亚信经 · 14段'),('athanasian','04 亚他那修信经 · 42段'),('comparison','05 三经深度比较'),('history','06 三经历史时间线'),('geography','07 地理与文化'),('difficulties','08 核心难点'),('memorize','09 原文与记忆工坊'),('support','10 辅助阅读'),('sources','11 来源与版本')]
    output=[]
    for sid,label in sections:
        output.append(f'<a href="#{sid}">{label}</a>')
        if sid in CREEDS:
            for x in comm[sid]:output.append(f'<a class="sub" href="#{E(x["id"])}">{E(x["range"])} · {E(x["title"].split("：")[0])}</a>')
    return ''.join(output)

def sources():
    records=[{'title':'CCI《敬拜手册》2015：版权与出版说明','url':CCI.rstrip('/'),'use':'指定中文认信版本。用户提供同版PDF并确认公开使用许可；原文本身的版权归原权利人。'}]
    for key,(_,_,name,_,_,path,_) in CREEDS.items():records.append({'title':'CCI · '+name,'url':CCI+'creeds/'+path,'use':'本项目正式中文全文的唯一网页来源；原文与原创解读明确分开。'})
    for title,key in [('海德堡要理问答','海'),('比利时信条','比'),('多特信经','多特')]:records.append({'title':'CCI · '+title,'url':CONF[key],'use':'中文原文与条号核对；不以其他网站译文替代。'})
    records += [
        {'title':'CCI ·《我属于》主日八','url':'https://ccifellowship.org/index.php/books/i-belong/8','use':'帮助把三一认识连回圣经启示。本站据此强调教学归属不能变成三位格独立分工；正文为原创说明。'},
        {'title':'CCI · 主日20：圣灵的工作','url':'https://ccifellowship.org/sermons/heidelberg-catechism/lord-day-20','use':'拓展圣灵使人归向基督的牧养视角；不以情绪强度替代对基督的信靠。'},
        {'title':'CCI · 成人洗礼仪文','url':CCI+'liturgical-forms/2','use':'观察父子圣灵之名、认信与教会生活之间的礼仪联系。'},
        {'title':'CCI · 圣餐仪文','url':CCI+'liturgical-forms/4','use':'观察共同认信与记念、领受基督之间的联系。'},
        {'title':'CCI · 主日5：得救的唯一道路','url':'https://ccifellowship.org/sermons/heidelberg-catechism/lord-day-05','use':'拓展罪、刑罚、中保与恢复相交的牧养逻辑；不复制讲章。'}]
    records += fw['sources']+comm['sources']
    seen=set();output=['<ol class="source-list">']
    for r in records:
        if r['url'] in seen:continue
        seen.add(r['url']);output.append(f'<li><a href="{E(r["url"])}" target="_blank" rel="noopener">{E(r["title"])} ↗</a><p>{E(r["use"])}</p></li>')
    output.append('</ol>')
    return ''.join(output)

html=(ROOT/'template.html').read_text(encoding='utf-8')
slots={'ESSENTIALS':essentials(ROOT,docs),'TOC':toc(),'HUB':hub(),'MATRIX':synthesis(),'OVERVIEW':overview(),'TIMELINE':timeline(),'MAP':map_svg(),'COMPARISON':comparison(),'CREEDS':creeds(),'DIFFICULTIES':difficulties(),'SOURCES':sources(),'REPO':'https://github.com/07-Je-GT-Love-Personal-20260918/three-creeds-GTstudy','DATA':json.dumps({'places':fw['places'],'originals':{k:docs[k]['sections'][0]['text'] for k in CREEDS if k in docs}},ensure_ascii=False).replace('</',r'<\/')}
for key,value in slots.items():html=html.replace('@@'+key+'@@',value)
assert not re.search(r'@@[A-Z]+@@',html),'Unresolved template slots'
ids=re.findall(r'\bid="([^"]+)"',html)
assert len(ids)==len(set(ids)),'Duplicate IDs'
for anchor in re.findall(r'href="#([^"]+)"',html):assert anchor in ids,anchor
assert [len(comm[k]) for k in CREEDS]==[12,14,12]
OUT.mkdir(exist_ok=True)
supporting_page(ROOT,fw,slots)
(OUT/'index.html').write_text(html,encoding='utf-8')
(OUT/'.nojekyll').write_text('',encoding='utf-8')
shutil.copyfile(CONTENT/'cci-source-audit.md',OUT/'source-audit.md')
if (CONTENT/'text-comparison.md').exists():shutil.copyfile(CONTENT/'text-comparison.md',OUT/'text-comparison.md')
if docs:
    from library import build_library
    build_library(ROOT,docs,safe_original)
atlas_data=build_atlas(ROOT,fw,map_svg())
enhance_pages(ROOT)
enhance_v4(ROOT,fw,atlas_data)
print(f'Built {len(html):,} characters; 38 commentary units; {len(ids)} unique anchors.')
