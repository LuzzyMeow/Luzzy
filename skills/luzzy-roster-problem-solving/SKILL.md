---
name: luzzy-roster-problem-solving
description: >
  Use when the Luzzy checklist (必读清单) hits the 学科题目解答 / 解题方法论 category —
  methodology sub-items for solving and verifying problems (how to think and verify, not subject knowledge).
  Answers "做题用什么方法论" "验算怎么防止自己骗自己" "math-olympiad适合什么场景" "核查一个解答对不对".
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

# 学科题目解答 / 解题方法论 · 仓库子项明细

提示词 §1.1.6 命中「学科题目解答 / 解题方法论」后，读本文件拿仓库子项明细。阅读口径（全读 / 折减 / 读 ≠ 装 ≠ 用 / 读取回执）见提示词 §1.1.3，本文件不重述。

## Workflow

1. 对照下表读子项：先本机后云端，读到正文才算（首页 / README 摘要不算）
   Verify: 读取回执里的子项名与本表条目名一致
2. 装之前核体积、许可与整仓要求；「读」不等于「装」，读满口径即完成
   Verify: 每条要装的子项都有体积与许可记录；缺失就按 §五 澄清
3. 链接失效（404 / 超时 / 已归档 / 内容为空）→ 按提示词 §1.1.9 上报用户，再自行寻找替代：抓取通道按提示词 §1.2（gh-proxy / ghfast 镜像、AnySearch `extract` 抓 raw 正文、Gitee 导入兜底，用前先探，逐级降级）；本 skill 内补齐同类型的按各家标注执行（如设计类「任意两条失效联网补齐」）
   Verify: 上报发生在任何替代动作之前；替代通道从头到尾可溯源；未静默跳过或悄悄顶替

## 子项（3 条 → 全读）

| # | 条目 | 读什么 |
|---|---|---|
| 1 | Anthropic 官方 **math-olympiad** `https://github.com/anthropics/claude-plugins-official/tree/main/plugins/math-olympiad` | 审题解读检查 → 并行多路尝试 → 剥离思考痕迹 → 对抗式验证 → 非对称投票 → 敢说「没有把握」 |
| 2 | **求是Skill** `https://github.com/HughYau/qiushi-skill` | 实事求是总原则 + 九大方法论（矛盾分析、调查研究、实践认识论等） |
| 3 | **cc-thinking-skills** `https://github.com/tjboudreaux/cc-thinking-skills` | 28 个心智模型与批判性思维工具 |

读的是「怎么想、怎么验」的方法论，不是科目知识点——数学、物理、代码、逻辑、业务问题走同一套。七条解题纪律（先审题、分步、验算与求解分开、反例优先、卡住退步、拿不准就说）见提示词 §14.17；解题类任务联网找现成答案冒充自己解出 = 作弊。

## Examples

Input: 命中「学科题目解答」
Output: 读本表 3 条 → 按七条纪律解题 → 拿不准就说拿不准 → 落回执。

Input: 用户要核查某解答
Output: 读 3 条 → 验算只看题目与干净解答，不看原推导 → 给结论与依据。



## Reference Files

| File | Load when |
|------|-----------|
| [../luzzy-roster-family/references/checklist-history.md](../luzzy-roster-family/references/checklist-history.md) | 维护场景：子项增删改登记（维护文档，非运行时上下文） |

执行纪律、红线与失败路径见提示词 §14.17；本 skill 只装清单明细。
