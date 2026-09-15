---
name: luzzy-bilibili-notes
description: >
  Use when the user provides a Bilibili video link or BV number and wants its
  content extracted: "提取B站视频", "B站视频转文档", "把这个B站视频整理成笔记",
  "B站视频转文字", "帮我把这个视频转成文字", "抓这个视频的字幕",
  "帮我看看这个视频讲了什么", "这个视频讲了啥", "这个视频说了什么",
  "把视频和评论一起整理出来", "抓一下这个视频的评论",
  "看看这个视频的简介和评论都说了啥", "这个视频下面大家都在讨论什么",
  "帮我提取这个视频的标题简介字幕和全部评论", "bilibili 视频 笔记",
  "BV号 转 文章", "BV 号提取内容", "b23.tv 短链提取", "字幕转 markdown",
  "视频内容整理成文档".
  Handles four retrievals by default: title, description, AI subtitle (ai-zh),
  and all public comments including replies. Also handles SRT parsing, transcript
  restructuring into a structured Markdown note, and collection (multi-part)
  directory extraction.
  Do NOT use for bulk or site-wide crawling, bypassing WBI signing or risk
  control, accessing paid/OGV/P-charge content, downloading the media file
  itself, reverse-looking-up danmaku senders' identities, rendering notes to
  HTML, or building player components.
license: MIT
compatibility: >
  requires: python>=3.10, yt-dlp (pip install -U yt-dlp).
  Bilibili subtitles and comments require a logged-in session; anonymous access
  returns danmaku only. Preferred cookie source is the Tabbit browser CLI (see
  Luzzy §14.16); fallback is yt-dlp --cookies-from-browser, which fails while
  that browser is running.
metadata:
  version: "1.1.0"
  author: "鹿溪 (LuzzyMeow)"
  category: "content-extraction"
  maturity: "L2"
---

# B 站视频转结构化笔记

把 B 站视频的标题、简介、AI 字幕与全部公开评论提取出来，重组为可检索的 Markdown 笔记。

## Default Retrieval Scope

默认抓取**四项**，缺一不可：

| # | 内容 | 取法 |
|---|---|---|
| 1 | 视频标题 | `scripts/fetch_video_info.py` |
| 2 | 视频简介 | `scripts/fetch_video_info.py` |
| 3 | 视频字幕（`ai-zh`） | yt-dlp（步骤 3） |
| 4 | 全部公开评论（含二级回复） | `scripts/fetch_video_info.py` |

用户只问「讲了什么」也要按四项取——这是默认范围，不是可选增项。
用户明确说只要某一项时才收窄。

## Workflow

1. 归一化输入为 BV 号。

   从用户给的链接中提取 `BV` 号（`https://www.bilibili.com/video/BV...`、
   `b23.tv` 短链、`/list/watchlater?...&bvid=BV...` 都含 BV 号）。短链与列表链接
   一律改写成标准形式 `https://www.bilibili.com/video/<BV号>` 再使用。

   Verify: 拿到规范的视频 URL，且 BV 号长度为 12 位。

2. 确定 cookie 来源，拿到登录态。

   按顺序尝试，第一个成功的即采用：

   - **首选 Tabbit CLI**（不受浏览器文件锁影响，且能取到 HttpOnly cookie）：
     在 `nodejs` 程序里取 `await context.cookies("https://www.bilibili.com")`，
     写成 Netscape 格式文本文件，路径落在临时目录。写法见
     [references/cookie-sourcing.md](references/cookie-sourcing.md)。
   - **回退 `--cookies-from-browser <chrome|edge|firefox>`**：仅在目标浏览器
     **未运行**时可用。
   - 两者都不可用 → 走步骤 7 的失败路径，不要凭空继续。

   cookie 文件必须落在临时目录（`%TEMP%` / `$TMPDIR`），并在步骤 6 删除。

   Verify: `yt-dlp --cookies <文件> --list-subs` 输出中出现 `ai-zh` 行，而不是
   只有 `danmaku`。只有 `danmaku` 说明没拿到登录态，回到本步换 cookie 来源。

