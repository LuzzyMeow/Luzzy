---
name: luzzy-roster-design-vue
description: >
  Use when the Luzzy checklist (必读清单) hits the 设计类子项 · Vue category —
  repository sub-items for Vue 3 / Nuxt design and component organization.
  Answers "Vue设计要读哪三条" "Nuxt UI的skill在哪" "写Vue页面读什么" "Vue组件库怎么选".
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

# 设计类子项 · Vue · 仓库子项明细

提示词 §1.1.6 命中「设计类子项 · Vue」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（3 条 → 全读（与设计基线叠加））

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **vuejs-ai/skills** `https://github.com/vuejs-ai/skills` | 取 `vue-best-practices` / `create-adaptable-composable` 等子技能 |
| 2 | **Nuxt UI** `https://github.com/nuxt/ui` | skill 在 `v4` 分支 `skills/nuxt-ui/`；官方接入页 `https://ui.nuxt.com/docs/getting-started/ai/skills` |
| 3 | **nuxt-skills** `https://github.com/onmax/nuxt-skills` | 正文 |

命中判据：写 / 改 Vue 组件与页面、UI 库选型与主题、Nuxt 界面；`.vue` 文件或 Vue / Nuxt 依赖即命中。

**与 `luzzy-roster-design` 的关系**：本 skill 管框架落地规范，基线四条管审美判断——叠加读，两边都缺一不可。

## Examples

Input: 命中 Vue / Nuxt 工程
Output: 基线 4 条 + 本表 3 条 = 7 条 → 回执分别列出。

Input: 跨框架同页（React + Vue 微前端）
Output: 本表与 `luzzy-roster-design-react` 各读 3 条 → 回执分别列出。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.1；本 skill 只装清单明细。
