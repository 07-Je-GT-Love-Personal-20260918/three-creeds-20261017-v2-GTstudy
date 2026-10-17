"""Full, flat, licensed confession library and three clean reading pages."""
from html import escape as E
import json

def build_library(root,docs,render):
    out=root/'dist'
    shell_start='''<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>认信原典 · 六份完整中文文本</title><link rel="icon" href="favicon.svg"><link rel="stylesheet" href="styles.css"><script src="library.js" defer></script></head><body class="library-page"><header class="topbar"><a class="brand" href="index.html">✦ 同一信仰 · 认信原典</a><div class="tools"><a href="index.html#union">返回深读</a><button id="lib-toc-toggle" aria-expanded="true">☰ 目录</button><button id="lib-print">打印</button></div></header><div class="layout"><aside class="toc" id="lib-toc"><div class="eyebrow">六份原典 · 章节导航</div><input class="toc-search" id="lib-search" type="search" placeholder="查找章节标题…" aria-label="查找章节标题">'''
    nav=[];body=['<main><div class="hero" style="min-height:0"><div class="eyebrow">THE CREEDS & THREE FORMS OF UNITY</div><h1 style="font-size:clamp(2.4rem,5vw,4rem)">认信原典</h1><p class="lead">三大普世信经 · 三项联合信条<br>六份完整中文正文，平铺阅读。</p><div class="note"><strong>版本与使用说明</strong>正文来自 ccifellowship.org 的《敬拜手册》2015版网页。用户提供同版PDF并确认已获公开使用许可；原译文版权仍归原权利人。保留网站字词、标点、段号、脚注与经文；仅调整网页布局。这里“原文”指指定中文译文，不是古希腊文或拉丁文原典。网页现存错字或编号差异不擅自改写。<a href="text-verification.json">查看逐节校验记录</a>。</div><p class="small">正文全部展开；桌面左侧目录可隐藏，手机用顶部目录按钮打开。浏览器内置查找可搜索全文。</p></div>']
    manifest=[]
    for key,doc in docs.items():
        nav.append(f'<a href="#{key}"><b>{E(doc["title"])}</b></a>')
        body.append(f'<section class="chapter" id="{key}"><div class="section-head"><div><div class="eyebrow">{E(key.upper())} · ORIGINAL TEXT</div><h2>{E(doc["title"])}</h2></div><a href="{E(doc["source"])}" target="_blank" rel="noopener">原站目录 ↗</a></div>')
        for i,s in enumerate(doc['sections']):
            sid=f'{key}-{i+1}'
            nav.append(f'<a class="sub" href="#{sid}">{E(s["title"])}</a>')
            body.append(f'<article class="original-panel original-section" id="{sid}"><h3>{E(s["title"])}</h3><div class="original-body">{render(s)}</div><div class="original-meta"><a href="{E(s["source"])}" target="_blank" rel="noopener">此节原站正文 ↗</a> · 正文 SHA-256：<code>{s["sha256"][:16]}…</code></div></article>')
            manifest.append({'document':key,'section':s['title'],'source':s['source'],'sha256':s['sha256'],'characters':len(s['text'])})
        body.append('</section>')
    body.append('<footer class="footer">六份正式文本与原创解读分别呈现。<a href="index.html">返回学习网站</a></footer></main></div></body></html>')
    (out/'library.html').write_text(shell_start+''.join(nav)+'</aside>'+''.join(body),encoding='utf-8')
    (out/'text-verification.json').write_text(json.dumps({'checked':'2026-10-17','source':'ccifellowship.org','normalization':'只改变HTML段落布局；hash针对抓取正文text字段的UTF-8字节，不是完整网页文件','sections':manifest},ensure_ascii=False,indent=2),encoding='utf-8')
    for key in ['apostles','nicene','athanasian']:
        if key not in docs:continue
        doc=docs[key];s=doc['sections'][0]
        page=f'''<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(doc['title'])} · 清洁阅读版</title><link rel="icon" href="favicon.svg"><link rel="stylesheet" href="styles.css"></head><body class="clean-page"><nav class="clean-nav"><a href="index.html#memorize">← 记忆工坊</a><a href="library.html">六份原典</a><button onclick="window.print()">打印</button></nav><main class="clean-reader"><div class="reader-title"><div class="eyebrow">CREDO · 指定版本原文</div><h1>{E(doc['title'])}</h1></div><div class="original-body">{render(s)}</div><footer class="original-meta">中文原文来源：<a href="{E(s['source'])}" target="_blank" rel="noopener">ccifellowship.org</a><br>《敬拜手册》2015版 · 2026年10月17日核对<br>依据用户提供的文本与公开使用许可制作。仅调整阅读排版，不改正文。</footer></main></body></html>'''
        (out/f'reader-{key}.html').write_text(page,encoding='utf-8')
