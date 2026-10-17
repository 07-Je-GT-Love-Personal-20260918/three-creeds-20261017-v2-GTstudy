> 更新：用户随后提供2015版完整PDF，并明确确认已获在三个公开网站与GitHub仓库使用六份全文的许可。下文的版权障碍是收到文件与授权声明前的审计记录，不再表示当前网站缺少全文。最新核对详见 text-comparison.md。

# CCI 来源与版本审计

核验日期：2026-10-17（用户时区 Asia/Taipei）。只读访问；未修改 sources/。

## 1. 六份文件的指定来源

| 文件 | 来源 |
| --- | --- |
| 使徒信经 | https://ccifellowship.org/books/book-of-praise/creeds/apostles-creed |
| 尼西亚信经 | https://ccifellowship.org/books/book-of-praise/creeds/nicene-creed |
| 亚他那修信经 | https://ccifellowship.org/books/book-of-praise/creeds/athanasian-creed |
| 比利时信条 | https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession |
| 海德堡要理问答 | https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism |
| 多特信经 | https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort |

这些页面隶属《敬拜手册》2015版。所谓“原文”须标成“指定网站中文译文”；不能让读者误以为这是古代希腊语、拉丁语或16世纪初版原语。

## 2. 转载许可与可执行方案

版权页：https://ccifellowship.org/books/book-of-praise 。页面明确标有版权归属和书面许可要求，未找到允许全文自由转载的许可。中文古代信经的内容古老，不代表现代译本自动属于公有领域；三项联合信条的现代译文同理。

本项目可制作原创逐条释义、有限短引文与准确来源链接。尚无权利人许可时，不应公开托管六份指定译文全文，也不应标注已获得许可。指定原站正文的用字、标点若引用必须逐字符核验，不能自动繁简转换、静默订正或混入其他译本。用户本机自行导入文本的阅读模式应明确其内容来源，不把导入文本打包发布。

原站响应包含 X-Frame-Options: SAMEORIGIN，因此跨站 iframe 不是可靠的阅读方案。主导航“联系我们”链接 https://ccifellowship.org/contact_us 在本次核验返回404，不能声称已联系版权方。

## 3. 版本细节与已发现的不一致

- 《使徒信经》引言明确不主张使徒亲笔合著；它描述罗马教会早期认信与后续形成。不要演绎为十二使徒一人写一句的史实。
- 《尼西亚信经》为传统西方使用的尼西亚—君士坦丁堡形态，包含 filioque。须区分325年尼西亚文本、381年君士坦丁堡扩展文本与西方后续添加；不能把当前文本每句话都标为325年会议原句。
- 《亚他那修信经》引言否认亚他那修为作者，说明拉丁西方背景，称6世纪上半叶已出现。具体作者及确切成文时间不确定，不宜给出确定人名或单一年份。
- 《亚他那修信经》本次实际HTML正文编号为1至42，连续无缺。引言却使用到43点的结构说明，二者不一致。教学注释宜以本页实际编号为准：1–2开场，3–28三一论，29–41道成肉身与审判，42收束。常见其他版本44分节不应套入这里。不可擅自把原站引言或正文改为某一常见版本。
- 《比利时信条》目录含37条；《海德堡要理问答》按52主日及三部编排；《多特信经》有第一、第二、第三／四、第五项四个结构单元，应保留其驳斥谬误部分，不能简化为仅五句口号。

## 4. 全站访问范围

直接检查17个入口：主页、敬拜手册、普世信经入口、三份信经、三项联合信条入口及三份文件目录、两种讲章目录、FAQ、robots.txt、两个常用sitemap地址、联系页。详细状态与发现链接见 cci-source-inventory.json。

robots.txt 返回200，未声明Sitemap；/sitemap.xml 与 /sitemap_index.xml 均404。这只能说明本次检查未发现这两个标准路径的站点地图，不能证明不存在其他索引。书籍导航另列烛台宣言、天上的礼物、圣经故事、真理的火焰、归正教会敬拜礼仪之美、I Belong。讲章和FAQ有独立索引／分页。

另对三项联合信条目录所链接的章节做有限递归元数据索引，见 cci-confession-index.json（标题、URL、状态）。索引发现不等于逐篇通读，不能声称“已吸收网站所有内容”。报告和成品应准确写为“已核查指定信经、相关信条与主题资料”。未储存或再发布版权正文。

## 5. 编写时必须分辨的层级

圣经是最高规范；普世信经与三项联合信条是教会从圣经归纳的认信；网站序言、讲章、FAQ属于可审查的说明材料。后者与正式认信不应赋予相同权威。

需要修正或避免沿用的表述：

1. 普世信经入口把来源拉回1世纪，教学应区分1世纪使徒教训根源与现存信经较晚形成。
2. 首页有关道成肉身的通俗说明容易把神说成肉身生父，并以生殖链解释无罪。应按圣子永恒受生、圣灵超自然使其取人性、基督真实无罪来澄清，避免神话式生殖观。
3. 尼西亚序言对325／381的简写不能抹去325年信经本身。东西方之争也不是只差一个词：需分辨希腊语与拉丁语发出术语、父为位格源头与子是否参与发出、以及教会会议权威。
4. 海德堡序言把腓德烈三世称王不够精确，应写普法尔茨选帝侯；对乌尔西努、俄利维亚努的贡献应避免把传统双作者说写成没有争论的定论。
5. 多特序言以现代五点口号概括抗辩派，不能替代1610抗辩书及后来发展的一手历史分析，特别是全然败坏与圣徒坚忍问题的表述。
6. FAQ将希伯来书作者直接称为保罗，教学须注明作者未署名、历史有不同归属传统。FAQ中医疗／心理学的概括不是信条内容，不要将其作为本项目实证医疗建议或把精神疾病一概归于个人犯罪。

## 6. 可核验的具体信条路径

- 比利时信条各条：https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession/9 （可按本次真实目录中的条号链接使用）。
- 多特第一项：https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort/section1
- 多特第二项：https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort/section2
- 多特第三／四项：https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort/section3-4
- 多特第五项：https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort/section5
- 海德堡主日1：https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism/lord-day-1

海德堡其他主日存在不同层级子路径，不能简单拼为顶层 lord-day-N；请从索引的实际链接引用。
