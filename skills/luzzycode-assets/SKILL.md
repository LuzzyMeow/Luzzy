---
name: luzzycode-assets
description: >
  Use when a task needs ready-made visual assets or a UI component library —
  AI/LLM brand logos, AIGC web app components, or game icons — and the source,
  consumption method, and license terms must be settled first.
  Handles selection among Lobe UI, Lobe Icons, and Game Icon Pack; npm and CDN
  consumption; repository-size traps; and asset license discipline including the
  trademark boundary that MIT does not cover for brand logos.
  Triggers: "icon", "logo", "brand logo", "AI logo", "component library",
  "UI kit", "game icon", "素材", "图标", "组件库", "品牌 logo", "游戏图标".
  Do NOT use for deciding visual style, color, or layout (see luzzycode-design),
  or for building and testing a page (see luzzycode-webdev).
metadata:
  version: "1.0.0"
  author: "LuzzyMeow"
  category: "assets"
---

# LuzzyCode · 素材与组件库

<!-- self-link -->
> **所属体系**：[LuzzyCode](https://github.com/LuzzyMeow/LuzzyCode) · 本 skill 正文 `skills/luzzycode-assets/SKILL.md` · [仓库内路径](https://github.com/LuzzyMeow/LuzzyCode/tree/main/skills/luzzycode-assets) · [raw 直链](https://raw.githubusercontent.com/LuzzyMeow/LuzzyCode/main/skills/luzzycode-assets/SKILL.md)

## 三家素材（口径见常驻提示词 §1.1）

| 素材 | 提供什么 | 怎么拿 | 许可 |
|---|---|---|---|
| **Lobe UI** | AIGC Web 应用组件库（基于 Antd） | `pnpm add @lobehub/ui` | MIT |
| **Lobe Icons** | 200+ AI / LLM 品牌 logo（React 组件 + 静态 SVG / PNG / WebP） | `npm i @lobehub/icons` 或 CDN | MIT（仓库代码） |
| **Game Icon Pack** | 800+ 圆角游戏图标（SVG + PNG，含留白 / 不留白两版） | Releases 压缩包，或 `svg/` 目录 | CC0-1.0 |

**它们是素材，不是 skill**：不存在「读完全部正文才能动手」——按需取用，取到即用。需要通读正文的是技能型资源，走本预设的必读流程。

## 官方文档与入口（固化，不必再搜）

| 素材 | 文档 / 入口 | 用途 |
|---|---|---|
| Lobe UI | https://ui.lobehub.com | 组件文档（安装、Provider 嵌套、I18n） |
| | https://github.com/lobehub/lobe-ui | 仓库与 README |
| Lobe Icons | **https://lobehub.com/icons/skill.md** | **agent 接入文件**——组件用法、CDN 规则、`toc` 元数据、自定义图标写法，**动手前先读它** |
| | https://icons.lobehub.com | 组件文档站 |
| | https://lobehub.com/icons | 在线浏览全部图标 |
| Game Icon Pack | https://nieobie.github.io/game-icon-pack | 在线预览全部图标 |
| | https://github.com/Nieobie/game-icon-pack/releases | 打包下载（SVG / PNG，含中文版） |
| | https://github.com/Nieobie/game-icon-pack/blob/main/Icon_Catalog.json | 图标目录（给 LLM 检索用） |
| | https://nieobie.itch.io/free-icons | itch.io 发布页 |

npm 包（已实测存在）：`@lobehub/ui`、`@lobehub/icons`、`@lobehub/icons-static-svg` / `-static-png` / `-static-webp` / `-static-avatar`。

## 消费方式

### Lobe UI（`@lobehub/ui`）

- ESM only，`pnpm add @lobehub/ui`
- NextJS page router 需在 `next.config.js` 加 `transpilePackages: ['@lobehub/ui']`，否则 SSR 报错
- `ConfigProvider` 必须包在 `ThemeProvider` **外层**，顺序反过来不工作
- 默认样式方案是 `antd-style`
- 它是**依赖**：装它是为了拿到组件，不是拿到设计规范。视觉风格照常走 §1.1 设计四项

### Lobe Icons

- 官方提供 agent 接入文件：`https://lobehub.com/icons/skill.md`（含组件用法、CDN 规则、`toc` 元数据、自定义图标写法）。**先读它，再动手**
- React 项目：`npm i @lobehub/icons`
- 非 React / 静态产物：用 `@lobehub/icons-static-svg` / `-png` / `-webp`，或直连 CDN
- **不要 clone 这个仓库**——221MB，绝大部分是历史图标产物；npm 包与 CDN 足够
- 组件 id 是 PascalCase（`OpenAI`、`Claude`、`DeepSeek`），CDN slug 是小写（`openai`）
- 变体按图标而异（`Color` / `Brand` / `Text` / `TextCn` / `Combine` / `Avatar`），用 `toc` 里的 `param` 标记确认该图标支持哪些

### Game Icon Pack

- **不要 clone**：用 Releases 的 svg / png 压缩包，或按需取 `svg/` 目录里的单个文件
- `Icon_Catalog.json` 在仓库根，每条含 `component_name` / `visual_features` / `use_cases` / `synonyms` / `core_semantic`——**就是给 LLM 检索用的**。选图标先查它，不要靠猜名字
- 本地浏览全部图标：`node server.js` → `http://localhost:3000`
- 在线预览：`https://nieobie.github.io/game-icon-pack`

## 许可纪律

| 素材 | 许可 | 要做什么 |
|---|---|---|
| Lobe UI | MIT | 保留版权与许可声明 |
| Lobe Icons | MIT（仓库代码） | 保留声明；**商标另算**，见下条 |
| Game Icon Pack | CC0-1.0 | 无需署名，商用可 |

**品牌 logo 的商标边界（最容易踩的一条）**

MIT 覆盖的是仓库里的代码与打包产物，**不覆盖 logo 本身的商标权**。OpenAI、Claude、Google 这些 logo 属于各自品牌方。把某个品牌的 logo 放进对外产品，可能被理解成存在合作或背书关系。

- 内部工具、文档配图、模型选择列表：常规用法，按 MIT 走
- 对外产品、宣传材料：先确认该品牌方的商标使用政策；拿不准就按 §五 澄清问用户
- 不要用品牌 logo 暗示未经授权的合作关系

**统一纪律**

- 交付说明里写明素材**来源与许可**，别把第三方素材说成自产
- 离线 / 内网项目：把素材**落地到项目内**，不要留外部 CDN 依赖
- 素材落进**用户的项目**，不落进 LuzzyCode 仓库

## 与相邻 skill 的分工

| 场景 | 走哪 |
|---|---|
| 选视觉风格、配色、排版 | `luzzycode-design`（四项必读） |
| 页面结构、能不能跑、浏览器实测 | `luzzycode-webdev` |
| 做 PPT 时的配图规范 | `luzzycode-ppt` |
| 要一个组件或一个图标文件 | 本 skill |
| AI 生成图片 | 图像生成类 skill，不由本 skill 负责 |

## 示例

Input: 「帮我找一个 Claude 的 logo 放到模型列表里」
Output: 命中 Lobe Icons → 先读 `https://lobehub.com/icons/skill.md` → 用组件形式（`<Claude.Color />`）或 CDN slug（`claude`）→ 说明 MIT 与商标边界 → 落地到项目内

Input: 「给这个游戏后台配一套图标」
Output: 选 Game Icon Pack（CC0，无需署名）→ 查 `Icon_Catalog.json` 的 `synonyms` / `core_semantic` 定位图标 → 从 Releases 取 SVG → 交付时说明 CC0

Input: 「这个 React 项目想用 Lobe UI」
Output: 确认 ESM 与 NextJS `transpilePackages` 配置 → `pnpm add @lobehub/ui` → 提醒 `ConfigProvider` 包 `ThemeProvider` → 视觉风格另走设计四项

## Verify

- 素材是**按需取用**的，有没有误走「通读仓库」？
- 有没有 clone Lobe Icons 或 Game Icon Pack？两者都不该 clone：前者 221MB，后者用 Releases
- 交付说明里写明**来源与许可**了吗？
- 用到**品牌 logo** 时说明商标边界了吗？对外产品是否提示过风险？
- 离线 / 内网项目，素材落地到项目内了吗？
- 选图标前查过 `Icon_Catalog.json` 或 `toc`，还是靠猜名字？
- 素材落进用户项目，没有污染 LuzzyCode 仓库吧？
