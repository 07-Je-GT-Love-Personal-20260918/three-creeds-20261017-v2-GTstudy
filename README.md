# 三大信经深读 · GTstudy v2

主题：使徒信经、尼西亚信经、亚他那修信经。版本：**2026-10-17 · v2.0**。

## 三个公开站点

- **GitHub Pages**：https://07-je-gt-love-personal-20260918.github.io/three-creeds-20261017-v2-GTstudy/
- **Netlify**：https://three-creeds-20261017-v2-gtstudy.netlify.app/
- **Surge**：https://three-creeds-20261017-v2-gtstudy.surge.sh/
- **同一仓库的新地址**：https://github.com/07-Je-GT-Love-Personal-20260918/three-creeds-20261017-v2-GTstudy

仓库从 `reformed-three-creeds-20261017-v1` 重命名而来，编号仍为1423064988。保留已有提交、权限、部署Secret与历史记录。

## 本轮更新

三份信经成为首页主线。先给简明的整本圣经与圣约总览，立即进入三份信经；较长的系统背景和三项联合信条介绍放到延伸阅读页，原典仍完整保留。

- 正文默认约21–22px；原文默认22–24px，独立清洁版23–25px。可连续调节18–30px，并记住个人偏好。
- 使徒经、尼西亚经、亚他那修经分别以绿、蓝、紫为记忆配色。
- 3幅原创SVG主题图，可单独放大；3组互动图解：降卑与升高、325/381/西方后续、三一与基督两性。
- 每经各4个真实历史场景、4段圣经主线，并有起源、文化、救恩关切、圣约解释和一句记忆提示。
- 历史故事可顺序演示；救赎故事可播放；阅读进入动画、轻浮动与交互反馈可关闭，并尊重系统减少动态效果的设置。
- 38组逐段深读完整保留：使徒12条、尼西亚14个教学段落、亚他那修12组覆盖指定正文42段。
- 新增主题矩阵；手机上的比较表自动纵向展开，主要内容平铺显示。
- 主站有15项三经相关历史节点与10个相关地理节点。16世纪认信背景保留在辅助阅读中。
- 3份独立原文阅读版；原文/提纲切换、设备朗读、遮词揭示、下载、打印、7日复习与6题自测。

## 页面与源文件

| 页面 | 用途 |
| --- | --- |
| `index.html` | 三份信经的主要学习内容 |
| `reader-apostles.html` | 使徒信经清洁版 |
| `reader-nicene.html` | 尼西亚信经清洁版 |
| `reader-athanasian.html` | 亚他那修信经清洁版 |
| `library.html` | 六份指定中文原典全部展开 |
| `background.html` | 完整圣经/圣约背景与三项联合信条互证 |
| `text-verification.json` | 232个正文单元的来源与摘要 |
| `text-comparison.md` | 用户PDF与网页的版本差异 |

构建源文件为 `build.py`、`edition_v2.py`、`library.py`、`template.html`、`support-template.html` 与 `content/`。界面资源在 `dist/styles.css`、`dist/v2.css`、`dist/app.js`、`dist/v2.js` 及 `dist/assets/`。阅读图解不直接绘制父神或把图形当作神的构造；术语图仅说明认信表达。

## 正文忠实性与来源

六份正式中文文本统一来自 https://ccifellowship.org/books/book-of-praise 对应页面。用户提供2015版完整手册PDF，并明确确认已获公开使用许可；译文版权仍归原权利人，不因本仓库公开而重新许可为开源内容。

`content/fulltexts.json` 的全部正文、安全排版HTML、来源、校验字段在v2保持与v1完全相同。构建验证SHA-256后再按白名单输出HTML。原文、历史叙述与原创解释分别标识；只调整阅读样式，不自动改写字词、标点或段号。PDF的彩色个人批注不纳入正文，PDF与网站差异单列，以指定网站当前正文为准。

本库按指定版本所载范围完整呈现：三经各1节、比利时37条、海德堡129问、多特59正面条款及4组驳谬，共232单元。网站及用户PDF未收其他版本所附的独立多特结语，因此不以别的译文补入。此处“原文”指指定中文译文，不是希腊或拉丁原典。

已审计17个入口及167个认信章节/目录页面，并择要研究相关书籍、讲道与仪文；没有宣称穷尽指定网站的所有文章。史料、古代文本和改革宗官方资料的具体用途可在网页来源区追查。

地理底图使用Natural Earth公版数据；现代坐标用于近似定位，不代表古代疆界。三幅新图为原创SVG；Noto Serif SC字体来自Google Fonts，并设本机字体回退。

## 本地开发与持续部署

只需Python 3.10+，无需前端打包器：

```sh
python build.py
python -m http.server 4173 -d dist
```

推送`main`后，两个GitHub Actions工作流构建并发布三个平台。Pages使用OIDC；Netlify使用仓库Secret `NETLIFY_AUTH_TOKEN`，Surge使用`SURGE_TOKEN`。原Netlify站点编号保持 `36b7cc36-7833-41b9-994f-e2c88c957ad6`，只更新名称与域名。凭据不写入源码或公开文件；`.netlify`和本地环境文件已忽略。

改变正式文本时必须重新核对指定网站并更新来源/摘要，不对其使用自动润色、标点替换或简繁转换。

## 验证

`qa/v2-report.json`记录1920、1440、820、390、320宽度的排版与互动检查；`qa/originals-report.json`记录232单元及3份清洁版的正文核对；`qa/v2-original-preservation.json`记录v1到v2正式数据没有改变。

开发检查可选安装Playwright，并使用Edge/Chromium运行：

```sh
node qa/browser-check.cjs
node qa/v2-check.cjs
node qa/originals-check.cjs
```

正文全部展开，动画不作为显示内容的前提。个人导入、字号、阅读位置与复习记录仅保存在浏览器本机。朗读依赖设备中文语音；已检查交互入口，不宣称验证了所有设备的音色与播放能力。

### V2上线验收（2026-10-17）

三个平台均已公开上线：每站17项页面及资源，共51项检查全部HTTP 200；首页均确认V2内容。每站232个正式文本单元逐一与校对数据一致，仅忽略排版空白。线上手机版版本图和基督两性图切换通过。

1920、1440、820、390、320宽度没有检测到页面横向溢出、顶栏重叠或图片损坏。正文实测22px，桌面原文24px，手机原文22px。原文数据与v1保持相同。详见 `qa/v2-report.json`、`qa/v2-public-deployment-report.json` 与 `qa/v2-live-originals-report.json`。

Pages运行39043699326、Netlify/Surge运行39043699430均成功；上线内容提交为 `2cf1bed`。后续提交只补充此验收记录。
