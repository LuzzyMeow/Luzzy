---
name: luzzycode-webdev
description: >
  Use when building HTML pages, web applications, static sites, or HTML artifacts,
  or when a page must be verified in a real browser.
  Handles selection among the Anthropic official skills, the Frontend Design
  Toolkit, and Superpowers, plus browser-based verification of the result.
  Triggers: "build a web page", "HTML artifact", "static site", "web app",
  "test the page in a browser", "网页", "HTML 页面", "静态站", "浏览器测试".
  Do NOT use for visual style and aesthetics (see luzzycode-design), for
  PowerPoint-style decks (see luzzycode-ppt), or for backend-only work.
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "web"
---

# LuzzyCode · HTML 网页开发

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-webdev/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-webdev) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-webdev/SKILL.md)

## 硬性前置：先读工具正文

| skill | 星数 | 拿它做什么 | 必须读吗 |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 176k | 取 [`web-artifacts-builder`](https://github.com/anthropics/skills)（生成 HTML 产物）与 `webapp-testing`（真浏览器测试） | **必读** |
| [Frontend Design Toolkit](https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit) | 1.1k | 70+ 前端工具的索引，找「该用哪个库/工具」时查 | 需要选型时读 |
| [Superpowers](https://github.com/obra/superpowers) | 285k | 通用研发方法论，写代码的完整流程 | 大型项目时读 |

**分工边界**：视觉风格与审美走 skill `luzzycode-design`（那 4 项设计 skill）；本 skill 管**能不能跑、能不能测、结构对不对**。

## 交付标准

1. **产物必须能直接打开**：单文件 HTML 用浏览器双击可看；多文件的给出启动命令
2. **必须真测**：用 `webapp-testing` 或等价的浏览器工具跑一遍，不要只看代码推断
3. **控制台无报错**：打开 DevTools 确认 console 干净
4. **响应式**：至少在窄屏（375px）与桌面（1440px）两个宽度下看过
5. **可访问性基础**：语义标签、`alt`、焦点可见、对比度——这几项**不因"只是 demo"而省**

## 与截图验收的关系

改完页面后，用图像读取工具（如 `read_image`）**亲眼看渲染结果**再判断，不要只读 CSS 推断（常驻提示词 §十）。看不到图就明说「未做视觉验收」，请用户确认。

## 示例

Input: 「做个数据看板页面」
Output: 读 Anthropic 官方 `web-artifacts-builder` → 确认数据来源与要展示的指标（有歧义先澄清）→ 生成单文件 HTML → 浏览器打开测试 → 截图看渲染 → 交付

Input: 「这个页面在手机上错位了」
Output: 读 `webapp-testing` → 用浏览器工具在 375px 宽度复现 → 定位是布局还是溢出 → 修 → 两个宽度都复测 → 截图对比

Input: 「帮我把这段终端输出做成一页好看的 HTML」
Output: 先看是**视觉呈现**还是**信息架构**——纯视觉走 `luzzycode-design`；结构 + 可交互走本 skill 的 `web-artifacts-builder`

## Verify

- 动手前：该读的 skill 正文读到了吗？
- 产物在浏览器里真的打开过吗？console 有报错吗？
- 窄屏与桌面两个宽度都看过吗？
- 用 `read_image` 看过渲染结果吗？没看就说「未做视觉验收」
- 可访问性四项（语义 / alt / 焦点 / 对比度）过了吗？
