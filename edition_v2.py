"""Focused three-creed teaching, diagrams and supporting reading."""
from html import escape as E
import json,re

NAMES={'apostles':'使徒信经','nicene':'尼西亚信经','athanasian':'亚他那修信经'}
ICONS={'book':'M4 4h6l2 2 2-2h6v16h-6l-2 2-2-2H4z M12 6v16','spark':'M12 2l2.7 7.3L22 12l-7.3 2.7L12 22l-2.7-7.3L2 12l7.3-2.7z','route':'M5 4v11a4 4 0 0 0 8 0V9a4 4 0 0 1 8 0v11 M2 7l3-3 3 3 M18 17l3 3 3-3','pin':'M12 22s8-7 8-13a8 8 0 1 0-16 0c0 6 8 13 8 13z M9 9a3 3 0 1 0 6 0 3 3 0 1 0-6 0','shield':'M12 2l9 4v6c0 6-9 10-9 10S3 18 3 12V6z M8 12l3 3 6-6','cross':'M12 2v20 M5 9h14','sunrise':'M2 18h20 M5 14a7 7 0 0 1 14 0 M12 1v4 M3 5l3 3 M21 5l-3 3','layers':'M2 7l10-5 10 5-10 5z M2 12l10 5 10-5 M2 17l10 5 10-5','scroll':'M5 3h13v15a3 3 0 0 1-6 0H3v-2h9 M5 3a3 3 0 0 0 0 6h3 M8 7h7 M8 11h7','bulb':'M8 17v-1a7 7 0 1 1 8 0v1z M8 20h8 M10 23h4','headphone':'M3 14v-3a9 9 0 0 1 18 0v3 M3 12h4v8H3z M17 12h4v8h-4z','target':'M12 3a9 9 0 1 0 .01 0 M12 7a5 5 0 1 0 .01 0 M12 10v4 M10 12h4'}
def icon(name):return f'<svg class="vicon" viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS.get(name,ICONS["book"])}"/></svg>'

def hub():
    specs=[('apostles','01','route','故事','信仰的救恩故事，发生了什么？','父与创造 · 子降卑与升高 · 灵与新生命','从完整原文到十二条深读'),('nicene','02','sunrise','身份','为我们施行救恩的子与灵，究竟是谁？','325 / 381 · 同质 · 圣灵同受敬拜','从会议现场到十四段深读'),('athanasian','03','shield','边界','一体三位、一位二性，应当怎样理解？','位格不混 · 本质不分 · 基督完整两性','按指定版本覆盖全部42段')]
    out=['<div class="creed-hub" id="creed-hub" aria-label="三份信经学习入口">']
    for key,num,ico,word,q,terms,detail in specs:
        out.append(f'<article class="hub-card theme-{key}"><div class="hub-top"><span class="hub-icon">{icon(ico)}</span><span class="hub-number">{num}</span></div><span class="hub-word">{word}</span><h2>{NAMES[key]}</h2><p>{q}</p><div class="hub-terms">{terms}</div><div class="hub-links"><a href="#{key}">开始深读 ↗</a><a href="reader-{key}.html">纯净原文</a></div><small>{detail}</small></article>')
    out.append('</div>');return ''.join(out)

def guide(root,key):
    p=root/'content/creed-guides.json'
    all_guides=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    if 'guides' in all_guides:all_guides=all_guides['guides']
    if isinstance(all_guides,list):all_guides={x['key']:x for x in all_guides}
    g=all_guides.get(key,{})
    out=[f'<figure class="creed-illustration"><a class="figure-zoom" href="assets/creed-story-{key}.svg" target="_blank" rel="noopener" aria-label="放大{NAMES[key]}图解"><img src="assets/creed-story-{key}.svg" alt="{NAMES[key]}核心图解" loading="lazy" width="1200" height="500"></a><figcaption>{icon("layers")}原创教学图解 · 点图可放大 · 配合下文阅读</figcaption></figure>']
    if g:
        out.append(f'<div class="central-question">{icon("bulb")}<div><span class="micro-label">抓住核心</span><h3>{E(g.get("question",""))}</h3><p>{E(g.get("answer",""))}</p></div></div>')
        out.append('<div class="reading-context"><article><h3>'+icon('scroll')+'为什么形成这份信经？</h3><p>'+E(g.get('origin',''))+'</p></article><article><h3>'+icon('pin')+'身处怎样的文化区域？</h3><p>'+E(g.get('culture',''))+'</p></article></div>')
        story=g.get('story',[])
        out.append(f'<div class="guided-story theme-{key}" data-story="{key}"><div class="mini-header"><h3>{icon("route")}把历史连成故事</h3><button class="guide-play" data-guide-play="{key}" aria-pressed="false">▶ 顺序演示</button></div><div class="story-stops">')
        for i,s in enumerate(story):
            out.append(f'<article class="story-stop" data-scene="{i}"><div class="stop-step">{i+1:02}</div><span class="stop-date">{E(s.get("date",""))}</span><h4>{E(s["title"])}</h4><p>{E(s["body"])}</p><div class="stop-place">{icon("pin")}{E(s.get("place",""))}</div>')
            if s.get('source','').startswith('https://'):out.append(f'<a class="source-link" href="{E(s["source"])}" target="_blank" rel="noopener">核查来源 ↗</a>')
            out.append('</article>')
        out.append('</div><p class="small">历史场景均为说明性叙述；正文保持全部展开，演示仅依次突出节点。</p></div>')
        out.append(f'<div class="stakes-banner">{icon("shield")}<p><b>它守护什么？</b> {E(g.get("stakes",""))}</p></div>')
        out.append('<h3 class="diagram-heading">'+icon('book')+'把这份信经放回整本圣经</h3><div class="bible-steps">')
        for i,b in enumerate(g.get('bibleFlow',[])):
            out.append(f'<article><span class="step-label">{E(b.get("stage",str(i+1)))}</span><h4>{E(b["title"])}</h4><p>{E(b["body"])}</p><div class="scripture-ref">{E(b.get("bible",""))}</div></article>')
        out.append('</div>')
        out.append(f'<div class="covenant-link"><h3>{icon("layers")}圣约视角：这与神的应许有什么关系？</h3><p>{E(g.get("covenant",""))}</p></div>')
        out.append(f'<div class="memory-ribbon">{icon("target")}<div><b>一句话记住</b><p>{E(g.get("quickMemory",""))}</p></div></div>')
    out.append(lab(key))
    return ''.join(out)

