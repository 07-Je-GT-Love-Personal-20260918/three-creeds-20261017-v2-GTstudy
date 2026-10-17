# 同一信仰 · 三大信经深读

欧陆改革宗视角的中文静态学习网站，版本 **2026-10-17 / v1.0**。

## 公开部署

- **GitHub Pages**：https://07-Je-GT-Love-Personal-20260918.github.io/reformed-three-creeds-20261017-v1/
- **Netlify**：https://reformed-three-creeds-20261017-v1.netlify.app/
- **Surge**：https://reformed-three-creeds-20261017-v1.surge.sh/
- **源文件仓库**：https://github.com/07-Je-GT-Love-Personal-20260918/reformed-three-creeds-20261017-v1

## 内容

- 从整本圣经与圣约神学进入三大普世信经。
- 18个历史节点、10个地理文化节点、38组深读及三经比较。
- 使徒信经12条、尼西亚信经14个教学段落、亚他那修信经12组覆盖网站正文42段。
- 六份完整中文原典；比利时37条、海德堡129问、多特各项教义与驳谬。
- 三份独立清洁阅读版、原文/记忆提纲切换、遮词、设备朗读、打印、下载、七日复习、六题自测。
- 可隐藏详细目录、搜索、阅读位置保存、字号、明暗主题、手机与平板适配。

## 页面

| 路径 | 内容 |
| --- | --- |
| `index.html` | 完整学习内容与记忆工坊 |
| `library.html` | 六份认信文本全部展开 |
| `reader-apostles.html` | 使徒信经清洁阅读版 |
| `reader-nicene.html` | 尼西亚信经清洁阅读版 |
| `reader-athanasian.html` | 亚他那修信经清洁阅读版 |
| `text-verification.json` | 逐节来源与正文校验摘要 |
| `text-comparison.md` | 用户PDF与网页的版本差异记录 |

## 文本与授权

六份认信文件的中文正文均来自 **https://ccifellowship.org/books/book-of-praise** 对应页面，不混用其他中文译本。用户提供2015版《敬拜手册》PDF，并明确确认已获公开使用许可。该许可声明来自用户；译文版权仍归原权利人，本仓库没有把译文重新许可为开源内容。用户PDF的彩色个人批注不作为信经正文。

原站的字词、标点、段号、脚注与参考经文均保留；只调整HTML排版。原文、历史介绍、原创神学解释分开显示。“原文”在此指指定网站的**中文译文**，不是希腊文或拉丁文原典。网站与PDF存在的差异单独记载，以网站当前正文为规范。

`content/fulltexts.json` 保存正文、来源与SHA-256。脚本在构建时验证摘要，再白名单处理排版HTML。原始网页整页HTML及用户完整PDF不公开保存。

没有宣称通读指定网站的全部文章。已审计17个入口及167个认信章节/目录页面，并选读相关要理、圣灵、洗礼、圣餐等资料。详见来源审计。

地理底图来自 Natural Earth 的公版1:110m数据，坐标近似，现代边界仅作定位参考；近邻点使用引线错开。字体使用 Google Fonts 的 Noto Serif SC，并提供本机宋体回退。插画和界面图示为本项目原创SVG。

## 本地开发

只需 Python 3.10+，不需要前端框架或打包器。

```sh
python build.py
python -m http.server 4173 -d dist
```

修改 `content/commentary.json`、`content/framework.json` 与 `template.html` 后重新构建。样式和交互在 `dist/styles.css`、`dist/app.js`。原典生成器为 `library.py`。

正式文本只应通过重新抓取并逐字核验来源更新；不要对其运行简繁转换、标点美化或自动润色。每次更新保留来源、访问日期和校验记录。

## 持续部署

推送 `main` 后，GitHub Actions 构建并部署 GitHub Pages，同时部署 Netlify 与 Surge。

- Pages 使用仓库内置令牌和OIDC，不需要保存个人GitHub密钥。
- Netlify 使用仓库Secret `NETLIFY_AUTH_TOKEN`；站点ID固定在工作流中。
- Surge 使用仓库Secret `SURGE_TOKEN`；域名固定在工作流中。
- 凭据不写入源码、HTML、README或日志；`.netlify` 与本地环境文件已忽略。

Netlify和Surge工作流重新部署当前提交；站点主体为 `dist/`。若删除部署凭据，更新对应仓库Secret即可恢复自动发布。不要把令牌直接放进工作流文本。

## 验证

`qa/browser-report.json` 保存桌面1440、平板820、手机390与320宽度的检查结果；涵盖目录锚点、横向溢出、原文阅读、地图、搜索、测验与主题切换。`qa/browser-check.cjs` 需要Playwright及Edge/Chromium，仅为开发检查依赖。

检查字体与排版需要实际浏览器；朗读使用设备自带语音，中文语音可用性因系统而异。阅读进度、个人导入文本与复习勾选只保存在访客浏览器本机，不上传。
