---
name: luzzy-roster-code-review
description: >
  Use when the Luzzy checklist (必读清单) hits the 代码审查 category —
  repository sub-items for code review: four review skills, read all, execute per need.
  Answers "代码审查用哪四家" "审PR的清单子项" "shippie是什么" "安全和性能问题用什么审".
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

# 代码审查 · 仓库子项明细

提示词 §1.1.6 命中「代码审查」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（4 条 → 全读（执行时按需求择一，与 Ponytail 的 `-review` 配合））

| # | 条目 | 读什么 |
|---|---|---|
| 1 | **Agent Skills（含 code-review-and-quality）** `https://github.com/addyosmani/agent-skills` | 正文 |
| 2 | **Open Code Review** `https://github.com/alibaba/open-code-review` | 正文 |
| 3 | **sanyuan-skills** `https://github.com/sanyuan0704/sanyuan-skills` | 正文 |
| 4 | **Shippie** `https://github.com/mattzcarey/shippie` | 正文 |

与 Ponytail（`luzzy-roster-backend` 里那条）的分工：Ponytail 只审「过度设计」，本类四家审**正确性、安全、性能、架构**——互补，可以都跑。审查输出格式（阻塞项 / 建议 / 已确认无问题）与「安全项零容忍」纪律见提示词 §14.7。

## Examples

Input: 命中「代码审查」
Output: 读本表 4 条 → 全读 → 执行择一，安全项零容忍 → 落回执。

Input: 审查整个仓库
Output: 先按 §五 确认审什么范围（本次改动 / 整文件 / 整仓），不擅自审全仓 → 再读四家。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.7；本 skill 只装清单明细。
