---
name: luzzy-roster-design-react
description: >
  Use when the Luzzy checklist (必读清单) hits the 设计类子项 · React category —
  repository sub-items for React / Next.js design, shadcn/ui and component patterns.
  Answers "React设计要读哪三条" "shadcn的skill正文在哪" "写React组件读什么" "Next.js界面规范".
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

# 设计类子项 · React · 仓库子项明细

提示词 §1.1.6 命中「设计类子项 · React」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

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
| 1 | **shadcn/ui** `https://github.com/shadcn-ui/ui` | 官方正文 `skills/shadcn/SKILL.md` |
| 2 | **Vercel agent-skills** `https://github.com/vercel-labs/agent-skills` | 取 `react-best-practices` / `composition-patterns` / `react-view-transitions` / `web-design-guidelines` |
| 3 | **Anthropic 官方 frontend-design** `https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design` | 正文 |

命中判据：写 / 改 React 组件与页面、组件库与设计系统落地；`.tsx` / `.jsx` 或 React / Next 依赖即命中。

**与 `luzzy-roster-design` 的关系**：本 skill 管框架落地规范，基线四条管审美判断——叠加读，缺一不可。

## Examples

Input: 命中 React / Next 工程
Output: 基线 4 条 + 本表 3 条 = 7 条 → 回执分别列出。

Input: 设计系统规范本身作为产物
Output: 留设计类：基线 + 本表都读 → 不走 HTML 单文件那一类。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.1；本 skill 只装清单明细。
