---
name: luzzy-roster-assets
description: >
  Use when the Luzzy checklist (必读清单) hits the 素材 / 图标 / 组件库 category —
  repository sub-items for icons, brand logos and UI component libraries; volume and license traps included.
  Answers "素材类哪个仓库不能整仓clone" "要现成的品牌logo去哪找" "Lobe Icons怎么接入" "游戏图标去哪找".
  Do NOT use for executing the task itself — discipline and red lines live in the Luzzy
  system prompt — nor for the reading gate, receipt, or triage logic, nor for other
  checklist categories or tasks unrelated to this one.
license: MIT
metadata:
  version: "1.0.0"
  author: "鹿溪 (LuzzyMeow)"
  category: "luzzy-roster"
  maturity: "L2"
---

# 素材 / 图标 / 组件库 · 仓库子项明细

提示词 §1.1.6 命中「素材 / 图标 / 组件库」后，读本文件拿仓库子项明细与执行细则。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（4 条 → 全读（读的是接入方式与许可条款，不是逐个素材文件））

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **Lobe UI** `https://github.com/lobehub/lobe-ui` | 正文；AIGC Web 组件库，基于 Antd，ESM only |
| 2 | **Lobe Icons** `https://github.com/lobehub/lobe-icons` | 接入方式；**不要 clone 整仓**——221MB，绝大部分是历史图标产物 |
| 3 | **Lobe Icons agent 接入页** `https://lobehub.com/icons/skill.md` | 组件用法、CDN 规则、`toc` 元数据、自定义图标写法——先读它再动手 |
| 4 | **Game Icon Pack** `https://github.com/Nieobie/game-icon-pack` | 接入方式；**不要 clone**——用 Releases 的 svg / png 压缩包；`Icon_Catalog.json` 就是给 LLM 检索用的，选图标先查它 |

许可：Lobe UI / Lobe Icons 为 MIT（**商标另算**——品牌 logo 放进对外产品前先确认该品牌方的商标使用政策，拿不准按 §五 澄清）；Game Icon Pack 为 CC0-1.0（无需署名，商用可）。商标边界见提示词 §14.11。

## 执行细则（提示词 §14.11 的操作明细）

**消费方式**（体积与「不要 clone」警示见上方子项表）：

- **Lobe UI**：`pnpm add @lobehub/ui`；ESM only；NextJS page router 需在 `next.config.js` 加 `transpilePackages: ['@lobehub/ui']`；`ConfigProvider` 必须包在 `ThemeProvider` **外层**（顺序反过来不工作）；默认样式方案是 `antd-style`。它是**依赖**，装它是拿组件，不是拿设计规范——视觉风格走提示词 §14.1
- **Lobe Icons**：接入文件先读子项表第 3 条。React 项目 `npm i @lobehub/icons`；静态产物用 `@lobehub/icons-static-svg` / `-png` / `-webp` 或直连 CDN。组件 id 是 PascalCase（`OpenAI`），CDN slug 是小写（`openai`）；变体按图标而异，用 `toc` 里的 `param` 确认
- **Game Icon Pack**：用 Releases 的 svg / png 压缩包，或按需取单个文件（选图标先查 `Icon_Catalog.json`，见子项表第 4 条）。本地浏览：`node server.js` → `http://localhost:3000`；在线预览：https://nieobie.github.io/game-icon-pack

## Examples

Input: 命中「素材 / 图标」
Output: 读本表 4 条（接入方式与许可）→ 选图标先查 `Icon_Catalog.json` → 落回执。

Input: 要把品牌 logo 放进对外产品
Output: 读完接入方式 → 按提示词 §14.11 确认商标政策 → 拿不准先问用户。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

纪律、红线与验收标准见提示词 §14.11；本 skill 装清单明细与操作性执行细则。
