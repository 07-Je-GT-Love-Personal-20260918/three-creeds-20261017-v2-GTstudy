"""Reliable geography, compact historical routes and shared navigation."""
from pathlib import Path
from html import escape as E
import json,re

ROUTES=[('apostles','Ⅰ','洗礼中的宣认','罗马 → 阿奎莱亚 → 拉丁西方','共同骨架，地域措辞，逐步定型。','roman','rome','aquileia','gaul'),('nicene','Ⅱ','争论中的澄清','亚历山大 → 尼西亚 → 君士坦丁堡','争论没有在325年结束；381年的展开同样关键。','council','alexandria','nicaea','constantinople'),('athanasian','Ⅲ','敬拜中的边界','东西方争论 → 拉丁教义归纳','一体三位，一位二性；名称不是作者署名证明。','boundary','antioch','chalcedon','gaul')]

def routes():
    paths=['<path d="M10 35h80m-64-6 8 6-8 6m43-12 8 6-8 6"/>','<path d="M10 35Q50 0 90 35M10 35Q50 70 90 35"/>','<path d="M13 10h74v50H13zM38 10v50M62 10v50"/>']
    cards=[]
    for i,(key,n,title,journey,why,_,*stops) in enumerate(ROUTES):
        cards.append(f'<article class="route-card theme-{key}"><div class="route-symbol"><span>{n}</span><svg viewBox="0 0 100 70" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">{paths[i]}<circle cx="10" cy="35" r="5"/><circle cx="50" cy="35" r="5"/><circle cx="90" cy="35" r="5"/></svg></div><h3>{title}</h3><p class="route-path">{journey}</p><p>{why}</p><div class="route-stops">'+''.join(f'<button type="button" data-atlas-stop="{s}">{j+1} · '+{'rome':'罗马','aquileia':'阿奎莱亚','gaul':'高卢','alexandria':'亚历山大','nicaea':'尼西亚','constantinople':'君士坦丁堡','antioch':'安提阿','chalcedon':'迦克墩'}[s]+'</button>' for j,s in enumerate(stops))+'</div></article>')
    return '<div class="route-grid">'+''.join(cards)+'</div><p class="small atlas-caption">以上为理解线索示意，箭头不表示某位作者的实际行程或精确传播路线。</p>'

def modern_map():
    return '''<section class="modern-map-panel" aria-labelledby="modern-map-heading"><div class="modern-map-heading"><div><span class="micro-label">真实地理 · 现代在线底图</span><h3 id="modern-map-heading">把历史地点放回今天的世界</h3></div><button type="button" id="map-load">◎ 打开可拖动地图</button></div><div class="map-services"><label>底图 <select id="map-provider"><option value="esri">Esri 全球街道图</option><option value="osm">OpenStreetMap 备选</option></select></label><button type="button" id="map-fit">⌖ 全部地点</button><button type="button" id="map-unload" hidden>收起在线地图</button><a id="map-external" href="https://www.openstreetmap.org/#map=4/40/20" target="_blank" rel="noopener">外部地图 ↗</a></div><p id="map-status" role="status">本地历史图始终可读。点击后才连接在线底图；可缩放、拖动、切换服务。</p><div id="modern-map" hidden aria-label="可缩放与拖动的现代地理地图"></div><p class="small">现代地图不是古代疆界，也不是实时卫星画面。任何在线服务都可能受地区网络影响；连接不佳时请切换服务或使用上方本地图。数据署名保留在地图内。</p></section>'''

def culture_cards(data,compact=False):
    places=data.get('places',[])
    if compact:places=[p for p in places if p['id'] in ['rome','nicaea','gaul']]
    out=[]
    for p in places:
        rows=[('为什么在这里',p['why']),('文化怎样影响表达',p['culture']),('必须分清',p['distinction'])]
        content=''.join(f'<div class="culture-row"><b>{label}</b><p data-note-scope="culture:{p["id"]}:{i}" data-note-label="{E(p["name"])} · {label}">{E(text)}</p></div>' for i,(label,text) in enumerate(rows))
        sources=' · '.join(f'<a href="{E(data["sources"][s]["url"])}" target="_blank" rel="noopener">{E(data["sources"][s]["title"])} ↗</a>' for s in p.get('sourceIds',[]) if s in data.get('sources',{}))
        out.append(f'<article class="culture-card" id="culture-{p["id"]}"><div class="culture-card-head"><span class="tag">⌖ {E(p["year"])}</span><button type="button" data-atlas-stop="{p["id"]}" aria-label="定位{E(p["name"])}">◎ 定位</button></div><h3>{E(p["name"])}</h3>{content}<details class="culture-recall"><summary>✦ 用一句话记住</summary><p>{E(p["recall"])}</p></details><div class="culture-sources">{sources}</div></article>')
    return '<div class="culture-grid">'+''.join(out)+'</div>'

