---
name: luzzy-roster-writing
description: >
  Use when the Luzzy checklist (必读清单) hits the 文档编写 / 写作 / 文案创作 category —
  repository sub-items for documentation and copywriting: two anti-AI-writing skills.
  Answers "写文案怎么去AI腔" "stop-slop是什么" "对外文章的清单子项" "写README的规范清单".
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

# 文档编写 / 写作 / 文案创作 · 仓库子项明细

提示词 §1.1.6 命中「文档编写 / 写作 / 文案创作」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（2 条 → 全读）

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **stop-slop** `https://github.com/hardikpandya/stop-slop` | 正文——机器生成文本的特征清单与替换策略 |
| 2 | **avoid-ai-writing** `https://github.com/conorbronsdon/avoid-ai-writing` | 正文——同上，专治 AI 腔 |

这两项专治 AI 腔：过度对仗、空洞排比、三段式总结、emoji 装饰。写作纪律（受众、具体优于抽象、术语一致、全角标点）见提示词 §14.4——不读就写，产出会带明显机器痕迹。

## Examples

Input: 命中「文档编写 / 写作」
Output: 读本表 2 条 → 全读 → 按 §14.4 纪律写作 → 落回执。

Input: 润色既有对外文章
Output: 同上两条都读 → 再动笔 → 落回执。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.4；本 skill 只装清单明细。