3. 抓取元数据与全部评论（标题 / 简介 / 评论三项）。

   ```bash
   python scripts/fetch_video_info.py "<BV号或视频URL>" \
     --cookies <cookie文件> --out "<临时目录>/bili_info.json"
   ```

   脚本一次取齐：视频标题、简介、UP 主、时长、分 P 目录、全部公开评论（含二级回复）。

   参数说明：
   - `--cookies` 必需，Netscape 格式 cookie 文件
   - `--out` 必需，输出 JSON 路径，落临时目录
   - `--max-pages` 可选，各接口翻页上限，默认 10
   - `--no-comments` 可选，只取元数据与分 P 目录

   接口契约、四个实测陷阱与完整性判据见
   [references/metadata-and-comments.md](references/metadata-and-comments.md)。

   Verify: JSON 里 `video.title`「`video.desc`」非空，`comments` 数组非空，
   且 `comments_summary` 给出了 `total_fetched` 与 `declared_count`。

4. 下载 AI 中文字幕。

   ```bash
   yt-dlp --cookies <cookie文件> "<视频URL>" \
     --write-subs --sub-lang ai-zh --skip-download --no-simulate \
     -o "<临时目录>/bili_output"
   ```

   `--no-simulate` 是必需的：带 `--print` 或单独用 `--skip-download` 时，
   yt-dlp 可能只打印而不落盘字幕文件。

   聚合（多分 P）视频默认会拉全部 P，**只处理用户指定的那一集**时加 `--no-playlist`
   并在 URL 上带 `?p=<集数>`。

   Verify: 临时目录出现 `bili_output.ai-zh.srt`，且非空。

5. 解析 SRT 并重组为笔记。

   用解析脚本把 SRT 转成纯文本，再读它做语义重组：

   ```bash
   python scripts/parse_srt.py "<字幕.srt>" --timestamps
   ```

   - `--timestamps` 保留 `[mm:ss]` 标记，便于回视频核对；不要则省略
   - `--out <路径>` 写入文件；省略则打到标准输出

   读到文本后按下列规则处理：

   - 合并被切碎的连续句为完整句子
   - 按语义划分章节（主题切换、步骤分节、概念定义、代码与配置）
   - 修正明显的语音识别错误（见 [references/asr-corrections.md](references/asr-corrections.md)）
   - 保留无法确定原词的表述，并在文末「存疑待核」列出，不做推测性改写

   输出结构照 [references/note-template.md](references/note-template.md)，
   该模板含元数据区、评论汇总区与整理说明区。

   Verify: 笔记含标题、来源元信息（BV 号 / UP 主 / 时长）、分节正文、
   评论汇总、以及「整理说明」段（已修正项 + 存疑项 + 由 AI 生成的自述）。

6. 落盘并清理。

   笔记写到用户指定位置；未指定则写工作区，文件名用 `{视频标题}.md`。
   删除 cookie 文件、临时 SRT 与临时 JSON。

   Verify: 笔记文件存在且非空；cookie 文件已删除（`Test-Path` / `ls` 应为否）。

7. 失败路径（按症状处理）。

   | 症状 | 处理 |
   |---|---|
   | 字幕列表只有 `danmaku` | 登录态缺失。换 cookie 来源重试步骤 2；用户未登录 B 站时如实告知「该视频字幕需要登录态，暂无法提取」 |
   | 该视频无 `ai-zh` 字幕 | 视频未开启 AI 字幕。告知用户，并提议改用元数据与评论做简版笔记（需用户同意） |
   | `Could not copy Chrome cookie database` | 浏览器正在运行、cookie 库被锁。改用步骤 2 的首选路径（Tabbit CLI） |
   | 实抓评论数少于页面显示 | **正常现象，不是遗漏**。差值来自已删除或隐藏的评论，它们仍计入总数但接口不再返回。如实报告 `comments_summary.gap`，不假装取全 |
   | 评论接口返回 `-352` / `-412` / `-509` 或 HTTP 403/412/429 | 触发风控。**立即停止请求**，告知用户，不重试、不换 IP、不换 UA、不调参数对抗 |
   | `--cookies-from-browser` 报文件锁 | 见上一行，改走 Tabbit CLI |
   | `yt-dlp` 未安装 | `python -m pip install -U yt-dlp` |
   | 聚合视频误抓全部 P | URL 加 `?p=<集数>`，命令加 `--no-playlist` |