def build_atlas(root,fw,map_svg):
    data=json.loads((root/'content/history-culture-v4.json').read_text(encoding='utf-8'))
    culture=culture_cards(data)
    scenes=''.join(f'<article class="atlas-scene {"is-current" if i==0 else ""}" data-atlas-scene="{i}"><button type="button" data-scene-pick="{i}" aria-pressed="{str(i==0).lower()}"><span>{i+1:02}</span>{E(x["step"])}</button><p>{E(x["point"])}</p></article>' for i,x in enumerate(data.get('storyline',[])))
    story='<section id="atlas-story"><div class="modern-map-heading"><div><span class="micro-label">记忆故事线 · 教学归纳</span><h2>十个地点，五步因果。</h2></div><button type="button" id="atlas-story-play" aria-pressed="false">▶ 顺着历史读一遍</button></div><div class="atlas-scenes">'+scenes+'</div><p class="small">演示只突出阅读次序，不代替精确年代；所有内容始终展开。</p></section>'
    html='''<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>历史 · 地图 · 文化 | 三大信经 GTstudy</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="v2.css"></head><body class="atlas-page"><header class="topbar"><a class="brand" href="index.html">✦ 三大信经深读</a><nav><a href="index.html#geography">返回主线</a> · <a href="library.html">原典</a></nav></header><main class="atlas-main"><div class="page-intro"><span class="eyebrow">HISTORY · PLACE · CULTURE</span><h1>把信经，放回真实世界。</h1><p>地点解释历史条件，文化解释表达方式；真理的根据仍是圣经。</p></div><section id="routes"><h2>三条线，记住三份信经</h2>'''+routes()+'''</section><section id="atlas-geography"><h2>先看关系，再看真实位置</h2><p>点选城市。下面的本地地理图无需连接地图服务，在线底图按需打开。</p><div class="map-panel">'''+map_svg+'''<div class="map-toolbar" id="map-buttons"></div><div class="place-info" id="place-info" aria-live="polite"></div></div>'''+modern_map()+'''<p class="small">本地地理轮廓：Natural Earth公版数据；标记为近似位置。南高卢仅是可能形成区域，不是确定作者故乡。</p></section><section id="culture"><h2>十个现场，抓住真实的因果</h2><p>历史叙述与原创教学概括，不是信经逐字引文。</p>'''+culture+'''</section><section id="language-bridge"><h2>语言不同，不能只按字面对号入座</h2><div class="language-bridge"><article><span>Α · 希腊语语境</span><h3>οὐσία / ὑπόστασις</h3><p>本质与位格的术语逐渐澄清；不同阶段的同一个词，未必已经具有后来的固定含义。</p></article><div aria-hidden="true">⇄</div><article><span>A · 拉丁语语境</span><h3>substantia / persona</h3><p>翻译必须忠于所指的真理。不能把现代“独立人格”直接套入古代位格，也不能把本质理解成可分割材料。</p></article></div><div class="note"><strong>文化是解释条件，不是真理的裁判。</strong>帝国召集会议、城市网络传播教义、礼仪塑造记忆；这些条件解释争论怎样发生，不能据此断言三一信仰只是政治产物。</div></section><footer class="footer"><a href="index.html">← 返回三份信经</a><span>GTstudy · 历史与文化学习页 · 2026.10.24</span></footer></main></body></html>'''
    html=html.replace('<section id="culture">',story+'<section id="culture">',1)
    html=html.replace('</div><section id="routes">','</div><nav class="atlas-local-nav" aria-label="地图页目录"><a href="#routes">三经示意</a><a href="#atlas-geography">真实地理</a><a href="#atlas-story">五步故事</a><a href="#culture">十个现场</a><a href="#language-bridge">语言桥梁</a></nav><section id="routes">',1)
    (root/'dist/atlas.html').write_text(html,encoding='utf-8')
    return data

def enhance_v4(root,fw,data):
    payload=json.dumps({'places':fw['places'],'culture':data.get('places',[])},ensure_ascii=False).replace('</',r'<\/')
    dock='''<nav class="corner-nav" aria-label="快捷导航"><div class="corner-nav-panel" id="corner-nav-panel" hidden><button type="button" data-nav="back" title="返回上一页" aria-label="返回上一页">←<small>返回</small></button><button type="button" data-nav="forward" title="前进一页" aria-label="前进一页">→<small>前进</small></button><button type="button" data-nav="top" title="到顶部" aria-label="到顶部">↑<small>顶部</small></button><button type="button" data-nav="bottom" title="到底部" aria-label="到底部">↓<small>底部</small></button><a href="index.html" title="主页" aria-label="主页">⌂<small>主页</small></a><a href="atlas.html" title="历史地图" aria-label="历史地图">◎<small>地图</small></a></div><button type="button" class="corner-nav-toggle" aria-controls="corner-nav-panel" aria-expanded="false" title="快捷导航" aria-label="展开快捷导航">⌘</button></nav>'''
    for file in (root/'dist').glob('*.html'):
        html=file.read_text(encoding='utf-8')
        html=html.replace('</head>','<link rel="stylesheet" href="v4.css"><script src="v4.js" defer></script></head>',1)
        if file.name=='index.html':
            html=html.replace('<div class="map-panel">', '<div class="geography-route-intro"><span class="micro-label">概念线索 · 真实地理 · 历史文化</span><h3>地图不是背景，而是理解线索。</h3></div>'+routes()+'<div class="map-panel">',1)
            marker='<div class="note"><strong>语言是历史条件，不是民族性格</strong>'
            html=html.replace(marker,modern_map()+'<div class="atlas-invite"><div><h3>十个现场，读清地点背后的因果</h3><p>从罗马洗礼、尼西亚会议，到拉丁西方的教义归纳。</p></div><a class="button" href="atlas.html">进入历史 · 地图 · 文化 ↗</a></div>'+culture_cards(data,True)+marker,1)
        if file.name in ['index.html','atlas.html']:
            html=html.replace('</body>',f'<script id="geography-data" type="application/json">{payload}</script></body>',1)
        html=html.replace('</body>',dock+'</body>',1)
        file.write_text(html,encoding='utf-8')
