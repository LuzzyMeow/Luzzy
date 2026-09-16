---
name: luzzy-roster-html
description: >
  Use when the Luzzy checklist (必读清单) hits the HTML / 网页开发 category —
  repository sub-items for HTML pages, landing pages, wireframes, prototypes and web games; seven entries, take four.
  Answers "HTML开发7条取4条，官方那两条是什么" "落地页用哪家skill" "网页游戏用哪家的技能" "线框图和交互原型用哪家".
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

# HTML / 网页开发 · 仓库子项明细

提示词 §1.1.6 命中「HTML / 网页开发」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（7 条 → 取 4 条（官方两项必读））

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **Anthropic 官方 skills** `https://github.com/anthropics/skills` | 取 `web-artifacts-builder`（出 HTML 产物）与 `webapp-testing`（跑真浏览器测试）——**每个 HTML 任务都读，是工程底线，不是风格选项** |
| 2 | **effective-html** `https://github.com/plannotator/effective-html` | 单文件 HTML 六件套：`html` 总路由 + `design-artifact` + `html-wireframe` 低保真线框 + `html-prototype` 交互原型 + `html-plan` 计划页 + `html-diagram` 图示——线框图、交互原型、plan 页、架构与流程图 |
| 3 | **taste-skill** `https://github.com/Leonxlnx/taste-skill` | 反 AI 味前端：三档旋钮（VARIANCE / MOTION / DENSITY）、设计系统映射表、重设计先审计——落地页 / 作品集 / 改版，尤其「一股模板味」时 |
| 4 | **garden-skills** `https://github.com/ConardLi/garden-skills` | `web-design-engineer` 设计工程（五档标定 + 25 套风格配方 + 评审五维打分）、`web-video-presentation` 录屏演示、`gpt-image-2` 出图——要成体系设计流程或录屏演示 |
| 5 | **MengTo/Skills** `https://github.com/MengTo/Skills` | 123 个技能：网页设计 81 + **网页游戏 20**（Three.js ARPG、关卡、敌人 AI、存档）——**网页游戏 / Three.js 交互**只有这一家覆盖 |
| 6 | **Frontend Design Toolkit** `https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit` | 前端视觉与交互工具箱——需要现成设计参照与组件思路 |
| 7 | **Superpowers** `https://github.com/obra/superpowers` | 通用工程方法论——需要更广的工程流程支撑时 |

**折减口径**：#1 的两项必读；其余六家按任务挑 2 家凑满 4 条。**读 ≠ 装**——不要七家全装，先看本机已有哪家。这几家都依赖 `assets/` `references/` `templates/` 等资源目录，**必须整仓安装**；安装前读该仓库 README 的安装章节，按 README 的命令装（多数支持 `npx skills add <owner>/<repo>`）。

反 AI 味纪律与交付标准（真测、控制台无报错、双宽度响应式、可访问性）见提示词 §14.2。

## Examples

Input: 命中 HTML 单文件任务
Output: 读 #1 两项 + 按任务挑 2 家 = 4 条 → 落回执 → 安装只装用到的（整仓）。

Input: 命中网页游戏（Three.js）
Output: #1 两项 + MengTo/Skills + taste-skill（或 garden）= 4 条 → 落回执。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.2；本 skill 只装清单明细。
