---
name: luzzy-roster-ppt
description: >
  Use when the Luzzy checklist (必读清单) hits the 做 PPT / 演示文稿 / 幻灯片 category —
  repository sub-items for slide decks: three PPT skills, read all three, install one.
  Answers "做PPT要读哪三家" "大狮PPT的正文在哪个子目录" "要导出pptx用哪家" "发布会风格的PPT用哪家".
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

# 做 PPT / 演示文稿 / 幻灯片 · 仓库子项明细

提示词 §1.1.6 命中「做 PPT / 演示文稿 / 幻灯片」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（3 条 → 全读（安装按需求择一，不要三家全装））

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **归藏PPT** `https://github.com/op7418/guizang-ppt-skill` | 横向翻页单文件 HTML；电子杂志×电子墨水 / 瑞士国际主义两套基调；WebGL 背景、演讲者视图——要设计感强的演讲 / 发布会风格 |
| 2 | **大狮PPT** `https://github.com/chuspeeism/dashi-ppt-skill` | 预置主题；可离线打开、浏览器里可编辑；支持导出 PPTX / PDF——要交付 .pptx / .pdf 时 |
| 3 | **HTML PPT Studio** `https://github.com/lewislulu/html-ppt-skill` | 模板驱动：36 主题 × 36 布局 × 20 画布特效 × 15 完整 deck——要快速出量、挑主题布局，或小红书图文排版 |

**安装要点差异**：归藏与 HTML PPT Studio 正文在仓库根；**大狮正文在 `skills/dashi-ppt/` 子目录**，需 Node.js 20+，导出 PPTX / PDF 要本机有 Chrome / Chromium / Edge。三家都依赖 `assets/` `references/` `templates/` 等资源目录——**必须整仓安装，只抓 `SKILL.md` 单文件拿不到可用能力**；安装前读该仓库 README 的安装章节，按 README 的命令装（多数支持 `npx skills add <owner>/<repo>`），不要自己发明命令。离线兜底：`git clone` 后把**含正文的那一层**拷进本机 skill 目录，拷完确认目标目录下能直接看到 `SKILL.md`；确认失败就别硬用，退回 `npx` 安装命令或改用另外两家。

## Examples

Input: 命中「做 PPT」，用户要 .pptx
Output: 三家正文都读对比 → 择大狮（可导出）→ 只装大狮（整仓）→ 落回执。

Input: 命中「做 PPT」，要发布会风格
Output: 三家都读 → 择归藏 → 安装归藏 → 落回执。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

纪律、红线与交付标准见提示词 §14.3；本 skill 装清单明细与安装要点差异。
