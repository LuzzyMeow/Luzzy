# 取 B 站 Cookie 的三种路径

B 站 AI 字幕需要登录态。匿名访问 `--list-subs` 只会返回 `danmaku`，拿不到 `ai-zh`。
本文件给出取 cookie 的路径，按可靠性排序。

## 路径一：Tabbit CLI（首选）

从浏览器的 Playwright 上下文直接取 cookie，**不受文件锁影响**，且能取到
`HttpOnly` 的 `SESSDATA`（`--cookies-from-browser` 在某些版本下取不到）。

前提：本机装了 Tabbit 浏览器（见 Luzzy §14.16）。

在 Tabbit `nodejs` 程序里执行，把 cookie 写成 Netscape 格式：

```js
const cookies = await context.cookies("https://www.bilibili.com");
const lines = ["# Netscape HTTP Cookie File", ""];
for (const c of cookies) {
  const expiry = Math.max(0, Math.floor(c.expires && c.expires > 0 ? c.expires : 0));
  lines.push([
    c.domain,
    c.domain.startsWith(".") ? "TRUE" : "FALSE",
    c.path || "/",
    c.secure ? "TRUE" : "FALSE",
    expiry,
    c.name,
    c.value,
  ].join("\t"));
}
const path = artifactPath("bili_cookies.txt");
await (await import("node:fs/promises")).writeFile(path, lines.join("\n") + "\n");
return {path, count: cookies.length, hasSessdata: cookies.some((c) => c.name === "SESSDATA")};
```

Windows 上把 JS 写进 UTF-8 临时文件，再用 `cmd /d /c "... nodejs --task <名> --request-id <id> < 文件"`
提交（PowerShell 管道与 here-string 会改写换行与编码）。

判断成功：返回的 `hasSessdata` 为 `true`。随后用返回的 `path` 作 `--cookies` 参数。

用完必须删除该文件——它等同于账号凭证。

## 路径二：yt-dlp 直读浏览器（回退）

```bash
yt-dlp --cookies-from-browser edge "<视频URL>" --list-subs --skip-download
# chrome / edge / firefox / safari 按本机实际选择
```

**仅当目标浏览器未运行时可用**。浏览器运行期间其 cookie 数据库被独占锁定，
yt-dlp 复制失败：

```
ERROR: Could not copy Chrome cookie database.
```

共享读方式（`FileShare.ReadWrite`）同样失败——Chromium 系浏览器持独占锁。
这不是参数问题，换写法无用，直接改走路径一。

## 路径三：手动导出（兜底）

用户用浏览器扩展导出 `cookies.txt`（Netscape 格式），或从开发者工具
（F12 → Application → Cookies）复制 `SESSDATA` 值，交给本技能使用。

适用于前两条路径都不可用、或用户不希望 Agent 接触浏览器配置的情况。

## Cookie 安全纪律

- cookie 文件**只落临时目录**（`%TEMP%` / `$TMPDIR`），文件名带用途，用完立即删
- **绝不入库**：确认 `.gitignore` 覆盖 `.env` / `*cookies*` / `*.key` 一类的模式
- **绝不外发**：不写进日志、不贴进回答、不发往任何第三方服务
- 只取 `bilibili.com` 域的 cookie，不要整库导出
- 会话结束前删干净；用户要求「保留以便下次用」时，说明凭证风险并让其自行决定