def lab(key):
    if key=='apostles':
        stages=[('取了人性','因圣灵感孕，从童贞女马利亚所生','路1:35；腓2:6–8','永恒的子取了真实人性，进入他要救赎的人类处境。'),('受难与十架','在本丢·彼拉多手下受难，被钉在十字架上','可15；罗3:24–26','彼拉多把受难置于真实政治历史中；十字架是担当罪罚的救赎行动。'),('受死与埋葬','受死，被埋葬，降在阴间','林前15:3–4；海德堡问答44','真实死亡与降卑不可被淡化。海44把“降在阴间”连于基督为我们承担的极深痛苦，这是改革宗的认信解释。'),('从死里复活','第三天从死里复活','林前15:20–23','同一位耶稣身体复活，胜过死亡；不是仅留下值得纪念的精神影响。'),('升天与掌权','他升天，坐在全能父神的右边','徒1:9–11；罗8:34','救主为属他的人代求、治理万有。父的右边表达尊荣与权柄，不是用身体尺寸丈量神。'),('再来与完成','将来必从那里降临，审判活人死人','太25:31–46；启21–22','救恩走向公开完成与身体复活；审判者就是曾为信徒舍己的救主。')]
        out=['<div class="doctrine-lab theme-apostles" id="lab-apostles"><div class="mini-header"><div><span class="micro-label">动态流程图 · 逐点探索</span><h3>一位救主：降卑 → 升高 → 再临</h3></div>'+icon('route')+'</div><div class="journey-track">']
        for i,(t,q,b,body) in enumerate(stages):out.append(f'<button class="journey-node {"down" if i<3 else "up"}" data-journey="{i}" aria-pressed="{str(i==0).lower()}"><span>{i+1:02}</span><b>{t}</b></button>')
        out.append('</div>')
        for i,(t,q,b,body) in enumerate(stages):out.append(f'<article class="journey-note" data-journey-note="{i}" {"hidden" if i else ""}><h4>{t}</h4><blockquote>{E(q)}</blockquote><p>{body}</p><div class="scripture-ref">{b}</div></article>')
        out.append('<p class="small">引文为指定网站《使徒信经》原文片段；标题、经文定位与解释为教学补充。</p></div>');return ''.join(out)
    if key=='nicene':
        versions=[('325','尼西亚会议','明确拒绝把子归为受造物。受生与受造不能混同；子与父同具神性。','焦点：子与父的关系','不能把今天通行长文本逐字倒写为325年文件。'),('381','君士坦丁堡会议','通行尼西亚—君士坦丁堡文本更充分地宣认圣灵、教会、洗礼和末世盼望。','焦点：圣灵与整全宣认','其文本与381会议的关系由451会议记录明确见证；传承细节须保留历史分寸。'),('西方后续','“和子”条款','指定网站采用西方含“和子”的版本。589年托莱多是其传播关键节点，1014年罗马礼仪采用。','焦点：版本层次与东西方差异','“和子”不在381年原有希腊文本中；不能把后加条款说成原始共有文字。')]
        out=['<div class="doctrine-lab theme-nicene" id="lab-nicene"><div class="mini-header"><div><span class="micro-label">版本演进图 · 点击年代</span><h3>同一传统，必须分清三层文本历史</h3></div>'+icon('layers')+'</div><div class="version-rail">']
        for i,(y,t,body,f,c) in enumerate(versions):out.append(f'<button data-version="{i}" aria-pressed="{str(i==0).lower()}"><b>{y}</b><span>{t}</span></button>')
        out.append('</div>')
        for i,(y,t,body,f,c) in enumerate(versions):out.append(f'<article class="version-note" data-version-note="{i}" {"hidden" if i else ""}><span class="tag blue">{f}</span><h4>{y} · {t}</h4><p>{body}</p><p class="precision-note">{icon("bulb")}{c}</p></article>')
        out.append('<p class="small">此图说明版本与争论脉络，不意味着教会发明了新的神。完整时间线见后文。</p></div>');return ''.join(out)
    return '''<div class="doctrine-lab theme-athanasian" id="lab-athanasian"><div class="mini-header"><div><span class="micro-label">术语关系图 · 不是神的形象或构造图</span><h3>先分清：你正在谈“神”，还是“基督”？</h3></div>'''+icon('shield')+'''</div><div class="term-tabs"><button data-term="trinity" aria-pressed="true">三一论：一体 · 三位</button><button data-term="christ" aria-pressed="false">基督论：一位 · 二性</button></div><div class="term-panel" data-term-panel="trinity"><div class="concept-anchor">独一 · 不可分割的神性</div><div class="concept-branches"><div><b>父</b><span>非受造 · 非受生</span></div><div><b>子</b><span>非受造 · 由父受生</span></div><div><b>圣灵</b><span>非受造 · 由父与子而出</span></div></div><p class="concept-rule"><b>位格不混淆 · 本质不分割</b><br>不是三个神，也不是一位神的三个面具；关系有区别，神性无等级。</p></div><div class="term-panel" data-term-panel="christ" hidden><div class="concept-anchor">同一位 · 永恒之子耶稣基督</div><div class="concept-branches two"><div><b>完全神性</b><span>与父同质 · 永恒不改变</span></div><div><b>完整人性</b><span>人的身体、理性灵魂与意志</span></div></div><p class="concept-rule"><b>二性不混合 · 一位不分裂</b><br>子取了人性；神性没有转变成人性，基督也没有成为两个主体。</p></div><p class="small">标签是原创教学概括。指定正文第3–28段论三一，第29–41段论道成肉身及救恩；第1–2、42段表达救恩关切。</p></div>'''

