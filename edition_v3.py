"""Core argument notes and portable personal study tools."""
from html import escape as E
from pathlib import Path
import json,re

PALETTES=[('forest','林间纸页','绿意 · 温润'),('ocean','海盐晴蓝','清透 · 宁静'),('violet','葡萄暮紫','柔和 · 专注'),('amber','琥珀书灯','暖金 · 沉静')]

def core_data(root):
    p=Path(root)/'content/core-notes.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'notes':{},'synthesis':[]}

def core_note(root,uid):
    note=core_data(root).get('notes',{}).get(uid)
    if not note:return ''
    logic=''.join(f'<span class="logic-stop"><i>{i+1:02}</i>{E(x)}</span>' for i,x in enumerate(note['logic']))
    return f'''<aside class="core-note" aria-label="核心学习笔记"><div class="core-note-head"><span>✦ 核心笔记</span><span class="note-kind">主张 · 区分 · 推论</span></div><p class="core-thesis" data-note-scope="core:{uid}:thesis"><strong>{E(note['thesis'])}</strong></p><div class="core-distinction"><span class="distinction-label">必须分清</span><p data-note-scope="core:{uid}:distinction">{E(note['distinction'])}</p></div><div class="logic-chain" aria-label="论证逻辑">{logic}</div><details class="recall-card"><summary>◌ 闭卷自测：{E(note['recallQuestion'])}</summary><p data-note-scope="core:{uid}:recall">{E(note['recallAnswer'])}</p></details></aside>'''

def essentials(root,docs):
    data=core_data(root);cards=[]
    paths=['<path d="M7 19V6l10-3 10 3v13c0 8-10 12-10 12S7 27 7 19Z"/><path d="m12 16 4 4 7-8"/>','<path d="M7 7h8c5 0 9 4 9 9v10M7 7v9c0 5 4 9 9 9h9"/><path d="m20 21 5 5 5-5M3 7h8M7 3v8"/>','<path d="M17 31V15M17 21C5 21 3 12 4 7c9 0 14 5 13 14Zm0-5c0-9 5-13 13-13 0 8-4 14-13 13Z"/>']
    for i,x in enumerate(data.get('synthesis',[])):
        glyph=f'<svg class="essential-glyph" viewBox="0 0 34 34" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[i%3]}</svg>'
        cards.append(f'<article class="essential-card" data-essential="{i}"><span class="essential-number">{i+1:02}</span>{glyph}<h3>{E(x["title"])}</h3><p>{E(x["thesis"])}</p><div class="essential-question">自问：{E(x["question"])}</div></article>')
    if not cards:return ''
    rows=[('只剩宗教观念，救恩不必真实发生','被钉在十字架上','apostles','十字架、死亡、复活发生于历史，信心有所信靠的事实。'),('救主只是最高等级的受造物','受生却非被造，与父同质','nicene','唯有真正的神能救赎；尊称耶稣不等于承认他的完整神性。'),('父子圣灵是一个位格的三种面具','其位格不紊，其本质不分','athanasian','位格的真实区别与独一神性必须同时持守。'),('神性吞没人性，或分裂为两个基督','基督仍是一位，而非两位','athanasian','神人两性完整联合于同一位子，中保才能真实代表并拯救我们。'),('救恩只是灵魂离开物质世界','我相信身体复活','apostles','基督所救的是完整的人，终点包括身体复活与新创造。')]
    table=[]
    for error,quote,key,why in rows:
        source=docs[key]['sections'][0]
        assert quote in source['text'],quote
        table.append(f'<tr><td data-label="误区">{E(error)}</td><td data-label="原文锚点"><q class="anchor-quote">{E(quote)}</q><a class="quote-source" href="{E(source["source"])}" target="_blank" rel="noopener">{E(docs[key]["title"])} ↗</a></td><td data-label="所守护的救恩">{E(why)}</td></tr>')
    return '<div class="essentials"><div class="essential-heading"><div><span class="micro-label">抓住最短的论证链</span><h3>救恩不能缺少的三层逻辑</h3></div><button id="essential-step" aria-label="依次突出三层救恩逻辑">顺着想一遍 →</button></div><div class="essential-grid">'+''.join(cards)+'</div><div class="note-legend"><b>读笔记的方法</b><span class="legend-bold">粗体：核心主张</span><span class="legend-fill">底纹：救恩关键</span><span class="legend-dash">虚线：必须区分</span><span class="legend-line">实线：原文锚点</span></div><div class="core-table-wrap"><table class="core-table"><caption>五个误区，五个原文锚点</caption><thead><tr><th>误区</th><th>指定版本原文片段</th><th>所守护的救恩</th></tr></thead><tbody>'+''.join(table)+'</tbody></table></div></div>'