## Compliance Boundary

只处理**公开可见视频的标题、简介、字幕、公开评论与元数据**，且以用户自己的登录态访问。

禁止：批量或全站抓取、绕过 WBI 签名与风控、访问付费/OGV/充电专属内容、
下载视频本体、通过弹幕反查发送者身份。这些是被平台明确主张侵权的行为，
已有律师函先例（见 [references/compliance.md](references/compliance.md)）。

用户要求上述任一行为 → 拒绝并说明理由，改为提供公开数据的合法替代方案。

## Examples

Input: 「把这个B站视频整理成笔记 https://www.bilibili.com/video/BV11q8J6CEZS」
Output: 临时目录得到 `bili_output.ai-zh.srt`（183 条）→ 重组为分十节、
含元数据区与「整理说明」段的 Markdown 笔记 → 落盘为 `{视频标题}.md`，
cookie 与 SRT 已删除。

Input: 「把这个视频和评论一起整理 https://www.bilibili.com/video/BV1La8j6nEwY」
Output: 归一化为标准 URL → 从 Tabbit CLI 取 cookie →
`fetch_video_info.py` 取到标题（76 字符）、简介（419 字符）、
一级评论 20 条 + 二级回复 14 条 = 34 条，页面声明 38 条（差 4 条为已删除评论）→
yt-dlp 取 `ai-zh` 字幕 → 笔记含「评论汇总」区，写明实抓数与声明数的差异。

Input: 「提取B站视频 https://www.bilibili.com/list/watchlater?oid=117122197882715&bvid=BV11q8J6CEZS&spm_id_from=...」
Output: 归一化为 `https://www.bilibili.com/video/BV11q8J6CEZS` → 因 Edge 正在运行
导致 `--cookies-from-browser` 失败 → 改从 Tabbit CLI 取 cookie 成功 →
`--list-subs` 确认有 `ai-zh` → 正常出笔记。

## Verify

- [ ] 输入已归一化为标准视频 URL，BV 号正确？
- [ ] 四项都取到了：标题、简介、字幕、全部评论（含二级回复）？
- [ ] `--list-subs` 确认到 `ai-zh`（而非只有 `danmaku`）才开始下载？
- [ ] 下载命令带 `--no-simulate`？
- [ ] 评论逐条核对过（每个 `rcount` == 实取子回复数）？差值如实写进笔记？
- [ ] 笔记含元数据区、评论汇总与「整理说明」段（已修正项 / 存疑项 / AI 生成自述）？
- [ ] cookie 文件与临时 SRT、临时 JSON 已删除？
- [ ] 全程只读公开数据，未触碰 Compliance Boundary 的禁止项？

## Reference Files

| File | Load when |
|------|-----------|
| [references/metadata-and-comments.md](references/metadata-and-comments.md) | 抓元数据与评论，或需要弄清接口契约、完整性判据、风控处置 |
| [references/cookie-sourcing.md](references/cookie-sourcing.md) | 需要取 B 站 cookie，或 `--cookies-from-browser` 报文件锁错误 |
| [references/note-template.md](references/note-template.md) | 要生成笔记正文，需要标准结构与措辞 |
| [references/asr-corrections.md](references/asr-corrections.md) | 重组字幕时，需要判断某个词是否为识别错误 |
| [references/compliance.md](references/compliance.md) | 用户要求批量抓取、绕过风控、付费内容，或需要说明边界依据 |

## Scripts

| Script | Run | Purpose |
|------|-----|---------|
| [scripts/fetch_video_info.py](scripts/fetch_video_info.py) | `python scripts/fetch_video_info.py <BV号> --cookies <文件> --out <JSON>` | 取标题、简介、UP 主、分 P 目录与全部公开评论 |
| [scripts/parse_srt.py](scripts/parse_srt.py) | `python scripts/parse_srt.py <字幕.srt> [--timestamps]` | SRT 转纯文本，合并碎片句 |