def synthesis():
    rows=[('创造与救恩','父创造；子救赎；灵更新','同一创造主藉子造万物','救主并非次等神明'),('子是真神','承认独生子为主','受生非受造，与父同质','按神性与父同等'),('子是真人','马利亚所生；真实受难','道成肉身，成为人','有人的灵魂与肉体'),('圣灵是真神','承认圣灵','赐生命，与父子同受敬拜','与父子同永恒、同全能'),('教会与盼望','圣徒相通、赦罪、复活、永生','一间教会、洗礼、复活、来世','复活、审判与永恒结局')]
    out=['<div class="visual-matrix"><div class="mini-header"><h3>'+icon('target')+'看同一真理，怎样从三个角度展开</h3></div><div class="matrix-grid"><div class="matrix-heading">同一主题</div><div class="matrix-heading theme-apostles">使徒 · 故事</div><div class="matrix-heading theme-nicene">尼西亚 · 身份</div><div class="matrix-heading theme-athanasian">亚他那修 · 边界</div>']
    for row in rows:
        for i,t in enumerate(row):out.append(f'<div class="matrix-cell {"matrix-topic" if i==0 else ""}" data-label="{["主题","使徒","尼西亚","亚他那修"][i]}">{E(t)}</div>')
    out.append('</div><p class="small">表内为原创主题概括，不是逐字引文，也不代表三份信经各自只讲一个主题。</p></div>')
    return ''.join(out)

def supporting_page(root,fw,slots):
    p=root/'support-template.html'
    if not p.exists():return
    inner=p.read_text(encoding='utf-8')
    inner=inner.replace('@@OVERVIEW@@',slots['OVERVIEW'])
    intro='''<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>延伸阅读 · 圣经、圣约与认信互证</title><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="v2.css"></head><body class="support-page"><header class="topbar"><a class="brand" href="index.html">← 三大信经深读</a><nav><a href="library.html">六份原典</a></nav></header><main class="support-main"><div class="page-intro"><span class="eyebrow">SUPPORTING READING</span><h1>把信经，读回圣经。</h1><p>这里保留完整的圣经全景、圣约说明和三项联合信条互证，供需要时查阅。主线学习请返回三份信经。</p><nav class="support-nav"><a href="#panorama">圣经全景</a><a href="#covenant">圣约脉络</a><a href="#union">三项联合信条</a><a href="#application">信仰应用</a></nav></div>'''
    (root/'dist/background.html').write_text(intro+inner+'<footer class="footer"><a href="index.html">返回三大信经 →</a></footer></main></body></html>',encoding='utf-8')