def controls(compact=False):
    buttons=''.join(f'<button type="button" class="palette-choice" data-palette-choice="{key}" aria-pressed="false"><span class="palette-dots" data-colors="{key}" aria-hidden="true"><i></i><i></i><i></i></span><span><b>{title}</b><small>{desc}</small></span></button>' for key,title,desc in PALETTES)
    return f'''<div class="study-tools {'compact' if compact else ''}" aria-label="主题与笔记工具"><div class="study-tool-heading"><span><b>◈ 阅读配色</b><small>选择喜欢的纸页氛围</small></span><div class="study-note-actions"><button type="button" data-notes-open>✎ 我的标记 <span class="note-count">0</span></button><button type="button" data-notes-visible aria-pressed="true">显示标记</button><button type="button" data-study-night aria-pressed="false">☾ 夜读</button></div></div><div class="palette-grid" role="group" aria-label="四套主题配色">{buttons}</div><p class="study-hint">在原文或解读段落选中文字，即可加粗、着色、加底纹、画实线或虚线，并附上笔记。<span class="theme-live" aria-live="polite"></span></p></div>'''

def panels():
    return '''<div id="selection-tools" class="selection-tools" hidden role="toolbar" aria-label="选中文字后的笔记标记"><span id="selection-preview"></span><div class="quick-mark-colors" role="group" aria-label="快速标记颜色"><button type="button" data-quick-color="gold" aria-label="金色标记" aria-pressed="false">金</button><button type="button" data-quick-color="red" aria-label="红色标记" aria-pressed="false">红</button><button type="button" data-quick-color="blue" aria-label="蓝色标记" aria-pressed="false">蓝</button><button type="button" data-quick-color="green" aria-label="绿色标记" aria-pressed="false">绿</button><button type="button" data-quick-color="purple" aria-label="紫色标记" aria-pressed="false">紫</button></div><button type="button" data-quick-mark="ink">A 字色</button><button type="button" data-quick-mark="bold">B 加粗</button><button type="button" data-quick-mark="fill">▨ 底纹</button><button type="button" data-quick-mark="solid">＿ 实线</button><button type="button" data-quick-mark="dashed">┄ 虚线</button><button type="button" id="mark-custom">✎ 更多 / 笔记</button><button type="button" id="selection-dismiss" aria-label="关闭选择工具">×</button></div>
<dialog id="mark-editor" class="study-dialog"><form id="mark-form"><div class="dialog-heading"><h2>标记这段话</h2><button type="button" data-close-dialog aria-label="关闭标记编辑">×</button></div><blockquote id="mark-quote"></blockquote><div class="mark-style-grid"><label><input type="checkbox" name="bold"> <b>加粗</b></label><label><input type="checkbox" name="ink"> 字体颜色</label><label><input type="checkbox" name="fill" checked> 底纹颜色</label><label><input type="checkbox" name="block"> 整段区块</label><label>下划线 <select name="underline"><option value="none">不加下划线</option><option value="solid">实线</option><option value="dashed">虚线</option></select></label></div><p id="mark-style-preview" class="mark-style-preview">重点不是记住术语，而是认清所信的神与救主。</p><fieldset class="mark-colors"><legend>选择标记颜色</legend><label><input type="radio" name="color" value="gold" checked><span data-note-color="gold">金</span></label><label><input type="radio" name="color" value="red"><span data-note-color="red">红</span></label><label><input type="radio" name="color" value="blue"><span data-note-color="blue">蓝</span></label><label><input type="radio" name="color" value="green"><span data-note-color="green">绿</span></label><label><input type="radio" name="color" value="purple"><span data-note-color="purple">紫</span></label></fieldset><label class="note-label" for="mark-note">自己的笔记（可选）</label><textarea id="mark-note" maxlength="5000" placeholder="用自己的话写下：这句话守护了什么？"></textarea><div class="dialog-actions"><button type="button" data-close-dialog>取消</button><button type="submit" class="save-mark">保存标记</button></div><p class="small">只保存在本机。标记改变显示样式，不改原文文字。</p></form></dialog>
<dialog id="notes-library" class="study-dialog notes-library"><div class="dialog-heading"><h2>我的重点与笔记</h2><button type="button" data-close-dialog aria-label="关闭笔记列表">×</button></div><div class="notes-library-actions"><button type="button" id="notes-export">↓ 导出笔记</button><label class="import-notes-label">↑ 导入笔记<input type="file" id="notes-import" accept="application/json,.json"></label><button type="button" id="notes-clear">清空本机标记</button></div><p class="small">导出文件可用于备份，或在另一个部署站点导入。切换网站域名时，本机存储不会自动同步。</p><input id="notes-search" class="notes-search" type="search" aria-label="搜索我的笔记" placeholder="搜索标记原句或自己的笔记"><div id="notes-list"></div><p id="notes-status" class="small" role="status"></p></dialog><div id="study-toast" class="study-toast" hidden role="status"></div>'''

def enhance_pages(root):
    for file in (Path(root)/'dist').glob('*.html'):
        html=file.read_text(encoding='utf-8')
        html=html.replace('<head>','<head><script src="theme-init.js"></script>',1)
        html=html.replace('</head>','<link rel="stylesheet" href="study.css"><script src="study.js" defer></script></head>',1)
        if file.name=='index.html':
            html=re.sub(r'(<div class="reading-toolbar".*?</div>)',lambda m:m.group(1)+controls(),html,count=1,flags=re.S)
        else:
            html=re.sub(r'(<main\b[^>]*>)',lambda m:m.group(1)+controls(True),html,count=1)
        html=html.replace('</body>',panels()+'</body>',1)
        file.write_text(html,encoding='utf-8')
